// Mock 데이터 - 백엔드 없이도 프론트엔드 테스트 가능
export const mockTrendingVideos = [
  {
    title: "💡 5분 만에 마케팅 고수 되는 법",
    category: "마케팅/비즈니스",
    views: "2.3M",
    engagement: "15.2%",
    keywords: ["마케팅", "비즈니스", "성장", "전략"],
    thumbnail: "📈",
    why_viral: "실용적인 팁과 간결한 설명",
    video_id: "mock_001",
    youtube_url: "#",
    shorts_url: "#",
    crawled_at: new Date().toISOString(),
    region: "국내",
    language: "한국어",
    trend_score: 95,
    is_shorts: true,
    video_type: "쇼츠"
  },
  {
    title: "🚀 창업 3년차가 말하는 진실",
    category: "창업/부업",
    views: "1.8M",
    engagement: "18.7%",
    keywords: ["창업", "부업", "성공", "경험"],
    thumbnail: "💼",
    why_viral: "솔직한 경험담과 조언",
    video_id: "mock_002",
    youtube_url: "#",
    shorts_url: "#",
    crawled_at: new Date().toISOString(),
    region: "국내",
    language: "한국어",
    trend_score: 92,
    is_shorts: true,
    video_type: "쇼츠"
  },
  {
    title: "💰 주식 초보도 이해하는 투자법",
    category: "재테크/금융",
    views: "3.1M",
    engagement: "12.4%",
    keywords: ["주식", "투자", "재테크", "초보"],
    thumbnail: "📊",
    why_viral: "복잡한 내용을 쉽게 설명",
    video_id: "mock_003",
    youtube_url: "#",
    shorts_url: "#",
    crawled_at: new Date().toISOString(),
    region: "국내",
    language: "한국어",
    trend_score: 88,
    is_shorts: true,
    video_type: "쇼츠"
  },
  {
    title: "🎯 목표 달성하는 사람들의 공통점",
    category: "자기계발",
    views: "1.5M",
    engagement: "20.1%",
    keywords: ["목표", "성공", "습관", "자기계발"],
    thumbnail: "🎯",
    why_viral: "실행 가능한 조언과 동기부여",
    video_id: "mock_004",
    youtube_url: "#",
    shorts_url: "#",
    crawled_at: new Date().toISOString(),
    region: "국내",
    language: "한국어",
    trend_score: 85,
    is_shorts: true,
    video_type: "쇼츠"
  },
  {
    title: "🔥 요리 초보도 만드는 간단 레시피",
    category: "요리/음식",
    views: "2.7M",
    engagement: "14.3%",
    keywords: ["요리", "레시피", "간단", "초보"],
    thumbnail: "🍳",
    why_viral: "실용적이고 따라하기 쉬운 내용",
    video_id: "mock_005",
    youtube_url: "#",
    shorts_url: "#",
    crawled_at: new Date().toISOString(),
    region: "국내",
    language: "한국어",
    trend_score: 82,
    is_shorts: true
  },
  {
    title: "💻 개발자 되고 싶다면 이것부터",
    category: "과학기술",
    views: "1.2M",
    engagement: "16.8%",
    keywords: ["개발", "프로그래밍", "코딩", "기술"],
    thumbnail: "💻",
    why_viral: "명확한 로드맵과 실용적 조언",
    video_id: "mock_006",
    youtube_url: "#",
    shorts_url: "#",
    crawled_at: new Date().toISOString(),
    region: "국내",
    language: "한국어",
    trend_score: 79,
    is_shorts: true,
    video_type: "쇼츠"
  },
  {
    title: "📚 마케팅의 모든 것 - 완전 정복 가이드",
    category: "마케팅/비즈니스",
    views: "850K",
    engagement: "8.5%",
    keywords: ["마케팅", "가이드", "교육", "완전정복"],
    thumbnail: "📖",
    why_viral: "체계적이고 상세한 교육 콘텐츠",
    video_id: "mock_006",
    youtube_url: "#",
    shorts_url: "#",
    crawled_at: new Date().toISOString(),
    region: "국내",
    language: "한국어",
    trend_score: 75,
    is_shorts: false,
    video_type: "롱폼"
  },
  {
    title: "🎬 창업 성공 스토리 - 3년간의 여정",
    category: "창업/부업",
    views: "1.2M",
    engagement: "12.3%",
    keywords: ["창업", "성공", "스토리", "여정"],
    thumbnail: "🎭",
    why_viral: "감동적인 성공 스토리와 솔직한 경험담",
    video_id: "mock_007",
    youtube_url: "#",
    shorts_url: "#",
    crawled_at: new Date().toISOString(),
    region: "국내",
    language: "한국어",
    trend_score: 82,
    is_shorts: false,
    video_type: "롱폼"
  },
  {
    title: "💰 투자 마스터 클래스 - 초보부터 전문가까지",
    category: "재테크/금융",
    views: "950K",
    engagement: "9.8%",
    keywords: ["투자", "마스터", "클래스", "전문가"],
    thumbnail: "🎓",
    why_viral: "전문적이고 깊이 있는 투자 교육",
    video_id: "mock_008",
    youtube_url: "#",
    shorts_url: "#",
    crawled_at: new Date().toISOString(),
    region: "국내",
    language: "한국어",
    trend_score: 78,
    is_shorts: false,
    video_type: "롱폼"
  }
];

export const mockKeywordAnalysis = {
  전체_인기_키워드: [
    { 키워드: "마케팅", 추천도: "매우높음", 빈도: 15 },
    { 키워드: "창업", 추천도: "높음", 빈도: 12 },
    { 키워드: "투자", 추천도: "높음", 빈도: 10 },
    { 키워드: "성공", 추천도: "높음", 빈도: 9 },
    { 키워드: "자기계발", 추천도: "보통", 빈도: 8 },
    { 키워드: "부업", 추천도: "보통", 빈도: 7 },
    { 키워드: "목표", 추천도: "보통", 빈도: 6 },
    { 키워드: "습관", 추천도: "보통", 빈도: 5 }
  ],
  카테고리별_키워드: {
    "마케팅/비즈니스": ["마케팅", "비즈니스", "성장", "전략", "브랜딩"],
    "창업/부업": ["창업", "부업", "성공", "경험", "아이디어"],
    "재테크/금융": ["투자", "주식", "재테크", "금융", "자산"],
    "자기계발": ["성공", "목표", "습관", "동기부여", "성장"]
  },
  트렌드_분석: {
    핫한_카테고리_TOP3: [
      { 카테고리: "마케팅/비즈니스", 영상수: 25, 인기도: "🔥🔥🔥" },
      { 카테고리: "창업/부업", 영상수: 20, 인기도: "🔥🔥" },
      { 카테고리: "재테크/금융", 영상수: 18, 인기도: "🔥" }
    ],
    공통_요소: ["실용적 팁", "간결한 설명", "감정적 연결", "공유 유도"]
  }
};

export const mockContentIdeas = {
  관련_급상승_영상수: 15,
  추천_제목_패턴: [
    "이것만 알면 {키워드} 마스터",
    "{키워드} 전문가가 알려주는 비밀",
    "초보도 이해하는 {키워드} 가이드"
  ],
  훅_아이디어: [
    "놀라운 사실: {키워드}의 진실",
    "이것 때문에 {키워드}가 실패한다",
    "{키워드}로 월 100만원 벌기"
  ],
  콘텐츠_아이디어: [
    "💡 {키워드} 초보자를 위한 완벽 가이드",
    "🚀 {키워드}로 성공한 사람들의 비밀",
    "💰 {키워드} 실전 노하우 5가지",
    "🎯 {키워드} 목표 달성하는 방법",
    "🔥 {키워드}로 인생 바꾸기"
  ]
};
