from __future__ import annotations

import logging
from pathlib import Path

from fastapi import BackgroundTasks, FastAPI, HTTPException, Query, Request, Response

from app.ai import build_provider
from app.config import Settings
from app.engine import JovitaEngine
from app.legal_docs import LegalDocsClient
from app.media import whatsapp_message_to_attachment
from app.storage import CaseStore
from app.whatsapp import WhatsAppClient, parse_webhook, verify_signature, verify_webhook_challenge

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('jovita')

settings = Settings.from_env()
store = CaseStore(settings)
ai = build_provider(settings)
legal_docs = LegalDocsClient(settings)
engine = JovitaEngine(settings=settings, store=store, ai=ai, legal_docs=legal_docs)
wa = WhatsAppClient(settings)

app = FastAPI(title='Jovita MVP - CTW 2026', version='0.1.0')


@app.get('/')
def root() -> dict:
    return {
        'service': 'jovita-bot-service',
        'status': 'ok',
        'ai_provider': settings.ai_provider,
        'whatsapp_dry_run': settings.whatsapp_dry_run,
        'legal_docs_mode': settings.legal_docs_mode,
    }


@app.get('/health')
def health() -> dict:
    return {'ok': True}


@app.get('/webhook')
def verify_webhook(
    hub_mode: str | None = Query(default=None, alias='hub.mode'),
    hub_verify_token: str | None = Query(default=None, alias='hub.verify_token'),
    hub_challenge: str | None = Query(default=None, alias='hub.challenge'),
):
    challenge = verify_webhook_challenge(
        mode=hub_mode,
        token=hub_verify_token,
        challenge=hub_challenge,
        expected_token=settings.whatsapp_verify_token,
    )
    if challenge is None:
        raise HTTPException(status_code=403, detail='Webhook verification failed')
    return Response(content=challenge, media_type='text/plain')


def _dispatch(sender_id: str, events) -> None:
    for event in events:
        if event.type == 'text':
            wa.send_text(sender_id, event.text or '')
        elif event.type == 'buttons':
            wa.send_buttons(sender_id, event.text or '', event.buttons)
        elif event.type == 'document' and event.file_path:
            wa.send_document(
                sender_id,
                Path(event.file_path),
                filename=event.filename,
                caption=event.caption,
            )


def _process_message(message) -> None:
    try:
        attachments = []
        if message.media_id:
            attachment = whatsapp_message_to_attachment(
                message,
                wa,
                store.case_dir(message.sender_id) / 'meta_downloads',
            )
            if attachment:
                attachments.append(attachment)
        result = engine.process(
            user_id=message.sender_id,
            text=message.text,
            attachments=attachments,
            profile_name=message.profile_name,
            message_id=message.message_id,
        )
        _dispatch(message.sender_id, result.events)
    except Exception:
        logger.exception('Error procesando mensaje WhatsApp %s', message.message_id)
        try:
            wa.send_text(
                message.sender_id,
                'Tuve un problema procesando ese mensaje. El caso quedó guardado; puedes intentar enviarlo de nuevo.',
            )
        except Exception:
            logger.exception('También falló el mensaje de error a WhatsApp')


@app.post('/webhook')
async def receive_webhook(request: Request, background_tasks: BackgroundTasks):
    raw = await request.body()
    if settings.meta_app_secret:
        signature = request.headers.get('X-Hub-Signature-256')
        if not verify_signature(raw_body=raw, signature_header=signature, app_secret=settings.meta_app_secret):
            raise HTTPException(status_code=401, detail='Invalid webhook signature')
    payload = await request.json()
    messages = parse_webhook(payload)
    for message in messages:
        background_tasks.add_task(_process_message, message)
    # Meta only needs a quick 200; processing happens immediately after the response.
    return {'ok': True, 'messages': len(messages)}


@app.get('/debug/case/{user_id}')
def debug_case(user_id: str):
    if settings.app_env == 'production':
        raise HTTPException(status_code=404)
    return store.load(user_id) or {'status': 'not_found'}
