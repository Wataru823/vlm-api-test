# keio_azure_test

Azure AI Foundry経由のGPT-5.6、およびGemini 3.1 Proの動作確認用スクリプト集です。
テキスト入力・画像入力の両方に対応しています。

## 構成

| パス | 内容 |
| --- | --- |
| `baseline/` | 各モデルの動作確認用スクリプト（`common.py` に共通処理をまとめています） |
| `sample/` | 動作確認用のサンプル画像 |

## セットアップ

[uv](https://docs.astral.sh/uv/) を使用します。

```bash
uv sync
```

`.env.example` を `.env` にコピーし、各APIキーを設定してください。

```bash
cp .env.example .env
```

| 変数名 | 説明 |
| --- | --- |
| `gpt_5_6_sol_project_endpoint` | Azure AI FoundryのプロジェクトエンドポイントURL |
| `gpt_5_6_sol_api_key` | Azure AI Foundryで発行したAPIキー |
| `gemini_3_1_pro_api_key` | Gemini APIキー |

`.env` はgitignoreされているため、実際のキーをコミットする心配はありません。

## 使い方

### GPT-5.6 (Azure AI Foundry)

```bash
# テキストのみ
uv run baseline/gpt_5_6_sol_high.py

# 画像入力（画像内の文字を読み取る）
uv run baseline/gpt_5_6_sol_high.py sample/mnist.png
```

- Responses API（`/openai/v1`）を使用しています。
- `reasoning.effort` を `"high"`（最上位）に設定しています。
- GPT-5系のreasoningモデルのため `temperature` パラメーターは指定できません。

### Gemini 3.1 Pro

```bash
# テキストのみ
uv run baseline/gemini_3_1_pro_high.py

# 画像入力
uv run baseline/gemini_3_1_pro_high.py sample/mnist.png
```

- Interactions APIを使用しています。
- `thinking_level` を `"high"` に設定しています。

## 補足

- 実行中は「リクエスト送信中...」と経過時間が表示されるため、処理が固まっているのか実行中なのかが分かります。
- 画像はローカルファイルをBase64エンコードしてインラインで送信します（URLやアップロード方式ではありません）。
