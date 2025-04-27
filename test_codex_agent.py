import os
from dotenv import load_dotenv
from codex_agent import run_codex_and_create_pr

# .envファイルの読み込み
load_dotenv()

# テスト用パラメータ（適宜書き換えてください）
repo = os.environ.get("TEST_REPO", "yourorg/yourrepo")
instruction = os.environ.get("TEST_INSTRUCTION", "Fix typo in README.md")
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