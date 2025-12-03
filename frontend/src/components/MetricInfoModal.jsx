import React, { useState, useEffect } from 'react';
import { getMetricInfo } from '../services/api';

const MetricInfoModal = ({ metricName, isOpen, onClose }) => {
  const [metricInfo, setMetricInfo] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (isOpen && metricName) {
      loadMetricInfo();
    }
  }, [isOpen, metricName]);

  const loadMetricInfo = async () => {
    setLoading(true);
    try {
      const info = await getMetricInfo(metricName);
      setMetricInfo(info);
    } catch (err) {
      console.error('Failed to load metric info:', err);
    } finally {
      setLoading(false);
    }
  };

  if (!isOpen) return null;

  const getScoreColor = (range) => {
    if (range.includes('0.9-1.0')) return 'text-green-400';
    if (range.includes('0.7-0.9') || range.includes('0.8')) return 'text-blue-400';
    if (range.includes('0.5-0.7') || range.includes('0.6')) return 'text-yellow-400';
    return 'text-red-400';
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-75 flex items-center justify-center z-50 p-4" onClick={onClose}>
      <div className="bg-gray-900 rounded-lg max-w-2xl w-full max-h-[90vh] overflow-y-auto border border-gray-700" onClick={(e) => e.stopPropagation()}>
        {/* Header */}
        <div className="sticky top-0 bg-gray-900 border-b border-gray-700 p-6 flex justify-between items-start">
          <div>
            <h2 className="text-2xl font-bold text-white mb-2">
              {metricInfo?.name || metricName}
            </h2>
            <p className="text-gray-400 text-sm">{metricInfo?.range}</p>
          </div>
          <button
            onClick={onClose}
            className="text-gray-400 hover:text-white text-2xl leading-none"
          >
            ×
          </button>
        </div>

        {/* Content */}
        <div className="p-6 space-y-6">
          {loading ? (
            <div className="text-center py-8">
              <div className="animate-spin inline-block w-8 h-8 border-4 border-white border-t-transparent rounded-full"></div>
              <p className="text-gray-400 mt-2">Loading metric information...</p>
            </div>
          ) : metricInfo ? (
            <>
              {/* Description */}
              <div>
                <h3 className="text-lg font-semibold text-white mb-2">What is it?</h3>
                <p className="text-gray-300 leading-relaxed">{metricInfo.description}</p>
              </div>

              {/* Formula */}
              <div className="bg-gray-800 rounded-lg p-4">
                <h3 className="text-sm font-semibold text-gray-400 mb-2">FORMULA</h3>
                <code className="text-blue-300 font-mono text-sm">{metricInfo.formula}</code>
              </div>

              {/* Example */}
              {metricInfo.example && (
                <div className="bg-gray-800 rounded-lg p-4">
                  <h3 className="text-sm font-semibold text-gray-400 mb-2">EXAMPLE</h3>
                  <p className="text-gray-300 text-sm">{metricInfo.example}</p>
                </div>
              )}

              {/* When to Use */}
              <div>
                <h3 className="text-lg font-semibold text-white mb-2">When to Use</h3>
                <p className="text-gray-300">{metricInfo.when_to_use}</p>
              </div>

              {/* Limitations */}
              {metricInfo.limitations && (
                <div className="bg-yellow-900 bg-opacity-20 border border-yellow-700 rounded-lg p-4">
                  <h3 className="text-sm font-semibold text-yellow-400 mb-2 flex items-center">
                    <svg className="w-4 h-4 mr-1" fill="currentColor" viewBox="0 0 20 20">
                      <path fillRule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
                    </svg>
                    LIMITATIONS
                  </h3>
                  <p className="text-gray-300 text-sm">{metricInfo.limitations}</p>
                </div>
              )}

              {/* Interpretation Guide */}
              {metricInfo.interpretation && (
                <div>
                  <h3 className="text-lg font-semibold text-white mb-3">How to Interpret Scores</h3>
                  <div className="space-y-2">
                    {Object.entries(metricInfo.interpretation).map(([range, meaning]) => (
                      <div key={range} className="flex items-start space-x-3">
                        <span className={`font-mono text-sm font-semibold ${getScoreColor(range)} min-w-[80px]`}>
                          {range}
                        </span>
                        <span className="text-gray-300 text-sm">{meaning}</span>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </>
          ) : (
            <div className="text-center py-8">
              <p className="text-gray-400">No information available for this metric.</p>
            </div>
          )}
        </div>

        {/* Footer */}
        <div className="sticky bottom-0 bg-gray-900 border-t border-gray-700 p-4">
          <button
            onClick={onClose}
            className="w-full px-4 py-2 bg-gray-800 hover:bg-gray-700 text-white rounded transition-colors"
          >
            Close
          </button>
        </div>
      </div>
    </div>
  );
};

export default MetricInfoModal;

