# 🚀 Content Creator AI - LinkedIn 콘텐츠 자동 생성 플랫폼

AI 기반 LinkedIn 콘텐츠 자동 생성 플랫폼입니다. Justin Welsh의 Content Operating System을 기반으로 주제만 입력하면 전문적인 LinkedIn 콘텐츠가 자동으로 생성됩니다.

## ✨ 주요 기능

- 🎯 **주제 기반 자동 생성**: 주제만 입력하면 LinkedIn 콘텐츠 자동 생성
- 📝 **다양한 콘텐츠 구조**: Trailer-Meat-Summary-CTC, Story-Based, Listicle 등
- 🎨 **10가지 콘텐츠 타입**: Actionable, Motivational, Analytical, Contrarian 등
- ✏️ **실시간 편집**: 생성된 콘텐츠를 바로 수정 가능
- 💾 **저장 및 히스토리**: 생성한 콘텐츠 저장 및 재사용
- 🏷️ **자동 해시태그**: 주제에 맞는 해시태그 자동 추천
- 📊 **통계 분석**: 단어 수, 글자 수 등 실시간 통계
- 🎭 **모던한 UI**: Tailwind CSS 기반의 아름다운 디자인
- 📱 **반응형 디자인**: 모바일, 태블릿, 데스크탑 모두 지원

## 🛠️ 기술 스택

### Backend
- **FastAPI**: 고성능 Python 웹 프레임워크
- **Python 3.9+**: 백엔드 로직
- **OpenPyXL**: Excel 템플릿 처리
- **PyPDF2**: PDF 콘텐츠 추출

### Frontend
- **React 18**: UI 프레임워크
- **TypeScript**: 타입 안정성
- **Vite**: 빠른 개발 서버
- **Tailwind CSS**: 유틸리티 기반 CSS
- **Framer Motion**: 애니메이션
- **React Hot Toast**: 알림 시스템
- **Axios**: HTTP 클라이언트

## 📦 설치 및 실행

### 1. 저장소 클론
```bash
cd /Users/ose-ung/Projects/methodus
```

### 2. 백엔드 설정
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. 프론트엔드 설정
```bash
cd ../frontend
npm install
```

### 4. 템플릿 데이터 추출 (최초 1회)
```bash
cd ../backend
source venv/bin/activate
python extract_templates.py
python extract_pdf.py
```

### 5. 서버 실행

#### 백엔드 실행
```bash
cd backend
source venv/bin/activate
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

#### 프론트엔드 실행 (새 터미널)
```bash
cd frontend
npm run dev
```

### 6. 브라우저에서 접속
- 프론트엔드: http://localhost:5173
- API 문서: http://localhost:8000/docs

## 🎯 사용 방법

### 1. 콘텐츠 생성
1. 주제 입력란에 원하는 주제 입력 (예: "LinkedIn 성장 전략")
2. 콘텐츠 구조 선택 (Trailer-Meat-Summary-CTC 추천)
3. 콘텐츠 타입 선택 (Actionable, Motivational 등)
4. 타겟 오디언스 입력 (선택사항)
5. 톤앤매너 선택
6. "콘텐츠 생성하기" 버튼 클릭

### 2. 콘텐츠 편집
- 생성된 콘텐츠 우측 상단의 편집 버튼 클릭
- 텍스트 수정 후 "수정 완료" 버튼 클릭

### 3. 콘텐츠 저장
- 저장 버튼 클릭하여 나중에 다시 사용 가능
- "저장된 콘텐츠" 버튼으로 저장된 목록 확인

### 4. 콘텐츠 복사
- 복사 버튼 클릭하여 클립보드에 복사
- LinkedIn에 바로 붙여넣기 가능

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

- `POST /api/generate` - 콘텐츠 생성
- `GET /api/structures` - 콘텐츠 구조 목록
- `GET /api/content-types` - 콘텐츠 타입 목록
- `GET /api/topics` - 추천 주제 목록
- `POST /api/save` - 콘텐츠 저장
- `GET /api/saved` - 저장된 콘텐츠 조회
- `DELETE /api/saved/{id}` - 콘텐츠 삭제
- `GET /api/health` - 서버 상태 확인

자세한 API 문서는 http://localhost:8000/docs 에서 확인하세요.

## 🔧 환경 변수

백엔드 디렉토리에 `.env` 파일을 생성하여 설정:

```env
OPENAI_API_KEY=your_openai_api_key_here  # (선택사항)
ANTHROPIC_API_KEY=your_anthropic_api_key_here  # (선택사항)
CORS_ORIGINS=http://localhost:3000,http://localhost:5173
```

*현재는 규칙 기반 생성 시스템으로 작동하므로 API 키 없이도 사용 가능합니다.*

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

## 📝 라이선스

이 프로젝트는 Justin Welsh의 Content Operating System을 기반으로 제작되었습니다.

## 🙏 감사의 말

- **Justin Welsh**: Content Operating System 프레임워크 제공
- **FastAPI**: 훌륭한 Python 웹 프레임워크
- **React & Vite**: 현대적인 프론트엔드 개발 도구

## 📞 문의

문제가 발생하거나 제안사항이 있으시면 이슈를 등록해주세요.

---

**Built with ❤️ for Content Creators**
