/**
 * Main App Component
 * Contains tab navigation and routes
 */

import React, { useState, useEffect } from 'react';
import GenerateQuiz from './pages/GenerateQuiz';
import History from './pages/History';
import { checkHealth } from './api';

function App() {
  const [activeTab, setActiveTab] = useState('generate');
  const [backendStatus, setBackendStatus] = useState('checking');

  // Check backend health on mount
  useEffect(() => {
    const checkBackend = async () => {
      try {
        await checkHealth();
        setBackendStatus('connected');
      } catch (error) {
        // If timeout, might be cold start - try once more
        if (error.includes('timeout')) {
          console.log('Backend might be sleeping, retrying...');
          setBackendStatus('waking');
          
          // Wait 30 seconds and retry
          setTimeout(async () => {
            try {
              await checkHealth();
              setBackendStatus('connected');
            } catch (retryError) {
              setBackendStatus('disconnected');
              console.error('Backend connection failed:', retryError);
            }
          }, 30000);
        } else {
          setBackendStatus('disconnected');
          console.error('Backend connection failed:', error);
        }
      }
    };

    checkBackend();
  }, []);

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white border-b border-gray-200 shadow-sm">
        <div className="max-w-7xl mx-auto px-4 py-6">
          <div className="text-center">
            <h1 className="text-4xl font-bold text-gray-900 mb-2">
               AI Wiki Quiz Generator
            </h1>
            <p className="text-gray-600 mb-4">
              Transform Wikipedia articles into interactive quizzes using AI
            </p>
            
            {/* Backend Status Indicator */}
            <div className="inline-flex items-center gap-2 bg-gray-100 rounded-full px-4 py-2">
              <div
                className={`w-2 h-2 rounded-full ${
                  backendStatus === 'connected'
                    ? 'bg-green-500'
                    : backendStatus === 'disconnected'
                    ? 'bg-red-500'
                    : backendStatus === 'waking'
                    ? 'bg-yellow-500 animate-pulse'
                    : 'bg-yellow-500'
                }`}
              />
              <span className="text-sm text-gray-700 font-medium">
                {backendStatus === 'connected'
                  ? 'Backend Connected'
                  : backendStatus === 'disconnected'
                  ? 'Backend Disconnected'
                  : backendStatus === 'waking'
                  ? 'Waking up backend... (30s)'
                  : 'Checking Backend...'}
              </span>
            </div>
          </div>
        </div>
      </div>

      {/* Backend Error Message */}
      {backendStatus === 'disconnected' && (
        <div className="max-w-3xl mx-auto px-4 mt-4">
          <div className="bg-red-50 border-l-4 border-red-500 p-4 rounded">
            <p className="font-semibold text-red-800"> Cannot connect to backend API</p>
            <p className="text-red-700 text-sm mt-1">
              Make sure the backend server is running on http://localhost:8000
            </p>
            <p className="text-red-700 text-sm">
              Run: <code className="bg-red-100 px-2 py-1 rounded">python -m uvicorn app.main:app --reload</code>
            </p>
          </div>
        </div>
      )}

      <div className="max-w-7xl mx-auto px-4 py-6">
        {/* Tab Navigation */}
        <div className="bg-white rounded-lg shadow-sm overflow-hidden mb-6">
          <div className="flex border-b border-gray-200">
            <button
              onClick={() => setActiveTab('generate')}
              className={`flex-1 py-4 px-6 font-semibold transition-all ${
                activeTab === 'generate'
                  ? 'bg-blue-600 text-white border-b-2 border-blue-600'
                  : 'bg-white text-gray-600 hover:bg-gray-50'
              }`}
            >
              
              Generate Quiz
            </button>
            <button
              onClick={() => setActiveTab('history')}
              className={`flex-1 py-4 px-6 font-semibold transition-all ${
                activeTab === 'history'
                  ? 'bg-blue-600 text-white border-b-2 border-blue-600'
                  : 'bg-white text-gray-600 hover:bg-gray-50'
              }`}
            >
              
              Quiz History
            </button>
          </div>

          {/* Tab Content */}
          <div className="p-6 bg-gray-50 min-h-[600px]">
            {activeTab === 'generate' ? <GenerateQuiz /> : <History />}
          </div>
        </div>

        {/* Footer */}
        <div className="text-center text-gray-500 text-sm py-4">
          <p className="mb-1">
            Built with React, FastAPI, PostgreSQL, and Google Gemini AI
          </p>
          <p className="text-gray-400">
            DeepKlarity Technologies • AI Wiki Quiz Generator
          </p>
        </div>
      </div>
    </div>
  );
}

export default App;