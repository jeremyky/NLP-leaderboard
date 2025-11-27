import React, { useState, useEffect } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import { getAllLeaderboards } from '../services/api';
import LeaderboardCard from '../components/LeaderboardCard';

const DomainBenchmarks = () => {
  const navigate = useNavigate();
  const [searchParams, setSearchParams] = useSearchParams();
  const [leaderboards, setLeaderboards] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [activeDomain, setActiveDomain] = useState(searchParams.get('domain') || 'multilingual');

  useEffect(() => {
    loadLeaderboards();
  }, []);

  const loadLeaderboards = async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await getAllLeaderboards();
      setLeaderboards(data);
    } catch (err) {
      setError('Failed to load leaderboards');
    } finally {
      setLoading(false);
    }
  };

  const handleDomainChange = (domain) => {
    setActiveDomain(domain);
    setSearchParams({ domain });
  };

  // Categorize datasets
  const multilingual = leaderboards.filter(lb => 
    lb.dataset_name.includes('XNLI') || 
    lb.dataset_name.includes('MGSM') || 
    lb.dataset_name.includes('XCOPA') ||
    lb.dataset_name.includes('XQUAD') ||
    lb.dataset_name.includes('MultiNLI Cross')
  );

  const finance = leaderboards.filter(lb => 
    lb.dataset_name.includes('Financial') || 
    lb.dataset_name.includes('FiQA') ||
    lb.dataset_name.includes('FinQA') ||
    lb.dataset_name.includes('Twitter')
  );

  const science = leaderboards.filter(lb =>
    lb.dataset_name.includes('Science') ||
    lb.dataset_name.includes('Biology') ||
    lb.dataset_name.includes('Chemistry') ||
    lb.dataset_name.includes('Physics')
  );

  const code = leaderboards.filter(lb =>
    lb.dataset_name.includes('Code') ||
    lb.dataset_name.includes('HumanEval') ||
    lb.dataset_name.includes('MBPP')
  );

  const reasoning = leaderboards.filter(lb =>
    lb.dataset_name.includes('Math') ||
    lb.dataset_name.includes('GSM') ||
    lb.dataset_name.includes('Reasoning')
  );

  const safety = leaderboards.filter(lb =>
    lb.dataset_name.includes('Truthful') ||
    lb.dataset_name.includes('Safety') ||
    lb.dataset_name.includes('Bias') ||
    lb.dataset_name.includes('Toxicity')
  );

  const domains = [
    { 
      id: 'multilingual', 
      name: 'Multilingual', 
      color: 'from-blue-500 to-cyan-500',
      data: multilingual,
      description: 'Cross-lingual evaluation across 20+ languages'
    },
    { 
      id: 'finance', 
      name: 'Finance & Business', 
      color: 'from-green-500 to-emerald-500',
      data: finance,
      description: 'Financial sentiment, Q&A, and entity recognition'
    },
    { 
      id: 'science', 
      name: 'Science & Education', 
      color: 'from-purple-500 to-pink-500',
      data: science,
      description: 'Scientific reasoning and educational tasks'
    },
    { 
      id: 'code', 
      name: 'Code Generation', 
      color: 'from-orange-500 to-red-500',
      data: code,
      description: 'Programming and software engineering tasks'
    },
    { 
      id: 'reasoning', 
      name: 'Mathematical Reasoning', 
      color: 'from-indigo-500 to-blue-500',
      data: reasoning,
      description: 'Multi-step problem solving and logical reasoning'
    },
    { 
      id: 'safety', 
      name: 'Safety & Alignment', 
      color: 'from-yellow-500 to-amber-500',
      data: safety,
      description: 'Truthfulness, toxicity, and bias evaluation'
    },
  ];

  const currentDomain = domains.find(d => d.id === activeDomain);
  const displayData = currentDomain?.data || [];

  return (
    <div className="min-h-screen bg-gray-900 pb-20 px-3">
      {/* Header */}
      <div className="max-w-7xl mx-auto pt-8 pb-6">
        <button
          onClick={() => navigate('/')}
          className="text-blue-400 hover:text-blue-300 mb-4"
        >
          ← Back to All Leaderboards
        </button>
        
        <h1 className="text-4xl font-bold text-white mb-2">Domain-Specific Benchmarks</h1>
        <p className="text-gray-400">
          Specialized evaluation suites for specific domains and frontier capabilities
        </p>
      </div>

      {/* Domain Navigation */}
      <div className="max-w-7xl mx-auto mb-8">
        <div className="bg-gray-950 rounded-lg p-4">
          <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3">
            {domains.map(domain => (
              <button
                key={domain.id}
                onClick={() => handleDomainChange(domain.id)}
                className={`p-4 rounded-lg border-2 transition-all ${
                  activeDomain === domain.id
                    ? `border-transparent bg-gradient-to-br ${domain.color} shadow-lg`
                    : 'border-gray-700 bg-gray-800 hover:border-gray-600 hover:bg-gray-700'
                }`}
              >
                <div className={`font-semibold text-sm mb-1 ${
                  activeDomain === domain.id ? 'text-white' : 'text-gray-300'
                }`}>
                  {domain.name}
                </div>
                <div className={`text-xs ${
                  activeDomain === domain.id ? 'text-white text-opacity-80' : 'text-gray-500'
                }`}>
                  {domain.data.length} {domain.data.length === 1 ? 'benchmark' : 'benchmarks'}
                </div>
              </button>
            ))}
          </div>
        </div>
      </div>

      {/* Content */}
      <div className="max-w-7xl mx-auto">
        {loading ? (
          <div className="text-white text-center py-12">
            <div className="animate-spin inline-block w-8 h-8 border-4 border-white border-t-transparent rounded-full mb-2"></div>
            <p>Loading benchmarks...</p>
          </div>
        ) : error ? (
          <div className="max-w-2xl mx-auto p-6 bg-red-900 border border-red-700 rounded-lg text-white">
            <p className="font-bold mb-2">Error</p>
            <p>{error}</p>
          </div>
        ) : (
          <>
            {/* Domain Header */}
            <div className={`bg-gradient-to-br ${currentDomain?.color} rounded-lg p-6 mb-8 shadow-lg`}>
              <div className="flex items-start">
                <div className="flex-1">
                  <h2 className="text-2xl font-bold text-white mb-2">
                    {currentDomain?.name}
                  </h2>
                  <p className="text-white text-opacity-90 mb-4">
                    {currentDomain?.description}
                  </p>
                  <div className="flex items-center space-x-4 text-sm">
                    <span className="px-3 py-1 bg-white bg-opacity-20 text-white rounded backdrop-blur-sm">
                      {displayData.length} {displayData.length === 1 ? 'Benchmark' : 'Benchmarks'}
                    </span>
                    <span className="px-3 py-1 bg-white bg-opacity-20 text-white rounded backdrop-blur-sm">
                      {displayData.reduce((sum, lb) => sum + lb.entries.length, 0)} Models
                    </span>
                  </div>
                </div>
              </div>
            </div>

            {/* Leaderboards */}
            {displayData.length === 0 ? (
              <div className="text-center text-gray-400 p-12 bg-gray-950 rounded-lg border border-gray-800">
                <svg className="w-16 h-16 mx-auto mb-4 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                <p className="text-xl mb-2 text-gray-300">Coming Soon</p>
                <p className="text-sm mb-6">
                  No {currentDomain?.name} benchmarks available yet.
                </p>
                <button
                  onClick={() => navigate('/create-dataset')}
                  className="px-6 py-2 btn-black rounded"
                >
                  Create First Benchmark
                </button>
              </div>
            ) : (
              <div className="flex flex-col space-y-8">
                {displayData.map((leaderboard) => (
                  <LeaderboardCard key={leaderboard.dataset_id} leaderboard={leaderboard} />
                ))}
              </div>
            )}
          </>
        )}
      </div>
    </div>
  );
};

export default DomainBenchmarks;

