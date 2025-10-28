import { useState, useEffect } from 'react';
import type { FilterOptions } from '../services/api';

interface VideoFiltersProps {
  filters: {
    category: string;
    region: string;
    language: string;
    min_trend_score: number;
    sort_by: string;
    video_type: string;
    time_filter: string;
  };
  onFiltersChange: (filters: {
    category?: string;
    region?: string;
    language?: string;
    min_trend_score?: number;
    sort_by?: string;
    video_type?: string;
    time_filter?: string;
  }) => void;
  onApplyFilters?: () => void;
  onResetFilters?: () => void;
  isLoading?: boolean;
}

export default function VideoFilters({ filters, onFiltersChange, onApplyFilters, onResetFilters, isLoading }: VideoFiltersProps) {
  const [filterOptions, setFilterOptions] = useState<FilterOptions | null>(null);
  // 로컬 state 제거 - 부모로부터 받은 filters 사용
  const [isExpanded, setIsExpanded] = useState(true); // 기본적으로 열린 상태

  useEffect(() => {
    loadFilterOptions();
  }, []);

  const loadFilterOptions = async () => {
    try {
      const { getFilterOptions } = await import('../services/api');
      const options = await getFilterOptions();
      setFilterOptions(options);
    } catch (error) {
      console.error('필터 옵션 로드 실패:', error);
    }
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
      region: '',
      language: '',
      min_trend_score: 0,  // 트렌드 점수 필터 제거
      sort_by: 'trend_score',
      video_type: '',
      time_filter: 'all'
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

  // filterOptions가 없어도 기본 필터 UI 표시
  const defaultFilterOptions = {
    categories: ['일반', '엔터테인먼트', '교육', '뉴스', '스포츠', '음악', '게임', '과학기술'],
    regions: ['국내', '해외'],
    sort_options: [
      { value: 'trend_score', label: '🔥 트렌드 점수' },
      { value: 'views', label: '👁️ 조회수' },
      { value: 'recent', label: '⏰ 최신순' }
    ],
    time_filter_options: [
      { value: 'all', label: '전체' },
      { value: 'today', label: '오늘 (24시간)' },
      { value: 'week', label: '이번 주 (7일)' },
      { value: 'month', label: '이번 달 (30일)' }
    ],
    video_type_options: [
      { value: '', label: '전체' },
      { value: '쇼츠', label: '📱 쇼츠' },
      { value: '롱폼', label: '🎥 롱폼' }
    ]
  };

  const options = filterOptions || defaultFilterOptions;

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

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-6 gap-4">
        {/* 기간 필터 */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            📅 기간
          </label>
          <select
            value={filters.time_filter}
            onChange={(e) => handleFilterChange('time_filter', e.target.value)}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            disabled={isLoading}
          >
            {options.time_filter_options?.map((option) => (
              <option key={option.value} value={option.value}>
                {option.label}
              </option>
            ))}
          </select>
        </div>
        
        {/* 영상 타입 필터 (쇼츠/롱폼) - 빠른 필터 버튼 */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            🎬 영상 타입
          </label>
          <div className="flex gap-2">
            <button
              onClick={() => handleFilterChange('video_type', '')}
              className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
                filters.video_type === '' 
                  ? 'bg-blue-500 text-white' 
                  : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
              }`}
              disabled={isLoading}
            >
              전체
            </button>
            <button
              onClick={() => handleFilterChange('video_type', 'shorts')}
              className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
                filters.video_type === 'shorts' 
                  ? 'bg-pink-500 text-white' 
                  : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
              }`}
              disabled={isLoading}
            >
              📱 쇼츠
            </button>
            <button
              onClick={() => handleFilterChange('video_type', 'long')}
              className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
                filters.video_type === 'long' 
                  ? 'bg-purple-500 text-white' 
                  : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
              }`}
              disabled={isLoading}
            >
              🎥 롱폼
            </button>
          </div>
        </div>
        
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

        {/* 지역 필터 */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            🌍 지역
          </label>
          <select
            value={filters.region}
            onChange={(e) => {
              const selectedValue = e.target.value;
              console.log('🌍 지역 선택:', selectedValue);
              console.log('🌍 현재 region 옵션들:', options.regions);
              handleFilterChange('region', selectedValue);
            }}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            disabled={isLoading}
          >
            <option value="">전체</option>
            <option value="국내">🇰🇷 국내</option>
            <option value="해외">🌏 해외</option>
          </select>
        </div>

        {/* 언어 필터 제거됨 */}
        {/* 트렌드 점수 필터 제거됨 */}

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
        {filters.video_type && (
          <span className="px-2 py-1 bg-pink-100 text-pink-800 text-xs rounded-full">
            🎬 {filters.video_type}
          </span>
        )}
        {filters.category && (
          <span className="px-2 py-1 bg-blue-100 text-blue-800 text-xs rounded-full">
            📂 {filters.category}
          </span>
        )}
        {filters.region && (
          <span className="px-2 py-1 bg-green-100 text-green-800 text-xs rounded-full">
            🌍 {filters.region}
          </span>
        )}
        {filters.min_trend_score > 50 && (
          <span className="px-2 py-1 bg-orange-100 text-orange-800 text-xs rounded-full">
            📈 {filters.min_trend_score}+ 점
          </span>
        )}
      </div>
    </div>
  );
}
