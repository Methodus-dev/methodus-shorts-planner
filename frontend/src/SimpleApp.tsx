function SimpleApp() {
  return (
    <div style={{
      minHeight: '100vh',
      background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      fontFamily: 'Arial, sans-serif'
    }}>
      <div style={{
        background: 'white',
        borderRadius: '12px',
        padding: '40px',
        boxShadow: '0 20px 40px rgba(0,0,0,0.1)',
        maxWidth: '500px',
        width: '90%',
        textAlign: 'center'
      }}>
        <h1 style={{
          fontSize: '2.5rem',
          fontWeight: 'bold',
          color: '#1e40af',
          marginBottom: '1rem'
        }}>
          🎉 Content Creator AI
        </h1>
        
        <p style={{
          color: '#6b7280',
          marginBottom: '2rem',
          fontSize: '1.1rem'
        }}>
          AI 기반 LinkedIn 콘텐츠 자동 생성 플랫폼
        </p>
        
        <div style={{
          background: '#f0f9ff',
          border: '2px solid #0ea5e9',
          borderRadius: '8px',
          padding: '20px',
          marginBottom: '20px'
        }}>
          <h3 style={{ color: '#0369a1', marginBottom: '10px' }}>
            ✅ 프론트엔드 연결 성공!
          </h3>
          <p style={{ color: '#0284c7', fontSize: '0.9rem' }}>
            React 애플리케이션이 정상적으로 로드되었습니다.
          </p>
        </div>
        
        <div style={{
          background: '#fef3c7',
          border: '2px solid #f59e0b',
          borderRadius: '8px',
          padding: '20px',
          marginBottom: '20px'
        }}>
          <h3 style={{ color: '#92400e', marginBottom: '10px' }}>
            🔧 백엔드 확인
          </h3>
          <p style={{ color: '#b45309', fontSize: '0.9rem' }}>
            API 서버: http://localhost:8000
          </p>
        </div>
        
        <div style={{
          background: '#f3e8ff',
          border: '2px solid #a855f7',
          borderRadius: '8px',
          padding: '20px',
          marginBottom: '30px'
        }}>
          <h3 style={{ color: '#6b21a8', marginBottom: '10px' }}>
            🚀 사용 준비 완료
          </h3>
          <p style={{ color: '#7e22ce', fontSize: '0.9rem' }}>
            이제 메인 애플리케이션으로 이동하세요!
          </p>
        </div>
        
        <button 
          onClick={() => {
            // 메인 앱으로 전환
            window.location.href = '/';
          }}
          style={{
            width: '100%',
            background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
            color: 'white',
            border: 'none',
            padding: '12px 24px',
            borderRadius: '8px',
            fontSize: '1rem',
            fontWeight: 'bold',
            cursor: 'pointer',
            transition: 'transform 0.2s'
          }}
          onMouseOver={(e) => (e.target as HTMLElement).style.transform = 'scale(1.02)'}
          onMouseOut={(e) => (e.target as HTMLElement).style.transform = 'scale(1)'}
        >
          메인 앱으로 이동
        </button>
        
        <div style={{
          marginTop: '20px',
          fontSize: '0.8rem',
          color: '#9ca3af'
        }}>
          <p>Powered by React + Vite</p>
          <p>Built with ❤️ for Content Creators</p>
        </div>
      </div>
    </div>
  );
}

export default SimpleApp;
