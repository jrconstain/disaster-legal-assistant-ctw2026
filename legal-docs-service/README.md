# Legal Docs Service - minimal local MVP (CTW 2026)

Servicio Python deliberadamente pequeno para probar una sola idea:

> recibe un JSON de caso + un Markdown de knowledge base; lee los PDF/fotos locales referenciados por el JSON; llama un LLM para obtener un draft estructurado; valida ese draft; y construye un PDF programaticamente en `outputs/`.

No hay webhook, Node.js, base de datos, RAG/vector DB ni FastAPI en esta version. La futura integracion solo debe llamar `generate_document(...)` o `generate_from_trigger(...)`.

## 1. Estructura

```text
.
├── main.py                  # CLI + simulador ACTIVAR
├── service/
│   ├── service.py           # pipeline completo
│   ├── io.py                # JSON, Markdown, PDFs y fotos locales
│   ├── llm.py               # OpenAI Structured Outputs + proveedor mock
│   ├── schemas.py           # contrato de salida del LLM
│   ├── validate.py          # guardrails simples
│   └── renderer.py          # PDF programatico con ReportLab
├── prompts/
│   ├── common.md
│   ├── insurance_notice.md
│   └── rental_notice.md
├── knowledge/
├── fixtures/
├── tests/
└── outputs/
```

## 2. Instalacion

Windows PowerShell:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
py -m pip install -r requirements.txt
Copy-Item .env.example .env
```

Luego edite `.env`:

```env
OPENAI_API_KEY=su_api_key
OPENAI_MODEL=gpt-5.6-luna
LLM_PROVIDER=openai
```

## 3. Prueba sin gastar API

```powershell
py main.py --demo insurance --provider mock
py main.py --demo rental --provider mock
```

El resultado queda en una subcarpeta de `outputs/` con:

```text
document.pdf
draft.json
result.json
```

## 4. Simular el trigger por consola

```powershell
py main.py --demo insurance --provider mock --interactive
```

La consola mostrara los datos cargados y pedira:

```text
Escribe ACTIVAR para generar el documento o SALIR:
```

Al escribir `ACTIVAR`, corre el mismo pipeline que luego podria invocar un webhook.

Tambien puede probar el pequeno JSON de trigger:

```powershell
py main.py --trigger fixtures/trigger_insurance.json --interactive
```

## 5. Prueba real con GPT-5.6 Luna

Despues de poner la API key:

```powershell
py main.py --demo insurance --provider openai
py main.py --demo rental --provider openai
```

El cliente usa Responses API + Structured Outputs (`client.responses.parse(..., text_format=LegalDocumentDraft)`). Las fotos locales se envian como `input_image` en base64. Los PDF locales se leen con `pypdf` y su texto se incorpora al contexto del modelo.

## 6. La interfaz que importa para la futura integracion

```python
from service.service import generate_document

result = generate_document(
    case_json_path="ruta/al/caso.json",
    knowledge_md_path="ruta/a/knowledge.md",
    route="auto",      # o insurance / rental
    provider="openai",
)

print(result["pdf"])
```

O un trigger minimo:

```python
from service.service import generate_from_trigger

result = generate_from_trigger({
    "route": "insurance",
    "case_json_path": "cases/123.json",
    "knowledge_md_path": "knowledge/current.md"
})
```

## 7. Cambios juridicos frente a la version anterior

### Seguro

El primer PDF es ahora **aviso inicial de siniestro**, no reclamacion completa:

- descriptivo;
- sin capitulo de fundamento juridico;
- sin gastos ni cuantificacion de perdida;
- incluye identidad, poliza, inmueble, evento, danos reportados, fotos y contactos;
- pide recepcion/referencia/instrucciones, no indemnizacion.

### Arrendamiento

La carta:

- informa sismo + afectaciones;
- conecta el objeto del arrendamiento (uso/goce) con la imposibilidad reportada de continuar normalmente el uso residencial;
- usa subsuncion: regla -> caso -> consecuencia/solicitud;
- solicita evaluacion/reparacion/habilitacion y definicion del tratamiento del canon;
- no afirma terminacion automatica ni inhabitabilidad sin soporte tecnico.

### Notificaciones

Ambas rutas incluyen una seccion final de **Notificaciones y datos de contacto**, usando solamente datos existentes en JSON/contrato/poliza.

## 8. Tests

```powershell
pytest -q
```

Los tests usan `provider=mock`, por lo que no necesitan API key y generan PDFs reales con los fixtures incluidos.

## 9. Limitaciones deliberadas del MVP

- Solo adjuntos locales; las URLs remotas quedan para la integracion posterior.
- Los PDFs se leen por capa de texto con `pypdf`; no hay OCR para escaneos.
- No hay RAG: el Markdown completo se entrega al modelo.
- No hay almacenamiento cloud: el PDF queda en `outputs/`.
- No hay webhook/API HTTP: el punto de integracion es una funcion Python pequena.
