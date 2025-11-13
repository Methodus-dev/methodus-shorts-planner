// 개발/프로덕션 환경에 따라 API URL 설정
const API_BASE_URL = import.meta.env.VITE_API_URL 
  ? import.meta.env.VITE_API_URL
  : (import.meta.env.PROD 
      ? 'https://methodus-backend.onrender.com'  // Production: Render 배포 서버
      : 'http://localhost:8000');  // Development: 로컬 서버 (포트 8000)

// 실제 크롤링 데이터만 사용

export interface ContentPlanRequest {
  topic: string;
  content_type: string;
  target_audience?: string;
  user_story?: Record<string, string>;
}

export interface ContentPlan {
  제목: string;
  생성_일시: string;
  타겟: string;
  콘텐츠_타입: string;
  '1_니치_전략': any;
  '2_스토리_구조': any;
  '3_콘텐츠_구조': any;
  '4_훅_아이디어': string[];
  '5_해시태그_전략': any;
  '6_최적화_체크리스트': string[];
  '7_바이럴_요소': string[];
  '8_플랫폼별_전략': any;
  추가_팁: any;
}

export interface ContentType {
  value: string;
  label: string;
  description: string;
  best_for: string;
}

export interface TrendingTopic {
  주제: string;
  이유: string;
  난이도: string;
}

// 콘텐츠 기획서 생성
export async function createContentPlan(data: ContentPlanRequest): Promise<ContentPlan> {
  try {
    const response = await fetch(`${API_BASE_URL}/create-plan`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    });
    
    if (!response.ok) {
      throw new Error('기획서 생성에 실패했습니다');
    }
    
    const result = await response.json();
    return result.plan;
  } catch (error) {
    console.error('기획서 생성 API 호출 실패:', error);
    throw new Error('기획서 생성에 실패했습니다. 잠시 후 다시 시도해주세요.');
  }
}

// 니치 분석
export async function analyzeNiche(topic: string, target_audience?: string) {
  const response = await fetch(`${API_BASE_URL}/analyze-niche`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ topic, target_audience }),
  });
  
  if (!response.ok) {
    throw new Error('니치 분석에 실패했습니다');
  }
  
  const result = await response.json();
  return result.analysis;
}

// 훅 아이디어 생성
export async function generateHooks(topic: string, count: number = 10): Promise<string[]> {
  const response = await fetch(`${API_BASE_URL}/generate-hooks`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ topic, count }),
  });
  
  if (!response.ok) {
    throw new Error('훅 생성에 실패했습니다');
  }
  
  const result = await response.json();
  return result.hooks;
}

// 콘텐츠 타입 목록
export async function getContentTypes(): Promise<ContentType[]> {
  const response = await fetch(`${API_BASE_URL}/content-types`);
  
  if (!response.ok) {
    throw new Error('콘텐츠 타입 조회에 실패했습니다');
  }
  
  const result = await response.json();
  return result.content_types;
}

// 트렌딩 주제
export async function getTrendingTopics(): Promise<TrendingTopic[]> {
  const response = await fetch(`${API_BASE_URL}/trending-topics`);
  
  if (!response.ok) {
    throw new Error('트렌딩 주제 조회에 실패했습니다');
  }
  
  const result = await response.json();
  return result.trending_topics;
}

// 해시태그 제안
export async function suggestHashtags(topic: string, category?: string) {
  const response = await fetch(`${API_BASE_URL}/suggest-hashtags`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ topic, category }),
  });
  
  if (!response.ok) {
    throw new Error('해시태그 제안에 실패했습니다');
  }
  
  const result = await response.json();
  return result.hashtags;
}

// 최적화 체크리스트
export async function getOptimizationChecklist() {
  const response = await fetch(`${API_BASE_URL}/optimization-checklist`);
  
  if (!response.ok) {
    throw new Error('체크리스트 조회에 실패했습니다');
  }
  
  return await response.json();
}

// 기획서 저장
export async function savePlan(plan: any) {
  const response = await fetch(`${API_BASE_URL}/save-plan`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(plan),
  });
  
  if (!response.ok) {
    throw new Error('기획서 저장에 실패했습니다');
  }
  
  return await response.json();
}

// 저장된 기획서 목록
export async function getSavedPlans() {
  const response = await fetch(`${API_BASE_URL}/saved-plans`);
  
  if (!response.ok) {
    throw new Error('기획서 목록 조회에 실패했습니다');
  }
  
  return await response.json();
}

// 기획서 삭제
export async function deleteSavedPlan(planId: string) {
  const response = await fetch(`${API_BASE_URL}/saved-plans/${planId}`, {
    method: 'DELETE',
  });
  
  if (!response.ok) {
    throw new Error('기획서 삭제에 실패했습니다');
  }
  
  return await response.json();
}

// YouTube 트렌드 분석 API
export interface TrendingVideo {
  title: string;
  category: string;
  views: string;
  engagement?: string;
  keywords?: string[];
  thumbnail: string;
  why_viral?: string;
  video_id?: string;
  youtube_url: string;
  shorts_url?: string;
  crawled_at?: string;
  published_at?: string;  // 영상 업로드 날짜 (YouTube 업로드 날짜)
  region?: string;
  language?: string;
  trend_score?: number;
  is_shorts?: boolean;
  video_type?: string;  // "쇼츠" 또는 "롱폼"
  duration?: number;
}

export interface FilterOptions {
  categories: string[];
  regions: string[];
  languages: string[];
  sort_options: { value: string; label: string }[];
  time_filter_options: { value: string; label: string }[];
  video_type_options: { value: string; label: string }[];
  trend_score_range: {
    min: number;
    max: number;
    default: number;
  };
}

export interface TrendingVideosResponse {
  trending_videos: TrendingVideo[];
  count: number;
  total_count?: number;
  filters_applied?: {
    category?: string;
    region?: string;
    language?: string;
    min_trend_score?: number;
    sort_by?: string;
  };
  last_updated: string;
  source: string;
}

export async function getYoutubeTrending(
  count: number = 20,
  filters?: {
    category?: string;
    region?: string;
    language?: string;
    min_trend_score?: number;
    sort_by?: string;
    video_type?: string;
    time_filter?: string;
  },
  forceRefresh: boolean = false
): Promise<TrendingVideosResponse> {
  // forceRefresh가 true면 GitHub Actions 트리거
  if (forceRefresh && import.meta.env.PROD) {
    try {
      console.log('🔄 최신화 요청 - GitHub Actions 트리거...');
      // GitHub API 대신 간단한 웹훅 트리거
      await fetch('https://api.github.com/repos/Methodus-dev/methodus-shorts-planner/actions/workflows/manual-update.yml/dispatches', {
        method: 'POST',
        headers: {
          'Accept': 'application/vnd.github.v3+json',
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          ref: 'main'
        })
      });
      console.log('✅ 최신화 요청 완료 - 5분 후 새로고침해주세요');
    } catch (error) {
      console.log('GitHub Actions 트리거 실패:', error);
    }
  }
  
  // API 호출
  try {
    const params = new URLSearchParams({
      count: count.toString(),
      ...(filters?.category && { category: filters.category }),
      ...(filters?.language && { language: filters.language }),
      ...(filters?.sort_by && { sort_by: filters.sort_by }),
      ...(filters?.video_type && { video_type: filters.video_type }),
      ...(forceRefresh && { force_refresh: 'true' })
    });
    
    console.log(`🔍 API 호출: ${API_BASE_URL}/api/youtube/trending?${params}`);
    const response = await fetch(`${API_BASE_URL}/api/youtube/trending?${params}`);
    
    if (!response.ok) {
      throw new Error(`API 호출 실패: ${response.status}`);
    }
    
    const result = await response.json();
    console.log(`✅ API 응답: ${result.count}개 영상`);
    return result;
  } catch (error) {
    console.error('❌ API 호출 실패:', error);
    // API 실패 시 에러를 다시 던져서 사용자에게 알림
    throw new Error('백엔드 서버에 연결할 수 없습니다. 잠시 후 다시 시도해주세요.');
  }
}

export async function getFilterOptions(): Promise<FilterOptions> {
  const response = await fetch(`${API_BASE_URL}/api/youtube/filter-options`);
  
  if (!response.ok) {
    throw new Error('필터 옵션 조회에 실패했습니다');
  }
  
  return await response.json();
}

export async function analyzeKeywords(videos?: TrendingVideo[]) {
  try {
    const response = await fetch(`${API_BASE_URL}/api/youtube/analyze-keywords`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ videos: videos || [] }),
    });
    
    if (!response.ok) {
      throw new Error('API 호출 실패');
    }
    
    const result = await response.json();
    return result.keyword_analysis;
  } catch (error) {
    console.error('키워드 분석 API 호출 실패:', error);
    throw new Error('키워드 분석에 실패했습니다. 잠시 후 다시 시도해주세요.');
  }
}

export async function getContentIdeas(keyword: string) {
  try {
    const response = await fetch(`${API_BASE_URL}/api/youtube/content-ideas`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ keyword }),
    });
    
    if (!response.ok) {
      throw new Error('API 호출 실패');
    }
    
    const result = await response.json();
    return result.content_ideas;
  } catch (error) {
    console.error('콘텐츠 아이디어 API 호출 실패:', error);
    throw new Error('콘텐츠 아이디어 생성에 실패했습니다. 잠시 후 다시 시도해주세요.');
  }
}

export async function getPostingTimes() {
  const response = await fetch(`${API_BASE_URL}/api/youtube/posting-times`);
  
  if (!response.ok) {
    throw new Error('업로드 시간 조회에 실패했습니다');
  }
  
  return await response.json();
}

// 강제 새로고침 API
export async function refreshTrendingData() {
  try {
    const response = await fetch(`${API_BASE_URL}/api/youtube/refresh`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' }
    });
    
    if (!response.ok) {
      throw new Error('새로고침에 실패했습니다');
    }
    
    return await response.json();
  } catch (error) {
    console.log('API 호출 실패, Mock 데이터 사용:', error);
    return { message: '새로고침 완료 (Mock 데이터)', status: 'success' };
  }
}

// 카테고리별 키워드 분석
export interface CategoryKeyword {
  keyword: string;
  frequency: number;
  percentage: number;
}

export interface CategoryKeywordsResponse {
  category: string;
  total_videos: number;
  keywords: CategoryKeyword[];
  last_updated: string;
}

export async function getCategoryKeywords(category: string): Promise<CategoryKeywordsResponse> {
  const response = await fetch(`${API_BASE_URL}/api/youtube/category-keywords/${encodeURIComponent(category)}`);
  
  if (!response.ok) {
    throw new Error('카테고리 키워드 분석에 실패했습니다');
  }
  
  return await response.json();
}

// 이전 API (하위 호환성)
export async function getStructures() {
  return ["훅-핵심-요약-행동유도", "스토리 기반", "리스트 형식"];
}

export async function getTopics() {
  const trending = await getTrendingTopics();
  return trending.map(t => t.주제);
}
