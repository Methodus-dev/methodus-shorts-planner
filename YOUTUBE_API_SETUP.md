# 🔑 YouTube Data API v3 설정 가이드

## 📝 개요

이 가이드는 Methodus 프로젝트에서 YouTube Data API v3를 사용하기 위한 API 키 발급 및 설정 방법을 안내합니다.

---

## 🚀 1단계: Google Cloud Console 프로젝트 생성

### 1.1 Google Cloud Console 접속
1. [Google Cloud Console](https://console.cloud.google.com/) 접속
2. Google 계정으로 로그인

### 1.2 새 프로젝트 생성
1. 상단 프로젝트 선택 드롭다운 클릭
2. "새 프로젝트" 클릭
3. 프로젝트 이름 입력: `Methodus-YouTube-API` (또는 원하는 이름)
4. "만들기" 클릭
5. 프로젝트가 생성될 때까지 대기 (약 10-30초)

---

## 🔧 2단계: YouTube Data API v3 활성화

### 2.1 API 라이브러리로 이동
1. 왼쪽 메뉴에서 "API 및 서비스" > "라이브러리" 클릭
2. 또는 직접 링크: https://console.cloud.google.com/apis/library

### 2.2 YouTube Data API v3 검색 및 활성화
1. 검색창에 `YouTube Data API v3` 입력
2. "YouTube Data API v3" 클릭
3. **"사용 설정"** 버튼 클릭
4. API가 활성화될 때까지 대기

---

## 🎫 3단계: API 키 생성

### 3.1 사용자 인증 정보 만들기
1. 왼쪽 메뉴에서 "API 및 서비스" > "사용자 인증 정보" 클릭
2. 상단의 **"+ 사용자 인증 정보 만들기"** 버튼 클릭
3. **"API 키"** 선택

### 3.2 API 키 복사
1. API 키가 생성되면 팝업 창이 나타납니다
2. **API 키를 복사**하여 안전한 곳에 저장하세요
3. 형식: `AIzaSy...` (약 39자)

### 3.3 API 키 제한 설정 (권장)
보안을 위해 API 키에 제한을 설정하는 것이 좋습니다:

1. 생성된 API 키 옆의 편집 버튼 클릭
2. **"API 제한사항"** 섹션에서:
   - "키 제한" 선택
   - "YouTube Data API v3" 체크
3. **"애플리케이션 제한사항"** (선택사항):
   - 로컬 개발: "없음" 선택
   - 프로덕션: "HTTP 리퍼러" 선택 후 도메인 추가
4. **"저장"** 클릭

---

## ⚙️ 4단계: 프로젝트에 API 키 설정

### 4.1 환경 변수 파일 생성
백엔드 디렉토리에 `.env` 파일을 생성합니다:

```bash
cd /Users/ose-ung/Projects/methodus/backend
touch .env
```

### 4.2 API 키 추가
`.env` 파일에 다음 내용을 추가합니다:

```env
# YouTube Data API v3
YOUTUBE_API_KEY=여기에_발급받은_API_키_붙여넣기

# 예시:
# YOUTUBE_API_KEY=AIzaSyBx1234567890abcdefghijklmnopqrst

# CORS 설정 (선택사항)
CORS_ORIGINS=http://localhost:5173,http://localhost:3000
```

### 4.3 .env 파일 보안
`.gitignore` 파일에 `.env`가 포함되어 있는지 확인:

```bash
# .gitignore 파일 확인
cat .gitignore | grep ".env"

# 없다면 추가
echo ".env" >> .gitignore
```

---

## 📊 5단계: API 할당량 확인

### 5.1 할당량 정보
YouTube Data API v3는 무료로 사용할 수 있지만 **일일 할당량**이 있습니다:

- **기본 할당량**: 10,000 units/day
- **비용 계산**:
  - `search.list`: 100 units
  - `videos.list`: 1 unit
  - `channels.list`: 1 unit

### 5.2 할당량 최적화 전략 (Methodus에서 구현됨)
1. **캐싱**: 동일한 요청 결과를 캐시하여 재사용
2. **배치 처리**: 여러 비디오 ID를 한 번에 조회 (최대 50개)
3. **선택적 필드**: 필요한 필드만 요청
4. **스마트 새로고침**: 2시간마다 자동 업데이트

### 5.3 할당량 모니터링
1. [Google Cloud Console - API 할당량](https://console.cloud.google.com/apis/api/youtube.googleapis.com/quotas) 접속
2. 현재 사용량 및 제한 확인
3. 필요시 할당량 증가 요청 (유료)

---

## ✅ 6단계: API 키 테스트

### 6.1 간단한 테스트
터미널에서 다음 명령어로 API 키를 테스트할 수 있습니다:

```bash
# API 키를 변수에 저장
export YOUTUBE_API_KEY="여기에_API_키_입력"

# 테스트 요청 (급상승 영상 조회)
curl "https://www.googleapis.com/youtube/v3/videos?part=snippet,statistics&chart=mostPopular&regionCode=KR&maxResults=5&key=$YOUTUBE_API_KEY"
```

성공하면 JSON 형식의 영상 데이터가 반환됩니다.

### 6.2 백엔드에서 테스트
백엔드 서버를 실행하고 API가 작동하는지 확인:

```bash
cd /Users/ose-ung/Projects/methodus/backend
source venv/bin/activate
python -c "
from youtube_api_service import YouTubeAPIService
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv('YOUTUBE_API_KEY')
print(f'API 키: {api_key[:10]}...' if api_key else 'API 키 없음')

service = YouTubeAPIService(api_key)
videos = service.get_trending_videos(region_code='KR', max_results=5)
print(f'✅ 성공! {len(videos)}개 영상 조회됨')
"
```

---

## 🚨 문제 해결

### 문제 1: "API key not valid" 오류
**원인**: API 키가 잘못되었거나 제한 설정이 잘못됨
**해결**:
1. API 키를 다시 복사하여 확인
2. Google Cloud Console에서 API 키 제한 설정 확인
3. YouTube Data API v3가 활성화되어 있는지 확인

### 문제 2: "Quota exceeded" 오류
**원인**: 일일 할당량(10,000 units)을 초과함
**해결**:
1. 내일까지 대기 (할당량은 매일 자정 PST에 리셋)
2. 캐시된 데이터 사용
3. 할당량 증가 요청 (유료)

### 문제 3: "Access Not Configured" 오류
**원인**: YouTube Data API v3가 활성화되지 않음
**해결**:
1. Google Cloud Console에서 "API 및 서비스" > "라이브러리" 접속
2. YouTube Data API v3 검색 후 "사용 설정" 클릭

### 문제 4: 환경 변수를 읽을 수 없음
**원인**: `.env` 파일이 올바른 위치에 없거나 형식이 잘못됨
**해결**:
1. `.env` 파일이 `backend/` 디렉토리에 있는지 확인
2. 파일에 `YOUTUBE_API_KEY=...` 형식으로 작성되었는지 확인
3. 따옴표 없이 직접 값 입력 (예: `YOUTUBE_API_KEY=AIza...`)

---

## 📚 참고 자료

- [YouTube Data API v3 공식 문서](https://developers.google.com/youtube/v3)
- [API 할당량 계산기](https://developers.google.com/youtube/v3/determine_quota_cost)
- [Python 클라이언트 라이브러리](https://github.com/googleapis/google-api-python-client)
- [YouTube API 샘플 코드](https://developers.google.com/youtube/v3/code_samples/python)

---

## 🎉 완료!

API 키 설정이 완료되었습니다! 이제 Methodus 백엔드를 실행하면 YouTube Data API를 통해 실시간 급상승 영상 데이터를 수집할 수 있습니다.

다음 단계:
1. ✅ API 키 발급 완료
2. 🚀 백엔드 서버 실행
3. 🎨 프론트엔드에서 데이터 확인
4. 📊 트렌딩 영상 분석 시작!

---

**문제가 발생하면 이 가이드를 다시 확인하거나 이슈를 등록해주세요.**
