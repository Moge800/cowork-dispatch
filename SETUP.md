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
- args: run, --link-mode, copy, cowork-dispatch
- env file: .env
- env: OLLAMA_HOST, OLLAMA_MODEL, OLLAMA_TIMEOUT_SECONDS

このリポジトリには VS Code 用の例として `.vscode/mcp.json` を含めています。必要に応じて `.env.example` を `.env` にコピーし、モデル名やタイムアウトを変更してください。

`command` は `uv` を指定します。`uvx` や `uv tool run` を使うと、`run` が uv のサブコマンドではなくパッケージ名として解釈され、`Package 'run' does not provide any executables.` のようなエラーになることがあります。

## 他のワークスペースから使う

このリポジトリの `.vscode/mcp.json` は、`cowork-dispatch` リポジトリ自身で使うための設定です。他のプロジェクトへそのままコピーすると、コピー先のワークスペースで `uv run cowork-dispatch` を探すため、コマンドが見つからないことがあります。

他のプロジェクトから中央の `cowork-dispatch` リポジトリを使う場合は、コピー先プロジェクトの `.vscode/mcp.json` を次のようにします。`/path/to/cowork-dispatch` は自分の配置場所に合わせて変更してください。

```json
{
	"servers": {
		"cowork-dispatch": {
			"type": "stdio",
			"command": "uv",
			"args": [
				"--directory",
				"/path/to/cowork-dispatch",
				"run",
				"--link-mode",
				"copy",
				"cowork-dispatch"
			],
			"envFile": "${workspaceFolder}/.env",
			"env": {
				"COWORK_WORKSPACE_ROOT": "${workspaceFolder}"
			}
		}
	}
}
```

`envFile` はコピー先プロジェクトの `.env` を読みます。`COWORK_WORKSPACE_ROOT` は `run_pytest` がどのワークスペースで `uv run pytest` を実行するかを指定します。

手元のターミナルで `uv run cowork-dispatch` を起動しているだけでは、別ワークスペースの Copilot には MCP サーバーとして接続されません。使いたいワークスペースごとに MCP 設定を登録してください。

## 公開ツール

- `ask_ollama`: ローカル Ollama の `/api/generate` にプロンプトを送り、応答テキストを返します。
- `run_pytest`: このワークスペースで `uv run pytest` を実行し、結果を返します。

## v1 の制約

- 同期応答のみ
- デフォルトは単一モデル前提
- 会話履歴は保持しない
- Ollama 側の詳細オプションはまだ expose しない