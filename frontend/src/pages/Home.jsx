import React, { useState, useEffect } from 'react';
import { getAllLeaderboards } from '../services/api';
import LeaderboardCard from '../components/LeaderboardCard';

const Home = () => {
  const [leaderboards, setLeaderboards] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [taskFilter, setTaskFilter] = useState('');

  useEffect(() => {
    loadLeaderboards();
  }, [taskFilter]);

  const loadLeaderboards = async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await getAllLeaderboards(taskFilter || null);
      setLeaderboards(data);
    } catch (err) {
      setError('Failed to load leaderboards. Make sure the API is running.');
    } finally {
      setLoading(false);
    }
  };

  const taskTypes = [
    { value: '', label: 'All Task Types' },
    { value: 'text_classification', label: 'Text Classification' },
    { value: 'named_entity_recognition', label: 'Named Entity Recognition' },
    { value: 'document_qa', label: 'Document Q&A' },
    { value: 'line_qa', label: 'Line Q&A' },
    { value: 'retrieval', label: 'Retrieval' },
  ];

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gray-900 pb-20 px-3">
      <h1 className="text-4xl font-bold text-white mb-4 mt-8">LLM Leaderboards</h1>
      <p className="text-gray-400 mb-4 text-center max-w-2xl">
        Transparent benchmarking platform for AI models across multiple task types
      </p>
      
      {/* Quick Links to Domains */}
      <div className="mb-8 flex flex-wrap gap-3 justify-center">
        <button
          onClick={() => window.location.href = '/domains?domain=multilingual'}
          className="px-5 py-2.5 bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 text-white rounded-lg text-sm font-medium transition-all shadow-lg hover:shadow-xl"
        >
          Multilingual Benchmarks
        </button>
        <button
          onClick={() => window.location.href = '/domains?domain=finance'}
          className="px-5 py-2.5 bg-gradient-to-r from-green-600 to-emerald-600 hover:from-green-700 hover:to-emerald-700 text-white rounded-lg text-sm font-medium transition-all shadow-lg hover:shadow-xl"
        >
          Finance Benchmarks
        </button>
        <button
          onClick={() => window.location.href = '/domains'}
          className="px-5 py-2.5 bg-gray-800 hover:bg-gray-700 text-white rounded-lg text-sm font-medium transition-all border border-gray-700 hover:border-gray-600"
        >
          View All Domains
        </button>
      </div>

      {/* Filter */}
      <div className="mb-8 w-full max-w-md">
        <select
          value={taskFilter}
          onChange={(e) => setTaskFilter(e.target.value)}
          className="w-full px-4 py-2 bg-gray-800 border border-gray-700 rounded text-white focus:outline-none focus:border-blue-500"
        >
          {taskTypes.map(type => (
            <option key={type.value} value={type.value}>
              {type.label}
            </option>
          ))}
        </select>
      </div>

      {/* Loading */}
      {loading && (
        <div className="text-white text-center">
          <div className="animate-spin inline-block w-8 h-8 border-4 border-white border-t-transparent rounded-full mb-2"></div>
          <p>Loading leaderboards...</p>
        </div>
      )}

      {/* Error */}
      {error && (
        <div className="max-w-2xl mx-auto p-6 bg-red-900 border border-red-700 rounded-lg text-white">
          <p className="font-bold mb-2">Error</p>
          <p>{error}</p>
          <button
            onClick={loadLeaderboards}
            className="mt-4 px-4 py-2 bg-red-700 hover:bg-red-600 rounded"
          >
            Retry
          </button>
        </div>
      )}

      {/* Leaderboards */}
      {!loading && !error && (
        <>
          {leaderboards.length === 0 ? (
            <div className="text-center text-gray-400 p-8">
              <p className="text-xl mb-4">No leaderboards found</p>
              <p className="text-sm">Create a dataset to get started!</p>
            </div>
          ) : (
            <div className="flex flex-col space-y-8 w-full max-w-[95%]">
              {leaderboards.map((leaderboard) => (
                <LeaderboardCard key={leaderboard.dataset_id} leaderboard={leaderboard} />
              ))}
            </div>
          )}

          <div className="mt-8 text-center text-gray-400 text-sm">
            <p>Showing {leaderboards.length} leaderboard{leaderboards.length !== 1 ? 's' : ''}</p>
          </div>
        </>
      )}
    </div>
  );
};

export default Home;

