# 🚀 Render로 백엔드 배포하기

## 📋 단계별 가이드

### 1️⃣ Render 가입 및 로그인

1. **Render 접속**: https://render.com
2. **Sign Up** 클릭
3. **GitHub로 로그인** (메소더스 계정 사용)
4. **GitHub 권한 승인**

### 2️⃣ 새 Web Service 생성

1. **Dashboard**에서 **"New +"** 클릭
2. **"Web Service"** 선택
3. **"Build and deploy from a Git repository"** 선택
4. **Repository 연결**:
   - Repository: `methodus-shorts-planner`
   - Branch: `main`
   - Root Directory: `backend`

### 3️⃣ 서비스 설정

**Basic Settings:**
- **Name**: `methodus-shorts-backend`
- **Environment**: `Python 3`
- **Region**: `Oregon (US West)`

**Build & Deploy:**
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`

**Advanced Settings:**
- **Auto-Deploy**: `Yes` (GitHub push 시 자동 배포)

### 4️⃣ 환경변수 설정 (선택사항)

현재는 필요 없지만, 나중에 필요하면:
- `PYTHON_VERSION` = `3.13`

### 5️⃣ 배포 시작

1. **"Create Web Service"** 클릭
2. 배포 진행 상황 확인 (약 3-5분)
3. **배포 완료 후 URL 확인** (예: `https://methodus-shorts-backend.onrender.com`)

### 6️⃣ 프론트엔드 API URL 업데이트

배포 완료 후:

1. Render에서 생성된 URL 복사
2. `frontend/src/services/api.ts` 파일에서 URL 업데이트:

```typescript
const API_BASE_URL = import.meta.env.VITE_API_URL 
  ? `${import.meta.env.VITE_API_URL}/api`
  : (import.meta.env.PROD 
      ? 'https://methodus-shorts-backend.onrender.com/api'  // Render URL로 변경
      : 'http://localhost:8000/api');
```

3. Vercel에 재배포

## 🎯 예상 결과

배포 완료 후:
- ✅ 실제 YouTube Shorts 데이터 표시
- ✅ 실시간 트렌드 분석
- ✅ 키워드 분석 작동
- ✅ 콘텐츠 기획서 생성 가능

## 💰 비용

- **Render 무료 플랜**: 
  - 월 750시간 무료
  - Sleep mode (15분 비활성 시 자동 sleep)
  - 일반적인 사용에는 충분

## 🆘 문제 해결

### 빌드 실패 시:
1. Render 로그 확인
2. Python 버전 호환성 확인
3. requirements.txt 의존성 확인

### API 연결 실패:
1. CORS 설정 확인
2. Render URL 정확성 확인
3. 프론트엔드 API URL 업데이트 확인

---

**Render 배포 후 전체 시스템이 실제 데이터로 작동할 것입니다!** 🎉
