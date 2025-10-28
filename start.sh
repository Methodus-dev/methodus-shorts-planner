#!/bin/bash

# Content Creator AI 실행 스크립트

echo "🚀 Content Creator AI 시작 중..."

# 현재 디렉토리 확인
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# 백엔드 시작
echo "📡 백엔드 서버 시작 중..."
cd backend
source venv/bin/activate
uvicorn main:app --reload --host 0.0.0.0 --port 8000 > ../logs/backend.log 2>&1 &
BACKEND_PID=$!
echo "   ✅ 백엔드 서버 시작됨 (PID: $BACKEND_PID)"
echo "   📍 http://localhost:8000"
cd ..

# 잠시 대기
sleep 2

# 프론트엔드 시작
echo "🎨 프론트엔드 서버 시작 중..."
cd frontend
npm run dev > ../logs/frontend.log 2>&1 &
FRONTEND_PID=$!
echo "   ✅ 프론트엔드 서버 시작됨 (PID: $FRONTEND_PID)"
echo "   📍 http://localhost:5173"
cd ..

# PID 저장
mkdir -p logs
echo $BACKEND_PID > logs/backend.pid
echo $FRONTEND_PID > logs/frontend.pid

echo ""
echo "✨ Content Creator AI가 실행 중입니다!"
echo ""
echo "📱 프론트엔드: http://localhost:5173"
echo "📡 백엔드 API: http://localhost:8000"
echo "📖 API 문서: http://localhost:8000/docs"
echo ""
echo "⏹️  종료하려면 ./stop.sh 를 실행하세요"
echo ""

