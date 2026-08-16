# Build context MUST be the repository root:
# docker build -f jovita-bot-service/Dockerfile -t jovita .
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8080 \
    DATA_DIR=/data \
    OUTPUT_DIR=/data/legal-docs-outputs \
    LEGAL_DOCS_ROOT=/opt/legal-docs-service \
    LEGAL_DOCS_KNOWLEDGE_PATH=/opt/legal-docs-service/knowledge/knowledgebase_inmuebles_colombia_v0.1.md

WORKDIR /opt

COPY jovita-bot-service/requirements.txt /tmp/jovita-requirements.txt
COPY legal-docs-service/requirements.txt /tmp/legal-requirements.txt
RUN pip install --no-cache-dir -r /tmp/jovita-requirements.txt -r /tmp/legal-requirements.txt

COPY legal-docs-service /opt/legal-docs-service
COPY jovita-bot-service /opt/jovita-bot-service

WORKDIR /opt/jovita-bot-service
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT}"]
