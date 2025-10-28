"""
YouTube 실시간 크롤러 - 실제 데이터만 사용
샘플/더미/임시 데이터 사용 금지
"""
import json
import time
import threading
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Optional
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import re

class YouTubeRealtimeCrawler:
    def __init__(self, cache_file: str = "../data/youtube_realtime_cache.json"):
        self.cache_file = Path(cache_file)
        self.cache_file.parent.mkdir(parents=True, exist_ok=True)
        self.last_update = None
        self.update_interval = 2 * 60 * 60  # 2시간
    
    def crawl_trending_shorts(self, count: int = 30) -> List[Dict]:
        """실제 YouTube Shorts 크롤링 - 샘플 데이터 사용 금지"""
        print(f"🎬 실제 YouTube Shorts 크롤링 시작 (목표: {count}개)...")
        
        driver = None
        try:
            # Chrome 옵션 설정
            chrome_options = Options()
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument('--disable-gpu')
            chrome_options.add_argument('--window-size=1920,1080')
            chrome_options.add_argument('--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36')
            
            driver = webdriver.Chrome(options=chrome_options)
            driver.get("https://www.youtube.com/shorts")
            
            # 페이지 로딩 대기
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            
            # 스크롤하여 더 많은 영상 로드
            for _ in range(5):
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)
            
            # 영상 정보 추출
            videos_data = self._extract_video_data(driver, count)
            
            if videos_data and len(videos_data) > 0:
                print(f"✅ 실제 크롤링 성공: {len(videos_data)}개 동영상")
                return videos_data
            else:
                print("❌ 실제 데이터 수집 실패")
                return []
                
        except Exception as e:
            print(f"❌ 크롤링 오류: {e}")
            print("🔄 실제 크롤링 재시도 중...")
            return self._retry_real_crawling(count)
        
        finally:
            if driver:
                driver.quit()
    
    def _retry_real_crawling(self, count: int) -> List[Dict]:
        """실제 크롤링 재시도 - 샘플 데이터 사용 금지"""
        print("🔄 실제 크롤링 재시도 중...")
        
        try:
            # 다른 크롤링 방법 시도
            videos = self._get_real_trending_videos(count)
            if videos:
                print(f"✅ 실제 크롤링 성공: {len(videos)}개 영상")
                return videos
            else:
                print("❌ 실제 데이터 수집 실패")
                return []
        except Exception as e:
            print(f"❌ 재시도 실패: {e}")
            return []
    
    def _get_fallback_data(self, count: int) -> List[Dict]:
        """실제 데이터만 사용 - 샘플 데이터 금지"""
        print("❌ 실제 데이터 수집 실패 - 빈 결과 반환")
        return []
    
    def _extract_video_data(self, driver, count: int) -> List[Dict]:
        """실제 영상 데이터 추출"""
        videos = []
        
        try:
            # 영상 요소들 찾기
            video_elements = driver.find_elements(By.CSS_SELECTOR, "a[href*='/shorts/']")
            
            for element in video_elements[:count]:
                try:
                    title = element.get_attribute("title") or "제목 없음"
                    href = element.get_attribute("href")
                    
                    if href and "/shorts/" in href:
                        video_id = href.split("/shorts/")[-1].split("?")[0]
                        
                        video_data = {
                            "title": title,
                            "category": self._categorize_video(title),
                            "views": self._get_view_count(element),
                            "engagement": "높음",
                            "keywords": self._extract_keywords(title),
                            "thumbnail": "📱",
                            "why_viral": self._analyze_viral_factors(title),
                            "video_id": video_id,
                            "youtube_url": f"https://www.youtube.com/watch?v={video_id}",
                            "shorts_url": href,
                            "is_shorts": True,
                            "region": "국내",
                            "language": "한국어",
                            "trend_score": self._calculate_trend_score(title)
                        }
                        
                        videos.append(video_data)
                        
                except Exception as e:
                    continue
            
            return videos
            
        except Exception as e:
            print(f"❌ 데이터 추출 오류: {e}")
            return []
    
    def _categorize_video(self, title: str) -> str:
        """영상 제목으로 카테고리 분류"""
        title_lower = title.lower()
        
        if any(word in title_lower for word in ['부업', '창업', '돈', '수익', 'n잡']):
            return '창업/부업'
        elif any(word in title_lower for word in ['주식', '투자', '재테크', '코인']):
            return '재테크/금융'
        elif any(word in title_lower for word in ['ai', 'chatgpt', '코딩', '개발']):
            return '과학기술'
        elif any(word in title_lower for word in ['운동', '헬스', '다이어트']):
            return '운동/건강'
        elif any(word in title_lower for word in ['요리', '레시피', '먹방']):
            return '요리/음식'
        else:
            return '기타'
    
    def _get_view_count(self, element) -> str:
        """조회수 추출"""
        try:
            view_element = element.find_element(By.CSS_SELECTOR, "[class*='view']")
            return view_element.text
        except:
            return "조회수 없음"
    
    def _extract_keywords(self, title: str) -> List[str]:
        """제목에서 키워드 추출"""
        keywords = []
        
        # 주요 키워드 패턴
        patterns = {
            '부업': ['부업', 'n잡', '투잡', '사이드'],
            '돈': ['돈', '수익', '월급', '벌기'],
            '주식': ['주식', '투자', '재테크'],
            'AI': ['ai', 'chatgpt', '인공지능'],
            '운동': ['운동', '헬스', '다이어트'],
            '요리': ['요리', '레시피', '먹방']
        }
        
        for category, words in patterns.items():
            if any(word in title.lower() for word in words):
                keywords.append(category)
        
        return keywords[:3]
    
    def _analyze_viral_factors(self, title: str) -> str:
        """바이럴 요소 분석"""
        elements = []
        
        if re.search(r'\d+', title):
            elements.append("숫자")
        if re.search(r'[!?]', title):
            elements.append("감정")
        if re.search(r'비법|꿀팁|방법', title):
            elements.append("하우투")
        
        return " + ".join(elements) if elements else "흥미로운 주제"
    
    def _calculate_trend_score(self, title: str) -> int:
        """트렌드 점수 계산"""
        score = 50  # 기본 점수
        
        # 제목 길이
        if len(title) > 20:
            score += 10
        
        # 숫자 포함
        if re.search(r'\d+', title):
            score += 15
        
        # 감정 표현
        if re.search(r'[!?]', title):
            score += 10
        
        # 키워드 점수
        viral_keywords = ['비법', '꿀팁', '방법', '공개', '진짜', '절대']
        for keyword in viral_keywords:
            if keyword in title:
                score += 5
        
        return min(score, 100)
    
    def save_to_cache(self, data: List[Dict]):
        """캐시에 저장"""
        cache_data = {
            "last_updated": datetime.now().isoformat(),
            "videos": data,
            "count": len(data),
            "source": "real_crawler"
        }
        
        with open(self.cache_file, 'w', encoding='utf-8') as f:
            json.dump(cache_data, f, ensure_ascii=False, indent=2)
        
        self.last_update = datetime.now()
        print(f"💾 실제 데이터 캐시 저장 완료: {len(data)}개 영상")
    
    def load_from_cache(self) -> Dict:
        """캐시에서 로드"""
        if self.cache_file.exists():
            with open(self.cache_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return None
