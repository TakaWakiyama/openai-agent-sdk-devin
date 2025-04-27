# Slack Code Fix Bot with OpenAI Agent SDK & Codex CLI

## 概要

Slackメンションを契機に、OpenAI Codex CLIとAgent SDKを活用してGitHubリポジトリのコード修正・PR作成を自動化するBotです。Google Cloud Run上で動作し、Slack→Cloud Run→GitHubの一連のDevOps自動化を実現します。

## アーキテクチャ

- Slackで@Botメンション → Cloud RunのFlaskアプリがイベント受信
- Codex CLI（Node.js製）で指示に基づきコード修正
- GitHubへ新規ブランチをpushし、PRを自動作成
- PRリンクをSlackに返信

## ディレクトリ構成

```
project-root/
├── main.py               # Flaskサーバー：Slackイベント受付とメンション処理エントリーポイント
├── codex_agent.py        # Codex CLIを用いたコード修正とGit操作のロジック
├── requirements.txt      # 依存パッケージ（slack-sdk, openai, requests など）
├── Dockerfile            # Cloud Run用Docker定義
└── README.md             # セットアップ手順や使い方のドキュメント
```

## 必要な環境変数

- `SLACK_BOT_TOKEN` : Slack Bot User OAuth Token (xoxb-...)
- `SLACK_SIGNING_SECRET` : Slack AppのSigning Secret
- `OPENAI_API_KEY` : OpenAI APIキー
- `GITHUB_TOKEN` : GitHub Personal Access Token (repo権限)

## セットアップ手順

1. **Slack App作成**
   - Event Subscriptionsで`app_mention`を購読
   - OAuthスコープ: `app_mentions:read`, `chat:write`, `reactions:write`
   - Botをワークスペースにインストールし、トークン/シークレットを取得
2. **GitHubトークン発行**
   - 対象リポジトリにアクセス可能なPATを作成
3. **OpenAI APIキー取得**
   - [OpenAI Platform](https://platform.openai.com/)でAPIキーを発行
4. **Cloud Run用Dockerイメージ作成**
   - Node.js 22+, Codex CLI, Git, Python依存を含める
   - 例: `docker build -t gcr.io/<PROJECT_ID>/slack-codex-bot:latest .`
5. **Cloud Runへデプロイ**
   - `gcloud run deploy slack-codex-bot --image gcr.io/<PROJECT_ID>/slack-codex-bot:latest --platform managed --region <リージョン> --allow-unauthenticated --memory 1Gi --set-env-vars SLACK_BOT_TOKEN=...,SLACK_SIGNING_SECRET=...,OPENAI_API_KEY=...,GITHUB_TOKEN=...`
6. **Slackイベント購読URL設定**
   - Cloud Runのエンドポイント`https://.../slack/events`をSlack AppのRequest URLに設定

## 主要技術

- Python 3.11 (Flask, slack_sdk, requests)
- Node.js 22+ / Codex CLI (@openai/codex)
- Google Cloud Run
- GitHub REST API

## 使い方

Slackで`@Bot repo:org/repo 修正指示`の形式でメンションすると、Botが自動でコード修正PRを作成し、リンクを返信します。

---

## 参考

- [Slack API](https://api.slack.com/)
- [OpenAI Codex CLI](https://github.com/openai/codex)
- [OpenAI Agents SDK](https://github.com/openai/openai-agents)
- [GitHub API](https://docs.github.com/en/rest)
- [Google Cloud Run](https://cloud.google.com/run)
