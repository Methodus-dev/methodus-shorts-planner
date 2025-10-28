from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict
from shorts_planner import ShortsPlannerSystem
from youtube_trends import YouTubeTrendsAnalyzer
from youtube_realtime_crawler import YouTubeRealtimeCrawler
from youtube_shorts_crawler import YouTubeShortsCrawler
from youtube_api_crawler import YouTubeAPIShortsCrawler
from youtube_ytdlp_crawler import YouTubeYTDLPCrawler
import json
from datetime import datetime, timedelta
from pathlib import Path
import subprocess
import threading

app = FastAPI(
    title="쇼츠 콘텐츠 기획 시스템",
    description="조회수 높은 쇼츠 콘텐츠를 기획하는 AI 어시스턴트",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 쇼츠 플래너 초기화
planner = ShortsPlannerSystem()
youtube_analyzer = YouTubeTrendsAnalyzer()
realtime_crawler = YouTubeRealtimeCrawler()
shorts_crawler = YouTubeShortsCrawler()
api_crawler = YouTubeAPIShortsCrawler()  # YouTube Data API v3 크롤러
ytdlp_crawler = YouTubeYTDLPCrawler()  # yt-dlp 크롤러 (실제 급상승 영상)

# 서버 시작 시 첫 크롤링 실행
@app.on_event("startup")
async def startup_event():
    """서버 시작 시 실행"""
    print("🚀 서버 시작 - YouTube Shorts 크롤링 시작...")
    
    import threading
    def initial_crawl():
        import time
        time.sleep(2)  # 서버 시작 후 2초 대기
        try:
            print("🎬 카테고리별 급상승 영상 크롤링 시작 (카테고리당 100개)...")
            
            # 주요 카테고리들
            main_categories = [
                '창업/부업', '재테크/금융', '과학기술', '자기계발', '마케팅/비즈니스',
                '요리/음식', '게임', '운동/건강', '교육/학습', '음악'
            ]
            
            # 카테고리별로 100개씩 수집
            videos = ytdlp_crawler.get_trending_by_category(main_categories, per_category=100)
            
            if videos and len(videos) > 0:
                ytdlp_crawler.save_to_cache(videos)
                shorts_count = sum(1 for v in videos if v.get('is_shorts'))
                long_count = len(videos) - shorts_count
                korean_count = sum(1 for v in videos if v.get('language') == '한국어')
                
                # 카테고리별 통계
                from collections import Counter
                category_counts = Counter(v.get('category') for v in videos)
                
                print(f"\n✅ 전체 수집 완료: {len(videos)}개")
                print(f"   쇼츠: {shorts_count}개 | 롱폼: {long_count}개")
                print(f"   한국어: {korean_count}개 | 영어: {len(videos) - korean_count}개")
                print(f"\n   카테고리별:")
                for cat, count in category_counts.most_common():
                    print(f"   - {cat}: {count}개")
            else:
                print("⚠️ 크롤링 실패")
        except Exception as e:
            print(f"❌ 크롤링 오류: {e}")
    
    threading.Thread(target=initial_crawl, daemon=True).start()
    
    # 2시간마다 자동 업데이트
    def auto_update_loop():
        import time
        while True:
            time.sleep(2 * 60 * 60)  # 2시간
            try:
                print(f"🔄 [{datetime.now().strftime('%H:%M:%S')}] 2시간 주기 자동 크롤링 시작...")
                
                main_categories = [
                    '창업/부업', '재테크/금융', '과학기술', '자기계발', '마케팅/비즈니스',
                    '요리/음식', '게임', '운동/건강', '교육/학습', '음악'
                ]
                
                videos = ytdlp_crawler.get_trending_by_category(main_categories, per_category=100)
                if videos and len(videos) > 0:
                    ytdlp_crawler.save_to_cache(videos)
                    print(f"✅ 자동 업데이트 완료: {len(videos)}개")
                else:
                    print("⚠️ 자동 업데이트 실패")
            except Exception as e:
                print(f"❌ 자동 업데이트 오류: {e}")
    
    threading.Thread(target=auto_update_loop, daemon=True).start()
    print("✅ yt-dlp 자동 크롤링 시스템 시작 (2시간마다)")

# Request/Response Models
class ContentPlanRequest(BaseModel):
    topic: str
    content_type: str = "Actionable"
    target_audience: Optional[str] = None
    user_story: Optional[Dict] = None

class ContentPlanResponse(BaseModel):
    plan: Dict
    generated_at: str

class NicheAnalysisRequest(BaseModel):
    topic: str
    target_audience: Optional[str] = None

class HookGenerationRequest(BaseModel):
    topic: str
    count: int = 10

class SavedPlan(BaseModel):
    id: str
    topic: str
    content_type: str
    plan: Dict
    created_at: str

# Storage file for saved plans
STORAGE_FILE = Path("../data/saved_plans.json")

def load_saved_plans() -> List[dict]:
    """저장된 기획서 로드"""
    if STORAGE_FILE.exists():
        with open(STORAGE_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def save_plan_to_file(plan: dict):
    """기획서 저장"""
    saved = load_saved_plans()
    saved.append(plan)
    
    STORAGE_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(STORAGE_FILE, 'w', encoding='utf-8') as f:
        json.dump(saved, f, ensure_ascii=False, indent=2)

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "쇼츠 콘텐츠 기획 시스템 - 조회수 높은 콘텐츠를 만들어보세요!",
        "version": "1.0.0",
        "docs": "/docs"
    }

@app.post("/api/create-plan", response_model=ContentPlanResponse)
async def create_content_plan(request: ContentPlanRequest):
    """콘텐츠 기획서 생성"""
    try:
        plan = planner.create_content_plan(
            topic=request.topic,
            content_type=request.content_type,
            target_audience=request.target_audience or "",
            user_story=request.user_story
        )
        
        # 생성 시간 추가
        plan['생성_일시'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        return ContentPlanResponse(
            plan=plan,
            generated_at=plan['생성_일시']
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"기획서 생성 실패: {str(e)}")

@app.post("/api/analyze-niche")
async def analyze_niche(request: NicheAnalysisRequest):
    """니치 분석"""
    try:
        analysis = planner.analyze_niche(
            topic=request.topic,
            target_audience=request.target_audience or ""
        )
        return {"analysis": analysis}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"니치 분석 실패: {str(e)}")

@app.post("/api/generate-hooks")
async def generate_hooks(request: HookGenerationRequest):
    """훅 아이디어 생성"""
    try:
        hooks = planner.generate_hooks(
            topic=request.topic,
            count=request.count
        )
        return {"hooks": hooks}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"훅 생성 실패: {str(e)}")

@app.get("/api/content-types")
async def get_content_types():
    """사용 가능한 콘텐츠 타입"""
    content_types = [
        {
            "value": "Actionable",
            "label": "실행 가능한 가이드",
            "description": "단계별 방법 제시",
            "best_for": "튜토리얼, 하우투"
        },
        {
            "value": "Motivational",
            "label": "동기부여 스토리",
            "description": "영감을 주는 이야기",
            "best_for": "Before/After, 성공 스토리"
        },
        {
            "value": "Analytical",
            "label": "분석 및 해부",
            "description": "심층 분석",
            "best_for": "리뷰, 비교"
        },
        {
            "value": "Contrarian",
            "label": "반대 의견",
            "description": "일반 상식에 도전",
            "best_for": "논란, 화제성"
        },
        {
            "value": "Observation",
            "label": "관찰 및 인사이트",
            "description": "흥미로운 발견",
            "best_for": "트렌드, 현상 분석"
        },
        {
            "value": "X vs. Y",
            "label": "비교 분석",
            "description": "두 가지 비교",
            "best_for": "비교, 대결"
        },
        {
            "value": "Present/Future",
            "label": "현재와 미래",
            "description": "트렌드 예측",
            "best_for": "전망, 예측"
        },
        {
            "value": "Listicle",
            "label": "목록형",
            "description": "리스트 형식",
            "best_for": "TOP 10, 추천"
        }
    ]
    return {"content_types": content_types}

@app.get("/api/trending-topics")
async def get_trending_topics():
    """트렌딩 주제 추천"""
    try:
        topics = planner.get_trending_topics()
        return {"trending_topics": topics}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"트렌딩 주제 조회 실패: {str(e)}")

@app.post("/api/suggest-hashtags")
async def suggest_hashtags(request: dict):
    """해시태그 제안"""
    try:
        topic = request.get("topic", "")
        category = request.get("category", "")
        
        hashtags = planner.suggest_hashtags(topic, category)
        return {"hashtags": hashtags}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"해시태그 제안 실패: {str(e)}")

@app.post("/api/save-plan")
async def save_plan(content: dict):
    """기획서 저장"""
    try:
        plan_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        saved_item = {
            "id": plan_id,
            "topic": content.get("topic"),
            "content_type": content.get("content_type"),
            "plan": content.get("plan"),
            "created_at": datetime.now().isoformat()
        }
        
        save_plan_to_file(saved_item)
        
        return {"message": "기획서가 저장되었습니다", "id": plan_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"기획서 저장 실패: {str(e)}")

@app.get("/api/saved-plans")
async def get_saved_plans():
    """저장된 기획서 목록"""
    try:
        saved = load_saved_plans()
        return {"saved_plans": saved, "count": len(saved)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"기획서 목록 조회 실패: {str(e)}")

@app.delete("/api/saved-plans/{plan_id}")
async def delete_saved_plan(plan_id: str):
    """기획서 삭제"""
    try:
        saved = load_saved_plans()
        saved = [item for item in saved if item.get('id') != plan_id]
        
        with open(STORAGE_FILE, 'w', encoding='utf-8') as f:
            json.dump(saved, f, ensure_ascii=False, indent=2)
        
        return {"message": "기획서가 삭제되었습니다"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"기획서 삭제 실패: {str(e)}")

@app.get("/api/optimization-checklist")
async def get_optimization_checklist():
    """최적화 체크리스트"""
    checklist = planner.system_data.get("쇼츠_최적화", {})
    return {
        "checklist": checklist.get("조회수_최적화_체크리스트", []),
        "viral_elements": checklist.get("바이럴_요소", []),
        "platforms": checklist.get("플랫폼별_전략", {})
    }

@app.get("/api/youtube/trending")
async def get_youtube_trending(
    count: int = 50,
    category: Optional[str] = None,
    region: Optional[str] = None,
    language: Optional[str] = None,
    min_trend_score: Optional[int] = None,
    sort_by: str = "trend_score",
    force_refresh: bool = False,
    video_type: Optional[str] = None,  # "쇼츠" 또는 "롱폼" 필터
    time_filter: Optional[str] = None  # "today", "week", "month", "all"
):
    """YouTube 급상승 동영상 (쇼츠+롱폼, 필터링 지원)"""
    try:
        # force_refresh가 True면 즉시 크롤링
        cache_file = Path("../data/youtube_shorts_cache.json")
        should_refresh = force_refresh
        
        if force_refresh:
            print("🔄 사용자 요청: 카테고리별 최신 데이터 즉시 크롤링...")
            import threading
            def force_crawl():
                try:
                    main_categories = [
                        '창업/부업', '재테크/금융', '과학기술', '자기계발', '마케팅/비즈니스',
                        '요리/음식', '게임', '운동/건강', '교육/학습', '음악'
                    ]
                    videos = ytdlp_crawler.get_trending_by_category(main_categories, per_category=100)
                    if videos:
                        ytdlp_crawler.save_to_cache(videos)
                        print(f"✅ 즉시 크롤링 완료: {len(videos)}개 (카테고리별 100개씩)")
                except Exception as e:
                    print(f"❌ 즉시 크롤링 실패: {e}")
            threading.Thread(target=force_crawl, daemon=True).start()
        
        if cache_file.exists():
            with open(cache_file, 'r', encoding='utf-8') as f:
                cache = json.load(f)
            
            # 캐시가 1시간 이상 오래된 경우에만 새로고침
            if cache.get('last_updated'):
                last_updated = datetime.fromisoformat(cache['last_updated'].replace('Z', '+00:00'))
                time_diff = (datetime.now() - last_updated).total_seconds()
                if time_diff > 3600:  # 1시간
                    should_refresh = True
                    print(f"🔄 캐시가 {int(time_diff/3600)}시간 전 데이터 - 새로고침")
        
        if should_refresh or not cache_file.exists():
            print("🔄 백그라운드에서 최신 데이터 크롤링 중...")
            # 백그라운드에서 크롤링 시작 (기존 데이터 먼저 반환)
            import threading
            def background_crawl():
                try:
                    videos = shorts_crawler.crawl_shorts_trending(200)
                    shorts_crawler.save_to_cache(videos)
                    print("✅ 백그라운드 크롤링 완료")
                except Exception as e:
                    print(f"❌ 백그라운드 크롤링 실패: {e}")
            
            threading.Thread(target=background_crawl, daemon=True).start()
            
            # 기존 캐시가 있으면 먼저 반환
            if cache and cache.get('videos'):
                print("📊 기존 데이터 먼저 반환, 백그라운드에서 업데이트 중...")
            else:
                # 캐시가 없으면 즉시 크롤링
                videos = shorts_crawler.crawl_shorts_trending(200)
                shorts_crawler.save_to_cache(videos)
                cache = {"videos": videos, "last_updated": datetime.now().isoformat()}
        
        if cache and cache.get('videos'):
            videos = cache['videos']
            
            # 필터링 적용
            filtered_videos = _apply_filters(videos, category, region, language, min_trend_score, video_type, time_filter)
            
            print(f"🔍 필터링 결과: {len(filtered_videos)}개 (전체 {len(videos)}개)")
            if category:
                print(f"   - 카테고리: {category}")
            if region:
                print(f"   - 지역: {region}")
            if time_filter:
                print(f"   - 기간: {time_filter}")
            
            # 정렬
            sorted_videos = _sort_videos(filtered_videos, sort_by)
            
            # 개수 제한
            final_videos = sorted_videos[:count]
            
            return {
                "trending_videos": final_videos,
                "count": len(final_videos),
                "total_count": len(filtered_videos),
                "filters_applied": {
                    "category": category,
                    "region": region,
                    "language": language,
                    "min_trend_score": min_trend_score,
                    "sort_by": sort_by,
                    "video_type": video_type,
                    "time_filter": time_filter
                },
                "last_updated": cache.get('last_updated'),
                "source": "shorts_cache",
                "auto_refreshed": should_refresh
            }
        
        # 캐시 없으면 즉시 Shorts 크롤링
        print("Shorts 캐시 없음 - 즉시 크롤링 실행")
        videos = shorts_crawler.crawl_shorts_trending(count)
        shorts_crawler.save_to_cache(videos)
        
        return {
            "trending_videos": videos,
            "count": len(videos),
            "last_updated": datetime.now().isoformat(),
            "source": "fresh_shorts_crawl"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Shorts 트렌드 조회 실패: {str(e)}")

def _apply_filters(videos: List[Dict], category: Optional[str], region: Optional[str], 
                  language: Optional[str], min_trend_score: Optional[int], video_type: Optional[str],
                  time_filter: Optional[str]) -> List[Dict]:
    """비디오 필터링 (개선된 버전)"""
    filtered = videos.copy()
    
    print(f"🔍 필터링 시작: 총 {len(filtered)}개 영상")
    
    # 카테고리 필터
    if category:
        before = len(filtered)
        filtered = [v for v in filtered if v.get('category', '').strip() == category.strip()]
        print(f"   카테고리 '{category}' 필터: {before}개 → {len(filtered)}개")
    
    # 지역 필터
    if region:
        before = len(filtered)
        filtered = [v for v in filtered if v.get('region', '').strip() == region.strip()]
        print(f"   지역 '{region}' 필터: {before}개 → {len(filtered)}개")
    
    # 언어 필터
    if language:
        before = len(filtered)
        filtered = [v for v in filtered if v.get('language', '').strip() == language.strip()]
        print(f"   언어 '{language}' 필터: {before}개 → {len(filtered)}개")
    
    # 트렌드 점수 필터
    if min_trend_score:
        before = len(filtered)
        filtered = [v for v in filtered if v.get('trend_score', 0) >= min_trend_score]
        print(f"   트렌드 점수 {min_trend_score}+ 필터: {before}개 → {len(filtered)}개")
    
    # 쇼츠/롱폼 필터
    if video_type:
        before = len(filtered)
        filtered = [v for v in filtered if v.get('video_type', '').strip() == video_type.strip()]
        print(f"   영상 타입 '{video_type}' 필터: {before}개 → {len(filtered)}개")
    
    # 기간 필터
    if time_filter and time_filter != "all":
        before = len(filtered)
        now = datetime.now()
        
        if time_filter == "today":
            # 오늘 (최근 24시간)
            cutoff = now - timedelta(days=1)
        elif time_filter == "week":
            # 이번 주 (최근 7일)
            cutoff = now - timedelta(days=7)
        elif time_filter == "month":
            # 이번 달 (최근 30일)
            cutoff = now - timedelta(days=30)
        else:
            cutoff = None
        
        if cutoff:
            def is_recent(video):
                crawled_at = video.get('crawled_at')
                if not crawled_at:
                    return False
                try:
                    crawled_time = datetime.fromisoformat(crawled_at.replace('Z', '+00:00'))
                    # timezone-aware인 경우 naive로 변환
                    if crawled_time.tzinfo is not None:
                        crawled_time = crawled_time.replace(tzinfo=None)
                    return crawled_time >= cutoff
                except (ValueError, AttributeError):
                    return False
            
            filtered = [v for v in filtered if is_recent(v)]
            print(f"   기간 '{time_filter}' 필터: {before}개 → {len(filtered)}개")
    
    print(f"✅ 최종 필터링 결과: {len(filtered)}개")
    return filtered

def _sort_videos(videos: List[Dict], sort_by: str) -> List[Dict]:
    """비디오 정렬"""
    if sort_by == "trend_score":
        return sorted(videos, key=lambda x: x.get('trend_score', 0), reverse=True)
    elif sort_by == "views":
        # 조회수 정렬 (K, M 처리)
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
        return sorted(videos, key=lambda x: parse_views(x.get('views', '0')), reverse=True)
    elif sort_by == "crawled_at":
        return sorted(videos, key=lambda x: x.get('crawled_at', ''), reverse=True)
    else:
        return videos

@app.post("/api/youtube/refresh")
async def refresh_youtube_trending():
    """최신 데이터로 강제 업데이트 - 백그라운드 크롤링 완료 후 사용"""
    try:
        print("🔄 최신 데이터 확인 중...")
        
        cache_file = Path("../data/youtube_shorts_cache.json")
        if cache_file.exists():
            with open(cache_file, 'r', encoding='utf-8') as f:
                cache = json.load(f)
            
            # 캐시가 최근 10분 이내면 최신 데이터
            if cache.get('last_updated'):
                last_updated = datetime.fromisoformat(cache['last_updated'].replace('Z', '+00:00'))
                time_diff = (datetime.now() - last_updated).total_seconds()
                if time_diff < 600:  # 10분 이내
                    print("✅ 이미 최신 데이터입니다")
                    return {
                        "message": "이미 최신 데이터입니다",
                        "last_updated": cache['last_updated'],
                        "count": len(cache.get('videos', [])),
                        "source": "cached_data",
                        "status": "already_fresh"
                    }
        
        # 최신 데이터가 아니면 강제 크롤링
        print("🔄 최신 데이터 크롤링 중...")
        videos = shorts_crawler.crawl_shorts_trending(200)
        shorts_crawler.save_to_cache(videos)
        
        print(f"✅ 최신 데이터 업데이트 완료: {len(videos)}개 동영상")
        
        return {
            "message": "최신 데이터로 업데이트 완료",
            "last_updated": datetime.now().isoformat(),
            "count": len(videos),
            "source": "fresh_crawl",
            "status": "success"
        }
    except Exception as e:
        print(f"❌ 최신 데이터 업데이트 실패: {e}")
        raise HTTPException(status_code=500, detail=f"업데이트 실패: {str(e)}")

@app.get("/api/youtube/category-keywords/{category}")
async def get_category_keywords(category: str):
    """특정 카테고리의 핫 키워드 분석"""
    try:
        # 캐시에서 해당 카테고리 영상들 가져오기
        cache_file = Path("../data/youtube_shorts_cache.json")
        if not cache_file.exists():
            raise HTTPException(status_code=404, detail="캐시 데이터가 없습니다")
            
        with open(cache_file, 'r', encoding='utf-8') as f:
            cache_data = json.load(f)
        
        category_videos = [v for v in cache_data.get('videos', []) if v.get('category') == category]
        
        if not category_videos:
            return {
                "category": category,
                "keywords": [],
                "message": f"{category} 카테고리 데이터가 없습니다"
            }
        
        # 키워드 추출 및 분석
        all_keywords = []
        for video in category_videos:
            all_keywords.extend(video.get('keywords', []))
        
        # 키워드 빈도 계산
        from collections import Counter
        keyword_counts = Counter(all_keywords)
        
        # 상위 키워드 추출
        top_keywords = []
        for keyword, count in keyword_counts.most_common(20):
            if keyword and len(keyword) > 1:  # 빈 문자열이나 1글자 키워드 제외
                top_keywords.append({
                    "keyword": keyword,
                    "frequency": count,
                    "percentage": round((count / len(category_videos)) * 100, 1)
                })
        
        return {
            "category": category,
            "total_videos": len(category_videos),
            "keywords": top_keywords,
            "last_updated": cache_data.get('last_updated', datetime.now().isoformat())
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"카테고리 키워드 분석 실패: {str(e)}")

@app.get("/api/youtube/filter-options")
async def get_filter_options():
    """사용 가능한 필터 옵션 제공"""
    try:
        cache_file = Path("../data/youtube_shorts_cache.json")
        if cache_file.exists():
            with open(cache_file, 'r', encoding='utf-8') as f:
                cache = json.load(f)
            
            if cache and cache.get('videos'):
                videos = cache['videos']
                
                # 실제 데이터에서 발견된 카테고리
                found_categories = list(set(v.get('category', '') for v in videos if v.get('category')))
                
                # 전체 YouTube 카테고리 목록
                all_categories = [
                    "영화/애니메이션", "자동차/차량", "음악", "반려동물/동물", "스포츠",
                    "여행/이벤트", "게임", "인물/블로그", "코미디", "엔터테인먼트",
                    "뉴스/정치", "노하우/스타일", "교육", "과학기술", "비영리/사회운동",
                    "요리/음식", "자기계발", "재테크/금융", "창업/부업", "마케팅/비즈니스", "일반"
                ]
                
                # 발견된 카테고리와 전체 카테고리 결합 (중복 제거)
                categories = sorted(list(set(found_categories + all_categories)))
                
                # 지역 옵션
                regions = list(set(v.get('region', '') for v in videos if v.get('region')))
                
                # 언어 옵션 (항상 한국어, 영어 포함)
                languages_from_data = list(set(v.get('language', '') for v in videos if v.get('language')))
                languages = sorted(list(set(languages_from_data + ["한국어", "영어"])))
                
                # 정렬 옵션
                sort_options = [
                    {"value": "trend_score", "label": "트렌드 점수"},
                    {"value": "views", "label": "조회수"},
                    {"value": "crawled_at", "label": "최신순"}
                ]
                
                # 기간 필터 옵션
                time_filter_options = [
                    {"value": "all", "label": "전체"},
                    {"value": "today", "label": "오늘 (24시간)"},
                    {"value": "week", "label": "이번 주 (7일)"},
                    {"value": "month", "label": "이번 달 (30일)"}
                ]
                
                # 영상 타입 옵션
                video_type_options = [
                    {"value": "", "label": "전체"},
                    {"value": "쇼츠", "label": "쇼츠"},
                    {"value": "롱폼", "label": "롱폼"}
                ]
                
                return {
                    "categories": sorted(categories),
                    "regions": sorted(regions),
                    "languages": sorted(languages),
                    "sort_options": sort_options,
                    "time_filter_options": time_filter_options,
                    "video_type_options": video_type_options,
                    "trend_score_range": {
                        "min": 1,
                        "max": 100,
                        "default": 50
                    }
                }
        
        # 기본 옵션 반환 (영어 항상 포함)
        return {
            "categories": [
                "영화/애니메이션",
                "자동차/차량",
                "음악",
                "반려동물/동물",
                "스포츠",
                "여행/이벤트",
                "게임",
                "인물/블로그",
                "코미디",
                "엔터테인먼트",
                "뉴스/정치",
                "노하우/스타일",
                "교육",
                "과학기술",
                "비영리/사회운동",
                "요리/음식",
                "자기계발",
                "재테크/금융",
                "창업/부업",
                "마케팅/비즈니스",
                "일반"
            ],
            "regions": ["국내", "해외"],
            "languages": ["한국어", "영어"],  # 항상 양쪽 언어 표시
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
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"필터 옵션 조회 실패: {str(e)}")

@app.post("/api/youtube/analyze-keywords")
async def analyze_keywords(request: dict):
    """급상승 동영상에서 키워드 분석"""
    try:
        videos = request.get("videos", [])
        if not videos:
            videos = youtube_analyzer.get_trending_videos(20)
        
        analysis = youtube_analyzer.extract_keywords_from_videos(videos)
        return {"keyword_analysis": analysis}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"키워드 분석 실패: {str(e)}")

@app.post("/api/youtube/content-ideas")
async def get_content_ideas(request: dict):
    """키워드 기반 콘텐츠 아이디어"""
    try:
        keyword = request.get("keyword", "")
        videos = youtube_analyzer.get_trending_videos(20)
        
        ideas = youtube_analyzer.suggest_content_ideas(keyword, videos)
        return {"content_ideas": ideas}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"아이디어 생성 실패: {str(e)}")

@app.get("/api/youtube/posting-times")
async def get_posting_times():
    """최적 업로드 시간"""
    try:
        times = youtube_analyzer.get_optimal_posting_times()
        return {"posting_times": times}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"시간 정보 조회 실패: {str(e)}")

@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "system_loaded": bool(planner.system_data),
        "youtube_analyzer_loaded": youtube_analyzer is not None
    }

# 스케줄러 관련 전역 변수
scheduler_process = None

@app.post("/api/start-scheduler")
async def start_scheduler():
    """스케줄러 시작"""
    global scheduler_process
    
    if scheduler_process and scheduler_process.poll() is None:
        return {"status": "already_running", "message": "스케줄러가 이미 실행 중입니다"}
    
    try:
        # 백그라운드에서 스케줄러 실행
        scheduler_process = subprocess.Popen(
            ['python', 'scheduler.py'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        return {
            "status": "success", 
            "message": "스케줄러가 시작되었습니다",
            "pid": scheduler_process.pid
        }
    except Exception as e:
        return {"status": "error", "message": f"스케줄러 시작 실패: {str(e)}"}

@app.post("/api/stop-scheduler")
async def stop_scheduler():
    """스케줄러 중지"""
    global scheduler_process
    
    if not scheduler_process or scheduler_process.poll() is not None:
        return {"status": "not_running", "message": "실행 중인 스케줄러가 없습니다"}
    
    try:
        scheduler_process.terminate()
        scheduler_process.wait(timeout=10)
        return {"status": "success", "message": "스케줄러가 중지되었습니다"}
    except Exception as e:
        return {"status": "error", "message": f"스케줄러 중지 실패: {str(e)}"}

@app.get("/api/scheduler-status")
async def get_scheduler_status():
    """스케줄러 상태 확인"""
    global scheduler_process
    
    if scheduler_process and scheduler_process.poll() is None:
        return {
            "status": "running",
            "message": "스케줄러가 실행 중입니다",
            "pid": scheduler_process.pid
        }
    else:
        return {
            "status": "stopped",
            "message": "스케줄러가 중지되었습니다"
        }

@app.post("/api/trigger-crawling")
async def trigger_crawling():
    """수동으로 크롤링 실행"""
    try:
        # 실시간 크롤링 실행
        result1 = subprocess.run(['python', 'youtube_realtime_crawler.py'], 
                               capture_output=True, text=True, timeout=300)
        
        # 쇼츠 크롤링 실행
        result2 = subprocess.run(['python', 'youtube_shorts_crawler.py'], 
                               capture_output=True, text=True, timeout=300)
        
        return {
            "status": "success",
            "message": "크롤링이 완료되었습니다",
            "realtime_result": result1.returncode == 0,
            "realtime_output": result1.stdout,
            "shorts_result": result2.returncode == 0,
            "shorts_output": result2.stdout
        }
    except Exception as e:
        return {"status": "error", "message": f"크롤링 실행 실패: {str(e)}"}

if __name__ == "__main__":
    import uvicorn
    import os
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
