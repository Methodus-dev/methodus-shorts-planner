/**
 * Methodus Shorts Planner - 샘플 영상 데이터
 * 백엔드 없이 프론트엔드에서 직접 사용하는 정적 데이터
 */

export interface TrendingVideo {
  title: string;
  views: string;
  category: string;
  language: string;
  video_type: string;
  youtube_url: string;
  thumbnail: string;
  trend_score: number;
  crawled_at: string;
  region?: string;
}

export const SAMPLE_VIDEOS: TrendingVideo[] = [
  {
    title: "7 Side Hustles Students Can Start In 2025",
    views: "6.9M",
    category: "창업/부업",
    language: "영어",
    video_type: "롱폼",
    youtube_url: "https://www.youtube.com/watch?v=2SLSser4y6U",
    thumbnail: "💼",
    trend_score: 95,
    crawled_at: new Date().toISOString(),
    region: "해외"
  },
  {
    title: "부업으로 월 100만원 벌기",
    views: "2.3M",
    category: "창업/부업",
    language: "한국어",
    video_type: "쇼츠",
    youtube_url: "https://www.youtube.com/shorts/abc123",
    thumbnail: "💰",
    trend_score: 88,
    crawled_at: new Date().toISOString(),
    region: "국내"
  },
  {
    title: "AI로 돈 버는 방법 2025",
    views: "1.8M",
    category: "과학기술",
    language: "한국어",
    video_type: "롱폼",
    youtube_url: "https://www.youtube.com/watch?v=def456",
    thumbnail: "🤖",
    trend_score: 92,
    crawled_at: new Date().toISOString(),
    region: "국내"
  },
  {
    title: "주식 투자 초보자 가이드",
    views: "3.2M",
    category: "재테크/금융",
    language: "한국어",
    video_type: "쇼츠",
    youtube_url: "https://www.youtube.com/shorts/ghi789",
    thumbnail: "📈",
    trend_score: 85,
    crawled_at: new Date().toISOString()
  },
  {
    title: "How to Make Money Online in 2025",
    views: "4.1M",
    category: "마케팅/비즈니스",
    language: "영어",
    video_type: "롱폼",
    youtube_url: "https://www.youtube.com/watch?v=jkl012",
    thumbnail: "💻",
    trend_score: 90,
    crawled_at: new Date().toISOString()
  },
  {
    title: "요리 초보도 할 수 있는 간단한 파스타",
    views: "1.5M",
    category: "요리/음식",
    language: "한국어",
    video_type: "쇼츠",
    youtube_url: "https://www.youtube.com/shorts/pasta123",
    thumbnail: "🍝",
    trend_score: 78,
    crawled_at: new Date().toISOString()
  },
  {
    title: "게임으로 돈 버는 방법",
    views: "2.8M",
    category: "게임",
    language: "한국어",
    video_type: "롱폼",
    youtube_url: "https://www.youtube.com/watch?v=game456",
    thumbnail: "🎮",
    trend_score: 82,
    crawled_at: new Date().toISOString()
  },
  {
    title: "10분 홈트레이닝",
    views: "3.5M",
    category: "운동/건강",
    language: "한국어",
    video_type: "쇼츠",
    youtube_url: "https://www.youtube.com/shorts/workout789",
    thumbnail: "💪",
    trend_score: 87,
    crawled_at: new Date().toISOString()
  },
  {
    title: "영어 공부 꿀팁 10가지",
    views: "2.1M",
    category: "교육/학습",
    language: "한국어",
    video_type: "롱폼",
    youtube_url: "https://www.youtube.com/watch?v=study123",
    thumbnail: "📚",
    trend_score: 80,
    crawled_at: new Date().toISOString()
  },
  {
    title: "피아노 치는 법 기초",
    views: "1.9M",
    category: "음악",
    language: "한국어",
    video_type: "쇼츠",
    youtube_url: "https://www.youtube.com/shorts/piano456",
    thumbnail: "🎹",
    trend_score: 75,
    crawled_at: new Date().toISOString()
  },
  {
    title: "부동산 투자 시작하기",
    views: "2.7M",
    category: "재테크/금융",
    language: "한국어",
    video_type: "롱폼",
    youtube_url: "https://www.youtube.com/watch?v=realestate123",
    thumbnail: "🏠",
    trend_score: 83,
    crawled_at: new Date().toISOString()
  },
  {
    title: "암호화폐 투자 가이드",
    views: "1.6M",
    category: "재테크/금융",
    language: "한국어",
    video_type: "쇼츠",
    youtube_url: "https://www.youtube.com/shorts/crypto456",
    thumbnail: "₿",
    trend_score: 79,
    crawled_at: new Date().toISOString()
  },
  {
    title: "ChatGPT 활용법 완벽 가이드",
    views: "3.8M",
    category: "과학기술",
    language: "한국어",
    video_type: "롱폼",
    youtube_url: "https://www.youtube.com/watch?v=chatgpt789",
    thumbnail: "🤖",
    trend_score: 91,
    crawled_at: new Date().toISOString()
  },
  {
    title: "프로그래밍 독학 로드맵",
    views: "2.4M",
    category: "교육/학습",
    language: "한국어",
    video_type: "쇼츠",
    youtube_url: "https://www.youtube.com/shorts/programming123",
    thumbnail: "💻",
    trend_score: 86,
    crawled_at: new Date().toISOString()
  },
  {
    title: "유튜브 채널 성장시키는 법",
    views: "4.2M",
    category: "마케팅/비즈니스",
    language: "한국어",
    video_type: "롱폼",
    youtube_url: "https://www.youtube.com/watch?v=youtube456",
    thumbnail: "📺",
    trend_score: 89,
    crawled_at: new Date().toISOString()
  },
  {
    title: "인스타그램 마케팅 전략",
    views: "1.7M",
    category: "마케팅/비즈니스",
    language: "한국어",
    video_type: "쇼츠",
    youtube_url: "https://www.youtube.com/shorts/instagram789",
    thumbnail: "📱",
    trend_score: 77,
    crawled_at: new Date().toISOString()
  },
  {
    title: "간단한 케이크 만들기",
    views: "2.9M",
    category: "요리/음식",
    language: "한국어",
    video_type: "롱폼",
    youtube_url: "https://www.youtube.com/watch?v=cake123",
    thumbnail: "🍰",
    trend_score: 84,
    crawled_at: new Date().toISOString()
  },
  {
    title: "롤 티어 올리는 꿀팁",
    views: "3.1M",
    category: "게임",
    language: "한국어",
    video_type: "쇼츠",
    youtube_url: "https://www.youtube.com/shorts/lol456",
    thumbnail: "🎮",
    trend_score: 81,
    crawled_at: new Date().toISOString()
  },
  {
    title: "헬스장에서 혼자 운동하기",
    views: "2.6M",
    category: "운동/건강",
    language: "한국어",
    video_type: "롱폼",
    youtube_url: "https://www.youtube.com/watch?v=gym789",
    thumbnail: "🏋️",
    trend_score: 88,
    crawled_at: new Date().toISOString()
  },
  {
    title: "일본어 기초 회화",
    views: "1.8M",
    category: "교육/학습",
    language: "한국어",
    video_type: "쇼츠",
    youtube_url: "https://www.youtube.com/shorts/japanese123",
    thumbnail: "🇯🇵",
    trend_score: 76,
    crawled_at: new Date().toISOString()
  },
  {
    title: "기타 치는 법 초보자용",
    views: "2.2M",
    category: "음악",
    language: "한국어",
    video_type: "롱폼",
    youtube_url: "https://www.youtube.com/watch?v=guitar456",
    thumbnail: "🎸",
    trend_score: 82,
    crawled_at: new Date().toISOString()
  },
  {
    title: "온라인 쇼핑몰 창업하기",
    views: "3.3M",
    category: "창업/부업",
    language: "한국어",
    video_type: "롱폼",
    youtube_url: "https://www.youtube.com/watch?v=shop789",
    thumbnail: "🛒",
    trend_score: 87,
    crawled_at: new Date().toISOString()
  },
  {
    title: "드롭쉬핑으로 돈 벌기",
    views: "2.0M",
    category: "창업/부업",
    language: "한국어",
    video_type: "쇼츠",
    youtube_url: "https://www.youtube.com/shorts/dropship123",
    thumbnail: "📦",
    trend_score: 80,
    crawled_at: new Date().toISOString()
  },
  {
    title: "자기계발 책 추천 10선",
    views: "1.9M",
    category: "자기계발",
    language: "한국어",
    video_type: "롱폼",
    youtube_url: "https://www.youtube.com/watch?v=books456",
    thumbnail: "📖",
    trend_score: 85,
    crawled_at: new Date().toISOString()
  },
  {
    title: "아침 루틴 만들기",
    views: "2.5M",
    category: "자기계발",
    language: "한국어",
    video_type: "쇼츠",
    youtube_url: "https://www.youtube.com/shorts/morning789",
    thumbnail: "🌅",
    trend_score: 83,
    crawled_at: new Date().toISOString()
  },
  {
    title: "시간 관리의 달인되기",
    views: "3.6M",
    category: "자기계발",
    language: "한국어",
    video_type: "롱폼",
    youtube_url: "https://www.youtube.com/watch?v=time123",
    thumbnail: "⏰",
    trend_score: 90,
    crawled_at: new Date().toISOString()
  },
  {
    title: "명상으로 스트레스 해소하기",
    views: "1.4M",
    category: "자기계발",
    language: "한국어",
    video_type: "쇼츠",
    youtube_url: "https://www.youtube.com/shorts/meditation456",
    thumbnail: "🧘",
    trend_score: 74,
    crawled_at: new Date().toISOString()
  },
  {
    title: "목표 설정하고 달성하는 법",
    views: "2.8M",
    category: "자기계발",
    language: "한국어",
    video_type: "롱폼",
    youtube_url: "https://www.youtube.com/watch?v=goals789",
    thumbnail: "🎯",
    trend_score: 86,
    crawled_at: new Date().toISOString()
  },
  {
    title: "습관 만들기의 과학",
    views: "1.6M",
    category: "자기계발",
    language: "한국어",
    video_type: "쇼츠",
    youtube_url: "https://www.youtube.com/shorts/habits123",
    thumbnail: "🔄",
    trend_score: 78,
    crawled_at: new Date().toISOString()
  },
  {
    title: "성공하는 사람들의 특징",
    views: "4.0M",
    category: "자기계발",
    language: "한국어",
    video_type: "롱폼",
    youtube_url: "https://www.youtube.com/watch?v=success456",
    thumbnail: "🏆",
    trend_score: 92,
    crawled_at: new Date().toISOString()
  },
  {
    title: "긍정적 사고방식 기르기",
    views: "1.7M",
    category: "자기계발",
    language: "한국어",
    video_type: "쇼츠",
    youtube_url: "https://www.youtube.com/shorts/positive789",
    thumbnail: "😊",
    trend_score: 79,
    crawled_at: new Date().toISOString()
  }
];

export const FILTER_OPTIONS = {
  categories: [
    "창업/부업", "재테크/금융", "과학기술", "자기계발", "마케팅/비즈니스",
    "요리/음식", "게임", "운동/건강", "교육/학습", "음악"
  ],
  regions: ["국내", "해외"],
  languages: ["한국어", "영어"],
  sort_options: [
    { value: "trend_score", label: "트렌드 점수" },
    { value: "views", label: "조회수" },
    { value: "crawled_at", label: "최신순" }
  ],
  trend_score_range: {
    min: 1,
    max: 100,
    default: 50
  }
};
