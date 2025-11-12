import React, { useState } from 'react';
import MetricInfoModal from './MetricInfoModal';

const DetailedMetrics = ({ scores, primaryMetric }) => {
  const [expandedMetrics, setExpandedMetrics] = useState(false);
  const [selectedMetric, setSelectedMetric] = useState(null);

  if (!scores || Object.keys(scores).length === 0) {
    return null;
  }

  // Separate primary metrics from diagnostic ones
  const metricScores = Object.entries(scores).filter(([key]) => 
    !['num_classes', 'total_predictions', 'true_positives', 'false_positives', 
      'false_negatives', 'total_questions', 'exact_matches_count', 'correct_retrievals',
      'total_queries', 'failed_retrievals'].includes(key)
  );

  const diagnosticInfo = Object.entries(scores).filter(([key]) => 
    ['num_classes', 'total_predictions', 'true_positives', 'false_positives', 
     'false_negatives', 'total_questions', 'exact_matches_count', 'correct_retrievals',
     'total_queries', 'failed_retrievals'].includes(key)
  );

  const getMetricBadgeColor = (metricName, value) => {
    if (metricName === primaryMetric) {
      return 'bg-blue-600 border-blue-500';
    }
    if (value >= 0.9) return 'bg-green-700 border-green-600';
    if (value >= 0.7) return 'bg-blue-700 border-blue-600';
    if (value >= 0.5) return 'bg-yellow-700 border-yellow-600';
    return 'bg-red-700 border-red-600';
  };

  return (
    <>
      <div className="mt-2 space-y-2">
        {/* Primary Metric Display */}
        <div className="flex flex-wrap gap-2">
          {metricScores.slice(0, expandedMetrics ? undefined : 4).map(([metric, value]) => (
            <button
              key={metric}
              onClick={() => setSelectedMetric(metric)}
              className={`px-3 py-1 rounded text-xs font-medium border ${getMetricBadgeColor(metric, value)} text-white hover:opacity-80 transition-opacity`}
              title="Click to learn more about this metric"
            >
              {metric.replace(/_/g, ' ').toUpperCase()}: {typeof value === 'number' ? value.toFixed(3) : value}
              {metric === primaryMetric && <span className="ml-1">★</span>}
            </button>
          ))}
        </div>

        {/* Toggle Button */}
        {metricScores.length > 4 && (
          <button
            onClick={() => setExpandedMetrics(!expandedMetrics)}
            className="text-xs text-blue-400 hover:text-blue-300 underline"
          >
            {expandedMetrics ? '↑ Show less' : `↓ Show ${metricScores.length - 4} more metrics`}
          </button>
        )}

        {/* Diagnostic Info */}
        {expandedMetrics && diagnosticInfo.length > 0 && (
          <div className="text-xs text-gray-400 space-y-1 pt-2 border-t border-gray-700">
            {diagnosticInfo.map(([key, value]) => (
              <div key={key} className="flex justify-between">
                <span className="capitalize">{key.replace(/_/g, ' ')}:</span>
                <span className="font-mono">{value}</span>
              </div>
            ))}
          </div>
        )}
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

export default DetailedMetrics;

