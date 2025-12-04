import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { getSubmissions, getDatasets } from '../services/api';

const SubmissionHistory = () => {
  const navigate = useNavigate();
  const [submissions, setSubmissions] = useState([]);
  const [datasets, setDatasets] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const [filters, setFilters] = useState({
    dataset_id: '',
    model_name: '',
    status: '',
  });

  useEffect(() => {
    loadDatasets();
    loadSubmissions();
  }, []);

  const loadDatasets = async () => {
    try {
      const data = await getDatasets();
      setDatasets(data);
    } catch (err) {
      // Don't block history page if dataset lookup fails
      console.error('Failed to load datasets for filters', err);
    }
  };

  const getDatasetInfo = (datasetId) => {
    return datasets.find(ds => ds.id === datasetId);
  };

  const loadSubmissions = async (nextFilters = filters) => {
    setLoading(true);
    setError(null);
    try {
      const nonEmptyFilters = Object.fromEntries(
        Object.entries(nextFilters).filter(([, v]) => v)
      );
      const data = await getSubmissions(nonEmptyFilters);
      setSubmissions(data);
    } catch (err) {
      setError('Failed to load submissions. Make sure the API is running.');
    } finally {
      setLoading(false);
    }
  };

  const handleFilterChange = (field, value) => {
    const next = { ...filters, [field]: value };
    setFilters(next);
    loadSubmissions(next);
  };

  const statusOptions = [
    { value: '', label: 'All statuses' },
    { value: 'pending', label: 'Pending' },
    { value: 'processing', label: 'Processing' },
    { value: 'completed', label: 'Completed' },
    { value: 'failed', label: 'Failed' },
  ];

  return (
    <div className="min-h-screen bg-gray-900 pb-20 px-3">
      <div className="max-w-7xl mx-auto pt-8">
        {/* Header */}
        <div className="mb-6 flex justify-between items-center">
          <button
            onClick={() => navigate('/')}
            className="text-blue-400 hover:text-blue-300"
          >
            ← Back to Leaderboards
          </button>
          <h1 className="text-2xl md:text-3xl font-bold text-white">
            Submission History
          </h1>
        </div>

        {/* Filters */}
        <div className="mb-6 grid grid-cols-1 md:grid-cols-3 gap-3">
          <div>
            <label className="block text-xs font-medium text-gray-400 mb-1">
              Dataset
            </label>
            <select
              value={filters.dataset_id}
              onChange={(e) => handleFilterChange('dataset_id', e.target.value)}
              className="w-full px-3 py-2 bg-gray-800 border border-gray-700 rounded text-white text-sm focus:outline-none focus:border-blue-500"
            >
              <option value="">All datasets</option>
              {datasets.map((ds) => (
                <option key={ds.id} value={ds.id}>
                  {ds.name}
                </option>
              ))}
            </select>
          </div>

          <div>
            <label className="block text-xs font-medium text-gray-400 mb-1">
              Model name
            </label>
            <input
              type="text"
              value={filters.model_name}
              onChange={(e) => handleFilterChange('model_name', e.target.value)}
              placeholder="e.g., GPT-4o"
              className="w-full px-3 py-2 bg-gray-800 border border-gray-700 rounded text-white text-sm focus:outline-none focus:border-blue-500"
            />
          </div>

          <div>
            <label className="block text-xs font-medium text-gray-400 mb-1">
              Status
            </label>
            <select
              value={filters.status}
              onChange={(e) => handleFilterChange('status', e.target.value)}
              className="w-full px-3 py-2 bg-gray-800 border border-gray-700 rounded text-white text-sm focus:outline-none focus:border-blue-500"
            >
              {statusOptions.map((opt) => (
                <option key={opt.value} value={opt.value}>
                  {opt.label}
                </option>
              ))}
            </select>
          </div>
        </div>

        {/* Error */}
        {error && (
          <div className="mb-4 p-4 bg-red-900 border border-red-700 text-red-100 rounded text-sm">
            {error}
          </div>
        )}

        {/* Loading */}
        {loading && (
          <div className="text-white text-center py-10">
            <div className="animate-spin inline-block w-8 h-8 border-4 border-white border-t-transparent rounded-full mb-2" />
            <p>Loading submissions...</p>
          </div>
        )}

        {/* Table */}
        {!loading && !error && (
          <div className="bg-gray-950 rounded-lg border border-gray-800 overflow-x-auto">
            {submissions.length === 0 ? (
              <div className="p-8 text-center text-gray-400">
                <p className="text-lg mb-2">No submissions found</p>
                <p className="text-sm">
                  Try adjusting your filters or submit a new model from the Submit page.
                </p>
              </div>
            ) : (
              <table className="min-w-full text-sm text-left">
                <thead className="bg-gray-800 text-gray-200">
                  <tr>
                    <th className="px-4 py-3">Model</th>
                    <th className="px-4 py-3">Dataset</th>
                    <th className="px-4 py-3">Status</th>
                    <th className="px-4 py-3">Primary Score</th>
                    <th className="px-4 py-3 hidden lg:table-cell">Created</th>
                  </tr>
                </thead>
                <tbody>
                  {submissions.map((sub) => (
                    <tr
                      key={sub.id}
                      className="border-t border-gray-800 hover:bg-gray-800/80"
                    >
                      <td className="px-4 py-3 text-white">
                        <div className="flex flex-col">
                          <span className="font-medium truncate">
                            {sub.model_name}
                          </span>
                          {sub.organization && (
                            <span className="text-xs text-gray-400">
                              {sub.organization}
                            </span>
                          )}
                        </div>
                      </td>
                      <td className="px-4 py-3">
                        {(() => {
                          const dataset = getDatasetInfo(sub.dataset_id);
                          if (dataset) {
                            return (
                              <button
                                onClick={(e) => {
                                  e.stopPropagation();
                                  navigate(`/leaderboard/${sub.dataset_id}`);
                                }}
                                className="text-left hover:text-blue-400 transition-colors"
                              >
                                <div className="flex flex-col">
                                  <span className="text-white font-medium truncate max-w-xs">
                                    {dataset.name}
                                  </span>
                                  <span className="text-xs text-gray-400">
                                    {dataset.task_type.replace('_', ' ')}
                                  </span>
                                </div>
                              </button>
                            );
                          }
                          return (
                            <span className="text-gray-500 text-xs">
                              {sub.dataset_id.slice(0, 8)}...
                            </span>
                          );
                        })()}
                      </td>
                      <td className="px-4 py-3">
                        <span
                          className={`px-2 py-1 rounded text-xs font-semibold uppercase ${
                            sub.status === 'completed'
                              ? 'bg-green-900 text-green-300'
                              : sub.status === 'failed'
                              ? 'bg-red-900 text-red-300'
                              : 'bg-yellow-900 text-yellow-300'
                          }`}
                        >
                          {sub.status}
                        </span>
                      </td>
                      <td className="px-4 py-3 text-gray-200">
                        {sub.primary_score != null
                          ? sub.primary_score.toFixed(4)
                          : '-'}
                      </td>
                      <td className="px-4 py-3 text-gray-400 text-xs hidden lg:table-cell">
                        {sub.created_at
                          ? new Date(sub.created_at).toLocaleString()
                          : '-'}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            )}
          </div>
        )}
      </div>
    </div>
  );
};

export default SubmissionHistory;


