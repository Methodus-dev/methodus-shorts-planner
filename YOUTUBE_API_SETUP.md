# YouTube Data API 설정 가이드

## 1. Google Cloud Console 접속
https://console.cloud.google.com/

## 2. 프로젝트 생성
- "프로젝트 만들기" 클릭
- 프로젝트 이름: "Methodus Shorts Planner"

## 3. YouTube Data API v3 활성화
1. 왼쪽 메뉴 → "API 및 서비스" → "라이브러리"
2. "YouTube Data API v3" 검색
3. "사용 설정" 클릭

## 4. API 키 생성
1. 왼쪽 메뉴 → "API 및 서비스" → "사용자 인증 정보"
2. "+ 사용자 인증 정보 만들기" → "API 키" 선택
3. API 키 복사

## 5. API 키 설정
```bash
cd /Users/ose-ung/Projects/methodus/backend
echo 'YOUTUBE_API_KEY=여기에_복사한_API_키_붙여넣기' > .env
```

## 6. 서버 재시작
```bash
cd /Users/ose-ung/Projects/methodus
./stop.sh
./start.sh
```

완료! 이제 실제 급상승 Shorts가 자동으로 수집됩니다.
