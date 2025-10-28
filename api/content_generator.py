import json
import random
from typing import Dict, List, Optional
from pathlib import Path

class ContentGenerator:
    def __init__(self):
        self.templates = self.load_templates()
        self.knowledge_base = self.load_knowledge_base()
    
    def load_templates(self) -> Dict:
        """Load templates from JSON"""
        templates_path = Path("../data/templates.json")
        if templates_path.exists():
            with open(templates_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
    
    def load_knowledge_base(self) -> Dict:
        """Load knowledge base from JSON"""
        kb_path = Path("../data/knowledge_base.json")
        if kb_path.exists():
            with open(kb_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
    
    def generate_content(
        self, 
        topic: str, 
        structure: str = "Trailer-Meat-Summary-CTC",
        content_type: str = "Actionable",
        target_audience: Optional[str] = None,
        tone: str = "professional"
    ) -> Dict:
        """Generate LinkedIn content based on topic and structure"""
        
        # Select generation method based on structure
        if structure == "Trailer-Meat-Summary-CTC":
            content = self.generate_trailer_meat_summary(topic, content_type, target_audience, tone)
        elif structure == "Story-Based":
            content = self.generate_story_based(topic, target_audience, tone)
        elif structure == "Listicle":
            content = self.generate_listicle(topic, target_audience, tone)
        else:
            content = self.generate_trailer_meat_summary(topic, content_type, target_audience, tone)
        
        # Add hashtags
        hashtags = self.select_hashtags(topic)
        
        return {
            "content": content,
            "hashtags": hashtags,
            "structure": structure,
            "content_type": content_type,
            "topic": topic,
            "character_count": len(content),
            "word_count": len(content.split())
        }
    
    def generate_trailer_meat_summary(
        self, 
        topic: str, 
        content_type: str,
        target_audience: Optional[str],
        tone: str
    ) -> str:
        """Generate content using Trailer-Meat-Summary-CTC structure"""
        
        # Trailer (Hook)
        hooks = [
            f"{topic}에 대한 진실을 아무도 말하지 않습니다...",
            f"나는 {topic}을 수년간 배웠습니다.\n\n첫날부터 알았더라면 좋았을 것들:",
            f"대부분의 사람들이 {topic}을 완전히 잘못 이해하고 있습니다.\n\n이유는:",
            f"{topic}의 비밀은?\n\n생각보다 간단합니다.",
            f"{topic}에 대해 모든 것을 바꾼 3가지:",
            f"모든 사람이 {topic}을 하라고 말합니다.\n\n하지만 가장 중요한 부분을 빼먹습니다:",
        ]
        
        trailer = random.choice(hooks)
        
        # Meat (Main Content)
        if content_type == "Actionable":
            meat_intro = f"\n{topic}을 마스터하는 방법:\n\n"
            points = [
                f"1. 기본부터 시작하세요\n   기초를 이해하는 것이 중요합니다. 이 단계를 건너뛰지 마세요.",
                f"2. 꾸준히 연습하세요\n   가끔의 완벽함보다 매일의 행동이 낫습니다. 습관으로 만드세요.",
                f"3. 피드백에서 배우세요\n   모든 실수는 교훈입니다. 학습 과정을 받아들이세요.",
                f"4. 시스템을 구축하세요\n   당신에게 맞는 프레임워크를 만드세요. 반복 가능하게 만드세요.",
                f"5. 여정을 공유하세요\n   다른 사람을 가르치는 것이 자신의 학습을 강화합니다."
            ]
        elif content_type == "Motivational":
            meat_intro = f"\n{topic}을 시작할 때, 저는 고생했습니다.\n\n"
            points = [
                "매일 자신을 의심했습니다.",
                "사람들은 불가능하다고 말했습니다.",
                "하지만 저는 계속했습니다.",
                "\n그러다가 뭔가 바뀌었습니다:",
                "성공은 꾸준히 나타나는 것에서 온다는 것을 깨달았습니다.",
                "\n이제 저는 다른 사람들도 그렇게 할 수 있도록 도와줍니다."
            ]
        elif content_type == "Contrarian":
            meat_intro = f"\n일반적인 {topic} 조언의 문제점:\n\n"
            points = [
                "❌ 모두 말합니다: '더 열심히 일하세요'\n   현실: 똑똑한 일 > 열심히 일하기",
                "❌ 모두 말합니다: '10년이 필요합니다'\n   현실: 올바른 전략이 필요합니다",
                "❌ 모두 말합니다: '군중을 따라가세요'\n   현실: 혁신은 다르게 생각하는 것에서 옵니다"
            ]
        else:  # Analytical
            meat_intro = f"\n{topic}을 분석해보겠습니다:\n\n"
            points = [
                "📊 첫째: 핵심 원리를 이해하세요\n   이것 없이는 다른 모든 것이 실패합니다.",
                "🎯 둘째: 당신의 특정 상황에 적용하세요\n   한 가지 방법이 모든 것에 맞지는 않습니다.",
                "🚀 셋째: 반복하고 개선하세요\n   완벽함은 목적지가 아닌 과정입니다."
            ]
        
        meat = meat_intro + "\n".join(random.sample(points, min(3, len(points))))
        
        # Summary
        summaries = [
            f"\n\n기억하세요:\n\n{topic}은 완벽함이 아닌 일관성에 관한 것입니다.\n\n작게 시작하세요. 집중하세요. 계속 개선하세요.",
            f"\n\n핵심은?\n\n{topic}은 복잡하지 않습니다.\n\n시작하고 계속하기만 하면 됩니다.",
            f"\n\n핵심 포인트:\n\n완벽함이 아닌 진전에 집중하여 {topic}을 마스터하세요.",
        ]
        
        summary = random.choice(summaries)
        
        # CTC (Call-to-Action)
        ctcs = [
            "\n\n이것에 대한 당신의 가장 큰 도전은 무엇인가요?\n\n댓글로 알려주세요. 👇",
            "\n\n이런 인사이트가 더 필요하신가요?\n\n성장과 성공에 대한 일일 콘텐츠를 위해 팔로우하세요.",
            "\n\n이 목록에 무엇을 추가하시겠어요?\n\n아래에 알려주세요. 💭",
            "\n\n어떤 팁이 가장 공감되시나요?\n\n생각을 공유해주세요. 👇",
        ]
        
        ctc = random.choice(ctcs)
        
        # Add audience customization if provided
        audience_note = ""
        if target_audience:
            audience_note = f"\n\n[{target_audience}를 위한]"
        
        return trailer + meat + summary + ctc + audience_note
    
    def generate_story_based(self, topic: str, target_audience: Optional[str], tone: str) -> str:
        """Generate story-based content"""
        
        story_template = f"""{topic}에 대해 어려운 방법으로 배웠습니다.

3년 전, 저는 고생하고 있었습니다.
어디서 시작해야 할지 몰랐습니다.
모든 사람들이 해결책을 찾은 것 같았지만 저만 그렇지 않았습니다.

그러다가 하나의 간단한 진실을 발견했습니다:

{topic}은 완벽한 것이 아닙니다.
지속적인 것입니다.

저에게 바뀐 것들:

→ "적절한 시간"을 기다리는 것을 멈췄습니다
→ 불완전한 행동을 시작했습니다
→ 모든 실수에서 배웠습니다
→ 천천히 하지만 확실하게 모멘텀을 구축했습니다

지금? 저는 정확히 원했던 곳에 있습니다.

교훈은?

준비되기 전에 시작하세요.
가면서 배우세요.
과정을 신뢰하세요.

무엇이 당신을 시작하지 못하게 막고 있나요?"""

        return story_template
    
    def generate_listicle(self, topic: str, target_audience: Optional[str], tone: str) -> str:
        """Generate listicle content"""
        
        numbers = [5, 7, 10]
        num = random.choice(numbers)
        
        listicle_template = f"""{topic}을 시작할 때 알았더라면 좋았을 {num}가지:

1. 생각보다 간단합니다
   너무 복잡하게 만들지 마세요.

2. 완벽함보다 일관성이 낫습니다
   힘들어도 매일 나타나세요.

3. 경쟁자들이 생각만큼 좋지 않습니다
   대부분의 사람들이 너무 일찍 포기합니다.

4. 기본기가 성공의 90%입니다
   먼저 기초를 마스터하세요.

5. 공부가 아닌 행동으로 배웁니다
   행동이 명확함을 만듭니다.

{"6. 커뮤니티가 성장을 가속화합니다" if num >= 6 else ""}
{"   올바른 사람들과 어울리세요." if num >= 6 else ""}

{"7. 인내심이 당신의 슈퍼파워입니다" if num >= 7 else ""}
{"   결과는 시간이 걸립니다. 과정을 신뢰하세요." if num >= 7 else ""}

{"8. 단순함이 확장됩니다" if num >= 8 else ""}
{"   더 빠르게 성장하려면 단순하게 유지하세요." if num >= 8 else ""}

{"9. 여정을 기록하세요" if num >= 9 else ""}
{"   당신의 스토리가 당신만의 독특한 장점입니다." if num >= 9 else ""}

{"10. 지금 시작하고 나중에 최적화하세요" if num >= 10 else ""}
{"    완벽함보다 완성된 것이 낫습니다." if num >= 10 else ""}

어떤 것이 가장 공감되시나요? 👇"""

        return listicle_template
    
    def select_hashtags(self, topic: str, count: int = 5) -> List[str]:
        """Select relevant hashtags based on topic"""
        
        all_hashtags = self.templates.get('hashtags', [])
        
        # Topic-based hashtag mapping
        topic_keywords = {
            'business': ['#Entrepreneurship', '#Business', '#Success'],
            'marketing': ['#Marketing', '#DigitalMarketing', '#Branding'],
            'startup': ['#Startup', '#Innovation', '#VentureCapital'],
            'career': ['#Careers', '#PersonalDevelopment', '#Success'],
            'content': ['#ContentCreation', '#Socialmedia', '#Writing'],
            'sales': ['#Sales', '#Business', '#Marketing'],
            'leadership': ['#Leadership', '#Management', '#Success'],
            'productivity': ['#Productivity', '#PersonalDevelopment', '#Success'],
        }
        
        # Find matching hashtags
        selected = []
        topic_lower = topic.lower()
        
        for key, tags in topic_keywords.items():
            if key in topic_lower:
                selected.extend(tags)
        
        # Add general hashtags
        general = ['#LinkedIn', '#Success', '#Growth', '#Business', '#Motivation']
        selected.extend(random.sample(general, 2))
        
        # Remove duplicates and limit count
        selected = list(dict.fromkeys(selected))[:count]
        
        return selected if selected else ['#성장', '#성공', '#마케팅', '#창업', '#개발']
    
    def get_available_structures(self) -> List[str]:
        """Get list of available content structures"""
        return [
            "Trailer-Meat-Summary-CTC",
            "Story-Based",
            "Listicle"
        ]
    
    def get_available_content_types(self) -> List[str]:
        """Get list of available content types"""
        structures = self.templates.get('content_matrix', {}).get('structures', [])
        return [s['name'] for s in structures] if structures else [
            "Actionable",
            "Motivational",
            "Analytical",
            "Contrarian",
            "Observation"
        ]
    
    def get_available_topics(self) -> List[str]:
        """Get list of suggested topics"""
        return [
            "마케팅",
            "창업",
            "개발",
            "투자",
            "부업",
            "성장",
            "리더십",
            "네트워킹",
            "브랜딩",
            "영업",
            "디자인",
            "데이터 분석",
            "인공지능",
            "블록체인",
            "금융",
            "부동산",
            "교육",
            "헬스케어",
            "E-커머스",
            "소셜미디어"
        ]

if __name__ == "__main__":
    # Test the generator
    generator = ContentGenerator()
    
    test_topics = ["LinkedIn growth", "Content creation", "Personal branding"]
    
    for topic in test_topics:
        print(f"\n{'='*60}")
        print(f"Topic: {topic}")
        print(f"{'='*60}")
        
        result = generator.generate_content(
            topic=topic,
            structure="Trailer-Meat-Summary-CTC",
            content_type="Actionable"
        )
        
        print(result['content'])
        print(f"\nHashtags: {' '.join(result['hashtags'])}")
        print(f"Words: {result['word_count']} | Chars: {result['character_count']}")

