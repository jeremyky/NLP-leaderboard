import React, { useState } from 'react';

const LanguageBreakdown = ({ scores }) => {
  const [expanded, setExpanded] = useState(false);

  if (!scores) return null;

  // Find per-language metrics
  const perLanguageMetrics = {};
  Object.entries(scores).forEach(([key, value]) => {
    if (typeof value === 'object' && value !== null && !Array.isArray(value)) {
      // This is a per-language metric
      perLanguageMetrics[key] = value;
    }
  });

  if (Object.keys(perLanguageMetrics).length === 0) {
    return null;
  }

  // Get all languages
  const allLanguages = new Set();
  Object.values(perLanguageMetrics).forEach(langScores => {
    Object.keys(langScores).forEach(lang => allLanguages.add(lang));
  });

  const languages = Array.from(allLanguages).sort();

  // Language names mapping
  const languageNames = {
    'en': '🇬🇧 English',
    'es': '🇪🇸 Spanish',
    'fr': '🇫🇷 French',
    'de': '🇩🇪 German',
    'zh': '🇨🇳 Chinese',
    'ja': '🇯🇵 Japanese',
    'ru': '🇷🇺 Russian',
    'ar': '🇸🇦 Arabic',
    'hi': '🇮🇳 Hindi',
    'vi': '🇻🇳 Vietnamese',
    'th': '🇹🇭 Thai',
    'tr': '🇹🇷 Turkish',
    'it': '🇮🇹 Italian',
    'sw': '🇰🇪 Swahili',
    'qu': '🇵🇪 Quechua',
    'ht': '🇭🇹 Haitian Creole',
    'et': '🇪🇪 Estonian',
    'id': '🇮🇩 Indonesian',
    'ta': '🇮🇳 Tamil',
    'el': '🇬🇷 Greek',
    'bn': '🇧🇩 Bengali',
    'te': '🇮🇳 Telugu',
  };

  const getScoreColor = (value) => {
    if (value >= 0.85) return 'bg-green-600';
    if (value >= 0.70) return 'bg-blue-600';
    if (value >= 0.55) return 'bg-yellow-600';
    return 'bg-red-600';
  };

  const getTextColor = (value) => {
    if (value >= 0.85) return 'text-green-400';
    if (value >= 0.70) return 'text-blue-400';
    if (value >= 0.55) return 'text-yellow-400';
    return 'text-red-400';
  };

  // Calculate average across languages for each metric
  const metricAverages = {};
  Object.entries(perLanguageMetrics).forEach(([metric, langScores]) => {
    const values = Object.values(langScores);
    metricAverages[metric] = values.reduce((a, b) => a + b, 0) / values.length;
  });

  const displayLanguages = expanded ? languages : languages.slice(0, 5);

  return (
    <div className="mt-4 bg-gray-800 rounded-lg p-4 border border-gray-700">
      <div className="flex justify-between items-center mb-3">
        <h4 className="text-sm font-bold text-white flex items-center">
          <svg className="w-4 h-4 mr-2 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3.055 11H5a2 2 0 012 2v1a2 2 0 002 2 2 2 0 012 2v2.945M8 3.935V5.5A2.5 2.5 0 0010.5 8h.5a2 2 0 012 2 2 2 0 104 0 2 2 0 012-2h1.064M15 20.488V18a2 2 0 012-2h3.064M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          Performance by Language
        </h4>
        {languages.length > 5 && (
          <button
            onClick={() => setExpanded(!expanded)}
            className="text-xs text-blue-400 hover:text-blue-300 underline"
          >
            {expanded ? '↑ Show less' : `↓ Show all ${languages.length} languages`}
          </button>
        )}
      </div>

      <div className="space-y-3">
        {displayLanguages.map(lang => {
          const langName = languageNames[lang] || `🌐 ${lang.toUpperCase()}`;
          
          return (
            <div key={lang} className="space-y-1">
              <div className="flex justify-between items-center text-sm">
                <span className="text-gray-300 font-medium">{langName}</span>
              </div>
              
              <div className="flex items-center space-x-2">
                {Object.entries(perLanguageMetrics).map(([metric, langScores]) => {
                  const score = langScores[lang];
                  if (score === undefined) return null;
                  
                  const percentage = score * 100;
                  
                  return (
                    <div key={metric} className="flex-1">
                      <div className="flex justify-between text-xs mb-1">
                        <span className="text-gray-400">{metric.replace('per_language_', '')}</span>
                        <span className={`font-mono ${getTextColor(score)}`}>
                          {score.toFixed(3)}
                        </span>
                      </div>
                      <div className="w-full bg-gray-700 rounded-full h-2">
                        <div
                          className={`h-2 rounded-full ${getScoreColor(score)} transition-all`}
                          style={{ width: `${percentage}%` }}
                        />
                      </div>
                    </div>
                  );
                })}
              </div>
            </div>
          );
        })}
      </div>

      {/* Summary Stats */}
      <div className="mt-4 pt-3 border-t border-gray-700">
        <div className="text-xs text-gray-400 space-y-1">
          <div className="flex justify-between">
            <span>Languages evaluated:</span>
            <span className="font-semibold text-white">{languages.length}</span>
          </div>
          {Object.entries(metricAverages).map(([metric, avg]) => (
            <div key={metric} className="flex justify-between">
              <span>Avg {metric.replace('per_language_', '')}:</span>
              <span className={`font-mono font-semibold ${getTextColor(avg)}`}>
                {avg.toFixed(3)}
              </span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default LanguageBreakdown;

