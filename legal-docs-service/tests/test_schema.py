from service.schemas import LegalDocumentDraft


def test_structured_output_schema_is_closed():
    schema = LegalDocumentDraft.model_json_schema()

    def walk(node):
        if isinstance(node, dict):
            if node.get("type") == "object":
                assert node.get("additionalProperties") is False
            for value in node.values():
                walk(value)
        elif isinstance(node, list):
            for value in node:
                walk(value)

    walk(schema)
