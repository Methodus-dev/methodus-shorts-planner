import { useState } from 'react';

function StepByStepApp() {
  const [step, setStep] = useState(1);

  return (
    <div style={{
      minHeight: '100vh',
      background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      fontFamily: 'Arial, sans-serif',
      padding: '20px'
    }}>
      <div style={{
        background: 'white',
        borderRadius: '12px',
        padding: '40px',
        boxShadow: '0 20px 40px rgba(0,0,0,0.1)',
        maxWidth: '600px',
        width: '90%',
        textAlign: 'center'
      }}>
        <h1 style={{
          fontSize: '2.5rem',
          fontWeight: 'bold',
          color: '#1e40af',
          marginBottom: '1rem'
        }}>
          🔧 단계별 진단
        </h1>
        
        <p style={{
          color: '#6b7280',
          marginBottom: '2rem',
          fontSize: '1.1rem'
        }}>
          메인 앱의 각 의존성을 단계별로 테스트합니다
        </p>
        
        <div style={{
          background: '#f0f9ff',
          border: '2px solid #0ea5e9',
          borderRadius: '8px',
          padding: '20px',
          marginBottom: '20px'
        }}>
          <h3 style={{ color: '#0369a1', marginBottom: '10px' }}>
            현재 단계: {step}/5
          </h3>
          <p style={{ color: '#0284c7', fontSize: '0.9rem' }}>
            {step === 1 && "1단계: 기본 React 상태 관리"}
            {step === 2 && "2단계: CSS 파일 로딩"}
            {step === 3 && "3단계: API 서비스"}
            {step === 4 && "4단계: 컴포넌트 로딩"}
            {step === 5 && "5단계: 전체 앱"}
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
            🔍 테스트 결과
          </h3>
          <p style={{ color: '#b45309', fontSize: '0.9rem' }}>
            {step === 1 && "✅ React 기본 기능 정상"}
            {step === 2 && "CSS 로딩 테스트 중..."}
            {step === 3 && "API 연결 테스트 중..."}
            {step === 4 && "컴포넌트 로딩 테스트 중..."}
            {step === 5 && "전체 앱 로딩 테스트 중..."}
          </p>
        </div>
        
        <div style={{
          display: 'flex',
          gap: '10px',
          justifyContent: 'center',
          marginBottom: '20px'
        }}>
          <button 
            onClick={() => setStep(1)}
            style={{
              padding: '8px 16px',
              background: step === 1 ? '#0ea5e9' : '#e5e7eb',
              color: step === 1 ? 'white' : '#6b7280',
              border: 'none',
              borderRadius: '4px',
              cursor: 'pointer'
            }}
          >
            1
          </button>
          <button 
            onClick={() => setStep(2)}
            style={{
              padding: '8px 16px',
              background: step === 2 ? '#0ea5e9' : '#e5e7eb',
              color: step === 2 ? 'white' : '#6b7280',
              border: 'none',
              borderRadius: '4px',
              cursor: 'pointer'
            }}
          >
            2
          </button>
          <button 
            onClick={() => setStep(3)}
            style={{
              padding: '8px 16px',
              background: step === 3 ? '#0ea5e9' : '#e5e7eb',
              color: step === 3 ? 'white' : '#6b7280',
              border: 'none',
              borderRadius: '4px',
              cursor: 'pointer'
            }}
          >
            3
          </button>
          <button 
            onClick={() => setStep(4)}
            style={{
              padding: '8px 16px',
              background: step === 4 ? '#0ea5e9' : '#e5e7eb',
              color: step === 4 ? 'white' : '#6b7280',
              border: 'none',
              borderRadius: '4px',
              cursor: 'pointer'
            }}
          >
            4
          </button>
          <button 
            onClick={() => setStep(5)}
            style={{
              padding: '8px 16px',
              background: step === 5 ? '#0ea5e9' : '#e5e7eb',
              color: step === 5 ? 'white' : '#6b7280',
              border: 'none',
              borderRadius: '4px',
              cursor: 'pointer'
            }}
          >
            5
          </button>
        </div>
        
        <button 
          onClick={() => {
            if (step < 5) {
              setStep(step + 1);
            } else {
              alert('모든 단계 테스트 완료! 이제 메인 앱으로 전환합니다.');
            }
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
        >
          {step < 5 ? '다음 단계' : '메인 앱으로 전환'}
        </button>
        
        <div style={{
          marginTop: '20px',
          fontSize: '0.8rem',
          color: '#9ca3af'
        }}>
          <p>단계별 진단 도구</p>
          <p>Built with ❤️ for Content Creators</p>
        </div>
      </div>
    </div>
  );
}

export default StepByStepApp;
