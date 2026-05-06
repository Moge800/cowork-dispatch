import subprocess

from cowork_dispatch.server import ask_ollama, mcp, run_pytest


def test_server_exposes_tool() -> None:
    tools = mcp._tool_manager.list_tools()
    assert any(tool.name == "ask_ollama" for tool in tools)
    assert any(tool.name == "run_pytest" for tool in tools)


def test_ask_ollama_uses_client(monkeypatch) -> None:
    class StubResponse:
        text = "local answer"

    def fake_generate(prompt: str, system: str | None = None) -> StubResponse:
        assert prompt == "question"
        assert system == "policy"
        return StubResponse()

    monkeypatch.setattr("cowork_dispatch.server.client.generate", fake_generate)

    assert ask_ollama("question", "policy") == "local answer"


def test_run_pytest_uses_uv(monkeypatch) -> None:
    def fake_run(command: list[str], cwd, capture_output: bool, text: bool, check: bool, stdin):
        assert command == ["uv", "run", "pytest"]
        assert capture_output is True
        assert text is True
        assert check is False
        assert stdin is subprocess.DEVNULL
        assert cwd.name == "cowork-dispatch"
        return subprocess.CompletedProcess(command, 0, stdout="2 passed\n", stderr="")

    monkeypatch.setattr("cowork_dispatch.server.subprocess.run", fake_run)

    assert run_pytest() == "2 passed"
