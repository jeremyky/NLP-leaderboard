import React from 'react';
import { useNavigate } from 'react-router-dom';
import SubmissionForm from '../components/SubmissionForm';

// Strip trailing slash to avoid double-slash in URLs
const API_BASE_URL = (import.meta.env.VITE_API_URL || 'http://localhost:8000').replace(/\/$/, '');

const Submit = () => {
  const navigate = useNavigate();

  const handleSuccess = (data) => {
    // Don't auto-navigate, let user see the results
  };

  return (
    <div className="min-h-screen bg-gray-900 py-8 px-3">
      <div className="max-w-6xl mx-auto">
        <div className="mb-6 flex justify-between items-center">
          <button
            onClick={() => navigate('/')}
            className="text-blue-400 hover:text-blue-300"
          >
            ← Back to Leaderboards
          </button>
          
          <a
            href={`${API_BASE_URL}/docs`}
            target="_blank"
            rel="noopener noreferrer"
            className="text-gray-400 hover:text-gray-300 text-sm"
          >
            API Documentation →
          </a>
        </div>
        
        <SubmissionForm onSuccess={handleSuccess} />
      </div>
    </div>
  );
};

export default Submit;

