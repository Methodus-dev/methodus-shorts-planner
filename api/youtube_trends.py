"""
YouTube 급상승 동영상 트렌드 분석 시스템
"""
import random
from typing import List, Dict
from datetime import datetime, timedelta
import re
from collections import Counter

class YouTubeTrendsAnalyzer:
    def __init__(self):
        # 실제 YouTube Data API를 사용할 수도 있지만, 
        # 우선 한국에서 인기있는 쇼츠 주제들을 시뮬레이션
        self.trending_categories = {
            "재테크/투자": ["부동산", "주식", "재테크", "투자", "금융"],
            "부업/창업": ["부업", "창업", "사업", "온라인비즈니스", "N잡"],
            "자기계발": ["자기계발", "성장", "생산성", "습관", "루틴"],
            "IT/테크": ["AI", "ChatGPT", "개발", "프로그래밍", "코딩"],
            "마케팅": ["마케팅", "브랜딩", "SNS마케팅", "콘텐츠마케팅"],
            "라이프스타일": ["브이로그", "일상", "미니멀리즘", "정리"],
            "건강/운동": ["홈트", "다이어트", "건강", "운동루틴"],
            "요리/먹방": ["요리", "레시피", "간단요리", "먹방"],
            "교육": ["영어", "공부법", "인강", "자격증"],
            "엔터테인먼트": ["챌린지", "밈", "쇼츠", "밀착"]
        }
    
    def get_trending_videos(self, count: int = 20) -> List[Dict]:
        """급상승 동영상 시뮬레이션 데이터"""
        trending_videos = []
        
        # 실제 트렌드를 반영한 주제들
        real_trending_topics = [
            {
                "title": "부동산 경매 첫 투자로 3천만원 벌었습니다",
                "category": "재테크/투자",
                "views": "1.2M",
                "engagement": "높음",
                "keywords": ["부동산", "경매", "투자", "수익", "첫투자"],
                "thumbnail": "🏠",
                "why_viral": "실전 경험 + 구체적 금액"
            },
            {
                "title": "ChatGPT로 하루 10만원 버는 부업 3가지",
                "category": "부업/창업",
                "views": "890K",
                "engagement": "매우높음",
                "keywords": ["ChatGPT", "AI", "부업", "돈버는법", "재테크"],
                "thumbnail": "🤖",
                "why_viral": "AI 트렌드 + 구체적 수익"
            },
            {
                "title": "억대 연봉자의 아침 루틴 공개",
                "category": "자기계발",
                "views": "750K",
                "engagement": "높음",
                "keywords": ["루틴", "아침루틴", "자기계발", "성공습관"],
                "thumbnail": "☀️",
                "why_viral": "성공 스토리 + 따라하기 쉬움"
            },
            {
                "title": "직장 다니면서 월 500 버는 법",
                "category": "부업/창업",
                "views": "680K",
                "engagement": "매우높음",
                "keywords": ["부업", "n잡", "직장인", "월급외수입"],
                "thumbnail": "💰",
                "why_viral": "현실적 목표 + 구체적 방법"
            },
            {
                "title": "3개월 만에 팔로워 10만 만든 비법",
                "category": "마케팅",
                "views": "620K",
                "engagement": "높음",
                "keywords": ["SNS", "팔로워", "인스타그램", "마케팅"],
                "thumbnail": "📱",
                "why_viral": "빠른 성과 + SNS 관심"
            },
            {
                "title": "요즘 대학생들 이렇게 돈 법니다",
                "category": "부업/창업",
                "views": "580K",
                "engagement": "높음",
                "keywords": ["대학생", "알바", "용돈벌이", "부업"],
                "thumbnail": "🎓",
                "why_viral": "타겟 명확 + 실용성"
            },
            {
                "title": "AI 그림으로 월 1000만원 버는 법",
                "category": "IT/테크",
                "views": "550K",
                "engagement": "매우높음",
                "keywords": ["AI그림", "미드저니", "AI", "부업"],
                "thumbnail": "🎨",
                "why_viral": "AI 트렌드 + 높은 수익"
            },
            {
                "title": "퇴사 후 1년, 수입 공개합니다",
                "category": "자기계발",
                "views": "520K",
                "engagement": "높음",
                "keywords": ["퇴사", "프리랜서", "수입공개", "자유"],
                "thumbnail": "✈️",
                "why_viral": "투명한 공개 + 공감대"
            },
            {
                "title": "블로그 3개월 만에 수익화 성공",
                "category": "부업/창업",
                "views": "480K",
                "engagement": "높음",
                "keywords": ["블로그", "애드센스", "수익화", "부업"],
                "thumbnail": "✍️",
                "why_viral": "빠른 성과 + 진입장벽 낮음"
            },
            {
                "title": "이것만 알면 주식 절대 안 잃습니다",
                "category": "재테크/투자",
                "views": "450K",
                "engagement": "높음",
                "keywords": ["주식", "투자", "손실방지", "재테크"],
                "thumbnail": "📈",
                "why_viral": "손실 공포 + 확신"
            },
            {
                "title": "30대 직장인의 부동산 투자 시작법",
                "category": "재테크/투자",
                "views": "420K",
                "engagement": "높음",
                "keywords": ["30대", "직장인", "부동산투자", "첫투자"],
                "thumbnail": "🏢",
                "why_viral": "타겟 명확 + 실전 가이드"
            },
            {
                "title": "SNS 마케팅 이렇게 하니까 매출 2배",
                "category": "마케팅",
                "views": "390K",
                "engagement": "높음",
                "keywords": ["SNS마케팅", "매출증대", "마케팅전략"],
                "thumbnail": "📊",
                "why_viral": "구체적 성과 + 실전"
            },
            {
                "title": "요즘 뜨는 부업 TOP 5",
                "category": "부업/창업",
                "views": "370K",
                "engagement": "매우높음",
                "keywords": ["부업추천", "사이드잡", "돈벌기"],
                "thumbnail": "🔥",
                "why_viral": "리스트형 + 최신 트렌드"
            },
            {
                "title": "코딩 몰라도 앱 만드는 법",
                "category": "IT/테크",
                "views": "340K",
                "engagement": "높음",
                "keywords": ["노코드", "앱제작", "창업", "코딩"],
                "thumbnail": "📲",
                "why_viral": "진입장벽 제거 + 창업"
            },
            {
                "title": "새벽 5시 기상 30일 도전 결과",
                "category": "자기계발",
                "views": "320K",
                "engagement": "높음",
                "keywords": ["기상", "습관", "도전", "자기계발"],
                "thumbnail": "⏰",
                "why_viral": "도전 + Before/After"
            },
            {
                "title": "1인 기업으로 연 1억 버는 법",
                "category": "부업/창업",
                "views": "310K",
                "engagement": "매우높음",
                "keywords": ["1인기업", "창업", "수익", "사업"],
                "thumbnail": "👤",
                "why_viral": "높은 목표 + 구체적"
            },
            {
                "title": "미국 주식 이렇게 사면 됩니다",
                "category": "재테크/투자",
                "views": "290K",
                "engagement": "높음",
                "keywords": ["미국주식", "해외투자", "ETF"],
                "thumbnail": "🇺🇸",
                "why_viral": "해외투자 관심 + 쉬운 설명"
            },
            {
                "title": "콘텐츠 제작으로 월 300 벌기",
                "category": "부업/창업",
                "views": "270K",
                "engagement": "높음",
                "keywords": ["콘텐츠제작", "크리에이터", "수익", "유튜브"],
                "thumbnail": "🎬",
                "why_viral": "크리에이터 이코노미"
            },
            {
                "title": "공부 잘하는 사람들의 비밀",
                "category": "교육",
                "views": "250K",
                "engagement": "높음",
                "keywords": ["공부법", "학습", "효율", "집중"],
                "thumbnail": "📚",
                "why_viral": "보편적 관심사"
            },
            {
                "title": "2025년 뜰 사업 아이템 10개",
                "category": "부업/창업",
                "views": "230K",
                "engagement": "매우높음",
                "keywords": ["사업아이템", "창업", "트렌드", "2025"],
                "thumbnail": "💡",
                "why_viral": "미래 예측 + 리스트형"
            }
        ]
        
        # 랜덤하게 섞어서 실시간 느낌 주기
        random.shuffle(real_trending_topics)
        
        # 조회수 기준으로 정렬
        real_trending_topics.sort(key=lambda x: self._parse_views(x["views"]), reverse=True)
        
        return real_trending_topics[:count]
    
    def _parse_views(self, views_str: str) -> int:
        """조회수 문자열을 숫자로 변환"""
        views_str = views_str.replace("M", "000000").replace("K", "000")
        return int(float(views_str))
    
    def extract_keywords_from_videos(self, videos: List[Dict]) -> Dict:
        """급상승 동영상들에서 키워드 추출 및 분석"""
        all_keywords = []
        category_keywords = {}
        
        for video in videos:
            keywords = video.get("keywords", [])
            category = video.get("category", "")
            
            all_keywords.extend(keywords)
            
            if category not in category_keywords:
                category_keywords[category] = []
            category_keywords[category].extend(keywords)
        
        # 키워드 빈도 분석
        keyword_freq = Counter(all_keywords)
        
        # 상위 키워드
        top_keywords = keyword_freq.most_common(20)
        
        return {
            "전체_인기_키워드": [
                {
                    "키워드": kw,
                    "빈도": freq,
                    "추천도": "⭐" * min(5, freq)
                }
                for kw, freq in top_keywords
            ],
            "카테고리별_키워드": {
                category: list(set(keywords))[:5]
                for category, keywords in category_keywords.items()
            },
            "트렌드_분석": self.analyze_trends(videos),
            "키워드_조합_추천": self.suggest_keyword_combinations(keyword_freq)
        }
    
    def analyze_trends(self, videos: List[Dict]) -> Dict:
        """트렌드 분석"""
        categories = [v["category"] for v in videos]
        category_freq = Counter(categories)
        
        # 바이럴 요소 분석
        viral_patterns = []
        for video in videos:
            if video.get("why_viral"):
                viral_patterns.append(video["why_viral"])
        
        return {
            "핫한_카테고리_TOP3": [
                {
                    "카테고리": cat,
                    "영상수": count,
                    "인기도": "🔥" * min(5, count)
                }
                for cat, count in category_freq.most_common(3)
            ],
            "바이럴_패턴": list(set(viral_patterns)),
            "공통_요소": [
                "💰 구체적인 숫자 (금액, 기간)",
                "🎯 명확한 타겟층",
                "✅ 실전/실용성 강조",
                "📊 Before/After 비교",
                "🔥 최신 트렌드 반영",
                "⚡ 빠른 성과 약속"
            ]
        }
    
    def suggest_keyword_combinations(self, keyword_freq: Counter) -> List[str]:
        """효과적인 키워드 조합 추천"""
        top_keywords = [kw for kw, _ in keyword_freq.most_common(10)]
        
        combinations = []
        
        # 패턴 기반 조합
        if "부업" in top_keywords:
            combinations.append("부업 + 재테크 + 첫투자")
            combinations.append("부업 + AI + 월수익")
        
        if "투자" in top_keywords:
            combinations.append("투자 + 초보 + 실전")
            combinations.append("투자 + 부동산 + 전략")
        
        if "AI" in top_keywords:
            combinations.append("AI + 돈벌기 + 부업")
            combinations.append("AI + 활용법 + 실전")
        
        # 일반적인 고성과 조합
        combinations.extend([
            "💰 [주제] + 돈벌기 + 실전",
            "🎯 [주제] + 초보 + 완벽가이드",
            "⚡ [주제] + 빠르게 + 성공",
            "🔥 [주제] + 최신 + 트렌드",
            "✅ [주제] + 실패없는 + 방법"
        ])
        
        return combinations[:10]
    
    def suggest_content_ideas(self, keyword: str, videos: List[Dict]) -> Dict:
        """키워드 기반 콘텐츠 아이디어 제안"""
        # 관련 급상승 동영상 찾기
        related_videos = [
            v for v in videos
            if keyword in v.get("title", "") or keyword in v.get("keywords", [])
        ]
        
        # 제목 패턴 분석
        title_patterns = self.analyze_title_patterns(related_videos if related_videos else videos)
        
        return {
            "키워드": keyword,
            "관련_급상승_영상수": len(related_videos),
            "추천_제목_패턴": title_patterns,
            "콘텐츠_아이디어": [
                f"{keyword} 초보가 피해야 할 3가지 실수",
                f"{keyword} 이것만 알면 성공합니다",
                f"하루 10분 {keyword}로 인생 바꾸기",
                f"{keyword} 망하는 사람 vs 성공하는 사람",
                f"{keyword} 아무도 안 알려주는 비밀"
            ],
            "훅_아이디어": [
                f"❌ {keyword} 이렇게 하면 망합니다",
                f"🔥 {keyword} 지금 시작 안 하면 후회",
                f"💰 {keyword}로 이렇게 벌었습니다",
                f"😱 {keyword}의 충격적인 진실",
                f"✅ {keyword} 3분 완벽 정리"
            ]
        }
    
    def analyze_title_patterns(self, videos: List[Dict]) -> List[str]:
        """제목 패턴 분석"""
        patterns = [
            "🎯 [숫자] + [주제] + [결과]",
            "💰 [주제] + 수익/금액 공개",
            "⚡ [기간] + [주제] + [성과]",
            "❌ [주제] + 하지마세요/실수",
            "✅ [주제] + 이렇게/방법",
            "🔥 요즘 + [주제] + 트렌드",
            "😱 [주제] + 충격/반전",
            "🎓 [주제] + 초보/입문/가이드"
        ]
        
        return patterns
    
    def get_optimal_posting_times(self) -> Dict:
        """최적 업로드 시간 분석"""
        return {
            "평일": {
                "아침": "07:00-09:00 (출근 시간)",
                "점심": "12:00-13:00 (점심 시간)",
                "저녁": "18:00-20:00 (퇴근 후)",
                "밤": "22:00-24:00 (취침 전)"
            },
            "주말": {
                "아침": "09:00-11:00",
                "오후": "14:00-16:00",
                "저녁": "19:00-22:00"
            },
            "최고_성과_시간대": [
                "🏆 1위: 저녁 6-8시 (퇴근 후 황금시간)",
                "🥈 2위: 점심 12-1시 (점심시간 휴식)",
                "🥉 3위: 밤 10-12시 (취침 전)"
            ]
        }

def main():
    """테스트"""
    analyzer = YouTubeTrendsAnalyzer()
    
    print("🎬 YouTube 급상승 동영상 트렌드 분석")
    print("=" * 80)
    
    # 급상승 동영상
    trending = analyzer.get_trending_videos(10)
    
    print(f"\n📈 급상승 동영상 TOP 10:\n")
    for idx, video in enumerate(trending, 1):
        print(f"{idx}. {video['thumbnail']} {video['title']}")
        print(f"   조회수: {video['views']} | 카테고리: {video['category']}")
        print(f"   키워드: {', '.join(video['keywords'][:3])}")
        print(f"   바이럴 이유: {video['why_viral']}\n")
    
    # 키워드 분석
    print("\n" + "=" * 80)
    print("🔑 키워드 트렌드 분석\n")
    
    keywords_analysis = analyzer.extract_keywords_from_videos(trending)
    
    print("인기 키워드 TOP 10:")
    for kw_data in keywords_analysis["전체_인기_키워드"][:10]:
        print(f"  {kw_data['추천도']} {kw_data['키워드']} (빈도: {kw_data['빈도']})")
    
    print(f"\n트렌드 분석:")
    for cat_data in keywords_analysis["트렌드_분석"]["핫한_카테고리_TOP3"]:
        print(f"  {cat_data['인기도']} {cat_data['카테고리']} ({cat_data['영상수']}개)")

if __name__ == "__main__":
    main()

