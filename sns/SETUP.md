# SNS自動投稿 セットアップ手順

---

## 全体の仕組み

```
毎週日曜 10:00  →  Claude が新しいツイート文を自動生成 → queue.json に追加
月・水・金・日 21:00  →  queue.json から1件取り出して X に自動投稿
```

---

## ステップ1：X Developer アカウントを作る（15分）

1. https://developer.twitter.com にアクセス
2. 「Sign up」→ 利用目的を英語で入力（例：`Posting content for my manga project`）
3. 審査通過後、「Create Project」→「Create App」
4. 「Keys and Tokens」タブで以下を取得・メモ：
   - API Key
   - API Key Secret
   - Access Token（**Read and Write** 権限で作成すること）
   - Access Token Secret

---

## ステップ2：Anthropic API キーを取得する（5分）

1. https://console.anthropic.com にアクセス
2. 「API Keys」→「Create Key」
3. 表示されたキーをメモ（一度しか表示されない）

---

## ステップ3：GitHub Secrets に登録する（5分）

GitHub リポジトリの **Settings → Secrets and variables → Actions** を開き、
以下の5つを「New repository secret」で登録：

| Secret名 | 値 |
|----------|-----|
| `X_API_KEY` | X の API Key |
| `X_API_SECRET` | X の API Key Secret |
| `X_ACCESS_TOKEN` | X の Access Token |
| `X_ACCESS_TOKEN_SECRET` | X の Access Token Secret |
| `ANTHROPIC_API_KEY` | Anthropic の API Key |

---

## ステップ4：mainブランチにマージして有効化

GitHub Actions は `main` ブランチの `.github/workflows/` を読む。
現在のブランチ `claude/rename-mira-files-YrPpY` を main にマージすると自動で動き始める。

---

## 手動で今すぐ投稿したいとき

GitHub リポジトリの **Actions タブ** → 「X 自動投稿」→ 「Run workflow」

---

## 投稿文を手動で追加したいとき

`sns/queue.json` に以下の形式で追加するだけ：

```json
{
  "id": "任意のID",
  "text": "投稿したい文章（140字以内）\n\n#ミラの未来視",
  "status": "pending"
}
```

---

## Note について

Note には公式APIがないため、以下の半自動運用を推奨：

1. `sns/note_ep01_intro.md` などの記事ファイルをこのリポジトリで管理
2. Claudeに「Note記事書いて」と指示 → mdファイルを生成・プッシュ
3. GitHub上で内容確認 → Note にコピー＆ペーストして投稿

完全自動投稿が必要な場合は Playwright による
ブラウザ自動化も構築可能（要相談）。
