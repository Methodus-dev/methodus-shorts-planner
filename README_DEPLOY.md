# 🎯 메소더스 쇼츠 기획 시스템

YouTube Shorts 콘텐츠를 위한 AI 기획 도구

## ✨ 주요 기능

- 🎬 **쇼츠 콘텐츠 기획**: 8가지 콘텐츠 타입 지원
- 📊 **실시간 트렌드 분석**: YouTube Shorts 급상승 영상 추적
- 🎯 **니치 전략**: 타겟 청중 분석 및 차별화 전략
- 💡 **훅 생성기**: 시선을 사로잡는 오프닝 아이디어
- #️⃣ **해시태그 전략**: 최적 해시태그 제안
- 📈 **바이럴 최적화**: 조회수 극대화 체크리스트

## 🚀 빠른 시작

### 로컬 개발

```bash
# 서버 시작
./start.sh

# 접속
프론트엔드: http://localhost:5173
백엔드 API: http://localhost:8000
API 문서: http://localhost:8000/docs

# 서버 종료
./stop.sh
```

## 📦 배포

### Vercel 배포 (추천)

**빠른 배포 가이드**: `QUICK_DEPLOY.md` 참고

1. GitHub에 Repository 생성
2. 코드 Push
3. Vercel에서 Import
4. 자동 배포 완료!

**상세 가이드**: `DEPLOYMENT_GUIDE.md` 참고

## 🛠 기술 스택

### Frontend
- React 18 + TypeScript
- Vite
- TailwindCSS
- Framer Motion
- Axios

### Backend
- FastAPI (Python 3.13)
- Uvicorn
- YouTube Data API
- BeautifulSoup4 (웹 크롤링)

## 📂 프로젝트 구조

```
methodus/
├── frontend/          # React 프론트엔드
│   ├── src/
│   │   ├── components/
│   │   ├── services/
│   │   └── App.tsx
│   └── dist/         # 빌드 결과물
├── backend/          # FastAPI 백엔드
│   ├── main.py       # API 엔트리포인트
│   ├── shorts_planner.py
│   ├── youtube_shorts_crawler.py
│   └── requirements.txt
├── data/             # JSON 데이터
│   ├── shorts_system.json
│   ├── templates.json
│   └── youtube_shorts_cache.json
└── vercel.json       # Vercel 배포 설정
```

## 🌐 API 엔드포인트

### 콘텐츠 기획
- `POST /api/create-plan` - 콘텐츠 기획서 생성
- `POST /api/analyze-niche` - 니치 분석
- `POST /api/generate-hooks` - 훅 아이디어 생성
- `GET /api/content-types` - 콘텐츠 타입 목록

### YouTube 트렌드
- `GET /api/youtube/trending` - 급상승 Shorts
- `POST /api/youtube/refresh` - 실시간 크롤링
- `GET /api/youtube/filter-options` - 필터 옵션
- `GET /api/youtube/category-keywords/{category}` - 카테고리 키워드

### 저장/관리
- `POST /api/save-plan` - 기획서 저장
- `GET /api/saved-plans` - 저장 목록
- `DELETE /api/saved-plans/{id}` - 기획서 삭제

전체 API 문서: `http://localhost:8000/docs`

## 📝 사용 가이드

1. **주제 입력**: 원하는 쇼츠 주제 입력
2. **타입 선택**: 8가지 콘텐츠 타입 중 선택
3. **기획서 생성**: AI가 완성된 기획서 생성
4. **트렌드 확인**: 급상승 Shorts 분석
5. **최적화**: 체크리스트로 완성도 높이기

## 🔒 보안

- API 키는 환경변수로 관리
- CORS 설정으로 허용된 도메인만 접근
- 민감 정보는 `.gitignore`로 제외

## 📄 라이선스

Proprietary - Methodus

## 👥 팀

**Methodus**
- Email: admin@methodus.kr
- Website: https://methodus.kr

---

Made with ❤️ by Methodus

