import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import MetricInfoModal from './MetricInfoModal';
import MultiMetricLeaderboard from './MultiMetricLeaderboard';
import ModelInsights from './ModelInsights';
import LanguageBreakdown from './LanguageBreakdown';

const LeaderboardCard = ({ leaderboard, compact = false, showAll = false }) => {
  const navigate = useNavigate();
  const [showMetricInfo, setShowMetricInfo] = useState(false);
  const [viewMode, setViewMode] = useState('simple'); // 'simple' or 'detailed'
  const [selectedModel, setSelectedModel] = useState(null);
  const [comparisonModels, setComparisonModels] = useState([]); // side-by-side comparison

  const getDatasetIcon = (name) => {
    const n = name.toLowerCase();
    if (n.includes('multilingual') || n.includes('xnli') || n.includes('xquad') || n.includes('mgsm')) {
      return '🌐';
    }
    if (n.includes('financial') || n.includes('fiqa') || n.includes('finqa') || n.includes('finance')) {
      return '💸';
    }
    if (n.includes('news') || n.includes('ag news')) {
      return '📰';
    }
    if (n.includes('sentiment') || n.includes('imdb') || n.includes('sst')) {
      return '🎬';
    }
    if (n.includes('squad') || n.includes('qa')) {
      return '📚';
    }
    if (n.includes('gsm') || n.includes('math')) {
      return '🧮';
    }
    if (n.includes('truthful') || n.includes('toxicity') || n.includes('safety')) {
      return '🧠';
    }
    if (n.includes('code') || n.includes('humaneval') || n.includes('mbpp')) {
      return '💻';
    }
    return '📊';
  };

  const headerGradientClass = (() => {
    switch (leaderboard.task_type) {
      case 'text_classification':
        return 'from-indigo-600/40 via-blue-600/40 to-sky-500/30';
      case 'document_qa':
      case 'line_qa':
        return 'from-emerald-600/40 via-teal-500/40 to-cyan-500/30';
      case 'named_entity_recognition':
        return 'from-pink-600/40 via-rose-500/40 to-orange-500/30';
      case 'retrieval':
        return 'from-amber-500/40 via-yellow-400/40 to-lime-400/30';
      default:
        return 'from-slate-600/40 via-slate-500/40 to-slate-400/30';
    }
  })();

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

  // Compact mode for grid view
  if (compact) {
    const topThree = leaderboard.entries.slice(0, 3);
    return (
      <>
        <div 
          className="w-full p-5 bg-gray-950/95 rounded-2xl shadow-[0_1px_4px_rgba(0,0,0,0.35)] hover:shadow-[0_10px_30px_rgba(0,0,0,0.7)] border border-gray-800/70 hover:border-gray-700 transition-all duration-200 hover:-translate-y-1 cursor-pointer flex flex-col h-full"
          onClick={() => navigate(`/leaderboard/${leaderboard.dataset_id}`)}
        >
          {/* Compact header */}
          <div className={`rounded-xl bg-gradient-to-r ${headerGradientClass} p-3 mb-4`}>
            <div className="text-base font-bold text-white flex items-center space-x-2 mb-1.5">
              <span className="text-lg">{getDatasetIcon(leaderboard.dataset_name)}</span>
              <span className="truncate">{leaderboard.dataset_name}</span>
            </div>
            <div className="flex items-center gap-2 text-xs">
              <span className="inline-flex items-center px-1.5 py-0.5 rounded-full bg-black/30 text-gray-100">
                📂 {leaderboard.task_type.replace('_', ' ')}
              </span>
              <span className="inline-flex items-center px-1.5 py-0.5 rounded-full bg-black/25 text-blue-100">
                📊 {leaderboard.primary_metric}
              </span>
            </div>
          </div>

          {/* Compact entries */}
          {topThree.length === 0 ? (
            <div className="flex-1 flex items-center justify-center text-gray-400 text-sm py-8">
              No submissions yet
            </div>
          ) : (
            <div className="space-y-2 flex-1">
              {topThree.map((entry) => (
                <div
                  key={entry.submission_id}
                  className="flex items-center justify-between p-3 bg-gray-900/70 rounded-lg border border-white/5 hover:bg-gray-800/80 transition-colors"
                >
                  <div className="flex items-center space-x-2 flex-1 min-w-0">
                    {entry.rank <= 3 && (
                      <span className="text-base flex-shrink-0">
                        {entry.rank === 1 ? '🥇' : entry.rank === 2 ? '🥈' : '🥉'}
                      </span>
                    )}
                    <div className="min-w-0 flex-1">
                      <div className="text-sm font-medium text-white truncate">
                        {entry.model_name}
                      </div>
                      {entry.is_internal && (
                        <span className="text-xs text-blue-300">Internal</span>
                      )}
                    </div>
                  </div>
                  <div className="flex items-center space-x-2 flex-shrink-0">
                    {/* Score bar */}
                    <div className="hidden sm:flex items-center space-x-1.5">
                      <div className="w-12 h-1.5 bg-gray-700 rounded-full overflow-hidden">
                        <div
                          className="h-full bg-gradient-to-r from-emerald-500 to-green-400 rounded-full"
                          style={{ width: `${Math.min(entry.score * 100, 100)}%` }}
                        />
                      </div>
                    </div>
                    <span className="text-sm font-mono font-semibold text-emerald-400 min-w-[4rem] text-right">
                      {entry.score.toFixed(3)}
                    </span>
                  </div>
                </div>
              ))}
            </div>
          )}

          {/* View more footer */}
          {leaderboard.entries.length > 3 && (
            <div className="mt-4 pt-3 border-t border-white/5 text-center">
              <span className="text-xs text-gray-400">
                +{leaderboard.entries.length - 3} more models →
              </span>
            </div>
          )}
        </div>

        <MetricInfoModal
          metricName={leaderboard.primary_metric}
          isOpen={showMetricInfo}
          onClose={() => setShowMetricInfo(false)}
        />
      </>
    );
  }

  // Full mode for list/single view
  return (
    <>
      <div className="w-full p-4 bg-gray-950/95 rounded-2xl shadow-[0_1px_4px_rgba(0,0,0,0.35)] hover:shadow-[0_10px_30px_rgba(0,0,0,0.7)] border border-gray-800/70 hover:border-gray-700 transition-transform duration-150 hover:-translate-y-0.5">
        {/* Header with subtle gradient banner */}
        <div className={`mb-4 rounded-xl bg-gradient-to-r ${headerGradientClass} p-4 flex flex-col md:flex-row md:items-center md:justify-between`}>
          <div>
            <h2 className="text-xl font-bold text-white flex items-center space-x-2">
              <span className="text-xl">
                {getDatasetIcon(leaderboard.dataset_name)}
              </span>
              <span>{leaderboard.dataset_name}</span>
            </h2>
            <div className="flex items-center flex-wrap gap-2 mt-2 text-xs md:text-sm">
              <span className="inline-flex items-center px-2 py-0.5 rounded-full bg-black/30 text-gray-100">
                <span className="mr-1">📂</span>
                {leaderboard.task_type.replace('_', ' ').toUpperCase()}
              </span>
              <button
                onClick={() => setShowMetricInfo(true)}
                className="inline-flex items-center px-2 py-0.5 rounded-full bg-black/25 text-blue-100 hover:text-white hover:bg-black/40 text-xs cursor-pointer transition-colors"
                title="Click to learn about this metric"
              >
                <span className="mr-1">📊 Metric:</span>
                <span className="font-semibold">{leaderboard.primary_metric}</span>
              </button>
              
              {/* Comprehensive test coverage badge */}
              {(() => {
                const testedDatasets = [
                  "AG News - Text Classification",
                  "SST-2 - Sentiment Analysis",
                  "SQuAD - Question Answering",
                  "XNLI - Cross-Lingual Natural Language Inference"
                ];
                if (testedDatasets.includes(leaderboard.dataset_name)) {
                  return (
                    <span 
                      className="inline-flex items-center px-2 py-0.5 rounded-full bg-green-900/40 text-green-300 border border-green-700/50 text-xs"
                      title="This dataset has 300+ comprehensive test cases validating evaluator correctness"
                    >
                      <span className="mr-1">✓</span>
                      <span>Comprehensive Tests</span>
                    </span>
                  );
                }
                return null;
              })()}
            </div>
          </div>
          <div className="mt-3 md:mt-0 flex items-center space-x-3">
          {leaderboard.url && (
            <a
              href={leaderboard.url}
                className="inline-flex items-center px-3 py-1.5 bg-black/30 hover:bg-black/40 text-sm text-blue-100 hover:text-white rounded-full border border-white/10 transition-colors"
              target="_blank"
              rel="noopener noreferrer"
            >
                <span className="mr-1">🔗</span>
              View Dataset
            </a>
          )}
          
          {/* View Toggle */}
            <div className="flex bg-black/30 rounded-full border border-white/10 overflow-hidden text-xs">
            <button
              onClick={() => setViewMode('simple')}
                className={`px-3 py-1 flex items-center space-x-1 ${
                  viewMode === 'simple'
                    ? 'bg-white/20 text-white'
                    : 'text-gray-200 hover:bg-white/10'
                }`}
            >
                <span className="text-xs">📈</span>
                <span>Simple</span>
            </button>
            <button
              onClick={() => setViewMode('detailed')}
                className={`px-3 py-1 flex items-center space-x-1 ${
                  viewMode === 'detailed'
                    ? 'bg-white/20 text-white'
                    : 'text-gray-200 hover:bg-white/10'
                }`}
            >
                <span className="text-xs">📊</span>
                <span>All Metrics</span>
            </button>
          </div>
        </div>
      </div>
      
      {viewMode === 'simple' ? (
        <>
          <div className="grid grid-cols-5 text-white font-semibold text-center bg-gray-900/80 p-3 rounded-t-xl border-b border-white/5 text-xs md:text-sm tracking-wide">
            <div className="flex items-center justify-center space-x-1">
              <span>🏆</span>
              <span>Rank</span>
            </div>
            <div className="flex items-center justify-center space-x-1">
              <span>🤖</span>
              <span>Model</span>
            </div>
            <div className="flex items-center justify-center space-x-1">
              <span>📊</span>
              <span>Score</span>
            </div>
            <div className="flex items-center justify-center space-x-1">
              <span>⏱</span>
              <span>Last Updated</span>
            </div>
            <div className="flex items-center justify-center space-x-1">
              <span>🔍</span>
              <span>Compare</span>
            </div>
          </div>
      
          <div>
            {leaderboard.entries.length === 0 ? (
              <div className="text-center p-8 text-gray-400 bg-gray-900/70 rounded-b-xl border border-t-0 border-gray-800/80">
                No submissions yet
              </div>
            ) : (
              (showAll ? leaderboard.entries : leaderboard.entries.slice(0, 5)).map((entry, index) => (
                <div
                  key={entry.submission_id}
                  className={`grid grid-cols-5 text-center px-4 py-3 text-white border-b border-white/5 last:rounded-b-xl last:border-b-0 hover:bg-gray-800 ${
                    !entry.is_internal 
                      ? 'bg-purple-900/30 border-l-4 border-l-purple-500' 
                      : index % 2 === 0 
                      ? 'bg-gray-900/70 bg-opacity-100' 
                      : 'bg-gray-900/70 bg-opacity-90'
                  }`}
                >
                  <div className="flex items-center justify-center">
                    {entry.rank <= 3 ? (
                      <span
                        className={`px-2 py-1 rounded-lg text-xs font-semibold inline-flex items-center space-x-1 ${
                          entry.rank === 1
                            ? 'bg-yellow-400/20 text-yellow-300 border border-yellow-400/40'
                            : entry.rank === 2
                            ? 'bg-gray-300/20 text-gray-200 border border-gray-300/40'
                            : 'bg-amber-500/20 text-amber-300 border border-amber-500/40'
                        }`}
                      >
                        <span>
                          {entry.rank === 1
                            ? '🥇'
                            : entry.rank === 2
                            ? '🥈'
                            : '🥉'}
                        </span>
                        <span>{entry.rank === 1 ? '1st' : entry.rank === 2 ? '2nd' : '3rd'}</span>
                      </span>
                    ) : (
                      <span className="px-2 py-1 rounded-lg text-xs bg-gray-800 text-gray-200 border border-gray-700">
                        #{entry.rank}
                      </span>
                    )}
                  </div>
                  <div
                    className="flex items-center justify-center space-x-2"
                    title={`${entry.model_name}${entry.is_internal ? ' • Internal' : ''}`}
                  >
                    <span className="truncate max-w-[9rem] md:max-w-[12rem]">
                    {entry.model_name}
                    </span>
                    {entry.is_internal && (
                      <span className="px-2 py-0.5 text-[10px] bg-blue-500/20 border border-blue-400/60 rounded-full text-blue-100">
                        Internal
                      </span>
                    )}
                  </div>
                  <div className="flex items-center justify-center space-x-2">
                    <div className="w-16 h-1.5 bg-gray-800 rounded-full overflow-hidden">
                      <div
                        className="h-full bg-emerald-400"
                        style={{
                          width: `${Math.max(
                            0,
                            Math.min(1, entry.score ?? 0)
                          ) * 100}%`,
                        }}
                      ></div>
                    </div>
                    <span className="text-sm font-mono">
                      {entry.score.toFixed(4)}
                    </span>
                  </div>
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

          {/* External submissions below top 5 */}
          {(() => {
            const externalNotInTop5 = leaderboard.entries
              .filter(e => !e.is_internal && e.rank > 5);
            
            if (externalNotInTop5.length > 0) {
              return (
                <div className="mt-4 p-4 bg-purple-900/20 border border-purple-700/50 rounded-xl">
                  <h4 className="text-sm font-semibold text-purple-300 mb-3 flex items-center">
                    <span className="mr-2">🆕</span>
                    Recent External Submissions
                  </h4>
                  <div className="space-y-2">
                    {externalNotInTop5.slice(0, 3).map((entry) => (
                      <div
                        key={entry.submission_id}
                        className="flex items-center justify-between px-3 py-2 bg-gray-900/50 rounded-lg text-sm"
                      >
                        <div className="flex items-center space-x-2">
                          <span className="text-gray-400 font-mono text-xs">#{entry.rank}</span>
                          <span className="text-white font-medium">{entry.model_name}</span>
                        </div>
                        <span className="text-emerald-400 font-mono">{entry.score.toFixed(4)}</span>
                      </div>
                    ))}
                  </div>
                </div>
              );
            }
            return null;
          })()}

          {leaderboard.entries.length > 5 && !showAll && (
            <div className="mt-3 flex flex-col md:flex-row md:items-center md:justify-between text-xs text-gray-400 space-y-2 md:space-y-0">
              <span>
                Showing top {Math.min(5, leaderboard.entries.length)} of {leaderboard.entries.length} submissions
                {leaderboard.entries.filter(e => !e.is_internal).length > 0 && (
                  <span className="ml-2 text-purple-400">
                    ({leaderboard.entries.filter(e => !e.is_internal).length} external)
                  </span>
                )}
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
          
          {showAll && leaderboard.entries.length > 0 && (
            <div className="mt-3 text-xs text-gray-400">
              Showing all {leaderboard.entries.length} submissions
              {leaderboard.entries.filter(e => !e.is_internal).length > 0 && (
                <span className="ml-2 text-purple-400">
                  ({leaderboard.entries.filter(e => !e.is_internal).length} external)
                </span>
              )}
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

