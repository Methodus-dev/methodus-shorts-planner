"""
Methodus Shorts Planner - 간소화된 백엔드
Render 무료 플랜용 최소 의존성 버전
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict
import json
from datetime import datetime
from pathlib import Path
import os

app = FastAPI(
    title="Methodus Shorts Planner API",
    description="YouTube 급상승 영상 분석 API",
    version="1.0.0"
)

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 간단한 데이터 모델
class TrendingVideo(BaseModel):
    title: str
    views: str
    category: str
    language: str
    video_type: str
    youtube_url: str
    thumbnail: str
    trend_score: int
    crawled_at: str

class TrendingVideosResponse(BaseModel):
    trending_videos: List[TrendingVideo]
    count: int
    total_count: int
    last_updated: str
    source: str

# 샘플 데이터 (실제로는 데이터베이스나 파일에서 로드)
SAMPLE_VIDEOS = [
    {
        "title": "7 Side Hustles Students Can Start In 2025",
        "views": "6.9M",
        "category": "창업/부업",
        "language": "영어",
        "video_type": "롱폼",
        "youtube_url": "https://www.youtube.com/watch?v=2SLSser4y6U",
        "thumbnail": "💼",
        "trend_score": 95,
        "crawled_at": datetime.now().isoformat()
    },
    {
        "title": "부업으로 월 100만원 벌기",
        "views": "2.3M",
        "category": "창업/부업",
        "language": "한국어",
        "video_type": "쇼츠",
        "youtube_url": "https://www.youtube.com/shorts/abc123",
        "thumbnail": "💰",
        "trend_score": 88,
        "crawled_at": datetime.now().isoformat()
    },
    {
        "title": "AI로 돈 버는 방법 2025",
        "views": "1.8M",
        "category": "과학기술",
        "language": "한국어",
        "video_type": "롱폼",
        "youtube_url": "https://www.youtube.com/watch?v=def456",
        "thumbnail": "🤖",
        "trend_score": 92,
        "crawled_at": datetime.now().isoformat()
    },
    {
        "title": "주식 투자 초보자 가이드",
        "views": "3.2M",
        "category": "재테크/금융",
        "language": "한국어",
        "video_type": "쇼츠",
        "youtube_url": "https://www.youtube.com/shorts/ghi789",
        "thumbnail": "📈",
        "trend_score": 85,
        "crawled_at": datetime.now().isoformat()
    },
    {
        "title": "How to Make Money Online in 2025",
        "views": "4.1M",
        "category": "마케팅/비즈니스",
        "language": "영어",
        "video_type": "롱폼",
        "youtube_url": "https://www.youtube.com/watch?v=jkl012",
        "thumbnail": "💻",
        "trend_score": 90,
        "crawled_at": datetime.now().isoformat()
    }
]

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Methodus Shorts Planner API",
        "version": "1.0.0",
        "status": "running",
        "docs": "/docs"
    }

@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "methodus-shorts-planner",
        "version": "1.0.0"
    }

@app.get("/api/youtube/trending", response_model=TrendingVideosResponse)
async def get_youtube_trending(
    count: int = 20,
    category: Optional[str] = None,
    region: Optional[str] = None,
    language: Optional[str] = None,
    min_trend_score: Optional[int] = None,
    sort_by: str = "trend_score",
    video_type: Optional[str] = None,
    time_filter: Optional[str] = None
):
    """YouTube 급상승 동영상 조회 (필터링 지원)"""
    try:
        # 샘플 데이터에서 필터링
        filtered_videos = SAMPLE_VIDEOS.copy()
        
        # 카테고리 필터
        if category:
            filtered_videos = [v for v in filtered_videos if v.get('category') == category]
        
        # 언어 필터
        if language:
            filtered_videos = [v for v in filtered_videos if v.get('language') == language]
        
        # 영상 타입 필터
        if video_type:
            if video_type == 'shorts':
                video_type_filter = '쇼츠'
            elif video_type == 'long':
                video_type_filter = '롱폼'
            else:
                video_type_filter = video_type
            filtered_videos = [v for v in filtered_videos if v.get('video_type') == video_type_filter]
        
        # 트렌드 점수 필터
        if min_trend_score:
            filtered_videos = [v for v in filtered_videos if v.get('trend_score', 0) >= min_trend_score]
        
        # 정렬
        if sort_by == "trend_score":
            filtered_videos.sort(key=lambda x: x.get('trend_score', 0), reverse=True)
        elif sort_by == "views":
            def parse_views(views_str):
                if 'M' in views_str:
                    return float(views_str.replace('M', '')) * 1000000
                elif 'K' in views_str:
                    return float(views_str.replace('K', '')) * 1000
                else:
                    try:
                        return float(views_str.replace(',', ''))
                    except:
                        return 0
            filtered_videos.sort(key=lambda x: parse_views(x.get('views', '0')), reverse=True)
        
        # 개수 제한
        final_videos = filtered_videos[:count]
        
        return TrendingVideosResponse(
            trending_videos=final_videos,
            count=len(final_videos),
            total_count=len(filtered_videos),
            last_updated=datetime.now().isoformat(),
            source="sample_data"
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"영상 조회 실패: {str(e)}")

@app.get("/api/youtube/filter-options")
async def get_filter_options():
    """사용 가능한 필터 옵션 제공"""
    return {
        "categories": [
            "창업/부업", "재테크/금융", "과학기술", "자기계발", "마케팅/비즈니스",
            "요리/음식", "게임", "운동/건강", "교육/학습", "음악"
        ],
        "regions": ["국내", "해외"],
        "languages": ["한국어", "영어"],
        "sort_options": [
            {"value": "trend_score", "label": "트렌드 점수"},
            {"value": "views", "label": "조회수"},
            {"value": "crawled_at", "label": "최신순"}
        ],
        "trend_score_range": {
            "min": 1,
            "max": 100,
            "default": 50
        }
    }

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)

# Render용 Gunicorn 설정
if __name__ != "__main__":
    import gunicorn.app.wsgiapp as wsgi
    wsgi.run()
