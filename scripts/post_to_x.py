"""
X（Twitter）自動投稿スクリプト
sns/queue.json のキューから1件取り出してXに投稿する。
GitHub Actionsから呼び出される。
"""

import os
import json
import tweepy
import sys
from pathlib import Path

QUEUE_FILE = Path(__file__).parent.parent / "sns" / "queue.json"


def load_queue():
    if not QUEUE_FILE.exists():
        print("キューファイルが見つかりません:", QUEUE_FILE)
        sys.exit(0)
    with open(QUEUE_FILE, encoding="utf-8") as f:
        return json.load(f)


def save_queue(data):
    with open(QUEUE_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def post_tweet(text: str) -> str:
    client = tweepy.Client(
        consumer_key=os.environ["X_API_KEY"],
        consumer_secret=os.environ["X_API_SECRET"],
        access_token=os.environ["X_ACCESS_TOKEN"],
        access_token_secret=os.environ["X_ACCESS_TOKEN_SECRET"],
    )
    response = client.create_tweet(text=text)
    return response.data["id"]


def main():
    queue = load_queue()
    pending = [p for p in queue["posts"] if p["status"] == "pending"]

    if not pending:
        print("投稿キューが空です。sns/queue.json に追加してください。")
        sys.exit(0)

    post = pending[0]
    print(f"投稿中: {post['text'][:40]}…")

    try:
        tweet_id = post_tweet(post["text"])
        post["status"] = "done"
        post["tweet_id"] = tweet_id
        print(f"投稿完了: https://x.com/i/web/status/{tweet_id}")
    except Exception as e:
        post["status"] = "error"
        post["error"] = str(e)
        print(f"投稿失敗: {e}")
        sys.exit(1)
    finally:
        save_queue(queue)


if __name__ == "__main__":
    main()
