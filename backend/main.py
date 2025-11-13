"""
Methodus Shorts Planner - YouTube Data API v3 백엔드
YouTube 데이터를 공식 API를 통해 제공
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
from youtube_api_service import YouTubeAPIService
from dotenv import load_dotenv

# 환경 변수 로드
load_dotenv()

# Gemini는 선택적으로 import
try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False
    print("⚠️ google-generativeai 패키지가 설치되지 않았습니다 (AI 기능 비활성화)")

app = FastAPI(
    title="Methodus Shorts Planner API",
    description="YouTube 급상승 영상 분석 API - YouTube Data API v3",
    version="3.0.0"
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
    published_at: Optional[str] = None  # 영상 업로드 날짜
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
# crawler = SimpleYouTubeCrawler()

# YouTube API 서비스 초기화
try:
    youtube_service = YouTubeAPIService()
    print("✅ YouTube API 서비스 초기화 완료")
except ValueError as e:
    print(f"⚠️ YouTube API 초기화 실패: {e}")
    print("💡 .env 파일에 YOUTUBE_API_KEY를 설정하세요.")
    print("   설정 방법은 YOUTUBE_API_SETUP.md를 참조하세요.")
    youtube_service = None

# Google Gemini 초기화 (선택적)
gemini_api_key = os.getenv("GEMINI_API_KEY")
gemini_model = None
if GEMINI_AVAILABLE and gemini_api_key:
    try:
        genai.configure(api_key=gemini_api_key)
        gemini_model = genai.GenerativeModel('gemini-2.0-flash')
        print("✅ Google Gemini 2.0 Flash 초기화 완료 (무료!)")
    except Exception as e:
        print(f"⚠️ Gemini API 초기화 실패: {e}")
        gemini_model = None
elif not GEMINI_AVAILABLE:
    print("⚠️ Gemini AI 패키지가 없습니다 (기본 패턴 사용)")
else:
    print("⚠️ GEMINI_API_KEY가 설정되지 않았습니다")

# 캐시된 데이터 저장소
cached_videos = []
last_update_time = None

def save_cache_to_file(videos):
    """캐시 데이터를 파일에 저장"""
    try:
        cache_data = {
            'videos': videos,
            'last_updated': datetime.now().isoformat(),
            'count': len(videos)
        }
        
        cache_file = Path('video_cache.json')
        with open(cache_file, 'w', encoding='utf-8') as f:
            json.dump(cache_data, f, ensure_ascii=False, indent=2)
        
        print(f"💾 캐시 저장 완료: {len(videos)}개 영상")
        return True
    except Exception as e:
        print(f"❌ 캐시 저장 실패: {e}")
        return False

def load_cache_from_file():
    """파일에서 캐시 데이터 로드"""
    try:
        cache_file = Path('video_cache.json')
        if cache_file.exists():
            with open(cache_file, 'r', encoding='utf-8') as f:
                cache_data = json.load(f)
            return cache_data.get('videos', []), cache_data.get('last_updated')
    except Exception as e:
        print(f"❌ 캐시 로드 실패: {e}")
    return [], None

def fetch_youtube_data():
    """YouTube API를 통해 데이터 수집"""
    global cached_videos, last_update_time
    
    if not youtube_service:
        print("❌ YouTube API 서비스가 초기화되지 않았습니다.")
        return False
    
    try:
        print(f"🔄 [{datetime.now().strftime('%H:%M:%S')}] YouTube API 데이터 수집 시작...")
        
        # 카테고리별로 여러 지역에서 종합 데이터 수집
        videos = youtube_service.get_comprehensive_data(
            region_codes=['KR', 'US', 'JP'],  # 한국, 미국, 일본
            min_videos_per_category=100
        )
        
        if videos and len(videos) > 0:
            cached_videos = videos
            last_update_time = datetime.now().isoformat()
            
            # 캐시 저장
            save_cache_to_file(videos)
            
            print(f"✅ YouTube API 데이터 수집 완료: {len(videos)}개 영상")
            return True
        else:
            print("⚠️ 수집된 데이터가 없습니다")
            return False
            
    except Exception as e:
        print(f"❌ YouTube API 데이터 수집 오류: {e}")
        return False

# 자동 데이터 수집 설정 (2시간마다)
def auto_fetch_loop():
    """2시간마다 자동으로 YouTube 데이터 수집"""
    while True:
        time.sleep(2 * 60 * 60)  # 2시간
        fetch_youtube_data()

# 초기 데이터 로드
print("🔄 초기 데이터 로드 중...")
cached_videos, last_update_time = load_cache_from_file()

# 캐시된 데이터가 없으면 즉시 수집
if not cached_videos and youtube_service:
    print("📡 캐시된 데이터가 없어서 즉시 데이터 수집을 시작합니다...")
    fetch_youtube_data()

# 백그라운드에서 자동 데이터 수집 시작
if youtube_service:
    threading.Thread(target=auto_fetch_loop, daemon=True).start()
    print("✅ 자동 데이터 수집 스레드 시작 (2시간 간격)")

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Methodus Shorts Planner API - YouTube Data API v3",
        "version": "3.0.0",
        "status": "running",
        "api_status": "active" if youtube_service else "not_configured",
        "docs": "/docs",
        "setup_guide": "YOUTUBE_API_SETUP.md"
    }

@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "methodus-shorts-planner",
        "version": "3.0.0",
        "youtube_api": "active" if youtube_service else "not_configured",
        "cached_videos": len(cached_videos) if cached_videos else 0,
        "last_update": last_update_time
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
    """YouTube 급상승 동영상 조회 (YouTube Data API v3)"""
    global cached_videos, last_update_time
    
    try:
        # 캐시된 데이터가 없으면 즉시 수집
        if not cached_videos and youtube_service:
            print("📡 캐시된 데이터가 없어서 즉시 데이터 수집을 시작합니다...")
            fetch_youtube_data()
        
        # 캐시된 데이터 사용
        cached_videos = cached_videos if cached_videos else []
        
        if not cached_videos or len(cached_videos) == 0:
            # 데이터가 없으면 빈 응답 반환
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
        
        # 정렬 (한국어 콘텐츠 우선)
        if sort_by == "trend_score":
            # 한국어 콘텐츠를 우선적으로 정렬
            filtered_videos.sort(key=lambda x: (
                x.get('language') != '한국어',  # 한국어가 아니면 True (뒤로)
                -x.get('trend_score', 0)  # 트렌드 점수 높은 순
            ))
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
            last_updated=last_update_time or datetime.now().isoformat(),
            source="youtube_api_v3"
        )
        
    except Exception as e:
        print(f"❌ 영상 조회 오류: {e}")
        raise HTTPException(status_code=500, detail=f"영상 조회 실패: {str(e)}")

@app.get("/api/youtube/filter-options")
async def get_filter_options():
    """사용 가능한 필터 옵션 제공 (실제 데이터 기반)"""
    # 실제 캐시된 데이터에서 카테고리 추출
    unique_categories = set()
    if cached_videos:
        for video in cached_videos:
            cat = video.get('category')
            if cat:
                unique_categories.add(cat)
    
    return {
        "categories": sorted(list(unique_categories)) if unique_categories else [
            "마케팅/비즈니스", "게임", "재테크/금융", "음악", "운동/건강",
            "자기계발", "과학기술", "엔터테인먼트", "교육/학습", "기타"
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

@app.post("/api/ai/generate-title-patterns")
async def generate_title_patterns(request: dict):
    """Google Gemini AI를 사용해서 키워드에 맞는 제목 패턴 생성"""
    keyword = request.get('keyword', '')
    related_videos = request.get('related_videos', [])
    
    if not gemini_model:
        # Gemini가 없으면 기본 패턴 반환
        return {
            "title_patterns": [
                f"{keyword} 완벽 가이드",
                f"{keyword} 핵심 정리",
                f"{keyword} 실전 활용법",
                f"{keyword} 트렌드 분석"
            ],
            "source": "default"
        }
    
    try:
        # 관련 영상 제목들을 문맥으로 제공
        video_titles_context = "\n".join([f"- {v['title']}" for v in related_videos[:10]]) if related_videos else "관련 영상 없음"
        
        # Google Gemini로 맞춤형 제목 패턴 생성
        prompt = f"""다음은 YouTube에서 급상승 중인 '{keyword}' 관련 영상들입니다:

{video_titles_context}

위 영상들의 패턴을 분석하여, '{keyword}'를 활용한 유튜브 콘텐츠 제목을 4개만 생성해주세요.

중요 규칙:
1. 실제 급상승 영상들의 스타일과 패턴을 정확히 따라야 합니다
2. 키워드가 인물명(연예인, 유명인)이면 인물 관련 콘텐츠만 (근황, 무대, 인터뷰, 화제의 순간)
3. 키워드가 기술/도구면 사용법, 가이드 형식
4. 키워드가 일반 주제면 정보/팁 형식
5. "~로 돈 버는 방법" 같은 뻔하고 부적절한 패턴은 절대 금지
6. 각 제목은 간결하고 클릭을 유도하는 형식으로
7. 인물명에 비즈니스/돈 관련 단어를 조합하지 마세요

응답은 반드시 JSON 형식으로만:
{{"titles": ["제목1", "제목2", "제목3", "제목4"]}}"""

        response = gemini_model.generate_content(prompt)
        result_text = response.text.strip()
        
        # JSON 파싱 (코드 블록 제거)
        import json
        import re
        
        # ```json ... ``` 형식이면 제거
        json_match = re.search(r'```json\s*(.*?)\s*```', result_text, re.DOTALL)
        if json_match:
            result_text = json_match.group(1)
        elif '```' in result_text:
            result_text = result_text.replace('```', '')
        
        result = json.loads(result_text)
        
        return {
            "title_patterns": result.get("titles", []),
            "source": "gemini_ai"
        }
        
    except Exception as e:
        print(f"❌ Gemini 제목 생성 오류: {e}")
        # 오류 시 실제 영상 제목 사용
        if related_videos and len(related_videos) > 0:
            return {
                "title_patterns": [v['title'] for v in related_videos[:4]],
                "source": "related_videos"
            }
        return {
            "title_patterns": [
                f"{keyword} 완벽 가이드",
                f"{keyword} 핵심 정리",
                f"{keyword} 실전 활용법",
                f"{keyword} 트렌드 분석"
            ],
            "source": "fallback"
        }

@app.post("/api/youtube/force-refresh")
async def force_refresh():
    """강제 새로고침 - 즉시 YouTube API로 데이터 수집"""
    if not youtube_service:
        raise HTTPException(
            status_code=503,
            detail="YouTube API가 설정되지 않았습니다. .env 파일에 YOUTUBE_API_KEY를 설정하세요."
        )
    
    try:
        print("🔄 강제 새로고침 요청...")
        
        success = fetch_youtube_data()
        
        if success:
            return {
                "success": True,
                "message": f"새로고침 완료: {len(cached_videos)}개 영상 업데이트",
                "timestamp": datetime.now().isoformat(),
                "source": "youtube_api_v3"
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