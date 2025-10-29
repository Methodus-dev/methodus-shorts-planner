"""
Methodus Shorts Planner - 실제 크롤링 백엔드
YouTube 데이터를 실제로 크롤링하여 제공
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict
import json
from datetime import datetime
from pathlib import Path
import os
import threading
import time
from youtube_ytdlp_crawler import YouTubeYtDlpCrawler

app = FastAPI(
    title="Methodus Shorts Planner API",
    description="YouTube 급상승 영상 분석 API - 실제 크롤링 데이터",
    version="2.0.0"
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
    region: Optional[str] = None
    keywords: Optional[List[str]] = None
    why_viral: Optional[str] = None
    engagement: Optional[str] = None

class TrendingVideosResponse(BaseModel):
    trending_videos: List[TrendingVideo]
    count: int
    total_count: int
    last_updated: str
    source: str

# 크롤러 초기화
ytdlp_crawler = YouTubeYtDlpCrawler()

# 자동 크롤링 설정
def auto_crawl_loop():
    """2시간마다 자동 크롤링"""
    while True:
        try:
            print(f"🔄 [{datetime.now().strftime('%H:%M:%S')}] 자동 크롤링 시작...")
            
            main_categories = [
                '창업/부업', '재테크/금융', '과학기술', '자기계발', '마케팅/비즈니스',
                '요리/음식', '게임', '운동/건강', '교육/학습', '음악'
            ]
            
            # 카테고리별로 30개씩 수집 (총 300개)
            videos = ytdlp_crawler.get_trending_by_category(main_categories, per_category=30)
            
            if videos and len(videos) > 0:
                ytdlp_crawler.save_to_cache(videos)
                print(f"✅ 자동 크롤링 완료: {len(videos)}개 영상 업데이트")
            else:
                print("⚠️ 자동 크롤링 실패")
                
        except Exception as e:
            print(f"❌ 자동 크롤링 오류: {e}")
        
        # 2시간 대기
        time.sleep(2 * 60 * 60)

# 서버 시작 시 초기 크롤링
def initial_crawl():
    """서버 시작 시 초기 크롤링"""
    time.sleep(5)  # 서버 시작 후 5초 대기
    try:
        print("🎬 초기 크롤링 시작...")
        
        main_categories = [
            '창업/부업', '재테크/금융', '과학기술', '자기계발', '마케팅/비즈니스',
            '요리/음식', '게임', '운동/건강', '교육/학습', '음악'
        ]
        
        videos = ytdlp_crawler.get_trending_by_category(main_categories, per_category=30)
        
        if videos and len(videos) > 0:
            ytdlp_crawler.save_to_cache(videos)
            print(f"✅ 초기 크롤링 완료: {len(videos)}개 영상 수집")
        else:
            print("⚠️ 초기 크롤링 실패")
            
    except Exception as e:
        print(f"❌ 초기 크롤링 오류: {e}")

# 백그라운드에서 크롤링 시작
threading.Thread(target=initial_crawl, daemon=True).start()
threading.Thread(target=auto_crawl_loop, daemon=True).start()

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Methodus Shorts Planner API - 실제 크롤링 데이터",
        "version": "2.0.0",
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
        "version": "2.0.0"
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
    """YouTube 급상승 동영상 조회 (실제 크롤링 데이터)"""
    try:
        # 캐시된 데이터 로드
        cached_videos = ytdlp_crawler.load_from_cache()
        
        if not cached_videos or len(cached_videos) == 0:
            # 캐시가 없으면 샘플 데이터 반환
            return TrendingVideosResponse(
                trending_videos=[],
                count=0,
                total_count=0,
                last_updated=datetime.now().isoformat(),
                source="no_data"
            )
        
        # 필터링 적용
        filtered_videos = cached_videos.copy()
        
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
        
        # 지역 필터
        if region:
            filtered_videos = [v for v in filtered_videos if v.get('region') == region]
        
        # 트렌드 점수 필터
        if min_trend_score:
            filtered_videos = [v for v in filtered_videos if v.get('trend_score', 0) >= min_trend_score]
        
        # 정렬
        if sort_by == "trend_score":
            filtered_videos.sort(key=lambda x: x.get('trend_score', 0), reverse=True)
        elif sort_by == "views":
            def parse_views(views_str):
                if 'M' in str(views_str):
                    return float(str(views_str).replace('M', '')) * 1000000
                elif 'K' in str(views_str):
                    return float(str(views_str).replace('K', '')) * 1000
                else:
                    try:
                        return float(str(views_str).replace(',', ''))
                    except:
                        return 0
            filtered_videos.sort(key=lambda x: parse_views(x.get('views', '0')), reverse=True)
        elif sort_by == "crawled_at":
            filtered_videos.sort(key=lambda x: x.get('crawled_at', ''), reverse=True)
        
        # 개수 제한
        final_videos = filtered_videos[:count]
        
        return TrendingVideosResponse(
            trending_videos=final_videos,
            count=len(final_videos),
            total_count=len(filtered_videos),
            last_updated=datetime.now().isoformat(),
            source="crawled_data"
        )
        
    except Exception as e:
        print(f"❌ 영상 조회 오류: {e}")
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

@app.post("/api/youtube/force-refresh")
async def force_refresh():
    """강제 새로고침 - 즉시 크롤링 실행"""
    try:
        print("🔄 강제 새로고침 요청...")
        
        main_categories = [
            '창업/부업', '재테크/금융', '과학기술', '자기계발', '마케팅/비즈니스',
            '요리/음식', '게임', '운동/건강', '교육/학습', '음악'
        ]
        
        videos = ytdlp_crawler.get_trending_by_category(main_categories, per_category=30)
        
        if videos and len(videos) > 0:
            ytdlp_crawler.save_to_cache(videos)
            return {
                "success": True,
                "message": f"새로고침 완료: {len(videos)}개 영상 업데이트",
                "timestamp": datetime.now().isoformat()
            }
        else:
            return {
                "success": False,
                "message": "새로고침 실패",
                "timestamp": datetime.now().isoformat()
            }
            
    except Exception as e:
        print(f"❌ 강제 새로고침 오류: {e}")
        raise HTTPException(status_code=500, detail=f"새로고침 실패: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)

# Render용 Gunicorn 설정
if __name__ != "__main__":
    import gunicorn.app.wsgiapp as wsgi
    wsgi.run()