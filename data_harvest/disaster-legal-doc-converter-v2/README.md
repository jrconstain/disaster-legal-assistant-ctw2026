# Disaster Legal Document Converter — v2

Conversor incremental de documentos a Markdown canónico para RAG.

## Cambio principal de v2

El Markdown ya NO contiene una ficha analítica gigantesca.

Front matter esperado:

```yaml
---
schema_version: 2.0.0
document_id: co_fasecolda_seguros_terremoto_2026-08-12
title: ¿Qué seguros protegen su vivienda ante un terremoto? Fasecolda explica
document_type: comunicado
issuer: Federación de Aseguradores Colombianos, Fasecolda
publication_date: '2026-08-12'
event_date: '2026-08-10'
jurisdiction: Colombia
source_file: FASECOLDA_comunicados_12aug-1357.pdf
topics: [seguros, vivienda, terremoto, reclamaciones de seguros, propiedad horizontal]
---
```

Después comienza inmediatamente el contenido.

Los detalles técnicos (`source_pages`, advertencias de extracción, QA, etc.) viven en
el JSON sidecar y NO contaminan el `.md`.

## Conversión incremental

El conversor mantiene:

```text
output/.state/manifest.json
```

Para cada archivo guarda su SHA-256.

Comportamiento:

| Situación | Acción |
|---|---|
| PDF nuevo | PROCESS |
| Mismo PDF, mismo contenido y salidas presentes | SKIP |
| Mismo nombre pero PDF cambió | PROCESS |
| Falta alguna salida | PROCESS |
| Conversión anterior falló | PROCESS en la próxima corrida |
| `--force` | PROCESS siempre |

El manifiesto solo se actualiza DESPUÉS de una conversión exitosa.

## Estructura

```text
.
├── convert.py
├── input/
├── output/
│   ├── markdown/
│   ├── structured/
│   ├── qa/
│   ├── errors/
│   └── .state/manifest.json
├── prompts/
├── schemas/
└── src/
```

También soporta subcarpetas dentro de `input/`; las replica en `output/`.

## Instalación Windows

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
py -m pip install -r requirements.txt
Copy-Item .env.example .env
notepad .env
```

Completa:

```text
OPENAI_API_KEY=...
OPENAI_MODEL=gpt-5.6
PDF_DETAIL=high
```

## Antes de gastar API: ver el plan

```powershell
py convert.py --dry-run
```

Ejemplo:

```text
SKIP    FASECOLDA_comunicados_12aug-1357.pdf  [ya_convertido]
PROCESS nuevo_documento.pdf                    [nuevo]

Dry-run: procesaría 1; omitiría 1.
```

## Convertir

```powershell
py convert.py
```

Vuelve a ejecutar el mismo comando mañana después de agregar PDFs.
Solo llamará la API para los nuevos/modificados.

## Reprocesar todo deliberadamente

```powershell
py convert.py --force
```

## Archivos por documento

Para `input/documento.pdf`:

```text
output/markdown/documento.md
output/structured/documento.json
output/qa/documento.qa.json
```

Si falla:

```text
output/errors/documento.error.json
```

Una falla no detiene los demás documentos.

## Por qué conservar structured JSON

El `.md` es el corpus limpio.

El `.json` conserva trazabilidad de páginas y estructura interna, útil después para:
- chunking;
- citas;
- debugging;
- auditoría;
- re-renderizar Markdown sin volver a pagar la extracción del PDF.
