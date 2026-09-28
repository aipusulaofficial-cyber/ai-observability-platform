import json
import logging

from observability import JsonFormatter


def test_json_formatter_emits_structured_fields():
    record = logging.LogRecord("test", logging.INFO, __file__, 1, "hello %s", ("world",), None)
    payload = json.loads(JsonFormatter().format(record))
    assert payload == {"level": "INFO", "message": "hello world", "logger": "test"}
