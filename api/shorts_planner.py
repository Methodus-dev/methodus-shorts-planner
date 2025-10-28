"""
쇼츠 콘텐츠 기획 시스템
크리에이터가 조회수 높은 쇼츠 콘텐츠를 기획하도록 돕는 AI 어시스턴트
"""
import json
import random
from pathlib import Path
from typing import Dict, List, Optional

class ShortsPlannerSystem:
    def __init__(self):
        self.system_data = self.load_system_data()
    
    def load_system_data(self) -> Dict:
        """쇼츠 시스템 데이터 로드"""
        data_path = Path("../data/shorts_system.json")
        if data_path.exists():
            with open(data_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
    
    def analyze_niche(self, topic: str, target_audience: str = "") -> Dict:
        """니치 분석 및 세분화 제안"""
        niche_strategy = self.system_data.get("니치_전략", {})
        
        analysis = {
            "주제": topic,
            "타겟_청중": target_audience,
            "니치_세분화_제안": [],
            "차별화_전략": []
        }
        
        # 니치 세분화 방법 제안
        segmentation_methods = niche_strategy.get("니치_세분화_방법", [])
        for method in segmentation_methods:
            analysis["니치_세분화_제안"].append({
                "방법": method.get("카테고리", ""),
                "적용_예시": f"{topic}를 {method.get('예시', '')}으로 세분화"
            })
        
        # 차별화 전략
        analysis["차별화_전략"] = [
            f"💎 {topic}의 프리미엄/고급 버전 공략",
            f"🎯 특정 연령대/성별에 특화",
            f"📍 지역 특화 (예: 서울, 부산 등)",
            f"💰 가격대별 세분화",
            f"🎨 스타일/취향별 세분화"
        ]
        
        return analysis
    
    def build_story_structure(self, user_story: Optional[Dict] = None) -> Dict:
        """스토리 구조 빌드"""
        story_builder = self.system_data.get("스토리_빌더", {})
        elements = story_builder.get("스토리_요소", [])
        
        structure = {
            "스토리_프레임워크": {},
            "쇼츠_스토리_팁": [
                "📱 15초 안에 문제 제시",
                "💡 30초 안에 해결책 제시",
                "🎬 마지막 5초에 강력한 CTA",
                "😊 감정 변화를 명확하게",
                "🎵 음악으로 분위기 극대화"
            ]
        }
        
        # 스토리 요소별 가이드
        for element in elements:
            element_name = element.get("요소", "")
            label = element.get("라벨", "")
            
            structure["스토리_프레임워크"][element_name] = {
                "질문": label,
                "쇼츠_적용": self.get_story_element_tips(element_name),
                "사용자_입력": user_story.get(element_name, "") if user_story else ""
            }
        
        return structure
    
    def get_story_element_tips(self, element: str) -> str:
        """스토리 요소별 쇼츠 적용 팁"""
        tips = {
            "문제_또는_도전": "첫 화면에 큰 글씨로 문제 제시 → 시청자 공감 유도",
            "내적_갈등": "표정과 몸짓으로 감정 표현 → 음악 활용",
            "외적_갈등": "실제 상황 재연 또는 비포/애프터 비교",
            "변화_이벤트": "극적인 전환점 - 화면 전환 효과 사용",
            "영감_순간": "깨달음의 순간 - 밝은 조명/음악 전환",
            "가이드_멘토": "조언자 등장 - 자막으로 핵심 메시지"
        }
        return tips.get(element, "스토리 흐름에 자연스럽게 녹이기")
    
    def suggest_content_structure(self, topic: str, content_type: str) -> Dict:
        """콘텐츠 구조 제안"""
        content_matrix = self.system_data.get("콘텐츠_매트릭스", {})
        structures = content_matrix.get("콘텐츠_구조", [])
        
        # 선택된 콘텐츠 타입 찾기
        selected_structure = None
        for structure in structures:
            if structure.get("타입") == content_type:
                selected_structure = structure
                break
        
        if not selected_structure:
            selected_structure = structures[0] if structures else {}
        
        shorts_tips = selected_structure.get("쇼츠_적용법", {})
        
        suggestion = {
            "주제": topic,
            "콘텐츠_타입": content_type,
            "설명": selected_structure.get("설명", ""),
            "쇼츠_스크립트_구조": {
                "훅_3초": {
                    "목적": "시청자를 즉시 붙잡기",
                    "템플릿": shorts_tips.get("훅", ""),
                    "예시": f"{topic}에 대한 {shorts_tips.get('훅', '')}"
                },
                "본론_30초": {
                    "목적": "핵심 가치 전달",
                    "템플릿": shorts_tips.get("구조", ""),
                    "시각화": shorts_tips.get("시각화", "")
                },
                "마무리_5초": {
                    "목적": "행동 유도",
                    "템플릿": shorts_tips.get("마무리", ""),
                    "CTA_예시": [
                        "❤️ 좋아요 누르고 저장하세요!",
                        "👉 팔로우하면 더 많은 꿀팁!",
                        "💬 댓글로 의견 알려주세요!",
                        "🔔 알림 설정 필수!",
                        "📤 친구에게 공유하세요!"
                    ]
                }
            },
            "편집_포인트": [
                "✂️ 2-3초마다 컷 전환",
                "📝 모든 대사에 자막",
                "🎵 트렌드 음악 사용",
                "🎨 밝고 선명한 색감",
                "👁️ 아이캐치 요소 추가"
            ]
        }
        
        return suggestion
    
    def generate_hooks(self, topic: str, count: int = 5) -> List[str]:
        """훅(Hook) 아이디어 생성"""
        script_structure = self.system_data.get("스크립트_구조", {})
        hook_templates = script_structure.get("쇼츠_훅_템플릿", [])
        
        hooks = []
        
        # 템플릿 기반 훅 생성
        hook_ideas = [
            f"❌ {topic} 이렇게 하면 망합니다",
            f"✅ {topic} 제대로 하는 법 3가지",
            f"🤔 {topic} 궁금하지 않으세요?",
            f"⚠️ {topic} 이거 모르면 큰일",
            f"💰 {topic}로 돈 버는 비밀",
            f"🔥 지금 {topic} 핫한 이유",
            f"😱 {topic}의 충격적인 진실",
            f"🎯 {topic} 단 3가지만 기억하세요",
            f"⏰ 시간 없으면 {topic} 이것만",
            f"🚀 {topic} 10배 빠르게 하는 법"
        ]
        
        # 랜덤 선택
        selected_hooks = random.sample(hook_ideas, min(count, len(hook_ideas)))
        
        return selected_hooks
    
    def suggest_hashtags(self, topic: str, category: str = "") -> Dict:
        """해시태그 제안"""
        hashtag_strategy = self.system_data.get("해시태그_전략", {})
        shorts_hashtags = hashtag_strategy.get("쇼츠_해시태그", {})
        
        suggestion = {
            "필수_태그": shorts_hashtags.get("필수_태그", []),
            "주제_태그": [
                f"#{topic}",
                f"#{topic}꿀팁",
                f"#{topic}추천",
                f"#{topic}정보"
            ],
            "카테고리_태그": [],
            "사용법": {
                "개수": "3-5개 권장",
                "위치": "제목 또는 첫 댓글",
                "조합": "필수태그 2개 + 주제태그 2개 + 카테고리태그 1개"
            }
        }
        
        # 카테고리별 태그
        if category:
            category_tags = shorts_hashtags.get("카테고리별_태그", {})
            suggestion["카테고리_태그"] = category_tags.get(category, [])[:5]
        
        return suggestion
    
    def create_content_plan(
        self,
        topic: str,
        content_type: str,
        target_audience: str = "",
        user_story: Optional[Dict] = None
    ) -> Dict:
        """통합 콘텐츠 기획서 생성"""
        
        # 1. 니치 분석
        niche_analysis = self.analyze_niche(topic, target_audience)
        
        # 2. 스토리 구조
        story_structure = self.build_story_structure(user_story)
        
        # 3. 콘텐츠 구조
        content_structure = self.suggest_content_structure(topic, content_type)
        
        # 4. 훅 아이디어
        hooks = self.generate_hooks(topic)
        
        # 5. 해시태그
        hashtags = self.suggest_hashtags(topic)
        
        # 6. 최적화 체크리스트
        optimization = self.system_data.get("쇼츠_최적화", {})
        
        # 통합 기획서
        plan = {
            "제목": f"{topic} 쇼츠 콘텐츠 기획서",
            "생성_일시": "",  # 실제 사용 시 timestamp 추가
            "타겟": target_audience,
            "콘텐츠_타입": content_type,
            
            "1_니치_전략": niche_analysis,
            "2_스토리_구조": story_structure,
            "3_콘텐츠_구조": content_structure,
            "4_훅_아이디어": hooks,
            "5_해시태그_전략": hashtags,
            "6_최적화_체크리스트": optimization.get("조회수_최적화_체크리스트", []),
            "7_바이럴_요소": optimization.get("바이럴_요소", []),
            "8_플랫폼별_전략": optimization.get("플랫폼별_전략", {}),
            
            "추가_팁": {
                "제작_전": [
                    "📊 경쟁 콘텐츠 10개 이상 분석",
                    "🎯 명확한 타겟 페르소나 설정",
                    "📝 스크립트 3번 이상 수정",
                    "🎬 촬영 전 리허설 필수"
                ],
                "촬영_시": [
                    "📱 세로 모드 (9:16 비율)",
                    "☀️ 밝은 조명 확보",
                    "🎤 명확한 음성",
                    "😊 에너지 넘치는 표정"
                ],
                "편집_시": [
                    "✂️ 불필요한 부분 과감히 제거",
                    "📝 자막은 크고 읽기 쉽게",
                    "🎵 트렌딩 음악 활용",
                    "🎨 일관된 색감/필터"
                ],
                "업로드_후": [
                    "💬 첫 30분 댓글 적극 응답",
                    "📤 다른 플랫폼에 교차 업로드",
                    "📊 성과 분석 및 개선",
                    "🔄 성공 패턴 반복"
                ]
            }
        }
        
        return plan
    
    def get_trending_topics(self) -> List[Dict]:
        """트렌딩 주제 제안 (추후 API 연동 가능)"""
        trending = [
            {"주제": "AI 활용법", "이유": "ChatGPT 열풍", "난이도": "중"},
            {"주제": "부업 아이디어", "이유": "경제 불황", "난이도": "하"},
            {"주제": "생산성 툴", "이유": "재택근무 증가", "난이도": "중"},
            {"주제": "투자 전략", "이유": "재테크 관심", "난이도": "상"},
            {"주제": "자기계발", "이유": "연중 인기", "난이도": "하"},
            {"주제": "건강 루틴", "이유": "웰빙 트렌드", "난이도": "하"},
            {"주제": "마케팅 팁", "이유": "1인 기업 증가", "난이도": "중"},
            {"주제": "부동산 정보", "이유": "주거 관심", "난이도": "상"}
        ]
        
        return random.sample(trending, 5)

def main():
    """테스트 실행"""
    planner = ShortsPlannerSystem()
    
    # 테스트: 콘텐츠 기획서 생성
    plan = planner.create_content_plan(
        topic="부동산 투자",
        content_type="Actionable",
        target_audience="30-40대 첫 투자자"
    )
    
    print("🎬 쇼츠 콘텐츠 기획서 생성 완료!")
    print(f"주제: {plan['제목']}")
    print(f"타겟: {plan['타겟']}")
    print(f"\n훅 아이디어 {len(plan['4_훅_아이디어'])}개:")
    for hook in plan['4_훅_아이디어']:
        print(f"  • {hook}")

if __name__ == "__main__":
    main()

