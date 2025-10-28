#!/bin/bash
# Personal Access Token을 입력하세요
echo "GitHub Personal Access Token을 입력하세요:"
read -s TOKEN

cd /Users/ose-ung/Projects/methodus

# Token을 사용하여 remote 추가
git remote add origin https://${TOKEN}@github.com/Methodus-dev/methodus-shorts-planner.git

# Push
git push -u origin main

echo ""
echo "✅ GitHub에 푸시 완료!"
echo "Vercel이 자동으로 배포를 시작합니다."
echo ""
echo "배포 확인: https://vercel.com/methodus-projects/methodus-shorts-planner"


