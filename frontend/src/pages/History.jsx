/**
 * History Page (Tab 2)
 * Shows list of all past quizzes with details modal
 */

import React, { useState, useEffect } from 'react';
import { getQuizList, getQuiz } from '../api';
import HistoryTable from '../components/HistoryTable';
import QuizModal from '../components/QuizModal';
import LoadingSpinner from '../components/LoadingSpinner';

const History = () => {
  const [quizzes, setQuizzes] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [selectedQuiz, setSelectedQuiz] = useState(null);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [modalLoading, setModalLoading] = useState(false);

  // Load quiz list on component mount
  useEffect(() => {
    loadQuizzes();
  }, []);

  // Fetch all quizzes from backend
  const loadQuizzes = async () => {
    setLoading(true);
    setError(null);

    try {
      const data = await getQuizList();
      setQuizzes(data);
    } catch (err) {
      setError(err.toString());
    } finally {
      setLoading(false);
    }
  };

  // Handle viewing quiz details
  const handleViewDetails = async (quizId) => {
    setIsModalOpen(true);
    setModalLoading(true);
    setSelectedQuiz(null);

    try {
      const data = await getQuiz(quizId);
      console.log('Fetched quiz data:', data); // Debug log
      setSelectedQuiz(data);
    } catch (err) {
      console.error('Error loading quiz details:', err);
      setError('Failed to load quiz details');
      setIsModalOpen(false);
    } finally {
      setModalLoading(false);
    }
  };

  // Close modal
  const handleCloseModal = () => {
    setIsModalOpen(false);
    setSelectedQuiz(null);
  };

  return (
    <div className="max-w-7xl mx-auto">
      {/* Header */}
      <div className="mb-6">
        <h2 className="text-2xl font-bold text-gray-900 mb-2">Quiz History</h2>
        <p className="text-gray-600">View all your previously generated quizzes</p>
      </div>

      {/* Refresh Button */}
      <div className="mb-6 flex justify-end">
        <button
          onClick={loadQuizzes}
          disabled={loading}
          className="bg-blue-600 text-white px-6 py-2 rounded-lg font-semibold hover:bg-blue-700 transition-colors shadow-sm disabled:opacity-50"
        >
           Refresh
        </button>
      </div>

      {/* Loading State */}
      {loading && (
        <div className="bg-white rounded-xl shadow-lg p-8">
          <LoadingSpinner message="Loading quiz history..." />
        </div>
      )}

      {/* Error State */}
      {error && !loading && (
        <div className="bg-white rounded-xl shadow-lg p-6">
          <div className="p-4 bg-red-50 border-l-4 border-red-500 rounded-lg">
            <p className="text-red-800 font-semibold">Error:</p>
            <p className="text-red-700 text-sm">{error}</p>
            <button
              onClick={loadQuizzes}
              className="mt-4 bg-red-600 text-white px-4 py-2 rounded-lg hover:bg-red-700 transition-colors"
            >
              Try Again
            </button>
          </div>
        </div>
      )}

      {/* Quiz List Table */}
      {!loading && !error && (
        <>
          <HistoryTable quizzes={quizzes} onViewDetails={handleViewDetails} />

          {/* Statistics */}
          {quizzes.length > 0 && (
            <div className="mt-6 grid grid-cols-1 md:grid-cols-3 gap-4">
              <div className="bg-white rounded-lg shadow-lg p-6 text-center">
                <div className="text-3xl font-bold text-blue-600 mb-2">
                  {quizzes.length}
                </div>
                <div className="text-gray-600 text-sm font-semibold">Total Quizzes</div>
              </div>
              <div className="bg-white rounded-lg shadow-lg p-6 text-center">
                <div className="text-3xl font-bold text-purple-600 mb-2">
                  {quizzes.reduce((sum, q) => sum + q.question_count, 0)}
                </div>
                <div className="text-gray-600 text-sm font-semibold">Total Questions</div>
              </div>
              <div className="bg-white rounded-lg shadow-lg p-6 text-center">
                <div className="text-3xl font-bold text-green-600 mb-2">
                  {Math.round(
                    quizzes.reduce((sum, q) => sum + q.question_count, 0) / quizzes.length
                  )}
                </div>
                <div className="text-gray-600 text-sm font-semibold">Avg Questions/Quiz</div>
              </div>
            </div>
          )}
        </>
      )}

      {/* Quiz Details Modal */}
      <QuizModal
        isOpen={isModalOpen}
        onClose={handleCloseModal}
        quiz={selectedQuiz}
        loading={modalLoading}
      />
    </div>
  );
};

export default History;