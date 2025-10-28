# 🚀 Vercel 배포 가이드 - 메소더스 쇼츠 기획 시스템

## 📋 준비사항

### 1. GitHub 계정 연동 준비
- 메소더스 이메일: `admin@methodus.kr`
- GitHub 로그인 사용

### 2. 새로운 GitHub Repository 생성

1. **GitHub에 로그인**: https://github.com
2. **New Repository 클릭**
3. **Repository 설정**:
   - Repository name: `methodus-shorts-planner`
   - Description: `YouTube Shorts 콘텐츠 기획 AI 시스템`
   - Public 또는 Private 선택
   - **Create repository** 클릭

### 3. 프로젝트를 새 Repository에 Push

터미널에서 다음 명령어 실행:

```bash
cd /Users/ose-ung/Projects/methodus

# 기존 git 연결 제거
rm -rf .git

# 새로운 git 저장소 초기화
git init

# 파일 추가
git add .

# 첫 커밋
git commit -m "Initial commit: 메소더스 쇼츠 기획 시스템"

# GitHub repository 연결 (YOUR_USERNAME을 실제 GitHub 사용자명으로 변경)
git remote add origin https://github.com/YOUR_USERNAME/methodus-shorts-planner.git

# Push
git branch -M main
git push -u origin main
```

## 🌐 Vercel 배포 단계

### Step 1: Vercel 가입

1. **Vercel 웹사이트 방문**: https://vercel.com
2. **"Sign Up" 클릭**
3. **"Continue with GitHub" 선택**
4. **GitHub 계정으로 로그인** (admin@methodus.kr)
5. **Vercel에 GitHub 연동 허용**

### Step 2: 프로젝트 Import

1. Vercel 대시보드에서 **"Add New..." → "Project" 클릭**
2. **"Import Git Repository" 섹션**에서 GitHub repository 선택
3. `methodus-shorts-planner` repository를 찾아서 **"Import" 클릭**

### Step 3: 프로젝트 설정

#### Build & Development Settings:

**Framework Preset**: 
- `Other` 선택

**Root Directory**: 
- `./` (기본값 유지)

**Build Command** (프론트엔드):
```bash
cd frontend && npm install && npm run build
```

**Output Directory** (프론트엔드):
```
frontend/dist
```

**Install Command**:
```bash
npm install
```

#### Environment Variables (선택사항):

현재는 필요 없지만, 나중에 API 키가 필요하면:
- `OPENAI_API_KEY` = `your-key-here`
- `ANTHROPIC_API_KEY` = `your-key-here`

### Step 4: 배포 시작

1. **"Deploy" 버튼 클릭**
2. 배포 진행 상황 확인 (약 2-3분 소요)
3. 배포 완료 후 **생성된 URL 확인** (예: `https://methodus-shorts-planner.vercel.app`)

## 🎯 배포 후 확인사항

### 1. 프론트엔드 확인
- 생성된 Vercel URL로 접속
- UI가 정상적으로 표시되는지 확인

### 2. 백엔드 API 확인
- `https://your-app.vercel.app/api/health` 접속
- API가 정상 응답하는지 확인

### 3. 기능 테스트
- 쇼츠 콘텐츠 기획 생성
- 트렌딩 비디오 조회
- 필터링 기능

## ⚠️ 주의사항

### Vercel 무료 플랜 제한:
- **월 대역폭**: 100GB
- **빌드 시간**: 월 100시간
- **Serverless Function 실행 시간**: 월 100GB-Hrs
- **동시 빌드**: 1개

### Python Backend 이슈:
Vercel의 Python 지원이 제한적이므로, 백엔드가 복잡하면 다음 대안 고려:
- **Railway** (https://railway.app) - Python/FastAPI에 최적화
- **Render** (https://render.com) - 무료 플랜 제공
- **Fly.io** - 컨테이너 기반 배포

## 🔧 트러블슈팅

### 빌드 실패 시:
1. Vercel 로그 확인
2. `package.json` 의존성 확인
3. Python 버전 호환성 확인

### API 연결 안되면:
1. CORS 설정 확인
2. API 경로 확인 (`/api/` prefix)
3. Vercel Function 로그 확인

### 데이터 파일 문제:
- `/data` 폴더의 JSON 파일들이 포함되었는지 확인
- `.gitignore`에서 필요한 파일 제외되지 않았는지 확인

## 📞 추가 도움

배포 중 문제가 발생하면:
1. Vercel 문서: https://vercel.com/docs
2. Vercel Discord: https://vercel.com/discord
3. GitHub Issues 확인

---

**배포 완료 후 팀에 공유할 정보:**
- 🌐 배포된 URL
- 📱 테스트 결과
- 🔗 GitHub Repository 링크

