from __future__ import annotations

from pathlib import Path
import subprocess

from mcp.server.fastmcp import FastMCP

from cowork_dispatch.config import load_config
from cowork_dispatch.ollama_client import OllamaClient, OllamaError

config = load_config()
client = OllamaClient(config)
mcp = FastMCP("cowork-dispatch", instructions="Use local delegate tools for bounded coding tasks and verification.")
WORKSPACE_ROOT = Path(__file__).resolve().parents[2]


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
        cwd=WORKSPACE_ROOT,
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