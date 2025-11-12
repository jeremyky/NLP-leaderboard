import React from 'react';
import { useNavigate } from 'react-router-dom';
import DatasetForm from '../components/DatasetForm';

const CreateDataset = () => {
  const navigate = useNavigate();

  const handleSuccess = (data) => {
    setTimeout(() => {
      navigate('/');
    }, 3000);
  };

  return (
    <div className="min-h-screen bg-gray-900 py-8 px-3">
      <div className="max-w-6xl mx-auto">
        <div className="mb-6">
          <button
            onClick={() => navigate('/')}
            className="text-blue-400 hover:text-blue-300"
          >
            ← Back to Leaderboards
          </button>
        </div>
        
        <DatasetForm onSuccess={handleSuccess} />
      </div>
    </div>
  );
};

export default CreateDataset;

