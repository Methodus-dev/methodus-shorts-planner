import schedule
import time
import subprocess
import logging
from datetime import datetime

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('scheduler.log'),
        logging.StreamHandler()
    ]
)

def run_youtube_crawling():
    """YouTube 트렌드 크롤링 실행"""
    try:
        logging.info("🔄 YouTube 트렌드 크롤링 시작...")
        
        # 실시간 크롤링 실행
        result1 = subprocess.run(['python', 'youtube_realtime_crawler.py'], 
                               capture_output=True, text=True)
        if result1.returncode == 0:
            logging.info("✅ 실시간 크롤링 완료")
        else:
            logging.error(f"❌ 실시간 크롤링 실패: {result1.stderr}")
        
        # 쇼츠 크롤링 실행
        result2 = subprocess.run(['python', 'youtube_shorts_crawler.py'], 
                               capture_output=True, text=True)
        if result2.returncode == 0:
            logging.info("✅ 쇼츠 크롤링 완료")
        else:
            logging.error(f"❌ 쇼츠 크롤링 실패: {result2.stderr}")
            
        logging.info("🎉 모든 크롤링 작업 완료")
        
    except Exception as e:
        logging.error(f"❌ 크롤링 실행 중 오류: {e}")

def main():
    """스케줄러 메인 함수"""
    logging.info("🚀 크롤링 스케줄러 시작")
    
    # 매일 오전 9시, 오후 6시에 크롤링 실행
    schedule.every().day.at("09:00").do(run_youtube_crawling)
    schedule.every().day.at("18:00").do(run_youtube_crawling)
    
    # 매주 월요일 오전 8시에 전체 크롤링 실행
    schedule.every().monday.at("08:00").do(run_youtube_crawling)
    
    logging.info("📅 스케줄 설정 완료:")
    logging.info("  - 매일 오전 9시, 오후 6시")
    logging.info("  - 매주 월요일 오전 8시")
    
    # 스케줄러 실행
    while True:
        schedule.run_pending()
        time.sleep(60)  # 1분마다 체크

if __name__ == "__main__":
    main()
