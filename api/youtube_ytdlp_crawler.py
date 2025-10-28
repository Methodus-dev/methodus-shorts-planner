"""
yt-dlp를 사용한 YouTube 급상승 Shorts 크롤러
YouTube Data API 없이도 실제 데이터 수집 가능
"""
import yt_dlp
import json
from datetime import datetime
from pathlib import Path
from typing import List, Dict
import re

class YouTubeYTDLPCrawler:
    def __init__(self, cache_file: str = "../data/youtube_shorts_cache.json"):
        self.cache_file = Path(cache_file)
        self.cache_file.parent.mkdir(parents=True, exist_ok=True)
    
    def get_trending_videos(self, max_results: int = 100, include_shorts: bool = True, include_long: bool = True) -> List[Dict]:
        """yt-dlp로 실제 급상승 영상 가져오기 (쇼츠 + 롱폼)"""
        
        try:
            print(f"🎬 최근 급상승 YouTube 동영상 수집 중... (목표: {max_results}개)")
            
            all_videos = []
            
            # 한국어 영상 수집 (60%)
            korean_target = int(max_results * 0.6)
            korean_videos = self._search_korean_videos(korean_target)
            all_videos.extend(korean_videos)
            print(f"✅ 한국어 급상승 영상: {len(korean_videos)}개")
            
            # 영어/글로벌 영상 수집 (40%)
            english_target = int(max_results * 0.4)
            global_videos = self._search_global_videos(english_target)
            all_videos.extend(global_videos)
            print(f"✅ 영어 급상승 영상: {len(global_videos)}개")
            
            # 쇼츠/롱폼 필터링
            filtered_videos = []
            for video in all_videos:
                if include_shorts and video.get('is_shorts'):
                    filtered_videos.append(video)
                elif include_long and not video.get('is_shorts'):
                    filtered_videos.append(video)
            
            # 급상승 우선 정렬
            sorted_videos = self._sort_by_trend_and_recency(filtered_videos)
            print(f"🎯 최종 급상승 영상 수집: {len(sorted_videos)}개 (트렌드 우선 정렬)")
            return sorted_videos[:max_results]
            
        except Exception as e:
            print(f"❌ yt-dlp 크롤링 오류: {e}")
            print("🔄 재시도 중...")
            # 재시도 로직
            try:
                return self._retry_crawling(max_results, include_shorts, include_long)
            except Exception as retry_error:
                print(f"❌ 재시도 실패: {retry_error}")
                return []
    
    def get_trending_by_category(self, categories: List[str], per_category: int = 50) -> List[Dict]:
        """카테고리별로 영상 수집 (한국어 60% + 영어 40%)"""
        all_videos = []
        
        for category in categories:
            print(f"📂 {category} 카테고리 크롤링 중 (목표: {per_category}개)...")
            try:
                # 한국어 60%, 영어 40%
                korean_count = int(per_category * 0.6)
                english_count = int(per_category * 0.4)
                
                # 한국어 영상
                category_videos_kr = self._search_by_category(category, korean_count)
                all_videos.extend(category_videos_kr)
                
                # 영어 영상 (카테고리의 영어 키워드로 검색)
                category_videos_en = self._search_by_category_english(category, english_count)
                all_videos.extend(category_videos_en)
                
                total_collected = len(category_videos_kr) + len(category_videos_en)
                print(f"   ✅ {total_collected}개 수집 완료 (한국어: {len(category_videos_kr)}, 영어: {len(category_videos_en)})")
            except Exception as e:
                print(f"   ❌ 실패: {e}")
        
        print(f"\n🎉 전체 수집 완료: {len(all_videos)}개 영상")
        return all_videos
    
    def _search_by_category_english(self, category: str, max_results: int) -> List[Dict]:
        """특정 카테고리의 영어 영상 검색"""
        # 카테고리별 영어 검색 키워드
        category_keywords_en = {
            '창업/부업': ['side hustle', 'startup', 'business', 'entrepreneur', 'make money'],
            '재테크/금융': ['investing', 'stock market', 'real estate', 'crypto', 'money'],
            '과학기술': ['AI', 'ChatGPT', 'coding', 'programming', 'tech', 'app'],
            '자기계발': ['self improvement', 'productivity', 'motivation', 'success', 'habits'],
            '마케팅/비즈니스': ['marketing', 'social media', 'instagram', 'youtube', 'branding'],
            '요리/음식': ['cooking', 'recipe', 'food', 'baking', 'meal prep'],
            '게임': ['gaming', 'gameplay', 'esports', 'minecraft', 'fortnite'],
            '운동/건강': ['workout', 'fitness', 'diet', 'gym', 'exercise'],
            '교육/학습': ['education', 'learning', 'study', 'tutorial', 'course'],
            '음악': ['music', 'song', 'cover', 'remix', 'beats']
        }
        
        keywords = category_keywords_en.get(category, ['trending'])
        videos = []
        
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'extract_flat': True,
        }
        
        per_keyword = max(5, max_results // len(keywords))
        
        for keyword in keywords:
            if len(videos) >= max_results:
                break
            
            try:
                search_url = f'ytsearch{per_keyword}:{keyword}'
                
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    result = ydl.extract_info(search_url, download=False)
                    
                    if result and 'entries' in result:
                        for entry in result['entries']:
                            if entry and len(videos) < max_results:
                                video_info = self._parse_ytdlp_data(entry, is_korean=False)
                                if video_info:
                                    video_info['category'] = category  # 카테고리 강제 설정
                                    videos.append(video_info)
            except Exception as e:
                continue
        
        return videos
    
    def _search_by_category(self, category: str, max_results: int) -> List[Dict]:
        """특정 카테고리의 인기 영상 검색"""
        # 카테고리별 검색 키워드
        category_keywords = {
            '창업/부업': ['부업', '창업', '사업', '스타트업', 'n잡', '투잡'],
            '재테크/금융': ['재테크', '주식', '투자', '부동산', '코인', '돈버는법'],
            '과학기술': ['ChatGPT', 'AI', '코딩', '프로그래밍', '개발', '앱개발'],
            '자기계발': ['자기계발', '루틴', '습관', '동기부여', '성공', '목표'],
            '마케팅/비즈니스': ['마케팅', 'SNS', '인스타', '유튜브', '브랜딩', '광고'],
            '요리/음식': ['요리', '레시피', '간단요리', '먹방', '맛집', '다이어트식단'],
            '게임': ['게임', '롤', '배그', 'LOL', 'FIFA', '마인크래프트'],
            '운동/건강': ['운동', '헬스', '다이어트', '홈트', '요가', '필라테스'],
            '교육/학습': ['공부', '영어', '학습', '수험생', '공무원', '자격증'],
            '음악': ['노래', '음악', 'K-POP', '가수', '뮤직비디오', '커버']
        }
        
        keywords = category_keywords.get(category, [category])
        videos = []
        
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'extract_flat': True,
        }
        
        per_keyword = max(10, max_results // len(keywords))
        
        for keyword in keywords:
            if len(videos) >= max_results:
                break
            
            try:
                search_url = f'ytsearch{per_keyword}:{keyword}'
                
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    result = ydl.extract_info(search_url, download=False)
                    
                    if result and 'entries' in result:
                        for entry in result['entries']:
                            if entry and len(videos) < max_results:
                                video_info = self._parse_ytdlp_data(entry, is_korean=True)
                                if video_info:
                                    video_info['category'] = category  # 카테고리 강제 설정
                                    videos.append(video_info)
            except Exception as e:
                continue
        
        return videos
    
    def _search_korean_videos(self, max_results: int) -> List[Dict]:
        """한국어 인기 영상 검색"""
        videos = []
        
        # 한국어 인기 키워드들
        korean_keywords = [
            '부업', '재테크', '주식', 'ChatGPT', '마케팅', 
            '자기계발', '요리', '게임', '운동', '공부'
        ]
        
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'extract_flat': True,
        }
        
        per_keyword = max(5, max_results // len(korean_keywords))
        
        for keyword in korean_keywords:
            if len(videos) >= max_results:
                break
            
            try:
                search_url = f'ytsearch{per_keyword}:{keyword}'
                
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    result = ydl.extract_info(search_url, download=False)
                    
                    if result and 'entries' in result:
                        for entry in result['entries']:
                            if entry and len(videos) < max_results:
                                video_info = self._parse_ytdlp_data(entry, is_korean=True)
                                if video_info:
                                    videos.append(video_info)
            except Exception as e:
                continue
        
        return videos
    
    def _search_global_videos(self, max_results: int) -> List[Dict]:
        """글로벌 인기 영상 검색 (영어)"""
        videos = []
        
        # 영어 인기 키워드들
        english_keywords = [
            'side hustle', 'make money online', 'AI tools', 'productivity', 
            'entrepreneur', 'business', 'investing', 'crypto', 'fitness', 'cooking'
        ]
        
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'extract_flat': True,
        }
        
        per_keyword = max(5, max_results // len(english_keywords))
        
        for keyword in english_keywords:
            if len(videos) >= max_results:
                break
            
            try:
                search_url = f'ytsearch{per_keyword}:{keyword}'
                
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    result = ydl.extract_info(search_url, download=False)
                    
                    if result and 'entries' in result:
                        for entry in result['entries']:
                            if entry and len(videos) < max_results:
                                video_info = self._parse_ytdlp_data(entry, is_korean=False)
                                if video_info:
                                    videos.append(video_info)
            except Exception as e:
                continue
        
        return videos
    
    def _parse_ytdlp_data(self, entry: dict, is_korean: bool = False) -> Dict:
        """yt-dlp 데이터 파싱"""
        try:
            title = entry.get('title', '')
            video_id = entry.get('id', '')
            view_count = entry.get('view_count', 0)
            duration = entry.get('duration', 0)
            
            if not title or not video_id:
                return None
            
            # 쇼츠 여부 판단 (60초 이하)
            is_shorts = duration and duration <= 60
            
            # 키워드 추출
            keywords = self._extract_keywords(title)
            category = self._estimate_category(title, keywords)
            
            # 지역/언어 판단 - 제목의 실제 언어 기반으로 판단
            has_korean = bool(re.search(r'[가-힣]', title))
            korean_ratio = len(re.findall(r'[가-힣]', title)) / len(title) if len(title) > 0 else 0
            
            # 한글이 30% 이상이면 한국어, 아니면 영어
            if korean_ratio >= 0.1 or has_korean:
                region = "국내"
                language = "한국어"
            else:
                region = "해외"
                language = "영어"
            
            return {
                "title": title,
                "category": category,
                "views": self._format_views(view_count),
                "engagement": self._calculate_engagement(view_count),
                "keywords": keywords,
                "thumbnail": self._get_emoji(category),
                "why_viral": self._analyze_viral(title, view_count),
                "video_id": video_id,
                "youtube_url": f"https://www.youtube.com/watch?v={video_id}",
                "shorts_url": f"https://www.youtube.com/shorts/{video_id}",
                "is_shorts": is_shorts,
                "video_type": "쇼츠" if is_shorts else "롱폼",
                "duration": duration,
                "region": region,
                "language": language,
                "trend_score": self._calculate_trend_score(view_count),
                "crawled_at": datetime.now().isoformat()
            }
        except Exception as e:
            return None
    
    def _format_views(self, count: int) -> str:
        """조회수 포맷"""
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
        """트렌드 점수"""
        if view_count >= 5000000:
            return 100
        elif view_count >= 1000000:
            return 95
        elif view_count >= 500000:
            return 90
        elif view_count >= 100000:
            return 85
        return 70
    
    def _extract_keywords(self, title: str) -> List[str]:
        """키워드 추출 - 더 많은 키워드 추출"""
        keyword_patterns = {
            '부업': r'부업|사이드|n잡|투잡|side.*hustle',
            '재테크': r'재테크|돈|수익|벌기|money|earn',
            '투자': r'투자|주식|부동산|코인|stock|invest',
            'AI': r'AI|ChatGPT|인공지능|artificial',
            '개발': r'개발|코딩|프로그래밍|coding|programming|dev',
            '마케팅': r'마케팅|SNS|인스타|틱톡|marketing|instagram|tiktok',
            '창업': r'창업|사업|스타트업|business|startup|entrepreneur',
            '자기계발': r'자기계발|루틴|습관|동기부여|motivation|routine|habit',
            '요리': r'요리|레시피|먹방|음식|cook|recipe|food',
            '게임': r'게임|롤|배그|game|gaming|lol',
            '운동': r'운동|헬스|다이어트|workout|fitness|diet',
            '공부': r'공부|학습|영어|study|learn|english',
            '브이로그': r'브이로그|일상|루틴|vlog|daily',
            '리뷰': r'리뷰|추천|비교|review|recommend',
            '꿀팁': r'꿀팁|비법|방법|노하우|tip|trick|hack'
        }
        
        keywords = []
        for keyword, pattern in keyword_patterns.items():
            if re.search(pattern, title, re.IGNORECASE):
                keywords.append(keyword)
        
        # 해시태그에서 추가 키워드 추출
        hashtags = re.findall(r'#(\w+)', title)
        for tag in hashtags[:3]:
            if len(tag) > 2 and tag not in keywords:
                keywords.append(tag)
        
        return keywords[:10] if keywords else ['트렌드']
    
    def _estimate_category(self, title: str, keywords: List[str]) -> str:
        """카테고리 추정"""
        if any(k in keywords for k in ['부업', '창업']):
            return '창업/부업'
        elif any(k in keywords for k in ['재테크', '투자']):
            return '재테크/금융'
        elif 'AI' in keywords or '개발' in keywords:
            return '과학기술'
        elif '마케팅' in keywords:
            return '마케팅/비즈니스'
        elif '자기계발' in keywords:
            return '자기계발'
        return '일반'
    
    def _get_emoji(self, category: str) -> str:
        """카테고리별 이모지"""
        emojis = {
            '창업/부업': '💼', '재테크/금융': '💰', '과학기술': '🔬',
            '자기계발': '💪', '마케팅/비즈니스': '📱', '게임': '🎮',
            '요리/음식': '🍳', '교육': '📚', '음악': '🎵'
        }
        return emojis.get(category, '🎬')
    
    def _analyze_viral(self, title: str, view_count: int) -> str:
        """바이럴 요소 분석"""
        elements = []
        
        if view_count >= 1000000:
            elements.append("초고조회수")
        
        if re.search(r'\d+만원|\d+억', title):
            elements.append("구체적 금액")
        if re.search(r'\d+개월|\d+일', title):
            elements.append("기간 명시")
        if re.search(r'비법|꿀팁|방법', title):
            elements.append("하우투")
        
        return " + ".join(elements) if elements else "인기 급상승"
    
    def _retry_crawling(self, max_results: int, include_shorts: bool, include_long: bool) -> List[Dict]:
        """크롤링 재시도 - 실제 데이터만 사용"""
        print("🔄 실제 크롤링 재시도 중...")
        
        try:
            videos = []
            search_terms = ['trending', 'viral', 'popular', 'shorts']
            
            for term in search_terms:
                if len(videos) >= max_results:
                    break
                    
                try:
                    search_url = f'ytsearch{max_results//len(search_terms)}:{term}'
                    ydl_opts = {
                        'quiet': True,
                        'no_warnings': True,
                        'extract_flat': True,
                    }
                    
                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        result = ydl.extract_info(search_url, download=False)
                        
                        if result and 'entries' in result:
                            for entry in result['entries']:
                                if entry and len(videos) < max_results:
                                    video_info = self._parse_ytdlp_data(entry)
                                    if video_info:
                                        videos.append(video_info)
                except Exception as e:
                    continue
            
            print(f"✅ 재시도 성공: {len(videos)}개 실제 영상 수집")
            return videos
            
        except Exception as e:
            print(f"❌ 재시도 실패: {e}")
            return []
    
    def save_to_cache(self, data: List[Dict]):
        """캐시 저장"""
        cache_data = {
            "last_updated": datetime.now().isoformat(),
            "videos": data,
            "count": len(data),
            "source": "yt-dlp_crawler"
        }
        
        with open(self.cache_file, 'w', encoding='utf-8') as f:
            json.dump(cache_data, f, ensure_ascii=False, indent=2)
        
        print(f"💾 캐시 저장 완료: {len(data)}개 영상")
    
    def _sort_by_trend_and_recency(self, videos: List[Dict]) -> List[Dict]:
        """트렌드 점수와 최신성을 종합하여 정렬 (급상승 우선)"""
        def sort_key(video):
            trend_score = video.get('trend_score', 0)
            views = video.get('views', 0)
            # 트렌드 점수 70%, 조회수 30% 가중치
            return (trend_score * 0.7) + (views / 1000000 * 0.3)
        
        return sorted(videos, key=sort_key, reverse=True)

if __name__ == "__main__":
    crawler = YouTubeYTDLPCrawler()
    print("🎬 100개 영상 수집 테스트 (쇼츠+롱폼, 한국어+영어)...")
    videos = crawler.get_trending_videos(100, True, True)
    
    if videos:
        print(f"\n📊 수집된 영상 {len(videos)}개:")
        shorts = [v for v in videos if v.get('is_shorts')]
        longs = [v for v in videos if not v.get('is_shorts')]
        korean = [v for v in videos if v.get('language') == '한국어']
        
        print(f"   쇼츠: {len(shorts)}개 | 롱폼: {len(longs)}개")
        print(f"   한국어: {len(korean)}개 | 영어: {len(videos) - len(korean)}개")
        print(f"\n상위 5개:")
        for i, v in enumerate(videos[:5], 1):
            print(f"{i}. {v['title'][:60]}...")
            print(f"   {v['video_type']} | {v['views']} | {v['language']}")
            print(f"   {v['youtube_url']}")
    else:
        print("\n⚠️ 영상 수집 실패")

