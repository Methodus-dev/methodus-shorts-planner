"""
YouTube Data API v3 서비스
급상승 영상 데이터를 YouTube 공식 API를 통해 수집
"""
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from typing import List, Dict, Optional
from datetime import datetime, timedelta
import random
import os
from dotenv import load_dotenv

# 환경 변수 로드
load_dotenv()

class YouTubeAPIService:
    """YouTube Data API v3를 사용한 데이터 수집 서비스"""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        YouTube API 서비스 초기화
        
        Args:
            api_key: YouTube Data API v3 키 (없으면 환경 변수에서 로드)
        """
        self.api_key = api_key or os.getenv('YOUTUBE_API_KEY')
        
        if not self.api_key:
            raise ValueError(
                "YouTube API 키가 필요합니다. "
                "환경 변수 YOUTUBE_API_KEY를 설정하거나 api_key 파라미터를 전달하세요. "
                "설정 방법은 YOUTUBE_API_SETUP.md 파일을 참조하세요."
            )
        
        # YouTube API 클라이언트 생성
        self.youtube = build('youtube', 'v3', developerKey=self.api_key)
        
        # 카테고리 매핑 (YouTube 카테고리 ID → 한국어 카테고리명)
        self.category_mapping = {
            '1': '영화/애니메이션',
            '2': '자동차/교통',
            '10': '음악',
            '15': '동물/반려동물',
            '17': '스포츠',
            '19': '여행/이벤트',
            '20': '게임',
            '22': '사람/블로그',
            '23': '코미디',
            '24': '엔터테인먼트',
            '25': '뉴스/정치',
            '26': '라이프스타일',
            '27': '교육/학습',
            '28': '과학기술',
            '29': '비영리/사회운동'
        }
        
        # YouTube 원본 카테고리를 그대로 사용 (더 정확한 분류)
        # 필요한 경우에만 소수의 카테고리만 매핑
        self.app_category_mapping = {
            '음악': '음악',
            '게임': '게임',
            '과학기술': '과학기술',
            '교육/학습': '교육/학습',
            '엔터테인먼트': '엔터테인먼트',
            '라이프스타일': '라이프스타일',
            '뉴스/정치': '뉴스/정치',
            '스포츠': '스포츠',
            '코미디': '코미디',
            '사람/블로그': '사람/블로그',
            '영화/애니메이션': '영화/애니메이션',
            '동물/반려동물': '동물/반려동물',
            '여행/이벤트': '여행/이벤트',
            '자동차/교통': '자동차/교통',
            '비영리/사회운동': '비영리/사회운동'
        }
    
    def detect_language(self, text: str) -> str:
        """
        텍스트에서 언어 감지
        
        Args:
            text: 분석할 텍스트
        
        Returns:
            감지된 언어 ('한국어', '일본어', '영어', '중국어', '기타')
        """
        if not text:
            return '기타'
        
        # 각 언어별 문자 개수 카운트
        korean_count = 0
        japanese_count = 0
        chinese_count = 0
        english_count = 0
        
        for char in text:
            # 한글 (가-힣)
            if '\uac00' <= char <= '\ud7a3':
                korean_count += 1
            # 일본어 히라가나 (ぁ-ん)
            elif '\u3040' <= char <= '\u309f':
                japanese_count += 1
            # 일본어 가타카나 (ァ-ヶ)
            elif '\u30a0' <= char <= '\u30ff':
                japanese_count += 1
            # 영어 (A-Z, a-z)
            elif ('A' <= char <= 'Z') or ('a' <= char <= 'z'):
                english_count += 1
            # 중국어 간체/번체 (CJK Unified Ideographs)
            elif '\u4e00' <= char <= '\u9fff':
                chinese_count += 1
        
        # 우선순위 기반 언어 감지
        # 1. 한글이 5개 이상 있으면 무조건 한국어
        if korean_count >= 5:
            return '한국어'
        
        # 2. 일본어 문자(히라가나 or 가타카나)가 3개 이상 있으면 일본어
        if japanese_count >= 3:
            return '일본어'
        
        # 3. 중국어 한자가 5개 이상 있고, 한글/일본어가 없으면 중국어
        if chinese_count >= 5 and korean_count == 0 and japanese_count == 0:
            return '중국어'
        
        # 4. 위 조건에 해당하지 않으면 가장 많이 사용된 언어
        counts = {
            '한국어': korean_count,
            '일본어': japanese_count,
            '중국어': chinese_count,
            '영어': english_count
        }
        
        max_count = max(counts.values())
        if max_count == 0:
            return '기타'
        
        # 가장 많이 사용된 언어 반환 (동점인 경우 우선순위)
        for lang in ['한국어', '일본어', '중국어', '영어']:
            if counts[lang] == max_count:
                return lang
        
        return '기타'
    
    def get_trending_videos(
        self,
        region_code: str = 'KR',
        max_results: int = 50,
        category_id: Optional[str] = None
    ) -> List[Dict]:
        """
        급상승 영상 목록 가져오기
        
        Args:
            region_code: 지역 코드 (KR=한국, US=미국, JP=일본 등)
            max_results: 최대 결과 수 (1-50)
            category_id: 카테고리 ID (선택사항)
        
        Returns:
            영상 정보 리스트
        """
        try:
            # API 요청 파라미터
            request_params = {
                'part': 'snippet,statistics,contentDetails',
                'chart': 'mostPopular',
                'regionCode': region_code,
                'maxResults': min(max_results, 50),  # API 제한: 최대 50
                'videoCategoryId': category_id
            }
            
            # category_id가 None이면 제거
            if not category_id:
                del request_params['videoCategoryId']
            
            # API 호출
            request = self.youtube.videos().list(**request_params)
            response = request.execute()
            
            # 결과 파싱
            videos = []
            for item in response.get('items', []):
                video_info = self._parse_video_item(item, region_code)
                if video_info:
                    videos.append(video_info)
            
            return videos
            
        except HttpError as e:
            print(f"❌ YouTube API 오류: {e}")
            if e.resp.status == 403:
                print("💡 할당량 초과 또는 API 키 문제일 수 있습니다.")
                print("   - Google Cloud Console에서 할당량 확인")
                print("   - API 키가 올바른지 확인")
            return []
        except Exception as e:
            print(f"❌ 예상치 못한 오류: {e}")
            return []
    
    def search_videos(
        self,
        query: str,
        max_results: int = 20,
        order: str = 'viewCount',
        published_after: Optional[datetime] = None
    ) -> List[Dict]:
        """
        키워드로 영상 검색
        
        Args:
            query: 검색 키워드
            max_results: 최대 결과 수
            order: 정렬 순서 (date, rating, relevance, title, videoCount, viewCount)
            published_after: 이 날짜 이후에 업로드된 영상만 검색
        
        Returns:
            영상 정보 리스트
        """
        try:
            # 기본값: 3개월 전
            if not published_after:
                published_after = datetime.now() - timedelta(days=90)
            
            # API 요청
            request = self.youtube.search().list(
                part='snippet',
                q=query,
                type='video',
                order=order,
                maxResults=min(max_results, 50),
                publishedAfter=published_after.isoformat() + 'Z',
                relevanceLanguage='ko'  # 한국어 영상 우선
            )
            response = request.execute()
            
            # 비디오 ID 추출
            video_ids = [item['id']['videoId'] for item in response.get('items', [])]
            
            # 비디오 상세 정보 가져오기 (조회수, 좋아요 등)
            if video_ids:
                return self.get_videos_by_ids(video_ids)
            
            return []
            
        except HttpError as e:
            print(f"❌ 검색 오류: {e}")
            return []
    
    def get_videos_by_ids(self, video_ids: List[str]) -> List[Dict]:
        """
        비디오 ID 리스트로 상세 정보 가져오기 (배치 처리)
        
        Args:
            video_ids: 비디오 ID 리스트 (최대 50개)
        
        Returns:
            영상 정보 리스트
        """
        try:
            # API는 한 번에 최대 50개 처리 가능
            video_ids = video_ids[:50]
            
            request = self.youtube.videos().list(
                part='snippet,statistics,contentDetails',
                id=','.join(video_ids)
            )
            response = request.execute()
            
            videos = []
            for item in response.get('items', []):
                video_info = self._parse_video_item(item)
                if video_info:
                    videos.append(video_info)
            
            return videos
            
        except HttpError as e:
            print(f"❌ 비디오 정보 조회 오류: {e}")
            return []
    
    def _parse_video_item(self, item: Dict, region_code: str = 'KR') -> Optional[Dict]:
        """
        YouTube API 응답 아이템을 우리 앱 형식으로 파싱
        
        Args:
            item: YouTube API 응답 아이템
            region_code: 지역 코드
        
        Returns:
            파싱된 영상 정보
        """
        try:
            snippet = item['snippet']
            statistics = item.get('statistics', {})
            content_details = item.get('contentDetails', {})
            
            video_id = item['id']
            
            # 조회수
            view_count = int(statistics.get('viewCount', 0))
            views_formatted = self._format_number(view_count)
            
            # 좋아요 수
            like_count = int(statistics.get('likeCount', 0))
            
            # 댓글 수
            comment_count = int(statistics.get('commentCount', 0))
            
            # 영상 길이 (ISO 8601 duration을 초로 변환)
            duration = self._parse_duration(content_details.get('duration', 'PT0S'))
            
            # 영상 타입 결정 (쇼츠 vs 롱폼)
            # YouTube Shorts: 60초 이하
            video_type = '쇼츠' if duration <= 60 else '롱폼'
            
            # 카테고리
            category_id = snippet.get('categoryId', '0')
            youtube_category = self.category_mapping.get(category_id, '기타')
            app_category = self.app_category_mapping.get(youtube_category, '기타')
            
            # 언어 감지 (제목 기반)
            title = snippet['title']
            language = self.detect_language(title)
            
            # 지역
            region = '국내' if region_code == 'KR' else '해외'
            
            # 업로드 날짜
            published_at = snippet['publishedAt']
            
            # 트렌드 점수 계산
            trend_score = self._calculate_trend_score(
                view_count, like_count, comment_count, published_at
            )
            
            # 키워드 추출 (제목에서)
            keywords = self._extract_keywords(title)
            
            # 썸네일
            thumbnails = snippet.get('thumbnails', {})
            thumbnail_url = (
                thumbnails.get('high', {}).get('url') or
                thumbnails.get('medium', {}).get('url') or
                thumbnails.get('default', {}).get('url', '')
            )
            
            # 바이럴 이유 생성
            why_viral = self._generate_viral_reason(view_count, like_count, trend_score)
            
            # 참여도 계산
            engagement_rate = (like_count / max(view_count, 1)) * 100
            engagement = f"{engagement_rate:.1f}%"
            
            return {
                'video_id': video_id,
                'title': title,
                'views': views_formatted,
                'view_count': view_count,
                'category': app_category,
                'language': language,
                'video_type': video_type,
                'youtube_url': f"https://www.youtube.com/watch?v={video_id}",
                'thumbnail': thumbnail_url,
                'trend_score': trend_score,
                'crawled_at': datetime.now().isoformat(),
                'published_at': published_at,
                'region': region,
                'keywords': keywords,
                'why_viral': why_viral,
                'engagement': engagement,
                'like_count': like_count,
                'comment_count': comment_count,
                'duration': duration,
                'channel_title': snippet.get('channelTitle', ''),
                'description': snippet.get('description', '')[:200],
                'source': 'youtube_api'
            }
            
        except Exception as e:
            print(f"❌ 영상 파싱 오류: {e}")
            return None
    
    def _parse_duration(self, duration_str: str) -> int:
        """
        ISO 8601 duration을 초로 변환
        
        예: PT1H2M10S → 3730초
            PT15M33S → 933초
            PT45S → 45초
        
        Args:
            duration_str: ISO 8601 형식의 duration
        
        Returns:
            초 단위 시간
        """
        import re
        
        pattern = r'PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?'
        match = re.match(pattern, duration_str)
        
        if not match:
            return 0
        
        hours = int(match.group(1) or 0)
        minutes = int(match.group(2) or 0)
        seconds = int(match.group(3) or 0)
        
        return hours * 3600 + minutes * 60 + seconds
    
    def _format_number(self, num: int) -> str:
        """
        숫자를 K, M 단위로 포맷
        
        Args:
            num: 숫자
        
        Returns:
            포맷된 문자열 (예: 1.2M, 345K)
        """
        if num >= 1_000_000:
            return f"{num / 1_000_000:.1f}M"
        elif num >= 1_000:
            return f"{num / 1_000:.1f}K"
        else:
            return str(num)
    
    def _calculate_trend_score(
        self,
        view_count: int,
        like_count: int,
        comment_count: int,
        published_at: str
    ) -> int:
        """
        트렌드 점수 계산 (0-100)
        
        Args:
            view_count: 조회수
            like_count: 좋아요 수
            comment_count: 댓글 수
            published_at: 업로드 날짜
        
        Returns:
            트렌드 점수 (0-100)
        """
        # 조회수 점수 (0-40)
        view_score = min(40, int(view_count / 100000))
        
        # 좋아요 비율 점수 (0-25)
        like_ratio = (like_count / max(view_count, 1)) * 100
        like_score = min(25, int(like_ratio * 5))
        
        # 댓글 참여도 점수 (0-15)
        comment_ratio = (comment_count / max(view_count, 1)) * 100
        comment_score = min(15, int(comment_ratio * 30))
        
        # 최신성 점수 (0-20)
        try:
            video_date = datetime.fromisoformat(published_at.replace('Z', '+00:00'))
            days_ago = (datetime.now(video_date.tzinfo) - video_date).days
            
            if days_ago <= 1:
                recency_score = 20
            elif days_ago <= 7:
                recency_score = 15
            elif days_ago <= 30:
                recency_score = 10
            elif days_ago <= 90:
                recency_score = 5
            else:
                recency_score = 0
        except:
            recency_score = 5
        
        total_score = view_score + like_score + comment_score + recency_score
        return min(100, max(0, total_score))
    
    def _extract_keywords(self, title: str, max_keywords: int = 5) -> List[str]:
        """
        제목에서 키워드 추출
        
        Args:
            title: 영상 제목
            max_keywords: 최대 키워드 수
        
        Returns:
            키워드 리스트
        """
        # 불용어 제거
        stop_words = {
            '의', '가', '이', '은', '들', '는', '좀', '잘', '걍', '과', '도', '를', '으로', '자', '에',
            '와', '한', '하다', 'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for'
        }
        
        # 특수문자 제거 및 단어 분리
        import re
        words = re.findall(r'\b\w+\b', title.lower())
        
        # 불용어 제거 및 길이 필터
        keywords = [
            word for word in words 
            if word not in stop_words and len(word) >= 2
        ]
        
        return keywords[:max_keywords]
    
    def _generate_viral_reason(
        self,
        view_count: int,
        like_count: int,
        trend_score: int
    ) -> str:
        """
        바이럴 이유 생성
        
        Args:
            view_count: 조회수
            like_count: 좋아요 수
            trend_score: 트렌드 점수
        
        Returns:
            바이럴 이유 문자열
        """
        reasons = [
            "실용적인 정보와 단계별 가이드",
            "초보자도 쉽게 따라할 수 있는 방법",
            "최신 트렌드와 실전 경험 공유",
            "구체적인 수치와 결과 제시",
            "독특한 관점과 새로운 접근법",
            "감정적 몰입과 스토리텔링",
            "시각적 임팩트와 편집 기법",
            "높은 참여도와 커뮤니티 반응"
        ]
        
        # 트렌드 점수에 따라 이유 선택
        if trend_score >= 80:
            return reasons[0]  # 가장 강력한 이유
        elif like_count / max(view_count, 1) > 0.05:
            return reasons[7]  # 높은 참여도
        else:
            return random.choice(reasons)
    
    def get_multiple_regions(
        self,
        region_codes: List[str] = ['KR', 'US', 'JP'],
        max_results_per_region: int = 20
    ) -> List[Dict]:
        """
        여러 지역의 급상승 영상을 한 번에 가져오기
        
        Args:
            region_codes: 지역 코드 리스트
            max_results_per_region: 지역당 최대 결과 수
        
        Returns:
            모든 지역의 영상 정보 리스트
        """
        all_videos = []
        
        for region_code in region_codes:
            print(f"📡 {region_code} 지역 급상승 영상 수집 중...")
            videos = self.get_trending_videos(
                region_code=region_code,
                max_results=max_results_per_region
            )
            all_videos.extend(videos)
            print(f"✅ {region_code}: {len(videos)}개 수집 완료")
        
        # 중복 제거 (video_id 기준)
        seen_ids = set()
        unique_videos = []
        for video in all_videos:
            if video['video_id'] not in seen_ids:
                seen_ids.add(video['video_id'])
                unique_videos.append(video)
        
        # 트렌드 점수 기준으로 정렬
        unique_videos.sort(key=lambda x: x['trend_score'], reverse=True)
        
        return unique_videos
    
    def get_trending_by_categories(
        self,
        region_code: str = 'KR',
        min_videos_per_category: int = 100
    ) -> List[Dict]:
        """
        카테고리별로 급상승 영상을 수집
        
        Args:
            region_code: 지역 코드 (KR, US, JP 등)
            min_videos_per_category: 카테고리당 최소 영상 수
        
        Returns:
            모든 카테고리의 영상 정보 리스트
        """
        # YouTube API 주요 카테고리 ID
        main_categories = {
            '10': '음악',
            '20': '게임',
            '28': '과학기술',
            '27': '교육/학습',
            '24': '엔터테인먼트',
            '26': '라이프스타일',
            '25': '뉴스/정치',
            '17': '스포츠',
            '23': '코미디',
            '22': '사람/블로그'
        }
        
        all_videos = []
        seen_ids = set()
        
        for category_id, category_name in main_categories.items():
            print(f"📂 [{category_name}] 카테고리 수집 중...")
            
            # 카테고리별로 50개씩 수집 (API 최대값)
            videos = self.get_trending_videos(
                region_code=region_code,
                max_results=50,
                category_id=category_id
            )
            
            # 중복 제거하면서 추가
            new_videos = 0
            for video in videos:
                if video['video_id'] not in seen_ids:
                    seen_ids.add(video['video_id'])
                    all_videos.append(video)
                    new_videos += 1
            
            print(f"✅ [{category_name}]: {new_videos}개 신규 수집 (중복 제외)")
        
        # 트렌드 점수 기준으로 정렬
        all_videos.sort(key=lambda x: x['trend_score'], reverse=True)
        
        return all_videos
    
    def get_comprehensive_data(
        self,
        region_codes: List[str] = ['KR', 'US', 'JP'],
        min_videos_per_category: int = 100
    ) -> List[Dict]:
        """
        여러 지역에서 카테고리별로 종합 데이터 수집
        
        Args:
            region_codes: 지역 코드 리스트
            min_videos_per_category: 카테고리당 최소 영상 수
        
        Returns:
            모든 영상 정보 리스트
        """
        all_videos = []
        seen_ids = set()
        
        for region_code in region_codes:
            print(f"\n🌍 {region_code} 지역 데이터 수집 시작...")
            
            # 카테고리별로 수집
            videos = self.get_trending_by_categories(
                region_code=region_code,
                min_videos_per_category=min_videos_per_category
            )
            
            # 중복 제거하면서 추가
            new_videos = 0
            for video in videos:
                if video['video_id'] not in seen_ids:
                    seen_ids.add(video['video_id'])
                    all_videos.append(video)
                    new_videos += 1
            
            print(f"✅ {region_code}: 총 {new_videos}개 신규 영상 수집")
        
        # 트렌드 점수 기준으로 정렬
        all_videos.sort(key=lambda x: x['trend_score'], reverse=True)
        
        print(f"\n🎉 전체 수집 완료: {len(all_videos)}개 영상")
        
        # 카테고리별 통계 출력
        from collections import Counter
        category_counts = Counter(v['category'] for v in all_videos)
        print("\n📊 카테고리별 영상 수:")
        for cat, count in category_counts.most_common():
            print(f"   {cat}: {count}개")
        
        return all_videos


# 사용 예시
if __name__ == "__main__":
    # 환경 변수에서 API 키 로드
    service = YouTubeAPIService()
    
    print("🎬 YouTube API 서비스 테스트\n")
    
    # 한국 급상승 영상 가져오기
    print("1️⃣ 한국 급상승 영상 TOP 10:")
    videos = service.get_trending_videos(region_code='KR', max_results=10)
    for i, video in enumerate(videos, 1):
        print(f"{i}. [{video['video_type']}] {video['title']}")
        print(f"   조회수: {video['views']} | 트렌드: {video['trend_score']}점")
        print(f"   카테고리: {video['category']} | 언어: {video['language']}\n")
    
    # 키워드 검색
    print("\n2️⃣ '부업' 키워드 검색:")
    search_results = service.search_videos('부업', max_results=5)
    for i, video in enumerate(search_results, 1):
        print(f"{i}. {video['title']}")
        print(f"   조회수: {video['views']} | {video['channel_title']}\n")
    
    # 여러 지역 데이터 수집
    print("\n3️⃣ 한국/미국/일본 급상승 영상:")
    multi_region = service.get_multiple_regions(['KR', 'US', 'JP'], max_results_per_region=5)
    print(f"✅ 총 {len(multi_region)}개 영상 수집 완료")


