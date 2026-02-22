#!/usr/bin/env python3
"""
Claude Code の UserPromptSubmit フックから呼び出され、
チャットへの入力メッセージを Twitter に自動投稿するスクリプト。

必要な環境変数:
  TWITTER_API_KEY
  TWITTER_API_SECRET
  TWITTER_ACCESS_TOKEN
  TWITTER_ACCESS_TOKEN_SECRET

インストール:
  pip install tweepy
"""

import json
import os
import sys

TWEET_MAX_LENGTH = 280


def post_tweet(text: str) -> None:
    import tweepy

    client = tweepy.Client(
        consumer_key=os.environ["TWITTER_API_KEY"],
        consumer_secret=os.environ["TWITTER_API_SECRET"],
        access_token=os.environ["TWITTER_ACCESS_TOKEN"],
        access_token_secret=os.environ["TWITTER_ACCESS_TOKEN_SECRET"],
    )
    client.create_tweet(text=text[:TWEET_MAX_LENGTH])


def main() -> None:
    raw = sys.stdin.read()
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as e:
        print(f"[post_to_twitter] JSON parse error: {e}", file=sys.stderr)
        sys.exit(0)

    message = data.get("prompt", "").strip()
    if not message:
        sys.exit(0)

    required_vars = [
        "TWITTER_API_KEY",
        "TWITTER_API_SECRET",
        "TWITTER_ACCESS_TOKEN",
        "TWITTER_ACCESS_TOKEN_SECRET",
    ]
    missing = [v for v in required_vars if not os.environ.get(v)]
    if missing:
        print(
            f"[post_to_twitter] 環境変数が未設定です: {', '.join(missing)}",
            file=sys.stderr,
        )
        sys.exit(0)

    try:
        post_tweet(message)
        print(f"[post_to_twitter] ツイート投稿完了: {message[:50]}…", file=sys.stderr)
    except Exception as e:
        print(f"[post_to_twitter] 投稿失敗: {e}", file=sys.stderr)

    sys.exit(0)


if __name__ == "__main__":
    main()
