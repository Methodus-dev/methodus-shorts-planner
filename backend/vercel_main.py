"""
Vercel용 FastAPI 엔트리포인트
"""
from main import app

# Vercel이 이 파일을 serverless function으로 실행
handler = app

