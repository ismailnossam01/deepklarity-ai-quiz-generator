/**
 * Loading Spinner Component
 * Shows animated spinner during API calls
 */

import React from 'react';

const LoadingSpinner = ({ message = 'Loading...' }) => {
  return (
    <div className="flex flex-col items-center justify-center p-8">
      <div className="relative">
        {/* Outer spinning circle */}
        <div className="w-16 h-16 border-4 border-blue-200 border-t-blue-600 rounded-full animate-spin"></div>
        
        {/* Inner pulsing circle */}
        <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2">
          <div className="w-8 h-8 bg-blue-500 rounded-full opacity-75 animate-pulse"></div>
        </div>
      </div>
      
      {/* Loading message */}
      <p className="mt-4 text-gray-700 font-medium">{message}</p>
      
      {/* Sub-message for quiz generation */}
      {message.includes('Generating') && (
        <p className="mt-2 text-sm text-gray-500">
          This may take 10-30 seconds...
        </p>
      )}
    </div>
  );
};

export default LoadingSpinner;