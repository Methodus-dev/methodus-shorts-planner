import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import type { TrendingVideo, TrendingVideosResponse } from './services/api';
import {
  getYoutubeTrending,
  analyzeKeywords,
  getContentIdeas,
  createContentPlan,
  getCategoryKeywords,
  type CategoryKeywordsResponse
} from './services/api';
import VideoFilters from './components/VideoFilters';

function App() {
  const [trendingVideos, setTrendingVideos] = useState<TrendingVideo[]>([]);
  const [keywordAnalysis, setKeywordAnalysis] = useState<any>(null);
  const [selectedKeyword, setSelectedKeyword] = useState<string>('');
  const [contentIdeas, setContentIdeas] = useState<any>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [currentView, setCurrentView] = useState<'trending' | 'keywords' | 'ideas' | 'plan'>('trending');
  const [filters, setFilters] = useState({
    category: '',
    region: '',
    language: '',
    min_trend_score: 0,
    sort_by: 'trend_score',
    video_type: '',
    time_filter: 'all'
  });
  const [videoResponse, setVideoResponse] = useState<TrendingVideosResponse | null>(null);
  const [hasMore, setHasMore] = useState(true);
  const [currentPage, setCurrentPage] = useState(1);
  const [isLoadingMore, setIsLoadingMore] = useState(false);
  const [selectedCategory, setSelectedCategory] = useState<string>('');
  const [categoryKeywords, setCategoryKeywords] = useState<CategoryKeywordsResponse | null>(null);
  const [isLoadingCategoryKeywords, setIsLoadingCategoryKeywords] = useState(false);
  const [lastUpdateTime, setLastUpdateTime] = useState<string>('');
  const [isAutoRefreshing, setIsAutoRefreshing] = useState(false);
  const [contentPlan, setContentPlan] = useState<any>(null);

  useEffect(() => {
    loadTrendingVideos();
    // 백엔드가 2시간마다 자동으로 크롤링
  }, []);

  // 무한 스크롤 이벤트 리스너
  useEffect(() => {
    const handleScroll = () => {
      if (
        window.innerHeight + document.documentElement.scrollTop >=
        document.documentElement.offsetHeight - 1000
      ) {
        loadMoreVideos();
      }
    };

    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, [hasMore, isLoadingMore]);

  const loadTrendingVideos = async (reset = true, forceRefresh = false) => {
    console.log('🔄 실제 크롤링 데이터 로드 시작:', { reset, forceRefresh, filters });
    
    if (reset) {
      setIsLoading(true);
      setCurrentPage(1);
      setHasMore(true);
    } else {
      setIsLoadingMore(true);
    }

    try {
      const pageSize = 20;
      const startIndex = reset ? 0 : (currentPage - 1) * pageSize;
      
      // 필터가 있으면 더 많은 데이터 요청 (무한 스크롤 지원)
      const requestCount = startIndex + pageSize;
      
      console.log('📡 API 호출:', { requestCount, filters });
      const response = await getYoutubeTrending(requestCount, filters, forceRefresh);
      console.log('📊 API 응답:', { count: response.count, total: response.total_count });
      
      const allVideos = response.trending_videos;
      const newVideos = allVideos.slice(startIndex, startIndex + pageSize);
      
      console.log('📋 영상 데이터:', { 
        total: allVideos.length, 
        new: newVideos.length,
        korean: allVideos.filter(v => v.language === '한국어').length,
        english: allVideos.filter(v => v.language === '영어').length
      });
      
      if (reset) {
        setTrendingVideos(newVideos);
        setVideoResponse(response);
        setLastUpdateTime(new Date().toLocaleString('ko-KR'));
        
        // 자동으로 키워드 분석
        try {
          const analysis = await analyzeKeywords(allVideos.slice(0, 50));
          setKeywordAnalysis(analysis);
        } catch (error) {
          console.error('키워드 분석 실패:', error);
          // 키워드 분석 실패 시 사용자에게 알림
          alert('키워드 분석에 실패했습니다. 잠시 후 다시 시도해주세요.');
        }
      } else {
        setTrendingVideos(prev => [...prev, ...newVideos]);
      }
      
      // 더 로드할 데이터가 있는지 확인
      setHasMore(newVideos.length === pageSize && (startIndex + pageSize) < allVideos.length);
      if (reset) {
        setCurrentPage(2);
      } else {
        setCurrentPage(prev => prev + 1);
      }
      
    } catch (error) {
      console.error('트렌드 로드 실패:', error);
    } finally {
      setIsLoading(false);
      setIsLoadingMore(false);
    }
  };

  const handleForceRefresh = async () => {
    setIsLoading(true);
    setIsAutoRefreshing(true);
    try {
      console.log('🔄 최신 데이터 새로고침 시작...');
      
      // 최신 데이터 로드 (백엔드에서 자동으로 최신 데이터 반환)
      await loadTrendingVideos(true);
      
      console.log('✅ 최신 데이터 로드 완료');
    } catch (error) {
      console.error('❌ 새로고침 오류:', error);
      alert('❌ 새로고침 중 오류가 발생했습니다.');
    } finally {
      setIsLoading(false);
      setIsAutoRefreshing(false);
    }
  };

  const loadMoreVideos = () => {
    if (hasMore && !isLoadingMore) {
      loadTrendingVideos(false);
    }
  };

  const loadCategoryKeywords = async (category: string) => {
    setIsLoadingCategoryKeywords(true);
    try {
      const response = await getCategoryKeywords(category);
      setCategoryKeywords(response);
      setSelectedCategory(category);
    } catch (error) {
      console.error('카테고리 키워드 분석 실패:', error);
    } finally {
      setIsLoadingCategoryKeywords(false);
    }
  };

  const handleFiltersChange = (newFilters: typeof filters) => {
    console.log('🔍 필터 변경:', newFilters);
    console.log('🔍 받은 필터 상세:', JSON.stringify(newFilters));
    setFilters(newFilters);
    
    // video_type 필터 변경 시에는 즉시 데이터 로드
    if (newFilters.video_type !== filters.video_type) {
      console.log('🎬 영상 타입 필터 변경 감지, 즉시 데이터 로드:', newFilters.video_type);
      setTimeout(() => loadTrendingVideos(true), 0);
    }
    // 다른 필터들은 Apply 버튼을 눌러야만 로드
    console.log('🔍 필터 상태 업데이트 완료:', newFilters);
  };

  const handleApplyFilters = () => {
    console.log('필터 적용됨:', filters);
    console.log('필터 적용 시 현재 filters state:', JSON.stringify(filters));
    // 필터 적용 시에만 데이터 로드
    loadTrendingVideos(true);
    console.log('🔍 API 호출 후 필터 상태 유지:', filters);
    console.log('🔍 필터 상태가 유지되는지 확인:', {
      region: filters.region,
      category: filters.category,
      video_type: filters.video_type,
      time_filter: filters.time_filter
    });
  };

  const handleResetFilters = () => {
    const defaultFilters = {
      category: '',
      region: '',
      language: '',
      min_trend_score: 0,  // 트렌드 점수 필터 제거
      sort_by: 'trend_score',
      video_type: '',
      time_filter: 'all'
    };
    setFilters(defaultFilters);
    // 필터 초기화 후 즉시 데이터 로드
    setTimeout(() => loadTrendingVideos(true), 0);
  };

  const handleVideoSelect = (video: TrendingVideo) => {
    setSelectedKeyword(video.keywords?.[0] || video.title.split(' ')[0]);
  };

  const handleKeywordClick = async (keyword: string) => {
    setSelectedKeyword(keyword);
    setCurrentView('ideas');
    
    setIsLoading(true);
    try {
      console.log(`🔑 키워드 "${keyword}" 선택 - 자동 플로우 시작`);
      
      // 1단계: 아이디어 생성
      console.log('💡 1단계: 콘텐츠 아이디어 생성 중...');
      const ideas = await getContentIdeas(keyword);
      setContentIdeas(ideas);
      console.log(`✅ 아이디어 생성 완료: ${ideas.콘텐츠_아이디어?.length || 0}개`);
      
      // 2단계: 자동으로 첫 번째 아이디어로 기획서 생성
      if (ideas && ideas.콘텐츠_아이디어 && ideas.콘텐츠_아이디어.length > 0) {
        console.log('📋 2단계: 첫 번째 아이디어로 기획서 자동 생성 중...');
        const firstIdea = ideas.콘텐츠_아이디어[0];
        const plan = await createContentPlan({
          topic: firstIdea,
          content_type: 'Actionable',
          target_audience: undefined
        });
        setContentPlan(plan);
        console.log('✅ 기획서 자동 생성 완료!');
        console.log('🎉 키워드 → 아이디어 → 기획서 자동 플로우 완료!');
      }
    } catch (error) {
      console.error('자동 플로우 실패:', error);
      alert('콘텐츠 아이디어 또는 기획서 생성에 실패했습니다. 잠시 후 다시 시도해주세요.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-50 via-pink-50 to-orange-50">
      {/* 헤더 */}
      <header className="bg-white/80 backdrop-blur-sm border-b border-gray-200 sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold gradient-text">🎬 유튜브 콘텐츠 기획 시스템</h1>
              <p className="text-gray-600 text-sm mt-1">
                급상승 동영상 분석 → 키워드 추출 → 쇼츠&롱폼 콘텐츠 기획
              </p>
            </div>
            <div className="flex items-center gap-3">
              <button
                onClick={() => loadTrendingVideos(true)}
                className="px-4 py-2 text-sm bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition-colors"
              >
                🔄 새로고침
              </button>
              <button
                onClick={handleForceRefresh}
                disabled={isLoading}
                className="px-4 py-2 text-sm bg-green-500 text-white rounded-lg hover:bg-green-600 transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2"
              >
                {isLoading ? (
                  <>
                    <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
                    {isAutoRefreshing ? '최신화 중...' : '로딩 중...'}
                  </>
                ) : (
                  <>
                    🔄 최신화
                  </>
                )}
              </button>
            </div>
          </div>
          
          {/* 사용방법 가이드 */}
          <div className="mt-4 p-3 bg-gradient-to-r from-primary-50 to-secondary-50 rounded-lg border border-primary-200">
            <div className="flex flex-col sm:flex-row sm:items-center gap-2 sm:gap-4 text-sm">
              <span className="font-semibold text-primary-700 whitespace-nowrap">💡 사용 방법:</span>
              <div className="grid grid-cols-2 sm:flex sm:flex-wrap gap-2 sm:gap-4 text-gray-600">
                <span className="text-xs sm:text-sm">1️⃣ 급상승 동영상 확인</span>
                <span className="text-xs sm:text-sm">2️⃣ 인기 키워드 파악</span>
                <span className="text-xs sm:text-sm">3️⃣ 콘텐츠 아이디어 선택</span>
                <span className="text-xs sm:text-sm">4️⃣ 기획서 자동 생성</span>
              </div>
            </div>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* 네비게이션 탭 */}
        <div className="flex flex-wrap gap-2 mb-8 justify-center sm:justify-start">
          <button
            onClick={() => setCurrentView('trending')}
            className={`px-4 py-2 sm:px-6 sm:py-3 rounded-lg font-semibold text-sm sm:text-base transition-all flex-1 sm:flex-none min-w-0 ${
              currentView === 'trending'
                ? 'bg-white shadow-lg border-2 border-primary-500 text-primary-600'
                : 'bg-white/60 hover:bg-white'
            }`}
          >
            <span className="hidden sm:inline">📈 급상승 동영상</span>
            <span className="sm:hidden">📈 급상승</span>
          </button>
          <button
            onClick={() => setCurrentView('keywords')}
            className={`px-4 py-2 sm:px-6 sm:py-3 rounded-lg font-semibold text-sm sm:text-base transition-all flex-1 sm:flex-none min-w-0 ${
              currentView === 'keywords'
                ? 'bg-white shadow-lg border-2 border-primary-500 text-primary-600'
                : 'bg-white/60 hover:bg-white'
            }`}
            disabled={!keywordAnalysis}
          >
            <span className="hidden sm:inline">🔑 키워드 분석</span>
            <span className="sm:hidden">🔑 키워드</span>
          </button>
          <button
            onClick={() => setCurrentView('ideas')}
            className={`px-4 py-2 sm:px-6 sm:py-3 rounded-lg font-semibold text-sm sm:text-base transition-all flex-1 sm:flex-none min-w-0 ${
              currentView === 'ideas'
                ? 'bg-white shadow-lg border-2 border-primary-500 text-primary-600'
                : 'bg-white/60 hover:bg-white'
            }`}
            disabled={!selectedKeyword}
          >
            <span className="hidden sm:inline">💡 콘텐츠 아이디어</span>
            <span className="sm:hidden">💡 아이디어</span>
          </button>
          <button
            onClick={() => setCurrentView('plan')}
            className={`px-4 py-2 sm:px-6 sm:py-3 rounded-lg font-semibold text-sm sm:text-base transition-all flex-1 sm:flex-none min-w-0 ${
              currentView === 'plan'
                ? 'bg-white shadow-lg border-2 border-primary-500 text-primary-600'
                : 'bg-white/60 hover:bg-white'
            }`}
            disabled={!contentPlan}
          >
            <span className="hidden sm:inline">📋 콘텐츠 기획서</span>
            <span className="sm:hidden">📋 기획서</span>
          </button>
        </div>

        {isLoading && (
          <div className="text-center py-12">
            <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
            <p className="mt-4 text-gray-600">분석 중...</p>
          </div>
        )}

        {/* 급상승 동영상 뷰 */}
        {currentView === 'trending' && !isLoading && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="space-y-6"
          >
            
            <div className="card">
              <h2 className="text-2xl font-bold mb-4">
                🔥 급상승 YouTube 영상 (쇼츠 + 롱폼)
              </h2>
              <p className="text-gray-600 mb-4">
                키워드를 클릭하면 콘텐츠 아이디어와 기획서를 자동으로 생성합니다
              </p>
              
              {/* 쇼츠/롱폼 빠른 필터 탭 */}
              <div className="mb-6 flex gap-3 items-center">
                <span className="text-sm font-semibold text-gray-700">빠른 필터:</span>
                <div className="flex gap-2">
                  <button
                    onClick={() => {
                      const newFilters = { ...filters, video_type: '' };
                      setFilters(newFilters);
                      loadTrendingVideos(true);
                    }}
                    className={`px-4 py-2 rounded-lg text-sm font-medium transition-all ${
                      filters.video_type === ''
                        ? 'bg-gradient-to-r from-purple-500 to-pink-500 text-white shadow-lg'
                        : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                    }`}
                  >
                    🎬 전체
                  </button>
                  <button
                    onClick={() => {
                      const newFilters = { ...filters, video_type: '쇼츠' };
                      setFilters(newFilters);
                      loadTrendingVideos(true);
                    }}
                    className={`px-4 py-2 rounded-lg text-sm font-medium transition-all ${
                      filters.video_type === '쇼츠'
                        ? 'bg-gradient-to-r from-pink-500 to-rose-500 text-white shadow-lg'
                        : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                    }`}
                  >
                    📱 쇼츠만
                  </button>
                  <button
                    onClick={() => {
                      const newFilters = { ...filters, video_type: '롱폼' };
                      setFilters(newFilters);
                      loadTrendingVideos(true);
                    }}
                    className={`px-4 py-2 rounded-lg text-sm font-medium transition-all ${
                      filters.video_type === '롱폼'
                        ? 'bg-gradient-to-r from-indigo-500 to-blue-500 text-white shadow-lg'
                        : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                    }`}
                  >
                    🎥 롱폼만
                  </button>
                </div>
              </div>
              
              {/* 필터링 UI */}
              <VideoFilters 
                filters={filters}
                onFiltersChange={(newFilters) => handleFiltersChange(newFilters as any)}
                onApplyFilters={handleApplyFilters}
                onResetFilters={handleResetFilters}
                isLoading={isLoading}
              />
              
              {/* 필터 결과 정보 */}
              {videoResponse && (
                <div className="mb-4 p-3 bg-blue-50 rounded-lg">
                  <div className="flex items-center justify-between">
                    <p className="text-sm text-blue-800">
                      📊 총 {videoResponse.total_count || videoResponse.count}개 중 {videoResponse.count}개 표시
                      {videoResponse.filters_applied && (
                        <span className="ml-2">
                          • 마지막 업데이트: {new Date(videoResponse.last_updated).toLocaleString('ko-KR')}
                        </span>
                      )}
                    </p>
                    {lastUpdateTime && (
                      <div className="flex items-center gap-2 text-xs text-green-600">
                        {isAutoRefreshing ? (
                          <>
                            <div className="animate-spin rounded-full h-3 w-3 border-b-2 border-green-600"></div>
                            <span>실시간 업데이트 중...</span>
                          </>
                        ) : (
                          <>
                            <span>🔄</span>
                            <span>로컬 업데이트: {lastUpdateTime}</span>
                          </>
                        )}
                      </div>
                    )}
                  </div>
                </div>
              )}

              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                {trendingVideos.map((video, idx) => (
                  <motion.div
                    key={idx}
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: idx * 0.05 }}
                    onClick={() => handleVideoSelect(video)}
                    className="p-4 bg-white rounded-xl border-2 border-gray-200 hover:border-primary-400 hover:shadow-xl transition-all cursor-pointer group"
                  >
                    {/* 순위 뱃지 */}
                    <div className="flex items-start justify-between mb-3">
                      <span className="text-3xl font-bold text-gray-300 group-hover:text-primary-500 transition-colors">
                        #{idx + 1}
                      </span>
                      <span className="text-3xl">{video.thumbnail}</span>
                    </div>

                    {/* 제목 */}
                    <h3 className="font-bold text-gray-800 mb-2 line-clamp-2 group-hover:text-primary-600 transition-colors">
                      {video.title}
                    </h3>

                    {/* 통계 */}
                    <div className="flex items-center gap-3 text-xs text-gray-600 mb-3">
                      <span className="flex items-center">
                        <span className="mr-1">👁️</span>
                        {video.views}
                      </span>
                      <span className="flex items-center">
                        <span className="mr-1">🔥</span>
                        {video.trend_score}점
                      </span>
                    </div>

                    {/* 카테고리 & 지역 & 영상타입 */}
                    <div className="mb-3 flex flex-wrap gap-2">
                      {video.video_type && (
                        <span className={`px-2 py-1 text-xs rounded-full ${
                          video.video_type === '쇼츠' 
                            ? 'bg-pink-100 text-pink-700' 
                            : 'bg-indigo-100 text-indigo-700'
                        }`}>
                          {video.video_type === '쇼츠' ? '📱 쇼츠' : '🎥 롱폼'}
                        </span>
                      )}
                      <span className="px-2 py-1 bg-purple-100 text-purple-700 text-xs rounded-full">
                        {video.category}
                      </span>
                      {video.region && (
                        <span className={`px-2 py-1 text-xs rounded-full ${
                          video.region === '국내' 
                            ? 'bg-blue-100 text-blue-700' 
                            : 'bg-green-100 text-green-700'
                        }`}>
                          {video.region === '국내' ? '🇰🇷 국내' : '🌏 해외'}
                        </span>
                      )}
                      {video.language && (
                        <span className={`px-2 py-1 text-xs rounded-full ${
                          video.language === '한국어' 
                            ? 'bg-red-100 text-red-700' 
                            : 'bg-yellow-100 text-yellow-700'
                        }`}>
                          {video.language === '한국어' ? '🇰🇷 한국어' : '🇺🇸 영어'}
                        </span>
                      )}
                      {video.trend_score && (
                        <span className="px-2 py-1 bg-orange-100 text-orange-700 text-xs rounded-full">
                          📈 {video.trend_score}점
                        </span>
                      )}
                    </div>

                    {/* 키워드 */}
                    <div className="flex flex-wrap gap-1 mb-3">
                      {(video.keywords || video.title.split(' ').slice(0, 3)).slice(0, 3).map((kw, kidx) => (
                        <span
                          key={kidx}
                          className="px-2 py-0.5 bg-gray-100 text-gray-700 text-xs rounded"
                        >
                          #{kw}
                        </span>
                      ))}
                    </div>

                    {/* 바이럴 이유 */}
                    <div className="text-xs text-gray-500 border-t border-gray-200 pt-2 mb-3">
                      💡 {video.why_viral || '실용적인 정보와 단계별 가이드로 인기'}
                    </div>

                    {/* YouTube 링크 - 영상 타입에 따라 적절한 버튼만 표시 */}
                    {video.youtube_url && (
                      <div className="flex gap-2">
                        {video.video_type === '쇼츠' ? (
                          <a
                            href={video.youtube_url}
                            target="_blank"
                            rel="noopener noreferrer"
                            className="flex-1 text-center px-3 py-2 bg-gradient-to-r from-pink-500 via-rose-500 to-red-500 text-white text-xs font-bold rounded-lg hover:shadow-xl hover:scale-105 transition-all"
                            onClick={(e) => e.stopPropagation()}
                          >
                            📱 쇼츠 보기
                          </a>
                        ) : (
                          <a
                            href={video.youtube_url}
                            target="_blank"
                            rel="noopener noreferrer"
                            className="flex-1 text-center px-3 py-2 bg-gradient-to-r from-blue-600 via-indigo-600 to-purple-600 text-white text-xs font-bold rounded-lg hover:shadow-xl hover:scale-105 transition-all"
                            onClick={(e) => e.stopPropagation()}
                          >
                            🎥 롱폼 보기
                          </a>
                        )}
                      </div>
                    )}
                  </motion.div>
                ))}
              </div>
              
              {/* 무한 스크롤 로딩 인디케이터 */}
              {isLoadingMore && (
                <div className="text-center py-8">
                  <div className="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600"></div>
                  <p className="mt-2 text-gray-600 text-sm">더 많은 영상을 불러오는 중...</p>
                </div>
              )}
              
              {/* 더 이상 로드할 데이터가 없을 때 */}
              {!hasMore && trendingVideos.length > 0 && (
                <div className="text-center py-8">
                  <p className="text-gray-500 text-sm">🎉 모든 영상을 불러왔습니다!</p>
                </div>
              )}
            </div>
          </motion.div>
        )}

        {/* 키워드 분석 뷰 */}
        {currentView === 'keywords' && keywordAnalysis && !isLoading && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="space-y-6"
          >
            {/* 인기 키워드 */}
            <div className="card">
              <h2 className="text-2xl font-bold mb-4">
                🔑 지금 가장 핫한 키워드
              </h2>
              <p className="text-gray-600 mb-6">
                💡 키워드를 클릭하면 <strong>아이디어 생성 → 기획서 자동 생성</strong>까지 한번에 진행됩니다!
              </p>
              
              <div className="flex flex-wrap gap-3">
                {keywordAnalysis.전체_인기_키워드?.slice(0, 15).map((kwData: {키워드: string, 추천도: string}, idx: number) => (
                  <button
                    key={idx}
                    onClick={() => handleKeywordClick(kwData.키워드)}
                    className={`px-6 py-3 rounded-xl font-semibold transition-all ${
                      selectedKeyword === kwData.키워드
                        ? 'bg-gradient-to-r from-primary-500 to-secondary-500 text-white shadow-lg scale-110'
                        : 'bg-white border-2 border-gray-200 hover:border-primary-400 hover:shadow-md'
                    }`}
                  >
                    <div className="text-lg mb-1">#{kwData.키워드}</div>
                    <div className="text-xs opacity-80">{kwData.추천도}</div>
                  </button>
                ))}
              </div>
            </div>

            {/* 카테고리별 키워드 */}
            <div className="card">
              <h3 className="text-xl font-bold mb-4">📂 카테고리별 인기 키워드</h3>
              
              {/* 카테고리 선택 버튼들 */}
              <div className="mb-6">
                <p className="text-gray-600 mb-3">카테고리를 선택하면 해당 카테고리의 핫 키워드를 분석합니다</p>
                <div className="flex flex-wrap gap-2">
                  {Object.keys(keywordAnalysis.카테고리별_키워드 || {}).map((category) => (
                    <button
                      key={category}
                      onClick={() => loadCategoryKeywords(category)}
                      className={`px-4 py-2 rounded-lg text-sm font-medium transition-all ${
                        selectedCategory === category
                          ? 'bg-primary-500 text-white shadow-lg'
                          : 'bg-white border border-gray-300 hover:border-primary-400 hover:shadow-md'
                      }`}
                    >
                      {category}
                    </button>
                  ))}
                </div>
              </div>

              {/* 선택된 카테고리의 상세 키워드 분석 */}
              {selectedCategory && (
                <div className="border-t border-gray-200 pt-6">
                  {isLoadingCategoryKeywords ? (
                    <div className="text-center py-8">
                      <div className="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600"></div>
                      <p className="mt-2 text-gray-600">키워드 분석 중...</p>
                    </div>
                  ) : categoryKeywords ? (
                    <div>
                      <h4 className="text-lg font-bold mb-4">
                        🔥 {selectedCategory} 카테고리 핫 키워드 ({categoryKeywords.total_videos}개 영상 분석)
                      </h4>
                      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
                        {categoryKeywords.keywords.slice(0, 15).map((kwData: {keyword: string, frequency: number, percentage: number}, idx: number) => (
                          <button
                            key={idx}
                            onClick={() => handleKeywordClick(kwData.keyword)}
                            className={`p-3 rounded-lg text-left transition-all ${
                              selectedKeyword === kwData.keyword
                                ? 'bg-gradient-to-r from-primary-500 to-secondary-500 text-white shadow-lg'
                                : 'bg-gradient-to-r from-blue-50 to-purple-50 border border-gray-200 hover:shadow-md'
                            }`}
                          >
                            <div className="font-semibold text-sm mb-1">#{kwData.keyword}</div>
                            <div className="text-xs opacity-80">
                              {kwData.frequency}회 언급 ({kwData.percentage}%)
                            </div>
                          </button>
                        ))}
                      </div>
                      <p className="text-xs text-gray-500 mt-4">
                        마지막 업데이트: {new Date(categoryKeywords.last_updated).toLocaleString('ko-KR')}
                      </p>
                    </div>
                  ) : null}
                </div>
              )}

              {/* 기본 카테고리별 키워드 미리보기 */}
              {!selectedCategory && (
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                  {Object.entries(keywordAnalysis.카테고리별_키워드 || {}).map(([category, keywords]: [string, any]) => (
                    <div key={category} className="p-4 bg-gradient-to-br from-purple-50 to-pink-50 rounded-lg">
                      <div className="font-bold text-purple-900 mb-2">{category}</div>
                      <div className="flex flex-wrap gap-1">
                        {keywords.slice(0, 5).map((kw: string, idx: number) => (
                          <button
                            key={idx}
                            onClick={() => handleKeywordClick(kw)}
                            className="px-2 py-1 bg-white text-purple-700 text-xs rounded hover:bg-purple-100 transition-colors"
                          >
                            #{kw}
                          </button>
                        ))}
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>

            {/* 트렌드 인사이트 */}
            <div className="card">
              <h3 className="text-xl font-bold mb-4">📊 트렌드 인사이트</h3>
              
              {/* 핫한 카테고리 */}
              <div className="mb-6">
                <h4 className="font-semibold text-gray-700 mb-3">🔥 핫한 카테고리 TOP 3</h4>
                <div className="space-y-2">
                  {keywordAnalysis.트렌드_분석?.핫한_카테고리_TOP3?.map((cat: any, idx: number) => (
                    <div key={idx} className="flex items-center justify-between p-3 bg-orange-50 rounded-lg">
                      <span className="font-medium">{cat.카테고리}</span>
                      <div className="flex items-center gap-2">
                        <span className="text-sm text-gray-600">{cat.영상수}개</span>
                        <span>{cat.인기도}</span>
                      </div>
                    </div>
                  ))}
                </div>
              </div>

              {/* 바이럴 공통 요소 */}
              <div>
                <h4 className="font-semibold text-gray-700 mb-3">✨ 바이럴 공통 요소</h4>
                <div className="grid grid-cols-2 md:grid-cols-3 gap-2">
                  {keywordAnalysis.트렌드_분석?.공통_요소?.map((element: string, idx: number) => (
                    <div key={idx} className="p-2 bg-green-50 text-green-800 text-sm rounded text-center">
                      {element}
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </motion.div>
        )}

        {/* 콘텐츠 기획서 뷰 */}
        {currentView === 'plan' && contentPlan && !isLoading && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="space-y-6"
          >
            <div className="card">
              <div className="flex items-center justify-between mb-6">
                <h2 className="text-2xl font-bold">
                  📋 콘텐츠 기획서
                </h2>
                <button
                  onClick={() => setCurrentView('ideas')}
                  className="btn-secondary"
                >
                  ← 아이디어로 돌아가기
                </button>
              </div>

              {contentPlan.plan && (
                <div className="space-y-6">
                  {/* 기본 정보 */}
                  <div className="p-4 bg-gradient-to-r from-purple-50 to-pink-50 rounded-lg">
                    <h3 className="font-bold text-lg mb-2">📌 기본 정보</h3>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-3 text-sm">
                      <div>
                        <span className="text-gray-600">주제:</span>
                        <span className="ml-2 font-medium">{contentPlan.plan.주제}</span>
                      </div>
                      <div>
                        <span className="text-gray-600">콘텐츠 타입:</span>
                        <span className="ml-2 font-medium">{contentPlan.plan.콘텐츠_타입}</span>
                      </div>
                      <div>
                        <span className="text-gray-600">타겟:</span>
                        <span className="ml-2 font-medium">{contentPlan.plan.타겟_오디언스 || '일반'}</span>
                      </div>
                      <div>
                        <span className="text-gray-600">생성일시:</span>
                        <span className="ml-2 font-medium">{contentPlan.generated_at}</span>
                      </div>
                    </div>
                  </div>

                  {/* 콘텐츠 구조 */}
                  {contentPlan.plan.콘텐츠_구조 && (
                    <div className="p-4 bg-blue-50 rounded-lg">
                      <h3 className="font-bold text-lg mb-3">🎬 콘텐츠 구조</h3>
                      <div className="space-y-3">
                        {Object.entries(contentPlan.plan.콘텐츠_구조).map(([key, value]: [string, any]) => (
                          <div key={key} className="p-3 bg-white rounded border border-blue-200">
                            <div className="font-semibold text-blue-900 mb-1">{key}</div>
                            <div className="text-sm text-gray-700">{value}</div>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}

                  {/* 제목 옵션 */}
                  {contentPlan.plan.제목_옵션 && (
                    <div className="p-4 bg-yellow-50 rounded-lg">
                      <h3 className="font-bold text-lg mb-3">💡 제목 옵션</h3>
                      <div className="space-y-2">
                        {contentPlan.plan.제목_옵션.map((title: string, idx: number) => (
                          <div
                            key={idx}
                            onClick={() => {
                              navigator.clipboard.writeText(title);
                              alert('제목이 복사되었습니다!');
                            }}
                            className="p-3 bg-white rounded border-2 border-yellow-300 hover:border-yellow-500 hover:shadow-md cursor-pointer transition-all"
                          >
                            <div className="font-medium">{title}</div>
                            <div className="text-xs text-gray-500 mt-1">클릭하여 복사</div>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}

                  {/* 해시태그 */}
                  {contentPlan.plan.해시태그 && (
                    <div className="p-4 bg-green-50 rounded-lg">
                      <h3 className="font-bold text-lg mb-3">#️⃣ 추천 해시태그</h3>
                      <div className="flex flex-wrap gap-2">
                        {contentPlan.plan.해시태그.map((tag: string, idx: number) => (
                          <span
                            key={idx}
                            onClick={() => {
                              navigator.clipboard.writeText(tag);
                              alert('해시태그가 복사되었습니다!');
                            }}
                            className="px-3 py-1 bg-green-200 text-green-800 rounded-full text-sm font-medium hover:bg-green-300 cursor-pointer transition-colors"
                          >
                            {tag}
                          </span>
                        ))}
                      </div>
                    </div>
                  )}

                  {/* 최적화 팁 */}
                  {contentPlan.plan.최적화_팁 && (
                    <div className="p-4 bg-purple-50 rounded-lg">
                      <h3 className="font-bold text-lg mb-3">🚀 최적화 팁</h3>
                      <div className="space-y-2">
                        {contentPlan.plan.최적화_팁.map((tip: string, idx: number) => (
                          <div key={idx} className="flex items-start">
                            <span className="text-purple-500 mr-2">•</span>
                            <span className="text-sm text-gray-700">{tip}</span>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}
                </div>
              )}
            </div>
          </motion.div>
        )}

        {/* 콘텐츠 아이디어 뷰 */}
        {currentView === 'ideas' && contentIdeas && !isLoading && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="space-y-6"
          >
            <div className="card">
              <div className="flex items-center justify-between mb-6">
                <div>
                  <h2 className="text-2xl font-bold">
                    💡 <span className="text-primary-600">#{selectedKeyword}</span> 콘텐츠 아이디어
                  </h2>
                  <p className="text-sm text-gray-600 mt-1">
                    관련 급상승 영상: {contentIdeas.관련_급상승_영상수}개
                  </p>
                  {contentPlan && (
                    <div className="mt-2">
                      <button
                        onClick={() => setCurrentView('plan')}
                        className="text-sm text-green-600 hover:text-green-700 font-semibold flex items-center gap-1"
                      >
                        ✅ 기획서 자동 생성 완료! 보러가기 →
                      </button>
                    </div>
                  )}
                </div>
                <div className="flex gap-2">
                  {contentPlan && (
                    <button
                      onClick={() => setCurrentView('plan')}
                      className="px-4 py-2 bg-green-500 text-white rounded-lg hover:bg-green-600 transition-colors text-sm"
                    >
                      📋 기획서 보기
                    </button>
                  )}
                  <button
                    onClick={() => setCurrentView('keywords')}
                    className="btn-secondary"
                  >
                    ← 키워드로 돌아가기
                  </button>
                </div>
              </div>

              {/* 추천 제목 패턴 */}
              <div className="mb-6">
                <h3 className="font-semibold text-lg mb-3">📝 추천 제목 패턴</h3>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                  {contentIdeas.추천_제목_패턴?.map((pattern: string, idx: number) => (
                    <div key={idx} className="p-3 bg-blue-50 border border-blue-200 rounded-lg text-sm">
                      {pattern}
                    </div>
                  ))}
                </div>
              </div>

              {/* 훅 아이디어 */}
              <div className="mb-6">
                <h3 className="font-semibold text-lg mb-3">⚡ 훅 (Hook) 아이디어</h3>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                  {contentIdeas.훅_아이디어?.map((hook: string, idx: number) => (
                    <div
                      key={idx}
                      onClick={() => {
                        navigator.clipboard.writeText(hook);
                        alert('복사되었습니다!');
                      }}
                      className="p-4 bg-gradient-to-r from-yellow-50 to-orange-50 border-2 border-yellow-300 rounded-lg hover:shadow-lg transition-all cursor-pointer"
                    >
                      <div className="font-medium text-gray-800">{hook}</div>
                      <div className="text-xs text-gray-500 mt-2">클릭하여 복사</div>
                    </div>
                  ))}
                </div>
              </div>

              {/* 콘텐츠 아이디어 */}
              <div className="mb-6">
                <h3 className="font-semibold text-lg mb-3">🎬 콘텐츠 아이디어</h3>
                <div className="space-y-3">
                  {contentIdeas.콘텐츠_아이디어?.map((idea: string, idx: number) => (
                    <div
                      key={idx}
                      className="p-4 bg-white border-2 border-gray-200 rounded-lg hover:border-primary-400 transition-all"
                    >
                      <div className="flex items-start">
                        <span className="text-2xl mr-3">{idx + 1}️⃣</span>
                        <div className="flex-1">
                          <div className="font-medium text-gray-800">{idea}</div>
                          <button
                            onClick={async () => {
                              setIsLoading(true);
                              try {
                                const plan = await createContentPlan({
                                  topic: idea,
                                  content_type: 'Actionable',
                                  target_audience: undefined
                                });
                                setContentPlan(plan);
                                setCurrentView('plan');
                                console.log('✅ 기획서 생성 완료');
                              } catch (error) {
                                console.error('기획서 생성 실패:', error);
                                alert('기획서 생성 실패: ' + error);
                              } finally {
                                setIsLoading(false);
                              }
                            }}
                            className="mt-2 text-xs text-primary-600 hover:text-primary-700 font-semibold"
                          >
                            → 이 아이디어로 기획서 만들기
                          </button>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </motion.div>
        )}
      </main>

    </div>
  );
}

export default App;
