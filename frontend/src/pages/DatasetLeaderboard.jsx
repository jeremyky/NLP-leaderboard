import React, { useEffect, useState } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { getLeaderboard } from '../services/api';
import LeaderboardCard from '../components/LeaderboardCard';

const DatasetLeaderboard = () => {
  const { datasetId } = useParams();
  const navigate = useNavigate();
  const [leaderboard, setLeaderboard] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const load = async () => {
      setLoading(true);
      setError(null);
      try {
        const data = await getLeaderboard(datasetId, true);
        setLeaderboard(data);
      } catch (err) {
        setError('Failed to load leaderboard. Make sure the API is running.');
      } finally {
        setLoading(false);
      }
    };

    if (datasetId) {
      load();
    }
  }, [datasetId]);

  return (
    <div className="min-h-screen bg-gray-900 pb-20 px-3">
      <div className="max-w-7xl mx-auto pt-8">
        <button
          onClick={() => navigate(-1)}
          className="text-blue-400 hover:text-blue-300 mb-4"
        >
          ← Back
        </button>

        {loading ? (
          <div className="text-center text-white py-10">
            <div className="animate-spin inline-block w-8 h-8 border-4 border-white border-t-transparent rounded-full mb-2" />
            <p>Loading leaderboard...</p>
          </div>
        ) : error ? (
          <div className="max-w-2xl mx-auto p-6 bg-red-900 border border-red-700 rounded-lg text-white">
            <p className="font-bold mb-2">Error</p>
            <p>{error}</p>
          </div>
        ) : leaderboard ? (
          <LeaderboardCard leaderboard={leaderboard} />
        ) : null}
      </div>
    </div>
  );
};

export default DatasetLeaderboard;


