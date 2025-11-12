import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import DatasetForm from '../components/DatasetForm';
import HFImporter from '../components/HFImporter';

const CreateDataset = () => {
  const navigate = useNavigate();
  const [activeTab, setActiveTab] = useState('manual'); // 'manual' or 'import'

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

        {/* Tabs */}
        <div className="mb-6 flex space-x-2 border-b border-gray-700">
          <button
            onClick={() => setActiveTab('manual')}
            className={`px-6 py-3 font-medium transition-colors ${
              activeTab === 'manual'
                ? 'text-white border-b-2 border-blue-500'
                : 'text-gray-400 hover:text-gray-300'
            }`}
          >
            📝 Manual Entry
          </button>
          <button
            onClick={() => setActiveTab('import')}
            className={`px-6 py-3 font-medium transition-colors ${
              activeTab === 'import'
                ? 'text-white border-b-2 border-blue-500'
                : 'text-gray-400 hover:text-gray-300'
            }`}
          >
            🤗 Import from HuggingFace
          </button>
        </div>
        
        {/* Content */}
        {activeTab === 'manual' ? (
          <DatasetForm onSuccess={handleSuccess} />
        ) : (
          <div className="max-w-3xl mx-auto">
            <HFImporter onSuccess={handleSuccess} />
          </div>
        )}
      </div>
    </div>
  );
};

export default CreateDataset;

