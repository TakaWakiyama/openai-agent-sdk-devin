import os
from codex_agent import run_codex_and_create_pr

# テスト用パラメータ（適宜書き換えてください）
repo = os.environ.get("TEST_REPO", "TakaWakiyama/openai-agent-sdk-devin")
instruction = os.environ.get("TEST_INSTRUCTION", "READ TODO.md and fix the codes.")
github_token = os.environ["GITHUB_TOKEN"]
openai_api_key = os.environ["OPENAI_API_KEY"]

print(f"Testing Codex PR creation for repo: {repo}")
print(f"Instruction: {instruction}")

pr_url = run_codex_and_create_pr(repo, instruction, github_token, openai_api_key)

if pr_url:
    print("PR作成成功! PR URL:")
    print(pr_url)
else:
    print("PR作成に失敗しました。")
    print("エラーやトークン設定を確認してください。")