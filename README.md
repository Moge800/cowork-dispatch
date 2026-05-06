# cowork-dispatch

GitHub Copilot からローカル Ollama を補助ツールとして使うための最小 MCP サーバーです。

現状の v1 は `ask_ollama` と `run_pytest` を公開します。Copilot の本体モデルを置き換えるものではなく、ローカル LLM を追加の相談先として接続する前提です。

## セットアップ

1. Ollama を起動し、利用するモデルを pull します。
2. Python 3.11+ と uv を用意します。
3. 依存関係を入れます。

```powershell
uv sync --extra dev
```

4. 環境変数を設定します。

```powershell
Copy-Item .env.example .env
```

5. MCP サーバーを stdio で起動します。

```powershell
uv run cowork-dispatch
```

詳しい接続手順は SETUP.md にまとめています。

## 公開ツール

- `ask_ollama`: ローカル Ollama の `/api/generate` にプロンプトを送り、応答テキストを返します。
- `run_pytest`: このワークスペースで `uv run pytest` を実行し、結果を返します。
