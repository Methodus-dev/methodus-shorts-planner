import React, { useState, useEffect } from 'react';

interface SchedulerStatus {
  status: 'running' | 'stopped';
  message: string;
  pid?: number;
}

const SchedulerManager: React.FC = () => {
  const [schedulerStatus, setSchedulerStatus] = useState<SchedulerStatus | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [message, setMessage] = useState('');

  // 스케줄러 상태 확인
  const checkSchedulerStatus = async () => {
    try {
      const response = await fetch('https://methodus-shorts-planner.onrender.com/api/scheduler-status');
      const data = await response.json();
      setSchedulerStatus(data);
    } catch (error) {
      console.error('스케줄러 상태 확인 실패:', error);
    }
  };

  // 스케줄러 시작
  const startScheduler = async () => {
    setIsLoading(true);
    setMessage('');
    try {
      const response = await fetch('https://methodus-shorts-planner.onrender.com/api/start-scheduler', {
        method: 'POST'
      });
      const data = await response.json();
      setMessage(data.message);
      if (data.status === 'success') {
        await checkSchedulerStatus();
      }
    } catch (error) {
      setMessage('스케줄러 시작 실패');
      console.error('스케줄러 시작 실패:', error);
    } finally {
      setIsLoading(false);
    }
  };

  // 스케줄러 중지
  const stopScheduler = async () => {
    setIsLoading(true);
    setMessage('');
    try {
      const response = await fetch('https://methodus-shorts-planner.onrender.com/api/stop-scheduler', {
        method: 'POST'
      });
      const data = await response.json();
      setMessage(data.message);
      if (data.status === 'success') {
        await checkSchedulerStatus();
      }
    } catch (error) {
      setMessage('스케줄러 중지 실패');
      console.error('스케줄러 중지 실패:', error);
    } finally {
      setIsLoading(false);
    }
  };

  // 수동 크롤링 실행
  const triggerCrawling = async () => {
    setIsLoading(true);
    setMessage('');
    try {
      const response = await fetch('https://methodus-shorts-planner.onrender.com/api/trigger-crawling', {
        method: 'POST'
      });
      const data = await response.json();
      setMessage(data.message);
    } catch (error) {
      setMessage('크롤링 실행 실패');
      console.error('크롤링 실행 실패:', error);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    checkSchedulerStatus();
    // 30초마다 상태 확인
    const interval = setInterval(checkSchedulerStatus, 30000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="bg-white rounded-lg shadow-md p-6 mb-6">
      <h3 className="text-lg font-semibold text-gray-800 mb-4">🔄 크롤링 스케줄러 관리</h3>
      
      {/* 스케줄러 상태 */}
      <div className="mb-4">
        <div className="flex items-center gap-2 mb-2">
          <span className="text-sm font-medium text-gray-700">스케줄러 상태:</span>
          {schedulerStatus && (
            <span className={`px-2 py-1 rounded-full text-xs font-medium ${
              schedulerStatus.status === 'running' 
                ? 'bg-green-100 text-green-800' 
                : 'bg-red-100 text-red-800'
            }`}>
              {schedulerStatus.status === 'running' ? '🟢 실행 중' : '🔴 중지됨'}
            </span>
          )}
        </div>
        {schedulerStatus?.pid && (
          <p className="text-xs text-gray-500">PID: {schedulerStatus.pid}</p>
        )}
      </div>

      {/* 스케줄 정보 */}
      <div className="mb-4 p-3 bg-blue-50 rounded-lg">
        <h4 className="text-sm font-medium text-blue-800 mb-1">📅 자동 크롤링 스케줄</h4>
        <ul className="text-xs text-blue-700 space-y-1">
          <li>• 매일 오전 9시, 오후 6시</li>
          <li>• 매주 월요일 오전 8시 (전체 크롤링)</li>
          <li>• GitHub Actions를 통한 백업 크롤링</li>
        </ul>
      </div>

      {/* 제어 버튼들 */}
      <div className="flex flex-wrap gap-2 mb-4">
        <button
          onClick={startScheduler}
          disabled={isLoading || schedulerStatus?.status === 'running'}
          className="px-3 py-2 bg-green-500 text-white rounded-md hover:bg-green-600 disabled:bg-gray-300 disabled:cursor-not-allowed text-sm"
        >
          {isLoading ? '처리 중...' : '스케줄러 시작'}
        </button>
        
        <button
          onClick={stopScheduler}
          disabled={isLoading || schedulerStatus?.status === 'stopped'}
          className="px-3 py-2 bg-red-500 text-white rounded-md hover:bg-red-600 disabled:bg-gray-300 disabled:cursor-not-allowed text-sm"
        >
          {isLoading ? '처리 중...' : '스케줄러 중지'}
        </button>
        
        <button
          onClick={triggerCrawling}
          disabled={isLoading}
          className="px-3 py-2 bg-blue-500 text-white rounded-md hover:bg-blue-600 disabled:bg-gray-300 disabled:cursor-not-allowed text-sm"
        >
          {isLoading ? '크롤링 중...' : '수동 크롤링'}
        </button>
        
        <button
          onClick={checkSchedulerStatus}
          disabled={isLoading}
          className="px-3 py-2 bg-gray-500 text-white rounded-md hover:bg-gray-600 disabled:bg-gray-300 disabled:cursor-not-allowed text-sm"
        >
          상태 새로고침
        </button>
      </div>

      {/* 메시지 표시 */}
      {message && (
        <div className={`p-3 rounded-md text-sm ${
          message.includes('실패') || message.includes('오류') 
            ? 'bg-red-100 text-red-800' 
            : 'bg-green-100 text-green-800'
        }`}>
          {message}
        </div>
      )}
    </div>
  );
};

export default SchedulerManager;
