# 🎬 Methodus - YouTube 콘텐츠 기획 시스템

YouTube Data API v3 기반 급상승 영상 분석 및 콘텐츠 기획 자동화 플랫폼입니다. 실시간 트렌드 분석으로 인기 키워드를 추출하고, AI 기반으로 콘텐츠 아이디어와 기획서를 자동 생성합니다.

## ✨ 주요 기능

### 🔥 1단계: 실시간 트렌드 분석
- **YouTube Data API v3 연동**: 공식 API로 안정적인 데이터 수집
- **급상승 영상 수집**: 한국/미국/일본 3개 지역 실시간 트렌드
- **쇼츠 & 롱폼 구분**: 영상 타입별 필터링 및 분석
- **다양한 필터**: 카테고리, 지역, 언어, 트렌드 점수 등

### 🔑 2단계: 키워드 분석
- **인기 키워드 자동 추출**: 급상승 영상에서 핫 키워드 분석
- **카테고리별 분석**: 각 카테고리의 트렌드 키워드
- **트렌드 인사이트**: 바이럴 공통 요소 및 성공 패턴 분석

### 💡 3단계: 콘텐츠 아이디어 생성
- **원클릭 아이디어 생성**: 키워드 클릭만으로 아이디어 자동 생성
- **제목 패턴 추천**: 검증된 제목 템플릿 제공
- **훅(Hook) 아이디어**: 시청자를 사로잡는 오프닝 제안

### 📋 4단계: 기획서 자동 생성
- **자동 플로우**: 키워드 → 아이디어 → 기획서 한번에
- **상세 콘텐츠 구조**: 인트로/본문/아웃트로 구성
- **최적화 팁**: SEO 및 바이럴 전략 제공
- **해시태그 자동 생성**: 트렌드 기반 해시태그 추천

### 🚀 추가 기능
- **무한 스크롤**: 끊김 없는 영상 탐색
- **실시간 업데이트**: 2시간마다 자동 데이터 갱신
- **스마트 캐싱**: API 할당량 최적화 (일일 0.36% 사용)
- **반응형 디자인**: 모바일/태블릿/데스크탑 완벽 지원

## 🛠️ 기술 스택

### Backend
- **FastAPI**: 고성능 Python 웹 프레임워크
- **Python 3.9+**: 백엔드 로직
- **YouTube Data API v3**: 공식 YouTube 데이터 수집
- **Google API Python Client**: YouTube API 클라이언트

### Frontend
- **React 18**: UI 프레임워크
- **TypeScript**: 타입 안정성
- **Vite**: 빠른 개발 서버
- **Tailwind CSS**: 유틸리티 기반 CSS
- **Framer Motion**: 애니메이션

## 📦 설치 및 실행

### 1. 저장소 클론
```bash
git clone <repository-url>
cd methodus
```

### 2. YouTube API 키 발급 ⭐ **중요!**
YouTube Data API v3 키가 필요합니다. 상세 가이드는 [`YOUTUBE_API_SETUP.md`](YOUTUBE_API_SETUP.md)를 참조하세요.

**빠른 가이드:**
1. [Google Cloud Console](https://console.cloud.google.com/) 접속
2. 새 프로젝트 생성
3. YouTube Data API v3 활성화
4. API 키 생성
5. `.env` 파일에 키 추가

### 3. 백엔드 설정
```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 4. 환경 변수 설정
`backend/.env` 파일 생성:
```env
YOUTUBE_API_KEY=여기에_발급받은_API_키_입력
```

### 5. 프론트엔드 설정
```bash
cd ../frontend
npm install
```

### 6. 서버 실행

#### 백엔드 실행 (터미널 1)
```bash
cd backend
source venv/bin/activate
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

#### 프론트엔드 실행 (터미널 2)
```bash
cd frontend
npm run dev
```

### 7. 브라우저에서 접속
- **프론트엔드**: http://localhost:5173
- **API 문서**: http://localhost:8000/docs
- **API 상태**: http://localhost:8000/api/health

## 🎯 사용 방법

### 1️⃣ 급상승 영상 확인
- 자동으로 한국/미국/일본 트렌드 영상 표시
- 쇼츠/롱폼 빠른 필터로 원하는 타입 선택
- 카테고리, 지역, 언어 필터 적용

### 2️⃣ 인기 키워드 파악
- "키워드 분석" 탭 클릭
- 전체 인기 키워드 또는 카테고리별 키워드 확인
- 트렌드 인사이트로 성공 패턴 분석

### 3️⃣ 콘텐츠 아이디어 생성
- 관심 있는 키워드 클릭
- 자동으로 제목 패턴, 훅, 아이디어 생성
- 마음에 드는 아이디어 선택

### 4️⃣ 기획서 자동 완성
- 아이디어 클릭 시 자동으로 기획서 생성
- 콘텐츠 구조, 제목 옵션, 해시태그, 최적화 팁 확인
- 복사하여 바로 사용

### 💡 팁
- **자동 플로우**: 키워드 클릭만으로 아이디어 → 기획서까지 자동 생성
- **새로고침**: 🔄 버튼으로 최신 트렌드 데이터 즉시 업데이트
- **필터 활용**: 원하는 카테고리와 지역에 집중

## 📂 프로젝트 구조

```
methodus/
├── backend/
│   ├── main.py                 # FastAPI 메인 애플리케이션
│   ├── content_generator.py    # 콘텐츠 생성 엔진
│   ├── extract_templates.py    # Excel 템플릿 추출
│   ├── extract_pdf.py          # PDF 콘텐츠 추출
│   ├── config.py               # 설정 파일
│   ├── requirements.txt        # Python 의존성
│   └── venv/                   # 가상환경
│
├── frontend/
│   ├── src/
│   │   ├── components/         # React 컴포넌트
│   │   │   ├── ContentForm.tsx
│   │   │   ├── ContentDisplay.tsx
│   │   │   └── SavedContentList.tsx
│   │   ├── services/
│   │   │   └── api.ts          # API 클라이언트
│   │   ├── App.tsx             # 메인 앱
│   │   ├── index.css           # 전역 스타일
│   │   └── main.tsx            # 엔트리 포인트
│   ├── package.json
│   ├── tailwind.config.js      # Tailwind 설정
│   └── vite.config.ts          # Vite 설정
│
├── data/
│   ├── templates.json          # 추출된 템플릿
│   ├── knowledge_base.json     # PDF 지식 베이스
│   └── saved_content.json      # 저장된 콘텐츠
│
└── README.md
```

## 🎨 템플릿 정보

### 콘텐츠 구조
1. **Trailer-Meat-Summary-CTC**: Hook → 핵심 내용 → 요약 → Call-to-Action
2. **Story-Based**: 스토리텔링 기반 콘텐츠
3. **Listicle**: 리스트 형식 콘텐츠

### 콘텐츠 타입
- **Actionable**: 실행 가능한 단계별 가이드
- **Motivational**: 영감을 주는 스토리
- **Analytical**: 분석 및 해부
- **Contrarian**: 기존 관념에 도전
- **Observation**: 관찰 및 인사이트
- **X vs. Y**: 비교 분석
- **Present/Future**: 현재와 미래 비교
- **Listicle**: 목록형 콘텐츠

## 📊 API 엔드포인트

### YouTube 트렌드 분석
- `GET /api/youtube/trending` - 급상승 영상 조회 (필터링 지원)
- `GET /api/youtube/filter-options` - 필터 옵션 목록
- `POST /api/youtube/force-refresh` - 강제 데이터 갱신

### 시스템
- `GET /` - API 상태 및 버전 정보
- `GET /api/health` - 서버 상태 확인 (YouTube API 연결 상태 포함)

**자세한 API 문서**: http://localhost:8000/docs

### API 응답 예시
```json
{
  "trending_videos": [...],
  "count": 20,
  "total_count": 90,
  "last_updated": "2025-11-12T...",
  "source": "youtube_api_v3"
}
```

## 🔧 환경 변수

백엔드 디렉토리에 `.env` 파일을 생성하여 설정:

```env
# YouTube Data API v3 (필수)
YOUTUBE_API_KEY=AIzaSy...

# CORS 설정 (선택사항)
CORS_ORIGINS=http://localhost:5173,http://localhost:3000
```

**⚠️ 주의사항:**
- YouTube API 키는 필수입니다
- API 키 발급 방법은 [`YOUTUBE_API_SETUP.md`](YOUTUBE_API_SETUP.md) 참조
- `.env` 파일은 절대 Git에 커밋하지 마세요 (이미 `.gitignore`에 포함됨)

## 🚀 프로덕션 빌드

### 백엔드
```bash
cd backend
source venv/bin/activate
pip install gunicorn
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000
```

### 프론트엔드
```bash
cd frontend
npm run build
# dist 폴더를 웹 서버에 배포
```

## 📈 API 할당량 관리

### 일일 사용량
- **기본 할당량**: 10,000 units/day
- **실제 사용량**: ~36 units/day (0.36%)
- **99.6% 여유**: 충분한 할당량

### 최적화 전략
- ✅ **배치 처리**: 50개 영상을 1 unit으로 조회
- ✅ **스마트 캐싱**: 2시간마다만 업데이트
- ✅ **자동 관리**: 할당량 초과 방지 로직

자세한 내용은 [`API_OPTIMIZATION.md`](backend/API_OPTIMIZATION.md) 참조

---

## 🚨 문제 해결

### "API key not valid" 오류
1. `.env` 파일에 API 키가 올바르게 입력되었는지 확인
2. Google Cloud Console에서 YouTube Data API v3가 활성화되었는지 확인
3. API 키 제한 설정 확인

### "Quota exceeded" 오류
- 일일 할당량(10,000 units) 초과 시 발생
- 내일까지 대기하거나 캐시된 데이터 사용
- 정상 사용 시 할당량 초과 가능성 매우 낮음 (0.36% 사용)

### 백엔드 연결 실패
1. 백엔드 서버가 실행 중인지 확인 (`uvicorn main:app --reload`)
2. 포트 8000이 사용 중인지 확인
3. CORS 설정 확인

상세한 문제 해결은 [`YOUTUBE_API_SETUP.md`](YOUTUBE_API_SETUP.md#문제-해결) 참조

---

## 📚 문서

- **[YouTube API 설정 가이드](YOUTUBE_API_SETUP.md)**: API 키 발급 및 설정 방법
- **[API 할당량 최적화](backend/API_OPTIMIZATION.md)**: 효율적인 API 사용 전략
- **[API 문서](http://localhost:8000/docs)**: 백엔드 API 상세 문서 (실행 후 접속)

---

## 🙏 감사의 말

- **Google/YouTube**: YouTube Data API v3 제공
- **FastAPI**: 훌륭한 Python 웹 프레임워크
- **React & Vite**: 현대적인 프론트엔드 개발 도구

## 📞 문의

문제가 발생하거나 제안사항이 있으시면 이슈를 등록해주세요.

---

**Built with ❤️ for YouTube Content Creators 🎬**
