# 필터 시스템 테스트 가이드

## 🧪 테스트 방법

### 1. 프론트엔드 접속
```
http://localhost:5173
```

### 2. 브라우저 개발자 도구 열기
- **Mac**: `Cmd + Option + I`
- **Windows**: `F12`

### 3. Console 탭에서 확인할 내용
```javascript
// 필터 변경 시
🔧 필터 변경: category = 창업/부업
🔧 필터 변경: region = 국내
🔧 필터 변경: time_filter = today

// 필터 적용 버튼 클릭 시
🔍 필터 적용 버튼 클릭: {category: '창업/부업', region: '국내', time_filter: 'today', ...}
🔄 데이터 로드 시작: {reset: true, forceRefresh: false, filters: {...}}
📡 API 호출: {requestCount: 20, filters: {...}}
🔍 API 호출: http://localhost:8000/api/youtube/trending?count=20&category=창업/부업&region=국내&time_filter=today&...
```

### 4. Network 탭에서 확인
- **Filter**: `trending`
- **요청 URL 확인**:
  ```
  http://localhost:8000/api/youtube/trending?
    count=20
    &category=창업/부업
    &region=국내
    &time_filter=today
    &min_trend_score=50
    &sort_by=trend_score
  ```

## ✅ 예상 결과

### 테스트 케이스 1: 카테고리만
- **필터**: 카테고리 = 창업/부업
- **예상 URL**: `?category=창업/부업&...`
- **예상 결과**: 창업/부업 카테고리 영상만 표시

### 테스트 케이스 2: 지역만
- **필터**: 지역 = 국내
- **예상 URL**: `?region=국내&...`
- **예상 결과**: 한국어 영상만 표시

### 테스트 케이스 3: 기간만
- **필터**: 기간 = 오늘
- **예상 URL**: `?time_filter=today&...`
- **예상 결과**: 최근 24시간 내 크롤링된 영상만 표시

### 테스트 케이스 4: 복합 필터
- **필터**: 
  - 카테고리 = 재테크/금융
  - 지역 = 국내
  - 기간 = 이번 주
- **예상 URL**: `?category=재테크/금융&region=국내&time_filter=week&...`
- **예상 결과**: 재테크/금융 + 국내 + 최근 7일 영상만 표시

## 🐛 문제가 있다면

### 1. 콘솔에서 확인
```javascript
// 필터 state 확인
console.log('현재 필터:', filters);

// API 요청 확인
console.log('API 호출:', requestURL);
```

### 2. 백엔드 로그 확인
```bash
tail -f /Users/ose-ung/Projects/methodus/logs/backend.log
```

로그에서 확인할 내용:
```
🔍 필터링 시작: 총 996개 영상
   카테고리 '창업/부업' 필터: 996개 → 100개
   지역 '국내' 필터: 100개 → 60개
   기간 'today' 필터: 60개 → 60개
✅ 최종 필터링 결과: 60개
```

### 3. 문제 유형별 해결

#### 문제: 필터 적용 안됨
- VideoFilters 컴포넌트의 `applyFilters` 함수 확인
- `onFiltersChange(filters)` 호출 확인

#### 문제: 기간 필터 작동 안함
- `timedelta` import 확인
- `crawled_at` 필드 존재 확인

#### 문제: URL에 필터 파라미터 없음
- `api.ts`의 `URLSearchParams` 생성 부분 확인
- 필터 값이 빈 문자열인지 확인

## 📊 디버깅 팁

### 콘솔에서 실시간 확인
```javascript
// 프론트엔드 콘솔에 붙여넣기
window.addEventListener('fetch', (e) => {
  console.log('Fetch:', e.request.url);
});
```

### 백엔드 로그 실시간 확인
```bash
tail -f /Users/ose-ung/Projects/methodus/logs/backend.log | grep "필터"
```

## 🎯 성공 기준

1. ✅ 필터 선택 시 콘솔에 로그 출력
2. ✅ 필터 적용 버튼 클릭 시 API 호출
3. ✅ API URL에 선택한 필터 파라미터 포함
4. ✅ 백엔드 로그에 필터링 단계 출력
5. ✅ 화면에 필터링된 결과만 표시

