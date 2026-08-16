# Jovita Bot Service — CTW 2026

MVP conversacional de WhatsApp para convertir un relato libre + documentos + evidencia multimedia en un `case.json` persistente y, después de confirmación explícita del usuario, disparar el `legal-docs-service` hermano.

## Qué implementa

- Mensaje inicial **fijo** de Jovita.
- Consentimiento obligatorio con botones antes de analizar el caso.
- Conversación guiada sin formulario largo.
- Extracción estructurada con `gpt-5.6-luna` mediante OpenAI Responses API.
- Lectura multimodal de pólizas PDF.
- Descripción prudente de fotos, separando observación visual de conclusión técnica.
- Transcripción de audio mediante un modelo configurable de speech-to-text.
- Persistencia del expediente como `case.json` y archivos locales.
- Máquina de estados pequeña: `new → consent_pending → triage/waiting_document → collecting_evidence → ready_to_offer → ready_to_confirm → ready_to_file`.
- Confirmación humana obligatoria antes de generar el documento.
- Integración con `../legal-docs-service` por subprocess en el mismo repo/contenedor.
- Webhook de WhatsApp Cloud API para texto, reply buttons, PDF, foto, audio y video.
- Envío del PDF final de vuelta a WhatsApp.
- Provider `mock` para tests sin red y stub `GeminiProvider` para una implementación futura con Gemini/Google Search.

## Estructura

```text
jovita-bot-service/
├── app/
│   ├── ai/
│   │   ├── base.py
│   │   ├── openai_provider.py
│   │   ├── mock_provider.py
│   │   └── gemini_provider.py
│   ├── config.py
│   ├── engine.py
│   ├── legal_docs.py
│   ├── main.py
│   ├── media.py
│   ├── models.py
│   ├── prompts.py
│   ├── scenario.py
│   ├── storage.py
│   └── whatsapp.py
├── fixtures/juan_jose/
│   ├── conversation.md
│   ├── poliza_hogar_sintetica_juan_jose_rojas_constain.pdf
│   └── evidence/
├── scripts/replay_markdown.py
├── tests/
├── Dockerfile
├── cloudbuild.yaml
├── requirements.txt
└── .env.example
```

## 1. Probar YA, sin WhatsApp y sin APIs

Desde `jovita-bot-service`:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
Copy-Item .env.example .env
python scripts/replay_markdown.py --provider mock --skip-docs
```

Esto reproduce todos los turnos de `fixtures/juan_jose/conversation.md`, copia localmente la póliza/fotos cuando corresponde y termina mostrando el `case.json` construido desde cero.

## 2. Probar conversación real con GPT-5.6 Luna, sin WhatsApp

En `.env`:

```env
AI_PROVIDER=openai
OPENAI_API_KEY=sk-...
OPENAI_MODEL=gpt-5.6-luna
```

Luego:

```powershell
python scripts/replay_markdown.py --provider openai --skip-docs
```

El PDF se envía como `input_file` y las fotos como `input_image`; la respuesta se restringe a modelos Pydantic con Structured Outputs.

## 3. E2E local incluyendo `legal-docs-service`

La estructura del repo debe ser:

```text
disaster-legal-assistant-ctw2026/
├── jovita-bot-service/
└── legal-docs-service/
```

Para probar todo sin costo de LLM:

```powershell
python scripts/replay_markdown.py --provider mock --legal-docs-provider mock
```

Para probar todo con OpenAI:

```powershell
python scripts/replay_markdown.py --provider openai --legal-docs-provider openai
```

Jovita llama:

```text
legal-docs-service/main.py
  --case <case.json final>
  --knowledge <knowledge fijo del legal-docs-service>
  --route insurance
  --provider <mock|openai>
```

Jovita **no pasa knowledge por la conversación**. Solo conoce la ruta fija del knowledge del servicio jurídico.

## 4. Levantar el webhook localmente

Configura `.env`. Para probar payloads sin mandar mensajes reales a Meta:

```env
AI_PROVIDER=mock
WHATSAPP_DRY_RUN=true
```

Arranca:

```powershell
uvicorn app.main:app --reload --port 8080
```

Endpoints:

```text
GET  /health
GET  /webhook       handshake de Meta
POST /webhook       mensajes entrantes
GET  /debug/case/{user_id}   solo no-producción
```

Para exponerlo temporalmente a Meta puedes usar un túnel HTTPS de tu preferencia y registrar:

```text
https://TU-DOMINIO/webhook
```

## 5. Conectar WhatsApp Cloud API

Variables mínimas:

```env
WHATSAPP_VERIFY_TOKEN=un-token-que-tu-elijas
WHATSAPP_ACCESS_TOKEN=...
WHATSAPP_PHONE_NUMBER_ID=...
META_APP_SECRET=...
WHATSAPP_DRY_RUN=false
```

Suscribe el webhook al evento `messages`. El adaptador:

1. verifica el handshake;
2. opcionalmente valida `X-Hub-Signature-256` cuando existe `META_APP_SECRET`;
3. recibe texto/botones/media;
4. descarga el archivo usando el `media_id`;
5. guarda el original;
6. ejecuta `JovitaEngine`;
7. envía mensajes/botones;
8. al final sube el PDF generado a Meta y lo envía como documento.

## 6. Docker / Cloud Run

**Importante:** el `Dockerfile` necesita como build context la raíz del repo porque copia también `legal-docs-service`.

Desde `disaster-legal-assistant-ctw2026/`:

```powershell
docker build -f jovita-bot-service/Dockerfile -t jovita .
docker run --rm -p 8080:8080 --env-file jovita-bot-service/.env jovita
```

Cloud Build:

```powershell
gcloud builds submit --config jovita-bot-service/cloudbuild.yaml .
```

Después despliega esa imagen a Cloud Run. Para el demo recomiendo:

- acceso público, porque Meta debe poder llamar `/webhook`;
- `DATA_DIR=/data`;
- montar un bucket de Cloud Storage en `/data` para persistir casos y adjuntos;
- `--concurrency 1` y `--max-instances 1` durante el hackathon para evitar carreras de escritura sobre el mismo `case.json`;
- guardar `OPENAI_API_KEY`, token de WhatsApp y `META_APP_SECRET` en Secret Manager.

Ejemplo del volumen en el deploy:

```powershell
gcloud run deploy jovita `
  --image REGION-docker.pkg.dev/PROJECT/ctw2026/jovita:latest `
  --region REGION `
  --allow-unauthenticated `
  --concurrency 1 `
  --max-instances 1 `
  --set-env-vars "DATA_DIR=/data,AI_PROVIDER=openai,WHATSAPP_DRY_RUN=false,LEGAL_DOCS_MODE=subprocess,LEGAL_DOCS_PROVIDER=openai" `
  --add-volume "mount-path=/data,type=cloud-storage,bucket=TU_BUCKET,readonly=false"
```

Añade los secretos por Secret Manager o desde la configuración de Cloud Run; no los commitees.

## 7. Tests

```powershell
pytest -q
```

Los tests cubren:

- bienvenida y consentimiento;
- replay E2E completo de Juan José;
- construcción del `case.json`;
- póliza + tres fotos;
- guardrail `technical_conclusion = null`;
- confirmación antes de documento;
- trigger del generador jurídico;
- parseo de texto, botones y media de WhatsApp;
- verificación HMAC del webhook.

## 8. Estado persistido

Localmente:

```text
data/cases/<usuario_hash>/case.json
data/cases/<usuario_hash>/attachments/*
data/cases/<usuario_hash>/processed_message_ids.json
```

En Cloud Run, la misma API de archivos funciona si `DATA_DIR=/data` está montado sobre Cloud Storage. Para una versión posterior con más concurrencia, conviene mover el estado transaccional a Firestore/SQL y dejar los blobs en Cloud Storage.

## 9. Guardrails del MVP

- No analiza datos antes del consentimiento.
- No trata “no recuerdo haber comprado seguro” como ausencia definitiva de cobertura cuando hay crédito hipotecario.
- No dice que una póliza garantiza el pago del caso.
- No certifica habitabilidad, estabilidad ni daño estructural desde fotos.
- No genera hasta que el usuario confirma el resumen del expediente.
- Conserva las rutas a originales en `documents[]` / `evidence[]`.
- El `case.json` es la fuente de verdad entre turnos; la transcripción es historial, no la base del sistema.
