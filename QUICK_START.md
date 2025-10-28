# 🚀 빠른 시작 가이드

## 30초 안에 시작하기

### 1단계: 실행
```bash
./start.sh
```

### 2단계: 브라우저 열기
http://localhost:5173

### 3단계: 콘텐츠 생성
1. 주제 입력: "LinkedIn 성장 전략"
2. "콘텐츠 생성하기" 클릭
3. 완성! 🎉

---

## 📋 설치 (처음 한 번만)

### 백엔드 설정
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python extract_templates.py
python extract_pdf.py
```

### 프론트엔드 설정
```bash
cd frontend
npm install
```

---

## 🎯 주요 기능

### ✨ 콘텐츠 자동 생성
- 주제만 입력하면 완성된 LinkedIn 포스트 생성
- 10가지 콘텐츠 타입 지원
- 자동 해시태그 추천

### ✏️ 실시간 편집
- 생성된 콘텐츠 바로 수정
- 미리보기로 확인
- 한 번에 클립보드 복사

### 💾 콘텐츠 관리
- 마음에 드는 콘텐츠 저장
- 히스토리 관리
- 재사용 가능

---

## 🎨 콘텐츠 타입

1. **Actionable** - 실행 가능한 팁
2. **Motivational** - 영감을 주는 스토리
3. **Analytical** - 깊이 있는 분석
4. **Contrarian** - 반대 의견 제시
5. **Observation** - 트렌드 관찰
6. **X vs. Y** - 비교 분석
7. **Present/Future** - 미래 예측
8. **Listicle** - 리스트 형식

---

## 💡 예시

### 입력
```
주제: 콘텐츠 마케팅
타입: Actionable
타겟: 스타트업 마케터
```

### 출력
```
Here's the truth about 콘텐츠 마케팅 that nobody talks about...

Here's how to master 콘텐츠 마케팅:

1. Start with the basics
   Understanding the fundamentals is crucial...

2. Practice consistently
   Daily action beats occasional perfection...

[자동 생성된 완전한 콘텐츠]

#ContentMarketing #Marketing #Startup
```

---

## 🛠️ 명령어

```bash
./start.sh      # 서버 시작
./stop.sh       # 서버 종료
./build.sh      # 프로덕션 빌드
```

---

## 📞 도움말

- 📖 [전체 사용 가이드](USAGE_GUIDE.md)
- 📚 [API 문서](http://localhost:8000/docs)
- 🐛 [문제 해결](README.md#문제-해결)

---

**Happy Creating! ✨**

