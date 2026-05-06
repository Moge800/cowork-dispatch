# Setup

## 前提

- Ollama がローカルで動いていること
- 対象モデルが取得済みであること
- Python 3.11 以上
- uv が使えること

## ローカル確認

1. Ollama 側の確認

```powershell
ollama list
ollama run qwen3:8b "hello"
```

2. 依存関係の導入

```powershell
uv sync --extra dev
```

3. テスト

```powershell
uv run pytest
```

4. MCP サーバー起動

```powershell
uv run cowork-dispatch
```

## Copilot 側での接続

利用中の Copilot Chat / agent mode の MCP 登録方法に合わせて、このサーバーを stdio コマンドで登録します。

- command: uv
- args: run, cowork-dispatch
- env file: .env
- env: OLLAMA_HOST, OLLAMA_MODEL, OLLAMA_TIMEOUT_SECONDS

このリポジトリには VS Code 用の例として `.vscode/mcp.json` を含めています。必要に応じて `.env.example` を `.env` にコピーし、モデル名やタイムアウトを変更してください。

## 公開ツール

- `ask_ollama`: ローカル Ollama の `/api/generate` にプロンプトを送り、応答テキストを返します。
- `run_pytest`: このワークスペースで `uv run pytest` を実行し、結果を返します。

## v1 の制約

- 同期応答のみ
- デフォルトは単一モデル前提
- 会話履歴は保持しない
- Ollama 側の詳細オプションはまだ expose しない