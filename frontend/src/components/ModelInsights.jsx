import React from 'react';

const ModelInsights = ({ scores, primaryMetric, modelName }) => {
  if (!scores || Object.keys(scores).length === 0) {
    return null;
  }

  const insights = [];

  // Get key metrics
  const accuracy = scores.accuracy;
  const precision = scores.precision;
  const recall = scores.recall;
  const f1 = scores.f1;
  const exactMatch = scores.exact_match;

  // Classification insights
  if (accuracy !== undefined && precision !== undefined && recall !== undefined) {
    // High precision, low recall
    if (precision >= 0.85 && recall < 0.70) {
      insights.push({
        type: 'warning',
        title: 'Model is Too Conservative',
        message: `Your precision (${precision.toFixed(2)}) is good, but recall (${recall.toFixed(2)}) is low. Your model is missing ${((1-recall)*100).toFixed(0)}% of positive cases.`,
        suggestions: [
          'Lower your decision threshold to increase recall',
          'Add more training examples for minority classes',
          'Consider cost-sensitive learning if false negatives are expensive'
        ]
      });
    }
    
    // Low precision, high recall
    if (precision < 0.70 && recall >= 0.85) {
      insights.push({
        type: 'warning',
        title: 'Too Many False Positives',
        message: `Your recall (${recall.toFixed(2)}) is good, but precision (${precision.toFixed(2)}) is low. About ${((1-precision)*100).toFixed(0)}% of positive predictions are wrong.`,
        suggestions: [
          'Raise your decision threshold to improve precision',
          'Add more negative examples to training data',
          'Review false positive cases for patterns'
        ]
      });
    }

    // Balanced and good
    if (precision >= 0.85 && recall >= 0.85) {
      insights.push({
        type: 'success',
        title: 'Well-Balanced Model',
        message: `Excellent balance! Both precision (${precision.toFixed(2)}) and recall (${recall.toFixed(2)}) are strong.`,
        suggestions: [
          'Model is well-tuned for this task',
          'Consider testing on more diverse data',
          'Monitor for edge cases in production'
        ]
      });
    }

    // Both low
    if (precision < 0.70 && recall < 0.70) {
      insights.push({
        type: 'error',
        title: 'Model Needs Significant Improvement',
        message: `Both precision (${precision.toFixed(2)}) and recall (${recall.toFixed(2)}) are below 70%. The model is struggling with this task.`,
        suggestions: [
          'Collect more high-quality training data',
          'Try a larger model or fine-tune longer',
          'Review data quality and labeling consistency',
          'Consider domain-specific pre-training'
        ]
      });
    }
  }

  // Q&A insights
  if (exactMatch !== undefined && f1 !== undefined) {
    const gap = f1 - exactMatch;
    
    if (gap > 0.15) {
      insights.push({
        type: 'info',
        title: 'Close But Not Exact Answers',
        message: `Your F1 (${f1.toFixed(2)}) is much higher than Exact Match (${exactMatch.toFixed(2)}). Answers are close but not precisely matching.`,
        suggestions: [
          'Improve answer extraction boundaries',
          'Post-process answers to normalize formatting',
          'Train on exact answer spans, not just context',
          'Review common mistakes in answer formatting'
        ]
      });
    }

    if (exactMatch < 0.50) {
      insights.push({
        type: 'warning',
        title: 'Low Answer Accuracy',
        message: `Only ${(exactMatch*100).toFixed(0)}% of answers match exactly. Model needs better comprehension or answer extraction.`,
        suggestions: [
          'Use a larger language model',
          'Fine-tune on similar domain-specific Q&A data',
          'Improve context retrieval quality',
          'Add more examples of the answer format you want'
        ]
      });
    }
  }

  // NER insights
  if (scores.true_positives !== undefined && scores.false_positives !== undefined) {
    const tp = scores.true_positives;
    const fp = scores.false_positives;
    const fn = scores.false_negatives;
    
    if (fp > fn * 1.5) {
      insights.push({
        type: 'warning',
        title: 'Over-Predicting Entities',
        message: `Model is predicting too many entities. ${fp} false positives vs ${fn} false negatives.`,
        suggestions: [
          'Increase confidence threshold for entity detection',
          'Review common false positive patterns',
          'Add negative examples (non-entities) to training'
        ]
      });
    }

    if (fn > fp * 1.5) {
      insights.push({
        type: 'warning',
        title: 'Missing Many Entities',
        message: `Model is missing entities. ${fn} false negatives vs ${fp} false positives.`,
        suggestions: [
          'Lower confidence threshold',
          'Add more examples of rare entity types',
          'Review missed entities for patterns'
        ]
      });
    }
  }

  // Comparative insights
  const primaryScore = scores[primaryMetric];
  if (primaryScore !== undefined) {
    if (primaryScore >= 0.90) {
      insights.push({
        type: 'success',
        title: 'Excellent Performance',
        message: `Your ${primaryMetric} of ${primaryScore.toFixed(3)} is in the top tier (>0.90). Great work!`,
        suggestions: [
          'Model is performing very well',
          'Test on more challenging datasets',
          'Consider this as a strong baseline'
        ]
      });
    } else if (primaryScore < 0.60) {
      insights.push({
        type: 'error',
        title: 'Below Baseline Performance',
        message: `Your ${primaryMetric} of ${primaryScore.toFixed(3)} is below 0.60. Significant tuning needed.`,
        suggestions: [
          'Check if training data matches test domain',
          'Ensure sufficient training data quantity',
          'Verify data preprocessing pipeline',
          'Try transfer learning from domain-specific models'
        ]
      });
    }
  }

  if (insights.length === 0) {
    return null;
  }

  const getIconAndColor = (type) => {
    switch (type) {
      case 'success': 
        return { 
          icon: (
            <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
              <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
            </svg>
          ), 
          color: 'bg-green-900 border-green-700 text-green-100' 
        };
      case 'warning': 
        return { 
          icon: (
            <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
              <path fillRule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
            </svg>
          ), 
          color: 'bg-yellow-900 border-yellow-700 text-yellow-100' 
        };
      case 'error': 
        return { 
          icon: (
            <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
              <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
            </svg>
          ), 
          color: 'bg-red-900 border-red-700 text-red-100' 
        };
      default: 
        return { 
          icon: (
            <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
              <path d="M11 3a1 1 0 100 2h2.586l-6.293 6.293a1 1 0 101.414 1.414L15 6.414V9a1 1 0 102 0V4a1 1 0 00-1-1h-5z" />
              <path d="M5 5a2 2 0 00-2 2v8a2 2 0 002 2h8a2 2 0 002-2v-3a1 1 0 10-2 0v3H5V7h3a1 1 0 000-2H5z" />
            </svg>
          ), 
          color: 'bg-blue-900 border-blue-700 text-blue-100' 
        };
    }
  };

  return (
    <div className="mt-6 space-y-4">
      <h3 className="text-lg font-bold text-white flex items-center">
        <svg className="w-5 h-5 mr-2 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
        </svg>
        Model Tuning Insights
        {modelName && <span className="ml-2 text-sm text-gray-400">for {modelName}</span>}
      </h3>

      {insights.map((insight, index) => {
        const { icon, color } = getIconAndColor(insight.type);
        return (
          <div key={index} className={`border rounded-lg p-4 ${color}`}>
            <div className="flex items-start">
              <span className="mr-3 flex-shrink-0">{icon}</span>
              <div className="flex-1">
                <h4 className="font-bold mb-2">{insight.title}</h4>
                <p className="text-sm mb-3">{insight.message}</p>
                
                <div className="mt-3">
                  <p className="text-xs font-semibold mb-2 flex items-center">
                    <svg className="w-4 h-4 mr-1" fill="currentColor" viewBox="0 0 20 20">
                      <path d="M11 3a1 1 0 100 2h2.586l-6.293 6.293a1 1 0 101.414 1.414L15 6.414V9a1 1 0 102 0V4a1 1 0 00-1-1h-5z" />
                      <path d="M5 5a2 2 0 00-2 2v8a2 2 0 002 2h8a2 2 0 002-2v-3a1 1 0 10-2 0v3H5V7h3a1 1 0 000-2H5z" />
                    </svg>
                    SUGGESTIONS:
                  </p>
                  <ul className="text-sm space-y-1">
                    {insight.suggestions.map((suggestion, i) => (
                      <li key={i} className="flex items-start">
                        <span className="mr-2">•</span>
                        <span>{suggestion}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              </div>
            </div>
          </div>
        );
      })}
    </div>
  );
};

export default ModelInsights;

