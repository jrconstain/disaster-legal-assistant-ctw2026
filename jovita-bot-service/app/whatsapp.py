from __future__ import annotations

import hashlib
import hmac
import mimetypes
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping

import requests

from app.config import Settings


@dataclass(slots=True)
class InboundMessage:
    message_id: str
    sender_id: str
    message_type: str
    text: str
    profile_name: str | None = None
    media_id: str | None = None
    mime_type: str | None = None
    filename: str | None = None


def verify_webhook_challenge(*, mode: str | None, token: str | None, challenge: str | None, expected_token: str) -> str | None:
    if mode == 'subscribe' and expected_token and token == expected_token and challenge is not None:
        return challenge
    return None


def verify_signature(*, raw_body: bytes, signature_header: str | None, app_secret: str) -> bool:
    if not app_secret or not signature_header or not signature_header.startswith('sha256='):
        return False
    expected = hmac.new(app_secret.encode(), raw_body, hashlib.sha256).hexdigest()
    return hmac.compare_digest(expected, signature_header[7:].strip())


def parse_webhook(payload: Mapping[str, Any]) -> list[InboundMessage]:
    result: list[InboundMessage] = []
    for entry in payload.get('entry', []) or []:
        for change in entry.get('changes', []) or []:
            value = change.get('value') or {}
            names = {
                str(c.get('wa_id')): str((c.get('profile') or {}).get('name') or '')
                for c in value.get('contacts', []) or []
                if c.get('wa_id')
            }
            for msg in value.get('messages', []) or []:
                sender = str(msg.get('from') or '').strip()
                mid = str(msg.get('id') or '').strip()
                typ = str(msg.get('type') or '').strip()
                if not sender or not mid:
                    continue
                text = ''
                media_id = None
                mime_type = None
                filename = None
                if typ == 'text':
                    text = str((msg.get('text') or {}).get('body') or '').strip()
                elif typ == 'interactive':
                    inter = msg.get('interactive') or {}
                    if inter.get('type') == 'button_reply':
                        reply = inter.get('button_reply') or {}
                        text = str(reply.get('id') or reply.get('title') or '').strip()
                    elif inter.get('type') == 'list_reply':
                        reply = inter.get('list_reply') or {}
                        text = str(reply.get('id') or reply.get('title') or '').strip()
                elif typ == 'button':
                    btn = msg.get('button') or {}
                    text = str(btn.get('payload') or btn.get('text') or '').strip()
                elif typ in {'image', 'document', 'audio', 'video'}:
                    media = msg.get(typ) or {}
                    media_id = str(media.get('id') or '').strip() or None
                    mime_type = str(media.get('mime_type') or '').strip() or None
                    filename = str(media.get('filename') or '').strip() or None
                    text = str(media.get('caption') or '').strip()
                else:
                    continue
                result.append(
                    InboundMessage(
                        message_id=mid,
                        sender_id=sender,
                        message_type=typ,
                        text=text,
                        profile_name=names.get(sender) or None,
                        media_id=media_id,
                        mime_type=mime_type,
                        filename=filename,
                    )
                )
    return result


class WhatsAppClient:
    def __init__(self, settings: Settings):
        self.s = settings
        self.base = f'https://graph.facebook.com/{settings.graph_api_version.lstrip("/")}'

    @property
    def headers(self) -> dict[str, str]:
        return {'Authorization': f'Bearer {self.s.whatsapp_access_token}'}

    def _post_message(self, payload: dict) -> dict:
        if self.s.whatsapp_dry_run:
            return {'dry_run': True, 'payload': payload}
        r = requests.post(
            f'{self.base}/{self.s.whatsapp_phone_number_id}/messages',
            headers={**self.headers, 'Content-Type': 'application/json'},
            json=payload,
            timeout=(5, 30),
        )
        if not r.ok:
            raise RuntimeError(f'WhatsApp HTTP {r.status_code}: {r.text[:2000]}')
        return r.json()

    def send_text(self, to: str, text: str) -> dict:
        return self._post_message({
            'messaging_product': 'whatsapp',
            'recipient_type': 'individual',
            'to': to,
            'type': 'text',
            'text': {'preview_url': True, 'body': text[:4096]},
        })

    def send_buttons(self, to: str, text: str, buttons: list[dict[str, str]]) -> dict:
        return self._post_message({
            'messaging_product': 'whatsapp',
            'recipient_type': 'individual',
            'to': to,
            'type': 'interactive',
            'interactive': {
                'type': 'button',
                'body': {'text': text[:1024]},
                'action': {
                    'buttons': [
                        {'type': 'reply', 'reply': {'id': x['id'], 'title': x['title'][:20]}}
                        for x in buttons[:3]
                    ]
                },
            },
        })

    def download_media(self, *, media_id: str, target_dir: Path, filename: str | None = None) -> tuple[Path, str]:
        if self.s.whatsapp_dry_run:
            raise RuntimeError('No se puede descargar media de Meta con WHATSAPP_DRY_RUN=true.')
        meta = requests.get(f'{self.base}/{media_id}', headers=self.headers, timeout=(5, 30))
        if not meta.ok:
            raise RuntimeError(f'No pude resolver media_id {media_id}: {meta.text[:1000]}')
        info = meta.json()
        url = info['url']
        mime = str(info.get('mime_type') or 'application/octet-stream')
        body = requests.get(url, headers=self.headers, timeout=(5, 60))
        if not body.ok:
            raise RuntimeError(f'No pude descargar media: HTTP {body.status_code}')
        target_dir.mkdir(parents=True, exist_ok=True)
        suffix = mimetypes.guess_extension(mime.split(';')[0]) or ''
        name = filename or f'{media_id}{suffix}'
        target = target_dir / name.replace('/', '_').replace('\\', '_')
        target.write_bytes(body.content)
        return target, mime

    def upload_media(self, file_path: Path) -> str:
        if self.s.whatsapp_dry_run:
            return 'dry-run-media-id'
        mime = mimetypes.guess_type(file_path.name)[0] or 'application/octet-stream'
        with file_path.open('rb') as fh:
            r = requests.post(
                f'{self.base}/{self.s.whatsapp_phone_number_id}/media',
                headers=self.headers,
                data={'messaging_product': 'whatsapp'},
                files={'file': (file_path.name, fh, mime)},
                timeout=(5, 60),
            )
        if not r.ok:
            raise RuntimeError(f'Upload de documento falló: {r.status_code} {r.text[:1500]}')
        return str(r.json()['id'])

    def send_document(self, to: str, file_path: Path, filename: str | None = None, caption: str | None = None) -> dict:
        media_id = self.upload_media(file_path)
        document: dict[str, str] = {'id': media_id, 'filename': filename or file_path.name}
        if caption:
            document['caption'] = caption
        return self._post_message({
            'messaging_product': 'whatsapp',
            'recipient_type': 'individual',
            'to': to,
            'type': 'document',
            'document': document,
        })
