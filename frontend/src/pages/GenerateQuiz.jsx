/**
 * GenerateQuiz Page (Tab 1)
 * Main page for generating new quizzes from Wikipedia URLs
 */

import React, { useState } from 'react';
import { generateQuiz } from '../api';
import QuizList from '../components/QuizList';
import LoadingSpinner from '../components/LoadingSpinner';

const GenerateQuiz = () => {
  const [url, setUrl] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [quizData, setQuizData] = useState(null);
  const [quizMode, setQuizMode] = useState('view'); // 'view' or 'take'

  // Handle quiz generation
  const handleGenerateQuiz = async (e) => {
    e.preventDefault();
    
    // Validate URL
    if (!url.trim()) {
      setError('Please enter a Wikipedia URL');
      return;
    }

    if (!url.includes('wikipedia.org/wiki/')) {
      setError('Please enter a valid Wikipedia article URL (e.g., https://en.wikipedia.org/wiki/Article_Name)');
      return;
    }

    setLoading(true);
    setError(null);
    setQuizData(null);

    try {
      const data = await generateQuiz(url);
      setQuizData(data);
      setError(null);
    } catch (err) {
      setError(err.toString());
      setQuizData(null);
    } finally {
      setLoading(false);
    }
  };

  // Handle quiz answer submission (for take quiz mode)
  const handleAnswerSubmit = (questionIndex, isCorrect) => {
    console.log(`Question ${questionIndex + 1}: ${isCorrect ? 'Correct' : 'Incorrect'}`);
  };

  // Reset form
  const handleReset = () => {
    setUrl('');
    setQuizData(null);
    setError(null);
    setQuizMode('view');
  };

  return (
    <div className="max-w-6xl mx-auto">
      {/* Header */}
      <div className="mb-6">
        <h2 className="text-2xl font-bold text-gray-900 mb-2">Generate New Quiz</h2>
        <p className="text-gray-600">Enter any Wikipedia article URL to create an AI-powered quiz</p>
      </div>

      {/* URL Input Form */}
      <div className="bg-white rounded-lg shadow-sm p-6 mb-6 border border-gray-200">
        <form onSubmit={handleGenerateQuiz}>
          <div className="mb-4">
            <label htmlFor="wiki-url" className="block text-sm font-semibold text-gray-700 mb-2">
              Wikipedia Article URL
            </label>
            <input
              type="text"
              id="wiki-url"
              value={url}
              onChange={(e) => setUrl(e.target.value)}
              placeholder="https://en.wikipedia.org/wiki/Alan_Turing"
              className="w-full px-4 py-3 border-2 border-gray-300 rounded-lg focus:outline-none focus:border-blue-500 transition-colors text-gray-900"
              disabled={loading}
            />
          </div>

          {/* Action Buttons */}
          <div className="flex gap-3">
            <button
              type="submit"
              disabled={loading}
              className={`flex-1 bg-blue-600 text-white py-3 rounded-lg font-semibold transition-all shadow-sm ${
                loading ? 'opacity-50 cursor-not-allowed' : 'hover:bg-blue-700'
              }`}
            >
              {loading ? 'Generating Quiz...' : ' Generate Quiz'}
            </button>
            
            {quizData && (
              <button
                type="button"
                onClick={handleReset}
                className="px-6 py-3 bg-gray-200 text-gray-700 rounded-lg font-semibold hover:bg-gray-300 transition-colors"
              >
                Reset
              </button>
            )}
          </div>
        </form>

        {/* Error Message */}
        {error && (
          <div className="mt-4 p-4 bg-red-50 border-l-4 border-red-500 rounded-lg">
            <p className="text-red-800 font-semibold">❌ Error:</p>
            <p className="text-red-700 text-sm">{error}</p>
          </div>
        )}

        {/* Example URLs */}
        {!quizData && !loading && (
          <div className="mt-6 p-4 bg-blue-50 rounded-lg">
            <p className="text-sm font-semibold text-blue-900 mb-2">Try these examples:</p>
            <div className="space-y-2">
              {[
                'https://en.wikipedia.org/wiki/Alan_Turing',
                'https://en.wikipedia.org/wiki/Artificial_intelligence',
                'https://en.wikipedia.org/wiki/Solar_System'
              ].map((exampleUrl) => (
                <button
                  key={exampleUrl}
                  onClick={() => setUrl(exampleUrl)}
                  className="block w-full text-left text-sm text-blue-700 hover:text-blue-900 hover:underline"
                >
                  {exampleUrl}
                </button>
              ))}
            </div>
          </div>
        )}
      </div>

      {/* Loading State */}
      {loading && (
        <div className="bg-white rounded-xl shadow-lg p-8">
          <LoadingSpinner message="Generating quiz from Wikipedia article..." />
        </div>
      )}

      {/* Quiz Results */}
      {quizData && !loading && (
        <div className="space-y-6">
          {/* Quiz Header */}
          <div className="bg-white rounded-xl shadow-lg p-6">
            <h2 className="text-2xl font-bold text-gray-800 mb-2">{quizData.title}</h2>
            
            {quizData.summary && (
              <p className="text-gray-600 mb-4">{quizData.summary}</p>
            )}

            <div className="flex items-center justify-between">
              <div className="flex gap-2">
                <span className="bg-blue-100 text-blue-800 px-3 py-1 rounded-full text-sm font-semibold">
                  {quizData.quiz?.length || 0} Questions
                </span>
                {quizData.sections && (
                  <span className="bg-purple-100 text-purple-800 px-3 py-1 rounded-full text-sm font-semibold">
                    {quizData.sections.length} Sections
                  </span>
                )}
              </div>

              {/* Toggle Quiz Mode */}
              <div className="flex gap-2">
                <button
                  onClick={() => setQuizMode('view')}
                  className={`px-4 py-2 rounded-lg font-semibold transition-colors ${
                    quizMode === 'view'
                      ? 'bg-blue-600 text-white'
                      : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
                  }`}
                >
                  View Mode
                </button>
                <button
                  onClick={() => setQuizMode('take')}
                  className={`px-4 py-2 rounded-lg font-semibold transition-colors ${
                    quizMode === 'take'
                      ? 'bg-green-600 text-white'
                      : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
                  }`}
                >
                  Take Quiz
                </button>
              </div>
            </div>
          </div>

          {/* Key Entities */}
          {quizData.key_entities && (
            <div className="bg-white rounded-xl shadow-lg p-6">
              <h3 className="text-lg font-bold text-gray-800 mb-4">Key Entities Extracted</h3>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                {quizData.key_entities.people?.length > 0 && (
                  <div>
                    <h4 className="font-semibold text-gray-700 mb-2">👥 People</h4>
                    <ul className="text-sm text-gray-600 space-y-1">
                      {quizData.key_entities.people.map((person, idx) => (
                        <li key={idx} className="flex items-center">
                          <span className="text-blue-500 mr-2">•</span>
                          {person}
                        </li>
                      ))}
                    </ul>
                  </div>
                )}
                {quizData.key_entities.organizations?.length > 0 && (
                  <div>
                    <h4 className="font-semibold text-gray-700 mb-2"> Organizations</h4>
                    <ul className="text-sm text-gray-600 space-y-1">
                      {quizData.key_entities.organizations.map((org, idx) => (
                        <li key={idx} className="flex items-center">
                          <span className="text-purple-500 mr-2">•</span>
                          {org}
                        </li>
                      ))}
                    </ul>
                  </div>
                )}
                {quizData.key_entities.locations?.length > 0 && (
                  <div>
                    <h4 className="font-semibold text-gray-700 mb-2">📍 Locations</h4>
                    <ul className="text-sm text-gray-600 space-y-1">
                      {quizData.key_entities.locations.map((loc, idx) => (
                        <li key={idx} className="flex items-center">
                          <span className="text-orange-500 mr-2">•</span>
                          {loc}
                        </li>
                      ))}
                    </ul>
                  </div>
                )}
              </div>
            </div>
          )}

          {/* Quiz Questions */}
          <div className="bg-white rounded-xl shadow-lg p-6">
            <h3 className="text-xl font-bold text-gray-800 mb-6">
              {quizMode === 'take' ? 'Take the Quiz' : 'Quiz Questions'}
            </h3>
            <QuizList
              quiz={quizData.quiz}
              showAnswers={quizMode === 'view'}
              onAnswerSubmit={handleAnswerSubmit}
            />
          </div>

          {/* Related Topics */}
          {quizData.related_topics && quizData.related_topics.length > 0 && (
            <div className="bg-gradient-to-r from-blue-50 to-purple-50 rounded-xl shadow-lg p-6">
              <h3 className="text-lg font-bold text-gray-800 mb-4">🔗 Related Topics for Further Reading</h3>
              <div className="flex flex-wrap gap-3">
                {quizData.related_topics.map((topic, idx) => (
                  <a
                    key={idx}
                    href={`https://en.wikipedia.org/wiki/${encodeURIComponent(topic.replace(/ /g, '_'))}`}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="bg-white px-4 py-2 rounded-full text-sm font-semibold text-blue-600 hover:bg-blue-600 hover:text-white transition-all transform hover:scale-105 shadow-md"
                  >
                    {topic} →
                  </a>
                ))}
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default GenerateQuiz;