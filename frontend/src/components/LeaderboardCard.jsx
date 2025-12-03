import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import MetricInfoModal from './MetricInfoModal';
import MultiMetricLeaderboard from './MultiMetricLeaderboard';
import ModelInsights from './ModelInsights';
import LanguageBreakdown from './LanguageBreakdown';

const LeaderboardCard = ({ leaderboard }) => {
  const navigate = useNavigate();
  const [showMetricInfo, setShowMetricInfo] = useState(false);
  const [viewMode, setViewMode] = useState('simple'); // 'simple' or 'detailed'
  const [selectedModel, setSelectedModel] = useState(null);
  const [comparisonModels, setComparisonModels] = useState([]); // side-by-side comparison

  const toggleCompare = (entry) => {
    setComparisonModels((prev) => {
      const exists = prev.find((e) => e.submission_id === entry.submission_id);
      if (exists) {
        return prev.filter((e) => e.submission_id !== entry.submission_id);
      }
      // Limit to 3 models to keep UI readable
      if (prev.length >= 3) {
        return [...prev.slice(1), entry];
      }
      return [...prev, entry];
    });
  };

  const isInComparison = (entry) =>
    comparisonModels.some((e) => e.submission_id === entry.submission_id);

  const allComparisonMetrics = Array.from(
    new Set(
      comparisonModels.flatMap((m) =>
        m.detailed_scores ? Object.keys(m.detailed_scores) : []
      )
    )
  ).filter(
    (metric) =>
      ![
        'num_classes',
        'total_predictions',
        'true_positives',
        'false_positives',
        'false_negatives',
        'total_questions',
        'exact_matches_count',
        'correct_retrievals',
        'total_queries',
        'failed_retrievals',
      ].includes(metric)
  );

  return (
    <>
      <div className="w-full p-4 bg-gray-950 rounded-lg shadow-lg card-hover">
        <div className="flex justify-between items-center mb-4">
          <div>
            <h2 className="text-xl font-bold text-white">{leaderboard.dataset_name}</h2>
            <div className="flex items-center space-x-2 mt-1">
              <p className="text-sm text-gray-400">
                {leaderboard.task_type.replace('_', ' ').toUpperCase()}
              </p>
              <span className="text-gray-600">|</span>
              <button
                onClick={() => setShowMetricInfo(true)}
                className="text-sm text-blue-400 hover:text-blue-300 underline cursor-pointer flex items-center space-x-1"
                title="Click to learn about this metric"
              >
                <span>Metric: {leaderboard.primary_metric}</span>
                <svg className="w-3 h-3" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clipRule="evenodd" />
                </svg>
              </button>
            </div>
          </div>
        <div className="flex items-center space-x-2">
          {leaderboard.url && (
            <a
              href={leaderboard.url}
              className="text-blue-400 hover:text-blue-500 text-sm underline"
              target="_blank"
              rel="noopener noreferrer"
            >
              View Dataset
            </a>
          )}
          
          {/* View Toggle */}
          <div className="flex bg-gray-800 rounded">
            <button
              onClick={() => setViewMode('simple')}
              className={`px-3 py-1 text-xs rounded-l ${viewMode === 'simple' ? 'bg-blue-600 text-white' : 'text-gray-400'}`}
            >
              Simple
            </button>
            <button
              onClick={() => setViewMode('detailed')}
              className={`px-3 py-1 text-xs rounded-r ${viewMode === 'detailed' ? 'bg-blue-600 text-white' : 'text-gray-400'}`}
            >
              All Metrics
            </button>
          </div>
        </div>
      </div>
      
      {viewMode === 'simple' ? (
        <>
          <div className="grid grid-cols-5 text-white font-bold text-center bg-gray-900 p-4 rounded-t-lg">
            <div>Rank</div>
            <div>Model</div>
            <div>Score</div>
            <div>Last Updated</div>
            <div>Compare</div>
          </div>
      
          <div>
            {leaderboard.entries.length === 0 ? (
              <div className="text-center p-8 text-gray-400">
                No submissions yet
              </div>
            ) : (
              leaderboard.entries.slice(0, 5).map((entry, index) => (
                <div
                  key={entry.submission_id}
                  className={`grid grid-cols-5 text-center p-4 ${
                    index % 2 === 0 ? 'bg-gray-700 text-white' : 'bg-gray-800 text-white'
                  } hover:bg-gray-600`}
                >
                  <div className="flex items-center justify-center">
                    {entry.rank <= 3 && (
                      <span className={`mr-2 text-lg font-bold ${
                        entry.rank === 1 ? 'text-yellow-400' : 
                        entry.rank === 2 ? 'text-gray-300' : 
                        'text-amber-600'
                      }`}>
                        {entry.rank === 1 ? '1st' : entry.rank === 2 ? '2nd' : '3rd'}
                      </span>
                    )}
                    {entry.rank > 3 && <span>{entry.rank}</span>}
                  </div>
                  <div className="flex items-center justify-center">
                    {entry.model_name}
                    {entry.is_internal && (
                      <span className="ml-2 px-2 py-1 text-xs bg-blue-500 rounded">Internal</span>
                    )}
                  </div>
                  <div>{entry.score.toFixed(4)}</div>
                  <div className="text-sm text-gray-300">{entry.updated_at}</div>
                  <div className="flex items-center justify-center">
                    <button
                      type="button"
                      onClick={() => toggleCompare(entry)}
                      className={`px-3 py-1 rounded text-xs border ${
                        isInComparison(entry)
                          ? 'bg-blue-600 border-blue-400 text-white'
                          : 'bg-gray-900 border-gray-600 text-gray-200 hover:bg-gray-800'
                      }`}
                    >
                      {isInComparison(entry) ? 'Selected' : 'Compare'}
                    </button>
                  </div>
                </div>
              ))
            )}
          </div>

          {leaderboard.entries.length > 5 && (
            <div className="mt-3 flex flex-col md:flex-row md:items-center md:justify-between text-xs text-gray-400 space-y-2 md:space-y-0">
              <span>
                Showing top {Math.min(5, leaderboard.entries.length)} of {leaderboard.entries.length} submissions
              </span>
              <button
                type="button"
                onClick={() => navigate(`/leaderboard/${leaderboard.dataset_id}`)}
                className="self-start md:self-auto px-3 py-1 bg-gray-800 hover:bg-gray-700 text-white rounded border border-gray-600"
              >
                View full leaderboard →
              </button>
            </div>
          )}

          {/* Model comparison section */}
          {comparisonModels.length >= 2 && (
            <div className="mt-6 p-4 bg-gray-900 rounded-lg border border-gray-800 overflow-x-auto">
              <div className="flex justify-between items-center mb-4">
                <h3 className="text-lg font-semibold text-white">
                  Model Comparison ({comparisonModels.length} models)
                </h3>
                <button
                  type="button"
                  onClick={() => setComparisonModels([])}
                  className="text-xs text-gray-300 hover:text-white underline"
                >
                  Clear selection
                </button>
              </div>
              <table className="min-w-full text-xs md:text-sm">
                <thead>
                  <tr className="bg-gray-800 text-gray-100">
                    <th className="px-3 py-2 text-left">Metric</th>
                    {comparisonModels.map((m) => (
                      <th key={m.submission_id} className="px-3 py-2 text-left">
                        {m.model_name}
                      </th>
                    ))}
                  </tr>
                </thead>
                <tbody>
                  {/* Primary score row */}
                  <tr className="border-t border-gray-800">
                    <td className="px-3 py-2 font-semibold text-gray-200">
                      {leaderboard.primary_metric} (primary)
                    </td>
                    {comparisonModels.map((m) => (
                      <td key={m.submission_id} className="px-3 py-2 text-gray-100">
                        {m.score != null ? m.score.toFixed(4) : '-'}
                      </td>
                    ))}
                  </tr>
                  {/* Detailed metrics */}
                  {allComparisonMetrics.map((metric) => (
                    <tr key={metric} className="border-t border-gray-800">
                      <td className="px-3 py-2 text-gray-300">
                        {metric.replace(/_/g, ' ')}
                      </td>
                      {comparisonModels.map((m) => (
                        <td key={m.submission_id} className="px-3 py-2 text-gray-100">
                          {m.detailed_scores && m.detailed_scores[metric] != null
                            ? m.detailed_scores[metric].toFixed(4)
                            : '-'}
                        </td>
                      ))}
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </>
      ) : (
        <MultiMetricLeaderboard leaderboard={leaderboard} />
      )}
      
      {/* Show insights for selected model */}
      {selectedModel && selectedModel.detailed_scores && (
        <div className="mt-4 p-4 bg-gray-900 rounded-lg">
          <button
            onClick={() => setSelectedModel(null)}
            className="float-right text-gray-400 hover:text-white transition-colors"
            aria-label="Close"
          >
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
          
          {/* Language Breakdown (for multilingual datasets) */}
          <LanguageBreakdown scores={selectedModel.detailed_scores} />
          
          {/* Model Insights */}
          <ModelInsights
            scores={selectedModel.detailed_scores}
            primaryMetric={leaderboard.primary_metric}
            modelName={selectedModel.model_name}
          />
        </div>
      )}
    </div>

      {/* Metric Info Modal */}
      <MetricInfoModal
        metricName={leaderboard.primary_metric}
        isOpen={showMetricInfo}
        onClose={() => setShowMetricInfo(false)}
      />
    </>
  );
};

export default LeaderboardCard;

