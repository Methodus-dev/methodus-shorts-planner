function TestApp() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-purple-50 flex items-center justify-center">
      <div className="bg-white rounded-lg shadow-xl p-8 max-w-md w-full">
        <h1 className="text-3xl font-bold text-center mb-4 text-blue-600">
          🎉 Content Creator AI
        </h1>
        <p className="text-gray-600 text-center mb-6">
          AI 기반 LinkedIn 콘텐츠 자동 생성 플랫폼
        </p>
        
        <div className="space-y-4">
          <div className="p-4 bg-green-50 rounded-lg border border-green-200">
            <h3 className="font-semibold text-green-800">✅ 프론트엔드 연결 성공!</h3>
            <p className="text-sm text-green-600 mt-1">
              React 애플리케이션이 정상적으로 로드되었습니다.
            </p>
          </div>
          
          <div className="p-4 bg-blue-50 rounded-lg border border-blue-200">
            <h3 className="font-semibold text-blue-800">🔧 백엔드 확인</h3>
            <p className="text-sm text-blue-600 mt-1">
              API 서버: http://localhost:8000
            </p>
          </div>
          
          <div className="p-4 bg-purple-50 rounded-lg border border-purple-200">
            <h3 className="font-semibold text-purple-800">🚀 사용 준비 완료</h3>
            <p className="text-sm text-purple-600 mt-1">
              이제 메인 애플리케이션으로 이동하세요!
            </p>
          </div>
        </div>
        
        <button 
          onClick={() => window.location.reload()}
          className="w-full mt-6 bg-blue-600 text-white py-2 px-4 rounded-lg hover:bg-blue-700 transition-colors"
        >
          메인 앱으로 이동
        </button>
      </div>
    </div>
  );
}

export default TestApp;
