from app.whatsapp import parse_webhook, verify_signature
import hashlib
import hmac


def test_parse_text_button_and_media():
    payload = {
        'entry': [{'changes': [{'value': {
            'contacts': [{'wa_id': '57300', 'profile': {'name': 'Juan'}}],
            'messages': [
                {'from': '57300', 'id': 'm1', 'type': 'text', 'text': {'body': 'hola'}},
                {'from': '57300', 'id': 'm2', 'type': 'interactive', 'interactive': {'type': 'button_reply', 'button_reply': {'id': 'consent_yes', 'title': 'Sí'}}},
                {'from': '57300', 'id': 'm3', 'type': 'document', 'document': {'id': 'media1', 'mime_type': 'application/pdf', 'filename': 'poliza.pdf'}},
                {'from': '57300', 'id': 'm4', 'type': 'image', 'image': {'id': 'media2', 'mime_type': 'image/jpeg', 'caption': 'foto'}},
            ]
        }}]}]
    }
    msgs = parse_webhook(payload)
    assert [m.text for m in msgs[:2]] == ['hola', 'consent_yes']
    assert msgs[2].media_id == 'media1'
    assert msgs[2].filename == 'poliza.pdf'
    assert msgs[3].message_type == 'image'
    assert msgs[3].text == 'foto'


def test_signature():
    raw = b'{"hello":"world"}'
    secret = 'abc'
    sig = 'sha256=' + hmac.new(secret.encode(), raw, hashlib.sha256).hexdigest()
    assert verify_signature(raw_body=raw, signature_header=sig, app_secret=secret)
