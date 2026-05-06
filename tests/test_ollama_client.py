import httpx
import pytest

from cowork_dispatch.config import OllamaConfig
from cowork_dispatch.ollama_client import OllamaClient, OllamaError


def test_generate_returns_trimmed_response() -> None:
    transport = httpx.MockTransport(
        lambda request: httpx.Response(200, json={"model": "demo", "response": " hello "})
    )
    http_client = httpx.Client(transport=transport)
    client = OllamaClient(OllamaConfig(), http_client=http_client)

    result = client.generate("hi")

    assert result.model == "demo"
    assert result.text == "hello"


def test_generate_raises_on_empty_text() -> None:
    transport = httpx.MockTransport(lambda request: httpx.Response(200, json={"response": ""}))
    http_client = httpx.Client(transport=transport)
    client = OllamaClient(OllamaConfig(), http_client=http_client)

    with pytest.raises(OllamaError):
        client.generate("hi")
