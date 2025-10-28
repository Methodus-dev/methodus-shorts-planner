#!/bin/bash

# Content Creator AI 프로덕션 빌드 스크립트

echo "🏗️  Content Creator AI 프로덕션 빌드 시작..."

# 현재 디렉토리 확인
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# 빌드 디렉토리 생성
mkdir -p dist
mkdir -p logs

echo ""
echo "📦 백엔드 의존성 설치 중..."
cd backend
source venv/bin/activate
pip install -q -r requirements.txt
pip install -q gunicorn
echo "   ✅ 백엔드 의존성 설치 완료"

echo ""
echo "🎨 프론트엔드 빌드 중..."
cd ../frontend
npm install
npm run build
echo "   ✅ 프론트엔드 빌드 완료"

# 빌드 파일 복사
echo ""
echo "📋 빌드 파일 복사 중..."
cp -r dist ../dist/frontend
echo "   ✅ 프론트엔드 빌드 파일 복사 완료"

cd ..

# 프로덕션 실행 스크립트 생성
cat > dist/run-production.sh << 'EOF'
#!/bin/bash

echo "🚀 Content Creator AI 프로덕션 서버 시작..."

# 백엔드 서버 시작
cd ../backend
source venv/bin/activate
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000 > ../logs/production.log 2>&1 &
echo $! > ../logs/production.pid

echo "✅ 프로덕션 서버가 시작되었습니다"
echo "📡 API: http://localhost:8000"
echo "📖 API Docs: http://localhost:8000/docs"
echo ""
echo "프론트엔드는 Nginx 또는 다른 웹 서버로 제공하세요"
echo "프론트엔드 파일 위치: ./frontend/"
EOF

chmod +x dist/run-production.sh

# Nginx 설정 예시 생성
cat > dist/nginx.conf.example << 'EOF'
server {
    listen 80;
    server_name your-domain.com;

    # 프론트엔드
    location / {
        root /path/to/dist/frontend;
        try_files $uri $uri/ /index.html;
    }

    # 백엔드 API
    location /api {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # API 문서
    location /docs {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
EOF

# 배포 가이드 생성
cat > dist/DEPLOYMENT.md << 'EOF'
# 배포 가이드

## 1. 서버 준비

### 필수 요구사항
- Python 3.9+
- Node.js 18+
- Nginx (프론트엔드 서빙)

### 설치
```bash
# Python 가상환경
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install gunicorn
```

## 2. 백엔드 배포

### Gunicorn으로 실행
```bash
cd backend
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000
```

### Systemd 서비스로 등록
```bash
sudo nano /etc/systemd/system/content-creator-api.service
```

```ini
[Unit]
Description=Content Creator AI API
After=network.target

[Service]
User=your-user
WorkingDirectory=/path/to/backend
Environment="PATH=/path/to/venv/bin"
ExecStart=/path/to/venv/bin/gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl daemon-reload
sudo systemctl start content-creator-api
sudo systemctl enable content-creator-api
```

## 3. 프론트엔드 배포

### Nginx 설정
```bash
sudo cp nginx.conf.example /etc/nginx/sites-available/content-creator
sudo ln -s /etc/nginx/sites-available/content-creator /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

### Vercel/Netlify 배포
```bash
# 환경 변수 설정
VITE_API_URL=https://your-api-domain.com

# 빌드
npm run build

# dist 폴더를 배포 플랫폼에 업로드
```

## 4. 도메인 및 SSL

### Let's Encrypt SSL 인증서
```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com
```

## 5. 모니터링

### 로그 확인
```bash
# API 로그
tail -f /path/to/logs/production.log

# Nginx 로그
tail -f /var/log/nginx/access.log
tail -f /var/log/nginx/error.log
```

### 서비스 상태
```bash
sudo systemctl status content-creator-api
```

## 6. 환경 변수

`.env` 파일 생성:
```env
# 프로덕션 설정
DEBUG=False
CORS_ORIGINS=https://your-domain.com
```

## 7. 백업

### 데이터 백업
```bash
# 저장된 콘텐츠 백업
cp -r data/ backups/data-$(date +%Y%m%d)/
```

### 자동 백업 크론잡
```bash
crontab -e
```

```
0 2 * * * /path/to/backup.sh
```
EOF

echo ""
echo "✅ 프로덕션 빌드 완료!"
echo ""
echo "📁 빌드 결과물:"
echo "   - dist/frontend/         : 프론트엔드 정적 파일"
echo "   - dist/run-production.sh : 프로덕션 실행 스크립트"
echo "   - dist/nginx.conf.example: Nginx 설정 예시"
echo "   - dist/DEPLOYMENT.md     : 배포 가이드"
echo ""
echo "📖 배포 방법은 dist/DEPLOYMENT.md 를 참고하세요"
echo ""

