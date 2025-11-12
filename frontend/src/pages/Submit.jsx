import React from 'react';
import { useNavigate } from 'react-router-dom';
import SubmissionForm from '../components/SubmissionForm';

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
            href="http://localhost:8000/docs"
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

