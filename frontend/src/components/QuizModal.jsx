/**
 * QuizModal Component
 * Modal popup to show quiz details
 */

import React, { useEffect, useRef } from 'react';
import QuizList from './QuizList';

const QuizModal = ({ isOpen, onClose, quiz, loading }) => {
  const modalRef = useRef(null);

  // Close modal when clicking outside
  useEffect(() => {
    const handleClickOutside = (event) => {
      if (modalRef.current && !modalRef.current.contains(event.target)) {
        onClose();
      }
    };

    if (isOpen) {
      document.addEventListener('mousedown', handleClickOutside);
      document.body.style.overflow = 'hidden'; // Prevent background scroll
    }

    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
      document.body.style.overflow = 'unset';
    };
  }, [isOpen, onClose]);

  // Close on Escape key
  useEffect(() => {
    const handleEscape = (event) => {
      if (event.key === 'Escape') {
        onClose();
      }
    };

    if (isOpen) {
      document.addEventListener('keydown', handleEscape);
    }

    return () => {
      document.removeEventListener('keydown', handleEscape);
    };
  }, [isOpen, onClose]);

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black bg-opacity-50">
      <div
        ref={modalRef}
        className="bg-white rounded-lg shadow-2xl w-full max-w-5xl max-h-[90vh] overflow-hidden flex flex-col"
      >
        {/* Modal Header */}
        <div className="bg-blue-600 px-6 py-4 flex items-center justify-between">
          <div className="flex-1">
            <h2 className="text-2xl font-bold text-white">
              {loading ? 'Loading Quiz...' : quiz?.title || 'Quiz Details'}
            </h2>
            {quiz?.url && (
              <a
                href={quiz.url}
                target="_blank"
                rel="noopener noreferrer"
                className="text-blue-100 hover:text-white text-sm mt-1 inline-block hover:underline"
              >
                View Original Article →
              </a>
            )}
          </div>
          <button
            onClick={onClose}
            className="ml-4 text-white hover:bg-blue-700 rounded-full p-2 transition-colors"
            title="Close"
          >
            <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        {/* Modal Body */}
        <div className="flex-1 overflow-y-auto p-6 bg-gray-50">
          {loading ? (
            <div className="flex items-center justify-center py-12">
              <div className="animate-spin rounded-full h-12 w-12 border-4 border-blue-600 border-t-transparent"></div>
            </div>
          ) : quiz ? (
            <div>
              {/* Debug: Check quiz structure */}
              {console.log('=== MODAL QUIZ DATA ===')}
              {console.log('Full quiz object:', quiz)}
              {console.log('quiz.quiz:', quiz.quiz)}
              {console.log('Is quiz an array?', Array.isArray(quiz))}
              {console.log('=======================')}
              
              {/* Quiz Summary */}
              {quiz.summary && (
                <div className="mb-6 p-4 bg-white rounded-lg border-l-4 border-blue-600 shadow-sm">
                  <h3 className="font-semibold text-gray-900 mb-2"> Summary</h3>
                  <p className="text-gray-700 text-sm leading-relaxed">{quiz.summary}</p>
                </div>
              )}

              {/* Key Entities */}
              {quiz.key_entities && (Object.keys(quiz.key_entities).some(key => quiz.key_entities[key]?.length > 0)) && (
                <div className="mb-6 grid grid-cols-1 md:grid-cols-3 gap-4">
                  {quiz.key_entities.people?.length > 0 && (
                    <div className="bg-white p-4 rounded-lg shadow-sm">
                      <h4 className="font-semibold text-gray-900 mb-2 flex items-center">
                        <span className="mr-2">👥</span> People
                      </h4>
                      <ul className="text-sm text-gray-700 space-y-1">
                        {quiz.key_entities.people.map((person, idx) => (
                          <li key={idx} className="flex items-start">
                            <span className="text-blue-600 mr-2">•</span>
                            <span>{person}</span>
                          </li>
                        ))}
                      </ul>
                    </div>
                  )}
                  {quiz.key_entities.organizations?.length > 0 && (
                    <div className="bg-white p-4 rounded-lg shadow-sm">
                      <h4 className="font-semibold text-gray-900 mb-2 flex items-center">
                        
                      </h4>
                      <ul className="text-sm text-gray-700 space-y-1">
                        {quiz.key_entities.organizations.map((org, idx) => (
                          <li key={idx} className="flex items-start">
                            <span className="text-blue-600 mr-2">•</span>
                            <span>{org}</span>
                          </li>
                        ))}
                      </ul>
                    </div>
                  )}
                  {quiz.key_entities.locations?.length > 0 && (
                    <div className="bg-white p-4 rounded-lg shadow-sm">
                      <h4 className="font-semibold text-gray-900 mb-2 flex items-center">
                        
                      </h4>
                      <ul className="text-sm text-gray-700 space-y-1">
                        {quiz.key_entities.locations.map((loc, idx) => (
                          <li key={idx} className="flex items-start">
                            <span className="text-blue-600 mr-2">•</span>
                            <span>{loc}</span>
                          </li>
                        ))}
                      </ul>
                    </div>
                  )}
                </div>
              )}

              {/* Quiz Questions */}
              <div className="mb-6">
                <h3 className="text-xl font-bold text-gray-900 mb-4 flex items-center">
                  
                  Quiz Questions ({Array.isArray(quiz.quiz) ? quiz.quiz.length : 0})
                </h3>
                {/* Debug info */}
                {console.log('Quiz data in modal:', quiz)}
                {console.log('Quiz.quiz:', quiz.quiz)}
                {console.log('Is array?', Array.isArray(quiz.quiz))}
                
                {quiz.quiz && Array.isArray(quiz.quiz) && quiz.quiz.length > 0 ? (
                  <QuizList quiz={quiz.quiz} showAnswers={true} />
                ) : (
                  <div className="bg-yellow-50 border-l-4 border-yellow-500 p-4 rounded">
                    <p className="text-yellow-800">No questions available for this quiz.</p>
                    <p className="text-xs text-yellow-700 mt-1">
                      Debug: quiz.quiz = {JSON.stringify(quiz.quiz)}
                    </p>
                  </div>
                )}
              </div>

              {/* Related Topics */}
              {quiz.related_topics && quiz.related_topics.length > 0 && (
                <div className="bg-white p-6 rounded-lg shadow-sm">
                  <h3 className="font-semibold text-gray-900 mb-3 flex items-center">
                    
                    Related Topics for Further Reading
                  </h3>
                  <div className="flex flex-wrap gap-2">
                    {quiz.related_topics.map((topic, idx) => (
                      <a
                        key={idx}
                        href={`https://en.wikipedia.org/wiki/${encodeURIComponent(topic.replace(/ /g, '_'))}`}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="bg-blue-50 hover:bg-blue-100 px-4 py-2 rounded-full text-sm font-medium text-blue-700 transition-colors border border-blue-200"
                      >
                        {topic}
                      </a>
                    ))}
                  </div>
                </div>
              )}
            </div>
          ) : (
            <div className="text-center py-8 text-gray-500">
              No quiz data available
            </div>
          )}
        </div>

        {/* Modal Footer */}
        <div className="border-t border-gray-200 px-6 py-4 bg-white flex justify-end">
          <button
            onClick={onClose}
            className="bg-gray-600 text-white px-6 py-2 rounded-lg hover:bg-gray-700 transition-colors font-semibold"
          >
            Close
          </button>
        </div>
      </div>
    </div>
  );
};

export default QuizModal;