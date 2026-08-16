from __future__ import annotations

from pathlib import Path

from app.models import LocalAttachment
from app.whatsapp import InboundMessage, WhatsAppClient


def whatsapp_message_to_attachment(message: InboundMessage, client: WhatsAppClient, download_dir: Path) -> LocalAttachment | None:
    if message.message_type not in {'image', 'document', 'audio', 'video'} or not message.media_id:
        return None
    path, mime = client.download_media(
        media_id=message.media_id,
        target_dir=download_dir,
        filename=message.filename,
    )
    kind = {
        'image': 'image',
        'document': 'document',
        'audio': 'audio',
        'video': 'video',
    }[message.message_type]
    return LocalAttachment(path=path, mime_type=mime, kind=kind, filename=message.filename or path.name)
