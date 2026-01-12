/**
 * QuizCard Component
 * Displays a single quiz question with options
 */

import React, { useState } from 'react';

const QuizCard = ({ question, index, showAnswers = false, onAnswerSubmit }) => {
  const [selectedOption, setSelectedOption] = useState(null);
  const [isAnswered, setIsAnswered] = useState(false);

  // Get difficulty badge color
  const getDifficultyColor = (difficulty) => {
    switch (difficulty) {
      case 'easy':
        return 'bg-green-100 text-green-800 border-green-300';
      case 'medium':
        return 'bg-yellow-100 text-yellow-800 border-yellow-300';
      case 'hard':
        return 'bg-red-100 text-red-800 border-red-300';
      default:
        return 'bg-gray-100 text-gray-800 border-gray-300';
    }
  };

  // Handle option selection
  const handleOptionClick = (option) => {
    if (!isAnswered && !showAnswers) {
      setSelectedOption(option);
    }
  };

  // Submit answer
  const handleSubmit = () => {
    setIsAnswered(true);
    if (onAnswerSubmit) {
      onAnswerSubmit(index, selectedOption === question.answer);
    }
  };

  // Get option style based on state
  const getOptionStyle = (option) => {
    const baseStyle = "p-4 rounded-lg border-2 cursor-pointer transition-all duration-200 bg-white";
    
    // If showing answers (details view)
    if (showAnswers) {
      if (option === question.answer) {
        return `${baseStyle} border-green-500 bg-green-50 text-gray-900`;
      }
      return `${baseStyle} border-gray-200 text-gray-700 hover:border-gray-300`;
    }
    
    // If answered (quiz mode)
    if (isAnswered) {
      if (option === question.answer) {
        return `${baseStyle} border-green-500 bg-green-50 text-gray-900`;
      }
      if (option === selectedOption) {
        return `${baseStyle} border-red-500 bg-red-50 text-gray-900`;
      }
      return `${baseStyle} border-gray-200 text-gray-700`;
    }
    
    // If selected but not answered
    if (option === selectedOption) {
      return `${baseStyle} border-blue-500 bg-blue-50 text-gray-900`;
    }
    
    // Default state
    return `${baseStyle} border-gray-200 hover:border-blue-400 hover:bg-blue-50 text-gray-800`;
  };

  return (
    <div className="bg-white rounded-lg shadow-sm p-6 mb-4 border border-gray-200 fade-in">
      {/* Question Header */}
      <div className="flex items-start justify-between mb-4">
        <h3 className="text-lg font-bold text-gray-900 flex-1">
          <span className="text-blue-600 mr-2">Q{index + 1}.</span>
          {question.question}
        </h3>
        <span className={`px-3 py-1 rounded-full text-xs font-semibold border ${getDifficultyColor(question.difficulty)}`}>
          {question.difficulty.toUpperCase()}
        </span>
      </div>

      {/* Options */}
      <div className="space-y-3 mb-4">
        {question.options.map((option, idx) => (
          <div
            key={idx}
            onClick={() => handleOptionClick(option)}
            className={getOptionStyle(option)}
          >
            <div className="flex items-center">
              <span className="font-semibold mr-3 text-gray-600">
                {String.fromCharCode(65 + idx)}.
              </span>
              <span className="flex-1">{option}</span>
              
              {/* Show checkmark or X */}
              {(showAnswers || isAnswered) && option === question.answer && (
                <span className="text-green-600 font-bold text-xl">✓</span>
              )}
              {isAnswered && option === selectedOption && option !== question.answer && (
                <span className="text-red-600 font-bold text-xl">✗</span>
              )}
            </div>
          </div>
        ))}
      </div>

      {/* Submit button (quiz mode) */}
      {!showAnswers && !isAnswered && selectedOption && (
        <button
          onClick={handleSubmit}
          className="w-full bg-blue-600 text-white py-3 rounded-lg font-semibold hover:bg-blue-700 transition-colors shadow-sm"
        >
          Submit Answer
        </button>
      )}

      {/* Explanation (shown after answering or in details view) */}
      {(showAnswers || isAnswered) && (
        <div className="mt-4 p-4 bg-blue-50 rounded-lg border-l-4 border-blue-500">
          <p className="text-sm font-semibold text-blue-900 mb-1">💡 Explanation:</p>
          <p className="text-sm text-gray-800">{question.explanation}</p>
          <p className="text-xs text-gray-700 mt-2">
            <strong>Correct Answer:</strong> {question.answer}
          </p>
        </div>
      )}
    </div>
  );
};

export default QuizCard;