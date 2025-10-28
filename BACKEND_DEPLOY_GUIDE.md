# 🚀 백엔드 배포 가이드 (Railway)

## 📋 문제 상황
- Vercel에서 Python 백엔드가 제대로 작동하지 않음
- API 호출이 404 에러 반환
- 프론트엔드는 정상 작동하지만 데이터를 가져올 수 없음

## 🔧 해결 방법: Railway로 백엔드 배포

### 1️⃣ Railway 가입 및 설정

1. **Railway 접속**: https://railway.app
2. **GitHub로 로그인**: 메소더스 계정 사용
3. **New Project** 클릭
4. **Deploy from GitHub repo** 선택
5. `methodus-shorts-planner` repository 선택
6. **Root Directory** 설정: `backend`

### 2️⃣ 환경변수 설정 (Railway 대시보드)

Railway 프로젝트 → Variables 탭에서 추가:

```
PYTHON_VERSION=3.13
PORT=8000
```

### 3️⃣ 배포 설정 확인

Railway가 자동으로 다음 파일들을 인식합니다:
- `railway.json` - 배포 설정
- `Procfile` - 시작 명령어
- `requirements.txt` - Python 의존성
- `runtime.txt` - Python 버전

### 4️⃣ 배포 시작

Railway가 자동으로 배포를 시작합니다. 
- 빌드 시간: 약 2-3분
- 배포 완료 후 URL 생성 (예: `https://methodus-shorts-planner-production.up.railway.app`)

### 5️⃣ 프론트엔드 API URL 업데이트

백엔드 배포 완료 후:

1. Railway에서 생성된 URL 확인
2. 프론트엔드 `api.ts` 파일에서 API URL 업데이트:

```typescript
const API_BASE_URL = import.meta.env.VITE_API_URL 
  ? `${import.meta.env.VITE_API_URL}/api`
  : (import.meta.env.PROD 
      ? 'https://your-railway-url.up.railway.app/api'  // Railway URL로 변경
      : 'http://localhost:8000/api');
```

3. Vercel에 재배포

### 6️⃣ 테스트

1. Railway URL + `/api/health` 접속하여 API 상태 확인
2. Railway URL + `/api/youtube/trending` 접속하여 데이터 확인
3. Vercel 프론트엔드에서 데이터 로드 확인

## 🎯 대안: Render 사용

Railway 대신 Render 사용 가능:

1. **Render 접속**: https://render.com
2. **New Web Service**
3. **Build Command**: `pip install -r requirements.txt`
4. **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`

## 📊 예상 결과

백엔드 배포 완료 후:
- ✅ 프론트엔드에서 데이터 정상 로드
- ✅ 급상승 동영상 표시
- ✅ 키워드 분석 작동
- ✅ 콘텐츠 기획서 생성 가능

## 💰 비용

- **Railway**: 무료 $5 크레딧/월
- **Render**: 무료 플랜 (sleep mode 있음)

일반적인 사용에는 무료 플랜으로 충분합니다!

---

## 🆘 문제 해결

### 빌드 실패 시:
1. Railway 로그 확인
2. Python 버전 호환성 확인
3. requirements.txt 의존성 확인

### API 연결 실패:
1. CORS 설정 확인
2. Railway URL 정확성 확인
3. 프론트엔드 API URL 업데이트 확인

---

**백엔드 배포 후 전체 시스템이 정상 작동할 것입니다!** 🎉
