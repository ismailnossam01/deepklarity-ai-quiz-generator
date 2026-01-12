/**
 * QuizList Component
 * Displays all questions in a quiz
 */

import React from 'react';
import QuizCard from './QuizCard';

const QuizList = ({ quiz, showAnswers = false, onAnswerSubmit }) => {
  if (!quiz || quiz.length === 0) {
    return (
      <div className="text-center py-8">
        <p className="text-gray-500">No questions available.</p>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {quiz.map((question, index) => (
        <QuizCard
          key={index}
          question={question}
          index={index}
          showAnswers={showAnswers}
          onAnswerSubmit={onAnswerSubmit}
        />
      ))}
    </div>
  );
};

export default QuizList;