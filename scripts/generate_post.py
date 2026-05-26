"""
Claude APIで新しいX投稿文を自動生成してキューに追加するスクリプト。
GitHub Actionsから呼び出される。
"""

import os
import json
import anthropic
from pathlib import Path
from datetime import datetime

QUEUE_FILE = Path(__file__).parent.parent / "sns" / "queue.json"
WORLD_FILE = Path(__file__).parent.parent / "world_setting.md"
CHARA_FILE = Path(__file__).parent.parent / "mira_character.md"
EP2_FILE   = Path(__file__).parent.parent / "scenarios" / "ep02_worldbuilding.md"

SYSTEM_PROMPT = """
あなたは近未来マンガ「ミラの未来視」のSNS担当です。
キャラクターや世界観の設定資料をもとに、X（Twitter）用の投稿文を1件作成してください。

ルール：
- 140文字以内
- 改行を使って読みやすくする
- 末尾に関連ハッシュタグ（#ミラの未来視 #創作 など）をつける
- ネタバレしすぎない
- 毎回違う切り口（セリフ・設定・キャラ・世界観・制作メモ）でローテーション
- 宣伝くさくせず、読み物として面白い内容にする
- 投稿文のみ返答し、説明・前置き不要
"""


def load_text(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def load_queue():
    if QUEUE_FILE.exists():
        with open(QUEUE_FILE, encoding="utf-8") as f:
            return json.load(f)
    return {"posts": []}


def save_queue(data):
    with open(QUEUE_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def generate():
    context = "\n\n".join([
        load_text(WORLD_FILE),
        load_text(CHARA_FILE),
        load_text(EP2_FILE),
    ])

    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=300,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": f"設定資料:\n{context}"}],
    )
    return message.content[0].text.strip()


def main():
    text = generate()
    print("生成されたツイート:")
    print(text)

    queue = load_queue()
    queue["posts"].append({
        "id": f"auto_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}",
        "text": text,
        "status": "pending",
        "generated_at": datetime.utcnow().isoformat(),
    })
    save_queue(queue)
    print("キューに追加しました。")


if __name__ == "__main__":
    main()
