"""
YouTube Data API v3를 사용한 실제 급상승 Shorts 크롤러
"""
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import json
from datetime import datetime
from pathlib import Path
from typing import List, Dict
import os
from dotenv import load_dotenv

load_dotenv()

class YouTubeAPIShortsCrawler:
    def __init__(self, cache_file: str = "../data/youtube_shorts_cache.json"):
        self.cache_file = Path(cache_file)
        self.cache_file.parent.mkdir(parents=True, exist_ok=True)
        self.api_key = os.getenv('YOUTUBE_API_KEY', '')
        
    def get_trending_shorts(self, max_results: int = 50) -> List[Dict]:
        """YouTube Data API로 실제 급상승 Shorts 가져오기"""
        
        if not self.api_key:
            print("⚠️ YouTube API 키가 설정되지 않았습니다")
            print("   실제 급상승 영상을 가져오려면 API 키가 필요합니다")
            print("   YOUTUBE_API_SETUP.md 파일 참고")
            return self._get_fallback_data()
        
        try:
            print(f"🎬 YouTube Data API로 실제 급상승 Shorts 수집 중...")
            
            youtube = build('youtube', 'v3', developerKey=self.api_key)
            
            videos = []
            
            # 1. 한국 급상승 동영상 가져오기 (mostPopular chart)
            videos_response = youtube.videos().list(
                part='snippet,statistics,contentDetails',
                chart='mostPopular',  # 급상승 차트
                regionCode='KR',  # 한국
                videoCategoryId='0',  # 모든 카테고리
                maxResults=min(max_results, 50)
            ).execute()
            
            for item in videos_response.get('items', []):
                # Shorts 영상만 필터링 (60초 이하)
                duration = item.get('contentDetails', {}).get('duration', '')
                if self._is_short_duration(duration):
                    video_info = self._parse_video_data(item)
                    if video_info:
                        videos.append(video_info)
            
            # Shorts가 부족하면 Shorts 태그로 검색
            if len(videos) < 20:
                search_response = youtube.search().list(
                    part='snippet',
                    q='#Shorts',
                    regionCode='KR',
                    type='video',
                    order='viewCount',
                    maxResults=30
                ).execute()
                
                video_ids = [item['id']['videoId'] for item in search_response.get('items', [])]
                if video_ids:
                    search_videos_response = youtube.videos().list(
                        part='snippet,statistics,contentDetails',
                        id=','.join(video_ids)
                    ).execute()
                    
                    for item in search_videos_response.get('items', []):
                        if self._is_short_duration(item.get('contentDetails', {}).get('duration', '')):
                            video_info = self._parse_video_data(item)
                            if video_info and video_info not in videos:
                                videos.append(video_info)
            
            print(f"✅ 실제 급상승 Shorts {len(videos)}개 수집 완료!")
            return videos[:max_results]
            
        except HttpError as e:
            print(f"❌ YouTube API 오류: {e}")
            print("   API 할당량 초과 또는 API 키 문제")
            return self._get_fallback_data()
        except Exception as e:
            print(f"❌ 오류: {e}")
            return self._get_fallback_data()
    
    def _is_short_duration(self, duration: str) -> bool:
        """영상이 60초 이하인지 확인 (Shorts 기준)"""
        import re
        
        # ISO 8601 duration 형식 파싱 (예: PT1M30S = 1분 30초)
        match = re.match(r'PT(?:(\d+)M)?(?:(\d+)S)?', duration)
        if match:
            minutes = int(match.group(1) or 0)
            seconds = int(match.group(2) or 0)
            total_seconds = minutes * 60 + seconds
            return total_seconds <= 60
        return False
    
    def _parse_video_data(self, item: dict) -> Dict:
        """YouTube API 응답을 파싱"""
        try:
            snippet = item.get('snippet', {})
            statistics = item.get('statistics', {})
            
            title = snippet.get('title', '')
            video_id = item.get('id', '')
            category_id = snippet.get('categoryId', '')
            
            # 조회수
            view_count = int(statistics.get('viewCount', 0))
            views_formatted = self._format_view_count(view_count)
            
            # 카테고리 매핑
            category = self._map_category(category_id, title)
            
            # 키워드 추출
            keywords = self._extract_keywords(title)
            
            return {
                "title": title,
                "category": category,
                "views": views_formatted,
                "engagement": self._calculate_engagement(view_count),
                "keywords": keywords,
                "thumbnail": self._get_emoji(category),
                "why_viral": self._analyze_viral(title, view_count),
                "video_id": video_id,
                "youtube_url": f"https://www.youtube.com/watch?v={video_id}",
                "shorts_url": f"https://www.youtube.com/shorts/{video_id}",
                "is_shorts": True,
                "region": "국내",
                "language": "한국어",
                "trend_score": self._calculate_trend_score(view_count),
                "crawled_at": datetime.now().isoformat()
            }
        except Exception as e:
            print(f"파싱 오류: {e}")
            return None
    
    def _format_view_count(self, count: int) -> str:
        """조회수 포맷팅"""
        if count >= 1000000:
            return f"{count/1000000:.1f}M"
        elif count >= 1000:
            return f"{count/1000:.0f}K"
        return str(count)
    
    def _calculate_engagement(self, view_count: int) -> str:
        """참여도 계산"""
        if view_count >= 1000000:
            return "매우높음"
        elif view_count >= 100000:
            return "높음"
        return "보통"
    
    def _calculate_trend_score(self, view_count: int) -> int:
        """트렌드 점수 계산"""
        if view_count >= 5000000:
            return 100
        elif view_count >= 1000000:
            return 95
        elif view_count >= 500000:
            return 90
        elif view_count >= 100000:
            return 85
        return 70
    
    def _map_category(self, category_id: str, title: str) -> str:
        """YouTube 카테고리 ID를 한글 카테고리로 매핑"""
        category_map = {
            '1': '영화/애니메이션',
            '2': '자동차/차량',
            '10': '음악',
            '15': '반려동물/동물',
            '17': '스포츠',
            '19': '여행/이벤트',
            '20': '게임',
            '22': '인물/블로그',
            '23': '코미디',
            '24': '엔터테인먼트',
            '25': '뉴스/정치',
            '26': '노하우/스타일',
            '27': '교육',
            '28': '과학기술',
            '29': '비영리/사회운동'
        }
        
        category = category_map.get(category_id, '일반')
        
        # 제목 기반 재분류
        if any(word in title for word in ['부업', '창업', '사업']):
            return '창업/부업'
        elif any(word in title for word in ['재테크', '투자', '주식', '코인']):
            return '재테크/금융'
        elif any(word in title for word in ['마케팅', 'SNS', '인스타']):
            return '마케팅/비즈니스'
        
        return category
    
    def _extract_keywords(self, title: str) -> List[str]:
        """제목에서 키워드 추출"""
        import re
        
        keyword_patterns = {
            '부업': r'부업|사이드|n잡|투잡',
            '재테크': r'재테크|돈|수익|벌기',
            '투자': r'투자|주식|부동산|코인',
            'AI': r'AI|ChatGPT|인공지능',
            '개발': r'개발|코딩|프로그래밍',
            '마케팅': r'마케팅|SNS|인스타',
            '창업': r'창업|사업|스타트업',
            '자기계발': r'자기계발|루틴|습관'
        }
        
        keywords = []
        for keyword, pattern in keyword_patterns.items():
            if re.search(pattern, title, re.IGNORECASE):
                keywords.append(keyword)
        
        return keywords[:5] if keywords else ['트렌드']
    
    def _get_emoji(self, category: str) -> str:
        """카테고리별 이모지"""
        emojis = {
            '창업/부업': '💼', '재테크/금융': '💰', '과학기술': '🔬',
            '자기계발': '💪', '마케팅/비즈니스': '📱', '게임': '🎮',
            '요리/음식': '🍳', '교육': '📚', '음악': '🎵',
            '영화/애니메이션': '🎬', '자동차/차량': '🚗',
            '반려동물/동물': '🐾', '스포츠': '⚽', '여행/이벤트': '✈️',
            '인물/블로그': '👤', '코미디': '😂', '엔터테인먼트': '🎭'
        }
        return emojis.get(category, '📺')
    
    def _analyze_viral(self, title: str, view_count: int) -> str:
        """바이럴 요소 분석"""
        elements = []
        
        if view_count >= 1000000:
            elements.append("초대박 조회수")
        elif view_count >= 500000:
            elements.append("높은 조회수")
        
        import re
        if re.search(r'\d+만원|\d+억', title):
            elements.append("구체적 금액")
        if re.search(r'\d+개월|\d+일', title):
            elements.append("기간 명시")
        if re.search(r'비법|꿀팁|방법', title):
            elements.append("하우투")
        
        return " + ".join(elements) if elements else "인기 콘텐츠"
    
    def _get_fallback_data(self) -> List[Dict]:
        """API 사용 불가 시 고품질 참고 데이터"""
        return [
            {
                "title": "💡 참고용: 부업으로 월 500만원 버는 법",
                "category": "창업/부업",
                "views": "2.1M",
                "engagement": "매우높음",
                "keywords": ["부업", "월수익", "재테크"],
                "thumbnail": "💼",
                "why_viral": "참고용 트렌드 데이터",
                "video_id": "",
                "youtube_url": "",
                "shorts_url": "",
                "is_shorts": True,
                "region": "국내",
                "language": "한국어",
                "trend_score": 95,
                "crawled_at": datetime.now().isoformat(),
                "note": "참고용 데이터 - 실제 영상 링크 없음"
            }
        ]
    
    def save_to_cache(self, data: List[Dict]):
        """캐시 저장"""
        cache_data = {
            "last_updated": datetime.now().isoformat(),
            "videos": data,
            "count": len(data),
            "source": "youtube_data_api_v3" if self.api_key else "fallback_data"
        }
        
        with open(self.cache_file, 'w', encoding='utf-8') as f:
            json.dump(cache_data, f, ensure_ascii=False, indent=2)
        
        print(f"💾 캐시 저장 완료: {len(data)}개 영상")

if __name__ == "__main__":
    crawler = YouTubeAPIShortsCrawler()
    videos = crawler.get_trending_shorts(25)
    
    print(f"\n수집된 영상 {len(videos)}개:")
    for i, v in enumerate(videos[:5], 1):
        print(f"{i}. {v['title']}")
        print(f"   조회수: {v['views']} | URL: {v['youtube_url']}")

