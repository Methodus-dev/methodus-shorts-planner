import { useState } from 'react';

interface VideoFiltersProps {
  filters: {
    category: string;
    language: string;
    sort_by: string;
    video_type: string;
  };
  onFiltersChange: (filters: {
    category?: string;
    language?: string;
    sort_by?: string;
    video_type?: string;
  }) => void;
  onApplyFilters?: () => void;
  onResetFilters?: () => void;
  isLoading?: boolean;
}

export default function VideoFilters({ filters, onFiltersChange, onApplyFilters, onResetFilters, isLoading }: VideoFiltersProps) {
  const [isExpanded, setIsExpanded] = useState(true); // 기본적으로 열린 상태

  // 정적 필터 옵션 정의 (YouTube 원본 카테고리 기준)
  const filterOptions = {
    categories: [
      "사람/블로그", "엔터테인먼트", "게임", "뉴스/정치", "음악", 
      "스포츠", "라이프스타일", "과학기술", "코미디", "영화/애니메이션",
      "교육/학습", "여행/이벤트", "자동차/교통", "동물/반려동물", "비영리/사회운동"
    ],
    languages: ['한국어', '영어', '일본어', '중국어'],
    sort_options: [
      { value: 'trend_score', label: '🔥 트렌드 점수' },
      { value: 'views', label: '👁️ 조회수' },
      { value: 'crawled_at', label: '⏰ 최신순' }
    ]
  };

  const handleFilterChange = (key: string, value: string | number) => {
    const newFilters = { ...filters, [key]: value };
    console.log(`🔧 필터 변경: ${key} = ${value}`, newFilters);
    // 로컬 state 없이 바로 부모에게 전달
    onFiltersChange(newFilters);
  };

  const resetFilters = () => {
    const defaultFilters = {
      category: '',
      language: '',
      sort_by: 'trend_score',
      video_type: ''
    };
    // 필터 전달
    onFiltersChange(defaultFilters);
    // Reset 핸들러 호출
    if (onResetFilters) {
      onResetFilters();
    }
    // 필터 리셋 후에도 창은 열린 상태로 유지 - 절대 자동으로 접지 않음
  };

  const applyFilters = () => {
    console.log('🔍 필터 적용 버튼 클릭:', filters);
    console.log('🔍 전달할 필터:', JSON.stringify(filters));
    // 필터 전달 (최신 상태 확실히 전달)
    onFiltersChange(filters);
    // Apply 핸들러 호출
    if (onApplyFilters) {
      onApplyFilters();
    }
    // 필터 창은 절대 자동으로 접지 않음 - 사용자가 수동으로만 접을 수 있음
    console.log('🔍 필터 적용 완료, 상태 유지:', filters);
  };

  const options = filterOptions;

  return (
    <div className="bg-white rounded-lg shadow-md p-4 mb-6">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-lg font-semibold text-gray-800">🎯 필터 & 정렬</h3>
        <div className="flex gap-2">
          <button
            onClick={() => setIsExpanded(!isExpanded)}
            className="px-3 py-1 text-sm bg-blue-100 text-blue-600 rounded-full hover:bg-blue-200 transition-colors"
          >
            {isExpanded ? '접기' : '펼치기'}
          </button>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {/* 카테고리 필터 */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            📂 카테고리
          </label>
          <select
            value={filters.category}
            onChange={(e) => handleFilterChange('category', e.target.value)}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            disabled={isLoading}
          >
            <option value="">전체</option>
            {options.categories.map((category) => (
              <option key={category} value={category}>
                {category}
              </option>
            ))}
          </select>
        </div>

        {/* 언어 필터 */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            🗣️ 언어
          </label>
          <select
            value={filters.language}
            onChange={(e) => {
              const selectedValue = e.target.value;
              console.log('🗣️ 언어 선택:', selectedValue);
              handleFilterChange('language', selectedValue);
            }}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            disabled={isLoading}
          >
            <option value="">전체</option>
            {options.languages.map((language) => (
              <option key={language} value={language}>
                {language === '한국어' ? '🇰🇷 한국어' : '🇺🇸 영어'}
              </option>
            ))}
          </select>
        </div>

        {/* 정렬 옵션 */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            🔄 정렬 기준
          </label>
          <select
            value={filters.sort_by}
            onChange={(e) => handleFilterChange('sort_by', e.target.value)}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            disabled={isLoading}
          >
            {options.sort_options.map((option) => (
              <option key={option.value} value={option.value}>
                {option.label}
              </option>
            ))}
          </select>
        </div>
      </div>

      {/* 필터 적용/초기화 버튼 */}
      <div className="mt-4 flex justify-center gap-3">
        <button
          onClick={applyFilters}
          className="px-6 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition-colors font-medium"
          disabled={isLoading}
        >
          🔍 필터 적용
        </button>
        <button
          onClick={resetFilters}
          className="px-6 py-2 bg-gray-500 text-white rounded-lg hover:bg-gray-600 transition-colors font-medium"
          disabled={isLoading}
        >
          🔄 초기화
        </button>
      </div>

      {/* 활성 필터 표시 */}
      <div className="mt-4 flex flex-wrap gap-2">
        {filters.category && (
          <span className="px-2 py-1 bg-blue-100 text-blue-800 text-xs rounded-full">
            📂 {filters.category}
          </span>
        )}
        {filters.language && (
          <span className="px-2 py-1 bg-purple-100 text-purple-800 text-xs rounded-full">
            🗣️ {filters.language}
          </span>
        )}
        {filters.sort_by && filters.sort_by !== 'trend_score' && (
          <span className="px-2 py-1 bg-yellow-100 text-yellow-800 text-xs rounded-full">
            🔄 {filters.sort_by === 'views' ? '조회수' : '최신순'}
          </span>
        )}
      </div>
    </div>
  );
}
