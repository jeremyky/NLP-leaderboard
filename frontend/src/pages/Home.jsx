import React, { useState, useEffect } from 'react';
import { getAllLeaderboards } from '../services/api';
import LeaderboardCard from '../components/LeaderboardCard';

const Home = () => {
  const [leaderboards, setLeaderboards] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [taskFilter, setTaskFilter] = useState('');
  const [layoutMode, setLayoutMode] = useState('list'); // 'list' | 'grid' | 'single'
  const [activeIndex, setActiveIndex] = useState(0);

  useEffect(() => {
    loadLeaderboards();
  }, [taskFilter]);

  const loadLeaderboards = async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await getAllLeaderboards(taskFilter || null);
      setLeaderboards(data);
      setActiveIndex(0);
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

  const visibleCount = leaderboards.length;

  const handlePrev = () => {
    setActiveIndex((prev) =>
      visibleCount === 0 ? 0 : (prev - 1 + visibleCount) % visibleCount
    );
  };

  const handleNext = () => {
    setActiveIndex((prev) =>
      visibleCount === 0 ? 0 : (prev + 1) % visibleCount
    );
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gray-900 pb-20 px-3">
      <h1 className="text-4xl font-bold text-white mb-4 mt-8">LLM Leaderboards</h1>
      <p className="text-gray-400 mb-4 text-center max-w-2xl">
        Transparent benchmarking platform for AI models across multiple task types
      </p>

      {/* Summary ribbon */}
      {!loading && !error && leaderboards.length > 0 && (
        <div className="mb-6 w-full max-w-3xl">
          <div className="px-4 py-2 rounded-full bg-gradient-to-r from-blue-600/40 via-indigo-600/40 to-purple-600/40 border border-white/10 text-xs md:text-sm text-gray-100 flex flex-wrap items-center justify-center gap-x-4 gap-y-1 shadow-[0_0_18px_rgba(0,0,0,0.4)]">
            {(() => {
              const totalSubmissions = leaderboards.reduce(
                (sum, lb) => sum + (lb.entries?.length || 0),
                0
              );
              const datasetCount = leaderboards.length;
              const domainCount = new Set(
                leaderboards.map((lb) => lb.task_type)
              ).size;
              return (
                <>
                  <span className="flex items-center space-x-1">
                    <span>🔥</span>
                    <span>
                      {totalSubmissions} submission
                      {totalSubmissions !== 1 ? 's' : ''}
                    </span>
                  </span>
                  <span className="flex items-center space-x-1">
                    <span>📚</span>
                    <span>
                      {datasetCount} dataset
                      {datasetCount !== 1 ? 's' : ''}
                    </span>
                  </span>
                  <span className="flex items-center space-x-1">
                    <span>🌐</span>
                    <span>
                      {domainCount} task type
                      {domainCount !== 1 ? 's' : ''}
                    </span>
                  </span>
                  <span className="hidden sm:inline-flex items-center space-x-1 text-gray-200/90">
                    <span>⏱</span>
                    <span>Updated in real time as submissions complete</span>
                  </span>
                </>
              );
            })()}
          </div>
        </div>
      )}
      
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

      {/* Filter + Layout Controls */}
      <div className="mb-8 w-full max-w-4xl flex flex-col md:flex-row md:items-center md:justify-between space-y-3 md:space-y-0">
        <div className="w-full md:w-1/2">
          <select
            value={taskFilter}
            onChange={(e) => setTaskFilter(e.target.value)}
            className="w-full px-4 py-2 bg-gray-800 border border-gray-700 rounded text-white focus:outline-none focus:border-blue-500"
          >
            {taskTypes.map((type) => (
              <option key={type.value} value={type.value}>
                {type.label}
              </option>
            ))}
          </select>
        </div>

        <div className="flex items-center space-x-2 justify-center md:justify-end">
          <span className="text-xs text-gray-400 mr-1">View:</span>
          <div className="inline-flex bg-gray-900 rounded-lg border border-gray-700 overflow-hidden shadow-sm">
            {/* List view icon */}
            <button
              type="button"
              onClick={() => setLayoutMode('list')}
              className={`px-2.5 py-1.5 flex items-center justify-center text-xs ${
                layoutMode === 'list'
                  ? 'bg-blue-600 text-white'
                  : 'text-gray-300 hover:bg-gray-800'
              }`}
              title="List view"
              aria-label="List view"
            >
              <svg
                className="w-4 h-4"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M4 6h16M4 12h16M4 18h10"
                />
              </svg>
            </button>

            {/* 3x3 waffle grid */}
            <button
              type="button"
              onClick={() => setLayoutMode('grid')}
              className={`px-2.5 py-1.5 flex items-center justify-center text-xs border-l border-gray-700 ${
                layoutMode === 'grid'
                  ? 'bg-blue-600 text-white'
                  : 'text-gray-300 hover:bg-gray-800'
              }`}
              title="3×3 grid view"
              aria-label="Grid view"
            >
              <svg
                className="w-4 h-4"
                fill="currentColor"
                viewBox="0 0 20 20"
              >
                <rect x="3" y="3" width="4" height="4" rx="0.75" />
                <rect x="8" y="3" width="4" height="4" rx="0.75" />
                <rect x="13" y="3" width="4" height="4" rx="0.75" />
                <rect x="3" y="8" width="4" height="4" rx="0.75" />
                <rect x="8" y="8" width="4" height="4" rx="0.75" />
                <rect x="13" y="8" width="4" height="4" rx="0.75" />
                <rect x="3" y="13" width="4" height="4" rx="0.75" />
                <rect x="8" y="13" width="4" height="4" rx="0.75" />
                <rect x="13" y="13" width="4" height="4" rx="0.75" />
              </svg>
            </button>

            {/* Single-card / focus view */}
            <button
              type="button"
              onClick={() => setLayoutMode('single')}
              className={`px-2.5 py-1.5 flex items-center justify-center text-xs border-l border-gray-700 ${
                layoutMode === 'single'
                  ? 'bg-blue-600 text-white'
                  : 'text-gray-300 hover:bg-gray-800'
              }`}
              title="One leaderboard at a time"
              aria-label="Single leaderboard view"
            >
              <svg
                className="w-4 h-4"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <rect
                  x="4"
                  y="6"
                  width="16"
                  height="12"
                  rx="2"
                  ry="2"
                  strokeWidth={2}
                />
                <path
                  d="M8 10h8"
                  strokeWidth={2}
                  strokeLinecap="round"
                  strokeLinejoin="round"
                />
                <path
                  d="M8 14h5"
                  strokeWidth={2}
                  strokeLinecap="round"
                  strokeLinejoin="round"
                />
              </svg>
            </button>
          </div>
        </div>
      </div>

      {/* Loading */}
      {loading && (
        <div className="w-full max-w-5xl space-y-4 mt-4">
          {[0, 1, 2].map((i) => (
            <div
              key={i}
              className="animate-pulse bg-gray-900/80 border border-gray-800 rounded-2xl p-5"
            >
              <div className="h-5 bg-gray-700 rounded w-1/3 mb-3" />
              <div className="h-3 bg-gray-800 rounded w-1/2 mb-4" />
              <div className="grid grid-cols-5 gap-3">
                {[0, 1, 2, 3, 4].map((j) => (
                  <div key={j} className="h-8 bg-gray-800 rounded" />
                ))}
              </div>
            </div>
          ))}
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
          ) : layoutMode === 'list' ? (
            <div className="flex flex-col space-y-8 w-full max-w-[95%]">
              {leaderboards.map((leaderboard) => (
                <LeaderboardCard
                  key={leaderboard.dataset_id}
                  leaderboard={leaderboard}
                />
              ))}
            </div>
          ) : layoutMode === 'grid' ? (
            <div className="w-full max-w-6xl grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6">
              {leaderboards.map((leaderboard) => (
                <LeaderboardCard
                  key={leaderboard.dataset_id}
                  leaderboard={leaderboard}
                  compact={true}
                />
              ))}
            </div>
          ) : (
            // Single-card "carousel" view
            <div className="w-full max-w-4xl">
              {leaderboards[activeIndex] && (
                <LeaderboardCard
                  leaderboard={leaderboards[activeIndex]}
                  key={leaderboards[activeIndex].dataset_id}
                />
              )}
              <div className="mt-4 flex items-center justify-between text-sm text-gray-300">
                <button
                  type="button"
                  onClick={handlePrev}
                  className="px-3 py-1 bg-gray-800 hover:bg-gray-700 rounded border border-gray-700"
                  disabled={visibleCount === 0}
                >
                  ← Previous
                </button>
                <span>
                  {visibleCount === 0 ? '0 / 0' : `${activeIndex + 1} / ${visibleCount}`}
                </span>
                <button
                  type="button"
                  onClick={handleNext}
                  className="px-3 py-1 bg-gray-800 hover:bg-gray-700 rounded border border-gray-700"
                  disabled={visibleCount === 0}
                >
                  Next →
                </button>
              </div>
            </div>
          )}

          <div className="mt-8 text-center text-gray-400 text-sm">
            <p>
              Showing {leaderboards.length} leaderboard
              {leaderboards.length !== 1 ? 's' : ''} (
              {layoutMode === 'list'
                ? 'List view'
                : layoutMode === 'grid'
                ? 'Grid view'
                : 'Single-card view'}
              )
            </p>
          </div>
        </>
      )}
    </div>
  );
};

export default Home;

