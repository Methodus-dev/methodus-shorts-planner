#!/bin/bash

# Content Creator AI 종료 스크립트

echo "⏹️  Content Creator AI 종료 중..."

# 현재 디렉토리 확인
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# PID 파일에서 프로세스 종료
if [ -f logs/backend.pid ]; then
    BACKEND_PID=$(cat logs/backend.pid)
    if ps -p $BACKEND_PID > /dev/null 2>&1; then
        kill $BACKEND_PID
        echo "   ✅ 백엔드 서버 종료됨"
    fi
    rm logs/backend.pid
fi

if [ -f logs/frontend.pid ]; then
    FRONTEND_PID=$(cat logs/frontend.pid)
    if ps -p $FRONTEND_PID > /dev/null 2>&1; then
        kill $FRONTEND_PID
        echo "   ✅ 프론트엔드 서버 종료됨"
    fi
    rm logs/frontend.pid
fi

# 관련 프로세스 정리
pkill -f "uvicorn main:app" 2>/dev/null
pkill -f "vite" 2>/dev/null
pkill -f "npm run dev" 2>/dev/null

echo ""
echo "✨ Content Creator AI가 종료되었습니다."
echo ""

