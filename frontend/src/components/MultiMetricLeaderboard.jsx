import React, { useState } from 'react';
import MetricInfoModal from './MetricInfoModal';

const MultiMetricLeaderboard = ({ leaderboard }) => {
  const [selectedMetric, setSelectedMetric] = useState(null);
  const [sortBy, setSortBy] = useState(leaderboard.primary_metric);
  const [sortDesc, setSortDesc] = useState(true);

  if (!leaderboard || !leaderboard.entries || leaderboard.entries.length === 0) {
    return null;
  }

  // Get all unique metrics from entries
  const allMetrics = new Set();
  leaderboard.entries.forEach(entry => {
    if (entry.detailed_scores) {
      Object.keys(entry.detailed_scores).forEach(metric => {
        // Filter out diagnostic metrics
        if (!['num_classes', 'total_predictions', 'true_positives', 'false_positives', 
              'false_negatives', 'total_questions', 'exact_matches_count', 'correct_retrievals',
              'total_queries', 'failed_retrievals'].includes(metric)) {
          allMetrics.add(metric);
        }
      });
    }
  });

  const metrics = Array.from(allMetrics);
  
  // Debug: log to see what we have
  console.log('Leaderboard:', leaderboard);
  console.log('Metrics found:', metrics);
  console.log('First entry:', leaderboard.entries[0]);
  
  // If no detailed metrics found, use primary metric as fallback
  if (metrics.length === 0) {
    return (
      <div className="p-8 text-center text-gray-400">
        <p className="mb-2">No detailed metrics available</p>
        <p className="text-sm">Switch to Simple view to see primary scores</p>
      </div>
    );
  }
  
  // Sort entries
  const sortedEntries = [...leaderboard.entries].sort((a, b) => {
    const aVal = a.detailed_scores?.[sortBy] || a.score;
    const bVal = b.detailed_scores?.[sortBy] || b.score;
    return sortDesc ? bVal - aVal : aVal - bVal;
  });

  const getScoreColor = (value) => {
    if (value >= 0.9) return 'text-green-400';
    if (value >= 0.7) return 'text-blue-400';
    if (value >= 0.5) return 'text-yellow-400';
    return 'text-red-400';
  };

  const handleSort = (metric) => {
    if (sortBy === metric) {
      setSortDesc(!sortDesc);
    } else {
      setSortBy(metric);
      setSortDesc(true);
    }
  };

  return (
    <>
      <div className="bg-gray-900 rounded-lg p-2 overflow-x-auto">
        <table className="w-full text-sm">
          <thead className="bg-gray-800 text-white">
            <tr>
              <th className="p-3 text-left w-16">Rank</th>
              <th className="p-3 text-left min-w-[180px]">Model</th>
              {metrics.map(metric => (
                <th 
                  key={metric}
                  className="p-3 text-center cursor-pointer hover:bg-gray-700 transition-colors"
                  onClick={() => handleSort(metric)}
                >
                  <button
                    onClick={(e) => {
                      e.stopPropagation();
                      setSelectedMetric(metric);
                    }}
                    className="text-blue-400 hover:text-blue-300 underline text-xs"
                  >
                    {metric.replace(/_/g, ' ').toUpperCase()}
                    {metric === leaderboard.primary_metric && <span className="ml-1">★</span>}
                  </button>
                  {sortBy === metric && (
                    <span className="ml-1">{sortDesc ? '↓' : '↑'}</span>
                  )}
                </th>
              ))}
              <th className="p-3 text-left">Updated</th>
            </tr>
          </thead>
          <tbody>
            {sortedEntries.map((entry, index) => (
              <tr 
                key={entry.submission_id}
                className={`${index % 2 === 0 ? 'bg-gray-700' : 'bg-gray-800'} hover:bg-gray-600 transition-colors`}
              >
                <td className="p-3 text-white">
                  <div className="flex items-center">
                    {index === 0 && (
                      <span className="mr-2 text-lg font-bold text-yellow-400">1st</span>
                    )}
                    {index === 1 && (
                      <span className="mr-2 text-lg font-bold text-gray-300">2nd</span>
                    )}
                    {index === 2 && (
                      <span className="mr-2 text-lg font-bold text-amber-600">3rd</span>
                    )}
                    {index > 2 && <span>{index + 1}</span>}
                  </div>
                </td>
                <td className="p-3 text-white">
                  <div className="flex items-center space-x-2">
                    <span className="font-medium">{entry.model_name}</span>
                    {entry.is_internal && (
                      <span className="px-2 py-0.5 text-xs bg-blue-600 rounded">Internal</span>
                    )}
                  </div>
                </td>
                {metrics.map(metric => {
                  const value = entry.detailed_scores?.[metric];
                  return (
                    <td key={metric} className={`p-3 text-center font-mono ${getScoreColor(value)}`}>
                      {value !== undefined ? value.toFixed(3) : '-'}
                    </td>
                  );
                })}
                <td className="p-3 text-gray-300 text-xs">{entry.updated_at}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Metric Info Modal */}
      {selectedMetric && (
        <MetricInfoModal
          metricName={selectedMetric}
          isOpen={!!selectedMetric}
          onClose={() => setSelectedMetric(null)}
        />
      )}
    </>
  );
};

export default MultiMetricLeaderboard;

