from __future__ import annotations

from dataclasses import dataclass

import httpx

from cowork_dispatch.config import OllamaConfig


class OllamaError(RuntimeError):
    pass


@dataclass(slots=True)
class OllamaResponse:
    model: str
    text: str


class OllamaClient:
    def __init__(self, config: OllamaConfig, http_client: httpx.Client | None = None) -> None:
        self._config = config
        self._http_client = http_client or httpx.Client(timeout=config.timeout_seconds)
        self._owns_client = http_client is None

    def close(self) -> None:
        if self._owns_client:
            self._http_client.close()

    def generate(self, prompt: str, system: str | None = None) -> OllamaResponse:
        payload = {
            "model": self._config.model,
            "prompt": prompt,
            "stream": False,
        }
        if system:
            payload["system"] = system

        try:
            response = self._http_client.post(f"{self._config.host}/api/generate", json=payload)
            response.raise_for_status()
        except httpx.HTTPError as exc:
            raise OllamaError(f"Ollama request failed: {exc}") from exc

        data = response.json()
        text = data.get("response")
        if not isinstance(text, str) or not text.strip():
            raise OllamaError("Ollama response did not contain text in 'response'.")

        model = data.get("model", self._config.model)
        return OllamaResponse(model=model, text=text.strip())