/**
 * API service for communicating with backend.
 * All backend API calls are defined here.
 */

import axios from 'axios';

// Get API URL from environment variable
const API_URL = import.meta.env.VITE_API_URL;

// Create axios instance with default config
const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 60000, // 60 second timeout (quiz generation can take time)
});

/**
 * Generate a new quiz from Wikipedia URL
 * @param {string} url - Wikipedia article URL
 * @returns {Promise} - Quiz data
 */
export const generateQuiz = async (url) => {
  try {
    const response = await api.post('/api/quiz/generate', { url });
    return response.data;
  } catch (error) {
    console.error('Error generating quiz:', error);
    throw error.response?.data?.detail || 'Failed to generate quiz. Please try again.';
  }
};

/**
 * Get a specific quiz by ID
 * @param {number} quizId - Quiz ID
 * @returns {Promise} - Quiz data
 */
export const getQuiz = async (quizId) => {
  try {
    const response = await api.get(`/api/quiz/${quizId}`);
    return response.data;
  } catch (error) {
    console.error('Error fetching quiz:', error);
    throw error.response?.data?.detail || 'Failed to fetch quiz.';
  }
};

/**
 * Get list of all quizzes (for history view)
 * @returns {Promise} - Array of quizzes
 */
export const getQuizList = async () => {
  try {
    const response = await api.get('/api/quizzes');
    return response.data;
  } catch (error) {
    console.error('Error fetching quiz list:', error);
    throw error.response?.data?.detail || 'Failed to fetch quiz list.';
  }
};

/**
 * Delete a quiz by ID (optional)
 * @param {number} quizId - Quiz ID
 * @returns {Promise}
 */
export const deleteQuiz = async (quizId) => {
  try {
    const response = await api.delete(`/api/quiz/${quizId}`);
    return response.data;
  } catch (error) {
    console.error('Error deleting quiz:', error);
    throw error.response?.data?.detail || 'Failed to delete quiz.';
  }
};

/**
 * Check API health
 * @returns {Promise}
 */
export const checkHealth = async () => {
  try {
    const response = await api.get('/');
    return response.data;
  } catch (error) {
    console.error('Error checking API health:', error);
    throw 'Backend API is not responding. Make sure it is running.';
  }
};

export default api;