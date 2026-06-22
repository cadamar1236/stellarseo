import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.jsx'

class ErrorBoundary extends React.Component {
  constructor(props) { super(props); this.state = { error: null }; }
  static getDerivedStateFromError(e) { return { error: e }; }
  render() {
    if (this.state.error) return (
      <div style={{ fontFamily: 'monospace', padding: '2rem', color: '#f87171', background: '#0f172a', minHeight: '100vh' }}>
        <h2 style={{ marginBottom: '1rem' }}>⚠️ App Error</h2>
        <pre style={{ whiteSpace: 'pre-wrap', marginBottom: '1rem' }}>{this.state.error.message}</pre>
        {this.state.error.stack && (
          <details open style={{ marginBottom: '1rem' }}>
            <summary style={{ cursor: 'pointer', color: '#94a3b8' }}>Stack trace</summary>
            <pre style={{ whiteSpace: 'pre-wrap', fontSize: '0.8em', color: '#94a3b8', marginTop: '0.5rem' }}>{this.state.error.stack}</pre>
          </details>
        )}
      </div>
    );
    return this.props.children;
  }
}

ReactDOM.createRoot(document.getElementById('root')).render(
  <ErrorBoundary>
    <App />
  </ErrorBoundary>
)