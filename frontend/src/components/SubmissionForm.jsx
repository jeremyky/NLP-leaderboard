import React, { useState, useEffect } from 'react';
import { getDatasets, submitPredictions, getSubmission } from '../services/api';
import DetailedMetrics from './DetailedMetrics';

const SubmissionForm = ({ onSuccess }) => {
  const [datasets, setDatasets] = useState([]);
  const [selectedDataset, setSelectedDataset] = useState(null);
  const [formData, setFormData] = useState({
    dataset_id: '',
    model_name: '',
    model_version: '',
    organization: '',
    is_internal: false,
  });
  
  const [predictions, setPredictions] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [submissionId, setSubmissionId] = useState(null);
  const [submissionStatus, setSubmissionStatus] = useState(null);

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
    setFormData(prev => ({ ...prev, dataset_id: datasetId }));
    
    const dataset = datasets.find(d => d.id === datasetId);
    setSelectedDataset(dataset);
    
    // Initialize predictions based on dataset questions
    if (dataset?.questions) {
      setPredictions(dataset.questions.map(q => ({ id: q.id, prediction: '' })));
    } else {
      // If test set is private, user must know the question IDs
      setPredictions([{ id: '', prediction: '' }]);
    }
  };

  const handlePredictionChange = (index, field, value) => {
    const updated = [...predictions];
    updated[index][field] = value;
    setPredictions(updated);
  };

  const addPredictionRow = () => {
    setPredictions([...predictions, { id: '', prediction: '' }]);
  };

  const removePredictionRow = (index) => {
    setPredictions(predictions.filter((_, i) => i !== index));
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
      
      // Start polling for status
      pollSubmissionStatus(subId);
      
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
        <div className="mb-4 p-4 bg-blue-900 border border-blue-700 text-blue-100 rounded">
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
            <div className="mt-2 p-3 bg-gray-800 rounded text-sm text-gray-300">
              <p><strong>Task:</strong> {selectedDataset.task_type}</p>
              <p><strong>Metric:</strong> {selectedDataset.primary_metric}</p>
              <p><strong>Examples:</strong> {selectedDataset.num_examples}</p>
              {!selectedDataset.test_set_public && (
                <p className="text-yellow-400 mt-2">⚠️ Test questions are private</p>
              )}
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
              onChange={(e) => setFormData(prev => ({ ...prev, model_name: e.target.value }))}
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
              onChange={(e) => setFormData(prev => ({ ...prev, model_version: e.target.value }))}
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
              onChange={(e) => setFormData(prev => ({ ...prev, organization: e.target.value }))}
              className="w-full px-4 py-2 bg-gray-800 border border-gray-700 rounded text-white focus:outline-none focus:border-blue-500"
              placeholder="e.g., OpenAI"
            />
          </div>

          <div className="flex items-center">
            <label className="flex items-center space-x-3">
              <input
                type="checkbox"
                checked={formData.is_internal}
                onChange={(e) => setFormData(prev => ({ ...prev, is_internal: e.target.checked }))}
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

            <p className="text-sm text-gray-400">
              💡 Tip: Your predictions will be evaluated against the ground truth. Scores will be computed automatically.
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
                model_version: '',
                organization: '',
                is_internal: false,
              });
              setPredictions([]);
              setSelectedDataset(null);
              setSubmissionId(null);
              setSubmissionStatus(null);
            }}
            className="px-6 py-2 bg-gray-700 hover:bg-gray-600 text-white rounded"
          >
            Reset
          </button>
          <button
            type="submit"
            disabled={loading || !formData.dataset_id}
            className="px-6 py-2 btn-black rounded disabled:opacity-50"
          >
            {loading ? 'Submitting...' : 'Submit Predictions'}
          </button>
        </div>
      </form>
    </div>
  );
};

export default SubmissionForm;

