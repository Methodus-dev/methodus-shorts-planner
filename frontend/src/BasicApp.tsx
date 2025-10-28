function BasicApp() {
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
            ✅ React 로딩 성공!
          </h3>
          <p style={{ color: '#0284c7', fontSize: '0.9rem' }}>
            기본 React 컴포넌트가 정상적으로 렌더링되었습니다.
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
            🔧 다음 단계
          </h3>
          <p style={{ color: '#b45309', fontSize: '0.9rem' }}>
            이제 메인 앱의 복잡한 컴포넌트들을 하나씩 추가해보겠습니다.
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
            🚀 개발된 기능들
          </h3>
          <p style={{ color: '#7e22ce', fontSize: '0.9rem' }}>
            • 콘텐츠 자동 생성<br/>
            • 실시간 편집<br/>
            • 저장 및 관리<br/>
            • 자동 해시태그
          </p>
        </div>
        
        <button 
          onClick={() => {
            alert('React가 정상적으로 작동하고 있습니다!');
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
          React 테스트
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

export default BasicApp;
