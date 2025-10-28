# 🚀 빠른 배포 가이드 (메소더스 계정용)

## ✅ 준비 완료!

모든 배포 설정이 완료되었습니다. 이제 다음 단계만 따라하시면 됩니다.

---

## 📝 배포 단계

### 1️⃣ Git 초기화 및 파일 정리

```bash
cd /Users/ose-ung/Projects/methodus

# 기존 git 제거 (다른 프로젝트 연결되어 있음)
rm -rf .git

# 새로운 git 저장소 초기화
git init

# 파일 추가
git add .

# 첫 커밋
git commit -m "feat: 메소더스 쇼츠 기획 시스템 v1.0"
```

### 2️⃣ GitHub에 새 Repository 생성

1. **GitHub 접속**: https://github.com
2. **로그인**: 메소더스 계정으로
3. **New repository 클릭** (우측 상단 + 버튼)
4. **Repository 정보 입력**:
   - Repository name: `methodus-shorts-planner`
   - Description: `YouTube Shorts 콘텐츠 기획 AI 시스템`
   - Public/Private: 선택 (추천: Private)
   - **Create repository** 클릭

5. **생성된 repository URL 복사** (예: `https://github.com/methodus/methodus-shorts-planner.git`)

### 3️⃣ 로컬 프로젝트를 GitHub에 Push

생성된 Repository URL을 사용하여:

```bash
# Remote 추가 (YOUR_URL을 실제 URL로 변경)
git remote add origin https://github.com/methodus/methodus-shorts-planner.git

# Branch 이름 확인/변경
git branch -M main

# Push
git push -u origin main
```

### 4️⃣ Vercel 배포

#### A. Vercel 가입

1. **Vercel 접속**: https://vercel.com
2. **"Sign Up" 클릭**
3. **"Continue with GitHub" 선택**
4. **메소더스 GitHub 계정으로 로그인**
   - Email: `admin@methodus.kr`
   - (GitHub 비밀번호 입력)
5. **Vercel 권한 승인**

#### B. 프로젝트 Import

1. Vercel 대시보드에서 **"Add New..." → "Project"**
2. **"Import Git Repository"** 섹션
3. `methodus-shorts-planner` 선택 → **"Import"**

#### C. 프로젝트 설정

**Framework Preset**: `Other` 선택

**Root Directory**: `./` (기본값)

**Build & Output Settings** - Override 활성화:

```
Build Command:
cd frontend && npm install && npm run build

Output Directory:
frontend/dist

Install Command:
npm install
```

**Environment Variables**: 
- 현재는 필요 없음 (나중에 필요시 추가)

#### D. 배포 시작

1. **"Deploy" 버튼 클릭**
2. 배포 진행 확인 (2-3분)
3. ✅ 배포 완료!

### 5️⃣ 배포 확인

생성된 URL로 접속 (예: `https://methodus-shorts-planner.vercel.app`)

테스트:
- ✅ 메인 페이지 로드
- ✅ 쇼츠 기획 생성
- ✅ 트렌딩 비디오 조회
- ✅ 필터 기능

---

## 🎯 배포 후 설정

### Custom Domain (선택사항)

Vercel 대시보드에서:
1. Project Settings → Domains
2. 도메인 추가 (예: `shorts.methodus.kr`)
3. DNS 설정 (Vercel이 안내)

### Auto-Deploy 설정

✅ 이미 설정됨! 
- GitHub에 Push하면 자동으로 Vercel 배포

---

## ⚠️ 참고사항

### Python Backend 제한

Vercel의 Python 지원이 제한적입니다. 
만약 백엔드 오류 발생 시:

**대안 1: Railway** (추천)
- https://railway.app
- Python/FastAPI에 최적화
- 무료 $5 크레딧/월

**대안 2: Render**
- https://render.com
- 무료 플랜 제공 (sleep mode 있음)

**대안 3: 프론트엔드만 Vercel + 백엔드 별도**
- 프론트엔드: Vercel
- 백엔드: Railway/Render

### 무료 플랜 제한

- 대역폭: 100GB/월
- 빌드 시간: 100시간/월
- Function 실행: 100GB-Hrs/월

일반적인 사용에는 충분합니다!

---

## 🆘 문제 해결

### 빌드 실패 시
1. Vercel 로그 확인
2. `frontend/package.json` 확인
3. Node.js 버전 확인 (18+)

### API 연결 실패
1. Network 탭에서 API 호출 확인
2. CORS 설정 확인
3. API 경로 확인 (`/api/*`)

### 데이터 로드 안됨
- `data/` 폴더가 Git에 포함되었는지 확인
- `.gitignore` 확인

---

## 📞 도움말

- Vercel 문서: https://vercel.com/docs
- Vercel 지원: support@vercel.com
- GitHub 이슈: repository에 Issue 생성

---

**배포 성공 후:**
1. 🎉 팀에 URL 공유
2. 📱 모바일에서도 테스트
3. 🔗 북마크/즐겨찾기 추가
4. ⭐ GitHub repository Star 추가

축하합니다! 🎊

