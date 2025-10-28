#!/bin/bash
# GitHub Repository URL을 입력하세요
# 예: https://github.com/your-username/methodus-shorts-planner.git

REPO_URL="YOUR_GITHUB_REPO_URL"

cd /Users/ose-ung/Projects/methodus

# Remote 추가
git remote add origin $REPO_URL

# Push
git push -u origin main

echo "✅ GitHub에 푸시 완료!"
echo "Vercel이 자동으로 새 배포를 시작합니다."


