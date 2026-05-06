from __future__ import annotations

from dataclasses import dataclass
import os


@dataclass(frozen=True)
class OllamaConfig:
    host: str = "http://127.0.0.1:11434"
    model: str = "qwen3:8b"
    timeout_seconds: float = 60.0


def load_config() -> OllamaConfig:
    timeout = float(os.getenv("OLLAMA_TIMEOUT_SECONDS", "60"))
    return OllamaConfig(
        host=os.getenv("OLLAMA_HOST", "http://127.0.0.1:11434").rstrip("/"),
        model=os.getenv("OLLAMA_MODEL", "qwen3:8b"),
        timeout_seconds=timeout,
    )