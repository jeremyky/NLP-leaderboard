import React, { useState } from 'react';
import { createDataset } from '../services/api';

const DatasetForm = ({ onSuccess }) => {
  const [formData, setFormData] = useState({
    name: '',
    description: '',
    url: '',
    task_type: 'text_classification',
    test_set_public: false,
    labels_public: false,
    primary_metric: 'accuracy',
    additional_metrics: '',
  });
  
  const [groundTruth, setGroundTruth] = useState([
    { id: '', question: '', answer: '' }
  ]);
  
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(null);

  const taskTypes = [
    { value: 'text_classification', label: 'Text Classification' },
    { value: 'named_entity_recognition', label: 'Named Entity Recognition' },
    { value: 'document_qa', label: 'Document Q&A' },
    { value: 'line_qa', label: 'Line Q&A' },
    { value: 'retrieval', label: 'Retrieval' },
  ];

  const metricsByTaskType = {
    text_classification: ['accuracy', 'f1', 'precision', 'recall'],
    named_entity_recognition: ['f1', 'precision', 'recall'],
    document_qa: ['exact_match', 'f1'],
    line_qa: ['exact_match', 'f1'],
    retrieval: ['retrieval_accuracy'],
  };

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value
    }));
  };

  const handleGroundTruthChange = (index, field, value) => {
    const updated = [...groundTruth];
    updated[index][field] = value;
    setGroundTruth(updated);
  };

  const addGroundTruthRow = () => {
    setGroundTruth([...groundTruth, { id: '', question: '', answer: '' }]);
  };

  const removeGroundTruthRow = (index) => {
    setGroundTruth(groundTruth.filter((_, i) => i !== index));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setSuccess(null);

    try {
      // Prepare data
      const additionalMetrics = formData.additional_metrics
        .split(',')
        .map(m => m.trim())
        .filter(m => m);

      const data = {
        ...formData,
        additional_metrics: additionalMetrics,
        ground_truth: groundTruth.filter(gt => gt.id && gt.question && gt.answer),
      };

      const response = await createDataset(data);
      setSuccess(`Dataset created successfully! ID: ${response.data.dataset_id}`);
      
      // Reset form
      setFormData({
        name: '',
        description: '',
        url: '',
        task_type: 'text_classification',
        test_set_public: false,
        labels_public: false,
        primary_metric: 'accuracy',
        additional_metrics: '',
      });
      setGroundTruth([{ id: '', question: '', answer: '' }]);
      
      if (onSuccess) onSuccess(response.data);
    } catch (err) {
      setError(err.response?.data?.message || err.message || 'Failed to create dataset');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto p-6 bg-gray-900 rounded-lg shadow-lg">
      <h2 className="text-2xl font-bold text-white mb-6">Create New Dataset</h2>
      
      {error && (
        <div className="mb-4 p-4 bg-red-900 border border-red-700 text-red-100 rounded">
          {error}
        </div>
      )}
      
      {success && (
        <div className="mb-4 p-4 bg-green-900 border border-green-700 text-green-100 rounded">
          {success}
        </div>
      )}

      <form onSubmit={handleSubmit} className="space-y-6">
        {/* Basic Info */}
        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-300 mb-2">
              Dataset Name *
            </label>
            <input
              type="text"
              name="name"
              value={formData.name}
              onChange={handleChange}
              required
              className="w-full px-4 py-2 bg-gray-800 border border-gray-700 rounded text-white focus:outline-none focus:border-blue-500"
              placeholder="e.g., Financial Sentiment Analysis"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-300 mb-2">
              Description
            </label>
            <textarea
              name="description"
              value={formData.description}
              onChange={handleChange}
              rows="3"
              className="w-full px-4 py-2 bg-gray-800 border border-gray-700 rounded text-white focus:outline-none focus:border-blue-500"
              placeholder="Describe your dataset..."
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-300 mb-2">
              Dataset URL
            </label>
            <input
              type="url"
              name="url"
              value={formData.url}
              onChange={handleChange}
              className="w-full px-4 py-2 bg-gray-800 border border-gray-700 rounded text-white focus:outline-none focus:border-blue-500"
              placeholder="https://..."
            />
          </div>
        </div>

        {/* Task Configuration */}
        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-300 mb-2">
              Task Type *
            </label>
            <select
              name="task_type"
              value={formData.task_type}
              onChange={handleChange}
              className="w-full px-4 py-2 bg-gray-800 border border-gray-700 rounded text-white focus:outline-none focus:border-blue-500"
            >
              {taskTypes.map(type => (
                <option key={type.value} value={type.value}>
                  {type.label}
                </option>
              ))}
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-300 mb-2">
              Primary Metric *
            </label>
            <select
              name="primary_metric"
              value={formData.primary_metric}
              onChange={handleChange}
              className="w-full px-4 py-2 bg-gray-800 border border-gray-700 rounded text-white focus:outline-none focus:border-blue-500"
            >
              {metricsByTaskType[formData.task_type].map(metric => (
                <option key={metric} value={metric}>
                  {metric}
                </option>
              ))}
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-300 mb-2">
              Additional Metrics (comma-separated)
            </label>
            <input
              type="text"
              name="additional_metrics"
              value={formData.additional_metrics}
              onChange={handleChange}
              className="w-full px-4 py-2 bg-gray-800 border border-gray-700 rounded text-white focus:outline-none focus:border-blue-500"
              placeholder="e.g., precision, recall, f1"
            />
          </div>
        </div>

        {/* Visibility Settings */}
        <div className="space-y-2 border border-gray-700 p-4 rounded">
          <h3 className="text-lg font-medium text-white mb-3">Anti-Gaming Settings</h3>
          
          <label className="flex items-center space-x-3">
            <input
              type="checkbox"
              name="test_set_public"
              checked={formData.test_set_public}
              onChange={handleChange}
              className="w-5 h-5 text-blue-600 bg-gray-800 border-gray-700 rounded focus:ring-blue-500"
            />
            <span className="text-gray-300">
              Make test questions public (allows users to see questions)
            </span>
          </label>
          
          <p className="text-sm text-gray-400 ml-8">
            ⚠️ Keep this OFF to prevent metric gaming and overfitting
          </p>
        </div>

        {/* Ground Truth */}
        <div className="space-y-4">
          <div className="flex justify-between items-center">
            <h3 className="text-lg font-medium text-white">Ground Truth Data *</h3>
            <button
              type="button"
              onClick={addGroundTruthRow}
              className="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded text-sm"
            >
              + Add Row
            </button>
          </div>

          <div className="space-y-3">
            {groundTruth.map((row, index) => (
              <div key={index} className="grid grid-cols-12 gap-2 items-start">
                <input
                  type="text"
                  value={row.id}
                  onChange={(e) => handleGroundTruthChange(index, 'id', e.target.value)}
                  placeholder="ID"
                  className="col-span-2 px-3 py-2 bg-gray-800 border border-gray-700 rounded text-white text-sm focus:outline-none focus:border-blue-500"
                />
                <input
                  type="text"
                  value={row.question}
                  onChange={(e) => handleGroundTruthChange(index, 'question', e.target.value)}
                  placeholder="Question / Text"
                  className="col-span-5 px-3 py-2 bg-gray-800 border border-gray-700 rounded text-white text-sm focus:outline-none focus:border-blue-500"
                />
                <input
                  type="text"
                  value={row.answer}
                  onChange={(e) => handleGroundTruthChange(index, 'answer', e.target.value)}
                  placeholder="Answer / Label"
                  className="col-span-4 px-3 py-2 bg-gray-800 border border-gray-700 rounded text-white text-sm focus:outline-none focus:border-blue-500"
                />
                <button
                  type="button"
                  onClick={() => removeGroundTruthRow(index)}
                  className="col-span-1 px-3 py-2 bg-red-600 hover:bg-red-700 text-white rounded text-sm"
                  disabled={groundTruth.length === 1}
                >
                  ×
                </button>
              </div>
            ))}
          </div>
        </div>

        {/* Submit */}
        <div className="flex justify-end space-x-4">
          <button
            type="button"
            onClick={() => {
              setFormData({
                name: '',
                description: '',
                url: '',
                task_type: 'text_classification',
                test_set_public: false,
                labels_public: false,
                primary_metric: 'accuracy',
                additional_metrics: '',
              });
              setGroundTruth([{ id: '', question: '', answer: '' }]);
            }}
            className="px-6 py-2 bg-gray-700 hover:bg-gray-600 text-white rounded"
          >
            Reset
          </button>
          <button
            type="submit"
            disabled={loading}
            className="px-6 py-2 btn-black rounded disabled:opacity-50"
          >
            {loading ? 'Creating...' : 'Create Dataset'}
          </button>
        </div>
      </form>
    </div>
  );
};

export default DatasetForm;

