from __future__ import annotations

import os
from pathlib import Path
import subprocess

from mcp.server.fastmcp import FastMCP

from cowork_dispatch.config import load_config
from cowork_dispatch.ollama_client import OllamaClient, OllamaError

config = load_config()
client = OllamaClient(config)
mcp = FastMCP("cowork-dispatch", instructions="Use local delegate tools for bounded coding tasks and verification.")
DEFAULT_WORKSPACE_ROOT = Path(__file__).resolve().parents[2]


def workspace_root() -> Path:
    configured_root = os.getenv("COWORK_WORKSPACE_ROOT")
    if configured_root:
        return Path(configured_root).expanduser().resolve()
    return DEFAULT_WORKSPACE_ROOT


@mcp.tool()
def ask_ollama(prompt: str, system: str = "") -> str:
    """Send a prompt to the local Ollama server and return its reply."""
    try:
        result = client.generate(prompt=prompt, system=system or None)
    except OllamaError as exc:
        raise ValueError(str(exc)) from exc
    return result.text


@mcp.tool()
def run_pytest() -> str:
    """Run the workspace test suite with uv and return the output."""
    result = subprocess.run(
        ["uv", "run", "pytest"],
        cwd=workspace_root(),
        capture_output=True,
        text=True,
        check=False,
        stdin=subprocess.DEVNULL,
    )
    output = (result.stdout + result.stderr).strip()
    if result.returncode != 0:
        raise ValueError(output or f"pytest failed with exit code {result.returncode}")
    return output or "pytest completed successfully with no output."


def main() -> None:
    mcp.run()


if __name__ == "__main__":
    main()