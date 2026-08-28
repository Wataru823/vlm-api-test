"""VLM APIスクリプト間で共通の処理をまとめたモジュール。"""

import base64
import mimetypes
import sys
import time
from contextlib import contextmanager

# 画像入力を省略した場合に使うデフォルトのテキストプロンプト
DEFAULT_TEXT_PROMPT = "What is the capital of France?"


def get_image_path_arg() -> str | None:
    """コマンドライン引数から画像パスを取得する（指定がなければNone）。"""
    return sys.argv[1] if len(sys.argv) > 1 else None


def encode_image(image_path: str) -> tuple[str, str]:
    """画像ファイルをBase64エンコードし、(base64文字列, MIMEタイプ) を返す。"""
    mime_type, _ = mimetypes.guess_type(image_path)
    if mime_type is None:
        mime_type = "application/octet-stream"
    with open(image_path, "rb") as f:
        b64_data = base64.b64encode(f.read()).decode("utf-8")
    return b64_data, mime_type


def encode_image_as_data_url(image_path: str) -> str:
    """画像ファイルをBase64エンコードし、data URL形式の文字列で返す。"""
    b64_data, mime_type = encode_image(image_path)
    return f"data:{mime_type};base64,{b64_data}"


@contextmanager
def timed_request():
    """リクエストの送信中メッセージと経過時間の表示を行うコンテキストマネージャー。"""
    print("リクエスト送信中...", flush=True)
    start = time.monotonic()
    yield
    elapsed = time.monotonic() - start
    print(f"応答受信（{elapsed:.1f}秒）", flush=True)
