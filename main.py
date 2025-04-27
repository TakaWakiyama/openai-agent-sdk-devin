import os
import re
from flask import Flask, request, jsonify
from slack_sdk.web import WebClient
from slack_sdk.signature import SignatureVerifier
import requests
from codex_agent import run_codex_and_create_pr

# 環境変数からトークン類を取得
SLACK_BOT_TOKEN = os.environ["SLACK_BOT_TOKEN"]
SLACK_SIGNING_SECRET = os.environ["SLACK_SIGNING_SECRET"]
OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]
GITHUB_TOKEN = os.environ["GITHUB_TOKEN"]

# Slackクライアントおよび署名検証器を初期化
slack_client = WebClient(token=SLACK_BOT_TOKEN)
signing_verifier = SignatureVerifier(SLACK_SIGNING_SECRET)

app = Flask(__name__)

def parse_mention_text(text):
    repo = None
    m = re.search(r'repo:([\w\-\/]+)', text)
    if m:
        repo = m.group(1)
    cleaned = re.sub(r'<@[A-Z0-9]+>', '', text).strip()
    if repo:
        cleaned = cleaned.replace(f"repo:{repo}", "").strip()
    instruction = cleaned
    return repo, instruction


@app.route("/slack/events", methods=["POST"])
def handle_slack_event():
    if not signing_verifier.is_valid_request(request.get_data(), request.headers):
        return ("Invalid request", 403)
    data = request.get_json()
    if data.get("type") == "url_verification":
        return jsonify({"challenge": data.get("challenge")})
    event = data.get("event", {})
    if event.get("type") == "app_mention":
        slack_client.reactions_add(
            channel=event["channel"], timestamp=event["ts"], name="speech_balloon"
        )
        # Parse mention text and run codex agent to create PR
        text = event.get("text", "")
        repo, instruction = parse_mention_text(text)
        pr_url = None
        if repo and instruction:
            pr_url = run_codex_and_create_pr(repo, instruction, GITHUB_TOKEN, OPENAI_API_KEY)
        if pr_url:
            msg = (
                f"<@{event['user']}> 修正したコードのPRを作成しました: {pr_url}"
            )
            slack_client.chat_postMessage(
                channel=event["channel"], thread_ts=event["ts"], text=msg
            )
            slack_client.reactions_add(
                channel=event["channel"], timestamp=event["ts"], name="white_check_mark"
            )
        else:
            msg = f"<@{event['user']}> 指示の処理中にエラーが発生しました。"
            slack_client.chat_postMessage(
                channel=event["channel"], thread_ts=event["ts"], text=msg
            )
    return ("", 200)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))