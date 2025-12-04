import React, { useState, useEffect, useRef } from 'react';
import { getDatasets, submitPredictions, getSubmission, getDatasetQuestions } from '../services/api';
import DetailedMetrics from './DetailedMetrics';

const SubmissionForm = ({ onSuccess }) => {
  const [datasets, setDatasets] = useState([]);
  const [selectedDataset, setSelectedDataset] = useState(null);
  const [formData, setFormData] = useState({
    dataset_id: '',
    model_name: '',
    // Default model_version to today's date for convenience; user can override
    model_version: new Date().toISOString().slice(0, 10),
    organization: '',
    is_internal: false,
  });
  
  const [predictions, setPredictions] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [submissionId, setSubmissionId] = useState(null);
  const [submissionStatus, setSubmissionStatus] = useState(null);
  const [questions, setQuestions] = useState(null);
  const [loadingQuestions, setLoadingQuestions] = useState(false);
  const [showQuestions, setShowQuestions] = useState(false);
  const [jsonUploadName, setJsonUploadName] = useState('');
  const [jsonText, setJsonText] = useState('');
  const [hasUnsavedChanges, setHasUnsavedChanges] = useState(false);
  const statusRef = useRef(null);

  useEffect(() => {
    loadDatasets();
  }, []);

  const loadDatasets = async () => {
    try {
      const data = await getDatasets();
      setDatasets(data);
    } catch (err) {
      setError('Failed to load datasets');
    }
  };

  const handleDatasetChange = async (datasetId) => {
    setHasUnsavedChanges(true);
    setFormData(prev => ({ ...prev, dataset_id: datasetId }));
    
    const dataset = datasets.find(d => d.id === datasetId);
    setSelectedDataset(dataset);
    setQuestions(null);
    setShowQuestions(false);
    
    // Initialize predictions based on dataset questions
    if (dataset?.questions) {
      setPredictions(dataset.questions.map(q => ({ id: q.id, prediction: '' })));
      setQuestions({ questions: dataset.questions });
    } else {
      // If test set is private, user must fetch questions
      setPredictions([{ id: '', prediction: '' }]);
    }
  };

  const fetchQuestions = async () => {
    if (!formData.dataset_id) return;
    
    setLoadingQuestions(true);
    setError(null);
    try {
      const data = await getDatasetQuestions(formData.dataset_id);
      setQuestions(data);
      setShowQuestions(true);
      
      // Auto-populate prediction rows with question IDs
      setPredictions(data.questions.map(q => ({ id: q.id, prediction: '' })));
    } catch (err) {
      setError(err.response?.data?.message || err.message || 'Failed to load questions');
    } finally {
      setLoadingQuestions(false);
    }
  };

  const downloadQuestions = () => {
    if (!questions) return;
    
    const dataStr = JSON.stringify(questions, null, 2);
    const dataBlob = new Blob([dataStr], { type: 'application/json' });
    const url = URL.createObjectURL(dataBlob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `${selectedDataset?.name || 'questions'}_questions.json`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
  };

  const handlePredictionChange = (index, field, value) => {
    const updated = [...predictions];
    updated[index][field] = value;
    setPredictions(updated);
    setHasUnsavedChanges(true);
  };

  const addPredictionRow = () => {
    setPredictions([...predictions, { id: '', prediction: '' }]);
    setHasUnsavedChanges(true);
  };
  
  const removePredictionRow = (index) => {
    setPredictions(predictions.filter((_, i) => i !== index));
    setHasUnsavedChanges(true);
  };

  const loadPredictionsFromJson = (text, sourceLabel = 'JSON') => {
    const parsed = JSON.parse(text);

    // Accept either a raw list of predictions or an object with a predictions field.
    const maybePredictions = Array.isArray(parsed)
      ? parsed
      : Array.isArray(parsed.predictions)
      ? parsed.predictions
      : null;

    if (!maybePredictions) {
      throw new Error(
        'Invalid JSON format. Expected an array of {id, prediction} objects or { "predictions": [...] }.'
      );
    }

    const normalized = maybePredictions.map((p) => ({
      id: p.id ?? '',
      // Be lenient: allow either "prediction" or "answer" for convenience.
      prediction: p.prediction ?? p.answer ?? '',
    }));

    if (normalized.length === 0) {
      throw new Error(`${sourceLabel} contains no predictions.`);
    }

    setPredictions(normalized);
    setError(null);
    setHasUnsavedChanges(true);
  };

  const handleJsonUpload = (event) => {
    const file = event.target.files?.[0];
    if (!file) return;

    const reader = new FileReader();
    reader.onload = (e) => {
      try {
        const text = e.target?.result;
        if (typeof text !== 'string') {
          throw new Error('Unable to read file contents');
        }

        loadPredictionsFromJson(text, `File "${file.name}"`);
        setJsonUploadName(file.name);
      } catch (err) {
        console.error('Error parsing predictions JSON file:', err);
        setError(
          err instanceof Error
            ? err.message
            : 'Failed to parse predictions JSON file.'
        );
      }
    };

    reader.readAsText(file);
  };

  const handleJsonPasteLoad = () => {
    try {
      if (!jsonText.trim()) {
        throw new Error('Please paste JSON into the text area first.');
      }
      loadPredictionsFromJson(jsonText, 'Pasted JSON');
      setHasUnsavedChanges(true);
    } catch (err) {
      console.error('Error parsing pasted predictions JSON:', err);
      setError(
        err instanceof Error
          ? err.message
          : 'Failed to parse pasted predictions JSON.'
      );
    }
  };

  const pollSubmissionStatus = async (subId) => {
    const maxAttempts = 30;
    let attempts = 0;

    const poll = async () => {
      try {
        const status = await getSubmission(subId);
        setSubmissionStatus(status);

        if (status.status === 'completed' || status.status === 'failed') {
          return; // Stop polling
        }

        attempts++;
        if (attempts < maxAttempts) {
          setTimeout(poll, 2000); // Poll every 2 seconds
        }
      } catch (err) {
        console.error('Error polling status:', err);
      }
    };

    poll();
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setSubmissionId(null);
    setSubmissionStatus(null);

    try {
      const data = {
        ...formData,
        predictions: predictions.filter(p => p.id && p.prediction),
      };

      if (data.predictions.length === 0) {
        throw new Error('Please provide at least one prediction');
      }

      const response = await submitPredictions(data);
      const subId = response.data.submission_id;
      setSubmissionId(subId);
      setHasUnsavedChanges(false);
      
      // Start polling for status
      pollSubmissionStatus(subId);

      // Scroll to the status panel so the user clearly sees the result
      if (statusRef.current) {
        statusRef.current.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
      
      if (onSuccess) onSuccess(response.data);
    } catch (err) {
      setError(err.response?.data?.message || err.message || 'Failed to submit predictions');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto p-6 bg-gray-900 rounded-lg shadow-lg">
      <h2 className="text-2xl font-bold text-white mb-6">Submit Model Predictions</h2>
      
      {error && (
        <div className="mb-4 p-4 bg-red-900 border border-red-700 text-red-100 rounded">
          {error}
        </div>
      )}
      
      {submissionId && (
        <div
          ref={statusRef}
          className="mb-4 p-4 bg-blue-900 border border-blue-700 text-blue-100 rounded"
        >
          <p className="font-bold mb-2">Submission received!</p>
          <p className="text-sm">Submission ID: {submissionId}</p>
          
          {submissionStatus && (
            <div className="mt-3 p-3 bg-gray-800 rounded">
              <p className="mb-2">
                Status: <span className="font-bold uppercase">{submissionStatus.status}</span>
              </p>
              
              {submissionStatus.status === 'completed' && (
                <div className="space-y-2">
                  <p>Primary Score: <span className="font-bold text-green-400 text-xl">
                    {submissionStatus.primary_score?.toFixed(4)}
                  </span></p>
                  {submissionStatus.detailed_scores && (
                    <div>
                      <p className="text-sm text-gray-400 mb-2">Detailed Metrics:</p>
                      <DetailedMetrics 
                        scores={submissionStatus.detailed_scores}
                        primaryMetric={selectedDataset?.primary_metric}
                      />
                    </div>
                  )}
                </div>
              )}
              
              {submissionStatus.status === 'failed' && (
                <p className="text-red-400">Error: {submissionStatus.error_message}</p>
              )}
              
              {(submissionStatus.status === 'pending' || submissionStatus.status === 'processing') && (
                <p className="flex items-center">
                  <span className="animate-spin mr-2">⏳</span>
                  Evaluating...
                </p>
              )}
            </div>
          )}
        </div>
      )}

      <form onSubmit={handleSubmit} className="space-y-6">
        {/* Dataset Selection */}
        <div>
          <label className="block text-sm font-medium text-gray-300 mb-2">
            Select Dataset *
          </label>
          <select
            value={formData.dataset_id}
            onChange={(e) => handleDatasetChange(e.target.value)}
            required
            className="w-full px-4 py-2 bg-gray-800 border border-gray-700 rounded text-white focus:outline-none focus:border-blue-500"
          >
            <option value="">Choose a dataset...</option>
            {datasets.map(dataset => (
              <option key={dataset.id} value={dataset.id}>
                {dataset.name} ({dataset.task_type})
              </option>
            ))}
          </select>
          
          {selectedDataset && (
            <div className="mt-2 space-y-3">
              {/* Dataset Info */}
              <div className="p-3 bg-gray-800 rounded text-sm text-gray-300">
                <p><strong>Task:</strong> {selectedDataset.task_type}</p>
                <p><strong>Metric:</strong> {selectedDataset.primary_metric}</p>
                <p><strong>Examples:</strong> {selectedDataset.num_examples}</p>
              </div>

              {/* Format Example */}
              {questions?.questions?.[0] && (
                <div className="p-4 bg-gray-800 rounded border border-gray-700">
                  <h4 className="text-white font-semibold mb-2 flex items-center">
                    <span className="mr-2">📝</span>
                    Prediction Format Example
                  </h4>
                  
                  {/* Show available classes for classification */}
                  {(selectedDataset.task_type === 'text_classification') && questions.questions && (
                    <div className="mb-3">
                      <p className="text-xs text-gray-400 mb-1">Available Classes:</p>
                      <div className="flex flex-wrap gap-1">
                        {Array.from(new Set(
                          questions.questions
                            .map(q => q.answer)
                            .filter(Boolean)
                        )).map((cls, idx) => (
                          <span
                            key={idx}
                            className="px-2 py-0.5 bg-blue-900/50 text-blue-300 rounded text-xs border border-blue-700"
                          >
                            {cls}
                          </span>
                        ))}
                      </div>
                    </div>
                  )}

                  <div className="text-xs">
                    <p className="text-gray-400 mb-2">Input (from ground truth):</p>
                    <pre className="bg-gray-900 p-2 rounded overflow-x-auto mb-3 text-gray-300">
{JSON.stringify(
  Object.fromEntries(
    Object.entries(questions.questions[0]).filter(([k]) => k !== 'answer')
  ),
  null,
  2
)}
                    </pre>
                    
                    <p className="text-gray-400 mb-2">Your prediction should be:</p>
                    <pre className="bg-gray-900 p-2 rounded overflow-x-auto text-emerald-400">
{JSON.stringify(
  {
    id: questions.questions[0].id,
    prediction: selectedDataset.task_type === 'named_entity_recognition'
      ? [["Example Entity", "TYPE"]]
      : selectedDataset.task_type === 'retrieval'
      ? ["doc_id_1", "doc_id_2"]
      : "your_answer_here"
  },
  null,
  2
)}
                    </pre>
                  </div>
                </div>
              )}

              {!selectedDataset.test_set_public && (
                <div className="mt-3 space-y-2">
                  <p className="text-yellow-400 flex items-center">
                    <svg className="w-4 h-4 mr-1" fill="currentColor" viewBox="0 0 20 20">
                      <path fillRule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
                    </svg>
                    Test questions are private
                  </p>
                  <button
                    type="button"
                    onClick={fetchQuestions}
                    disabled={loadingQuestions}
                    className="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded text-sm disabled:opacity-50 flex items-center"
                  >
                    {loadingQuestions ? (
                      <>
                        <svg className="animate-spin -ml-1 mr-2 h-4 w-4 text-white" fill="none" viewBox="0 0 24 24">
                          <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                          <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                        </svg>
                        Loading...
                      </>
                    ) : (
                      <>
                        <svg className="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                        </svg>
                        Get Questions & IDs
                      </>
                    )}
                  </button>
                </div>
              )}
            </div>
          )}
          
          {/* Questions Display */}
          {questions && showQuestions && (
            <div className="mt-4 p-4 bg-gray-800 rounded-lg border border-gray-700">
              <div className="flex justify-between items-center mb-3">
                <h4 className="text-white font-semibold">
                  Test Questions ({questions.num_questions || questions.questions?.length || 0} total)
                </h4>
                <div className="flex space-x-2">
                  <button
                    type="button"
                    onClick={downloadQuestions}
                    className="px-3 py-1 bg-green-600 hover:bg-green-700 text-white rounded text-sm flex items-center"
                  >
                    <svg className="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
                    </svg>
                    Download JSON
                  </button>
                  <button
                    type="button"
                    onClick={() => setShowQuestions(false)}
                    className="px-3 py-1 bg-gray-600 hover:bg-gray-700 text-white rounded text-sm"
                  >
                    Hide
                  </button>
                </div>
              </div>
              
              <div className="max-h-96 overflow-y-auto space-y-3">
                {questions.questions?.map((q, idx) => (
                  <div key={q.id || idx} className="p-3 bg-gray-900 rounded border border-gray-700">
                    <div className="flex items-start justify-between mb-2">
                      <span className="text-xs font-mono text-blue-400 bg-blue-900 px-2 py-1 rounded">
                        ID: {q.id}
                      </span>
                    </div>
                    <div className="space-y-1 text-sm text-gray-300">
                      {q.question && (
                        <p><strong>Question:</strong> {q.question}</p>
                      )}
                      {q.context && (
                        <p><strong>Context:</strong> {q.context}</p>
                      )}
                      {q.text && (
                        <p><strong>Text:</strong> {q.text}</p>
                      )}
                      {q.sentence && (
                        <p><strong>Sentence:</strong> {q.sentence}</p>
                      )}
                      {q.premise && (
                        <p><strong>Premise:</strong> {q.premise}</p>
                      )}
                      {q.hypothesis && (
                        <p><strong>Hypothesis:</strong> {q.hypothesis}</p>
                      )}
                      {q.query && (
                        <p><strong>Query:</strong> {q.query}</p>
                      )}
                      {q.language && (
                        <p><strong>Language:</strong> {q.language}</p>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>

        {/* Model Info */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-300 mb-2">
              Model Name *
            </label>
            <input
              type="text"
              value={formData.model_name}
              onChange={(e) => {
                setFormData(prev => ({ ...prev, model_name: e.target.value }));
                setHasUnsavedChanges(true);
              }}
              required
              className="w-full px-4 py-2 bg-gray-800 border border-gray-700 rounded text-white focus:outline-none focus:border-blue-500"
              placeholder="e.g., GPT-4o"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-300 mb-2">
              Model Version
            </label>
            <input
              type="text"
              value={formData.model_version}
              onChange={(e) => {
                setFormData(prev => ({ ...prev, model_version: e.target.value }));
                setHasUnsavedChanges(true);
              }}
              className="w-full px-4 py-2 bg-gray-800 border border-gray-700 rounded text-white focus:outline-none focus:border-blue-500"
              placeholder="e.g., 2024-11-01"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-300 mb-2">
              Organization
            </label>
            <input
              type="text"
              value={formData.organization}
              onChange={(e) => {
                setFormData(prev => ({ ...prev, organization: e.target.value }));
                setHasUnsavedChanges(true);
              }}
              className="w-full px-4 py-2 bg-gray-800 border border-gray-700 rounded text-white focus:outline-none focus:border-blue-500"
              placeholder="e.g., OpenAI"
            />
          </div>

          <div className="flex items-center">
            <label className="flex items-center space-x-3">
              <input
                type="checkbox"
                checked={formData.is_internal}
                onChange={(e) => {
                  setFormData(prev => ({ ...prev, is_internal: e.target.checked }));
                  setHasUnsavedChanges(true);
                }}
                className="w-5 h-5 text-blue-600 bg-gray-800 border-gray-700 rounded focus:ring-blue-500"
              />
              <span className="text-gray-300">Internal Submission</span>
            </label>
          </div>
        </div>

        {/* Predictions */}
        {formData.dataset_id && (
          <div className="space-y-4">
            <div className="flex justify-between items-center">
              <div className="flex flex-col md:flex-row md:items-center md:space-x-3 space-y-3 md:space-y-0">
                <h3 className="text-lg font-medium text-white">Predictions *</h3>

                {!selectedDataset?.test_set_public && (
                  <button
                    type="button"
                    onClick={addPredictionRow}
                    className="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded text-sm"
                  >
                    + Add Row
                  </button>
                )}

                <div className="flex flex-col space-y-2 md:space-y-1">
                  <div className="flex items-center space-x-2">
                    <label className="text-xs text-gray-300">
                      Or upload JSON:
                    </label>
                    <input
                      type="file"
                      accept="application/json"
                      onChange={handleJsonUpload}
                      className="text-xs text-gray-300"
                    />
                    {jsonUploadName && (
                      <span className="text-xs text-gray-500">
                        Loaded: {jsonUploadName}
                      </span>
                    )}
                  </div>
                  <div className="flex flex-col space-y-1">
                    <label className="text-xs text-gray-400">
                      Or paste JSON here (e.g. {"[{\"id\": \"1\", \"prediction\": \"...\"}]"} or with <code>answer</code>):
                    </label>
                    <div className="flex items-start space-x-2">
                      <textarea
                        value={jsonText}
                        onChange={(e) => setJsonText(e.target.value)}
                        rows={3}
                        className="flex-1 px-2 py-1 bg-gray-800 border border-gray-700 rounded text-white text-xs font-mono focus:outline-none focus:border-blue-500"
                        placeholder='{"predictions": [{"id": "1", "answer": "business"}, ...]}'
                      />
                      <button
                        type="button"
                        onClick={handleJsonPasteLoad}
                        className="px-3 py-1 bg-blue-600 hover:bg-blue-700 text-white rounded text-xs h-8 mt-1"
                      >
                        Load
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <div className="space-y-3">
              {predictions.map((pred, index) => (
                <div key={index} className="grid grid-cols-12 gap-2 items-center">
                  <input
                    type="text"
                    value={pred.id}
                    onChange={(e) => handlePredictionChange(index, 'id', e.target.value)}
                    placeholder="Question ID"
                    disabled={selectedDataset?.test_set_public}
                    className="col-span-3 px-3 py-2 bg-gray-800 border border-gray-700 rounded text-white text-sm focus:outline-none focus:border-blue-500 disabled:opacity-50"
                  />
                  <input
                    type="text"
                    value={pred.prediction}
                    onChange={(e) => handlePredictionChange(index, 'prediction', e.target.value)}
                    placeholder="Your model's prediction"
                    className="col-span-8 px-3 py-2 bg-gray-800 border border-gray-700 rounded text-white text-sm focus:outline-none focus:border-blue-500"
                  />
                  {!selectedDataset?.test_set_public && (
                    <button
                      type="button"
                      onClick={() => removePredictionRow(index)}
                      className="col-span-1 px-3 py-2 bg-red-600 hover:bg-red-700 text-white rounded text-sm"
                      disabled={predictions.length === 1}
                    >
                      ×
                    </button>
                  )}
                </div>
              ))}
            </div>

            <p className="text-sm text-gray-400 flex items-start">
              <svg className="w-4 h-4 mr-1 mt-0.5 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                <path d="M11 3a1 1 0 100 2h2.586l-6.293 6.293a1 1 0 101.414 1.414L15 6.414V9a1 1 0 102 0V4a1 1 0 00-1-1h-5z" />
                <path d="M5 5a2 2 0 00-2 2v8a2 2 0 002 2h8a2 2 0 002-2v-3a1 1 0 10-2 0v3H5V7h3a1 1 0 000-2H5z" />
              </svg>
              <span>Your predictions will be evaluated against the ground truth. Scores will be computed automatically. Use the "Get Questions & IDs" button above to load all test questions.</span>
            </p>
          </div>
        )}

        {/* Submit */}
        <div className="flex justify-end space-x-4">
          <button
            type="button"
            onClick={() => {
              setFormData({
                dataset_id: '',
                model_name: '',
                model_version: new Date().toISOString().slice(0, 10),
                organization: '',
                is_internal: false,
              });
              setPredictions([]);
              setSelectedDataset(null);
              setSubmissionId(null);
              setSubmissionStatus(null);
              setHasUnsavedChanges(false);
            }}
            className="px-6 py-2 bg-gray-700 hover:bg-gray-600 text-white rounded"
          >
            Reset
          </button>
          <button
            type="submit"
            disabled={loading || !formData.dataset_id || !hasUnsavedChanges}
            className="px-6 py-2 btn-black rounded disabled:opacity-50"
          >
            {loading
              ? 'Submitting...'
              : hasUnsavedChanges
              ? 'Submit Predictions'
              : 'Submitted'}
          </button>
        </div>
      </form>
    </div>
  );
};

export default SubmissionForm;

