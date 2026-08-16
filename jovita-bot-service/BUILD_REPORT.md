# Build report — Jovita MVP CTW 2026

Build date: 2026-08-16

## Implemented

- Fixed Jovita welcome + consent gate before any case extraction.
- Persistent `case.json` per WhatsApp user plus local/media attachments.
- Deterministic route state for the Juan José demo (`mortgage_insurance` → `insurance`).
- OpenAI provider configured for `gpt-5.6-luna` with Pydantic Structured Outputs.
- PDF policy extraction, cautious image observations, and configurable audio transcription.
- `MockProvider` for local tests without network/API keys.
- Provider interface plus `GeminiProvider` stub for a future Gemini + Google Search implementation.
- WhatsApp Cloud API webhook adapter: text, buttons, PDF, images, audio, video, media download, and final PDF upload/send.
- Human confirmation gate before invoking the legal document generator.
- Sibling `legal-docs-service` adapter by subprocess (default) or HTTP (optional).
- Markdown-driven local E2E replay for Juan José with local PDF/photo paths.
- Dockerfile + Cloud Build + Cloud Run configuration notes.

## Verification performed in this environment

```text
python -m compileall -q app scripts tests
pytest -q
```

Result:

```text
4 passed
```

Local Markdown replay, without WhatsApp and without invoking the legal generator:

```text
python scripts/replay_markdown.py --provider mock --skip-docs
```

Observed final state:

```text
name=Juan José Rojas Constaín
cedula=1-113-682-988
ownership_status=owner
credit.bank=Bancolombia
has_insurance=true
policy_number=HOG-2026-0081640
event.date=2026-08-10
evidence=3
is_confirmed=true
route=insurance
state=ready_to_generate   # legal generation deliberately skipped by this command
```

FastAPI smoke test with `AI_PROVIDER=mock` also returned HTTP 200 for `/` and `/health`.

## Not executed here

- No live OpenAI request: this runtime does not have the user's `OPENAI_API_KEY` and the OpenAI SDK is not installed in the host environment. The repo's `requirements.txt` includes it for the target environment.
- No live Meta/WhatsApp request: no Meta credentials were supplied.
- No real sibling `legal-docs-service` subprocess execution inside this sandbox: that service is expected to exist as a sibling directory in the user's repository. The adapter contract matches its existing CLI (`main.py --case ... --knowledge ... --route insurance --provider ...`).
- No Cloud Run deployment was executed; deployment files/instructions are included.

## Demo fixture warning

The Juan José policy and evidence used by this repo are synthetic CTW 2026 fixtures. They are not for real insurance use.
