import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Dataset APIs
export const getDatasets = async (taskType = null) => {
  const params = taskType ? { task_type: taskType } : {};
  const response = await api.get('/api/datasets', { params });
  return response.data;
};

export const getDataset = async (datasetId) => {
  const response = await api.get(`/api/datasets/${datasetId}`);
  return response.data;
};

export const getDatasetQuestions = async (datasetId) => {
  const response = await api.get(`/api/datasets/${datasetId}/questions`);
  return response.data;
};

export const createDataset = async (datasetData) => {
  const response = await api.post('/api/datasets', datasetData);
  return response.data;
};

// Submission APIs
export const submitPredictions = async (submissionData) => {
  const response = await api.post('/api/submissions', submissionData);
  return response.data;
};

export const getSubmission = async (submissionId) => {
  const response = await api.get(`/api/submissions/${submissionId}`);
  return response.data;
};

export const getSubmissions = async (filters = {}) => {
  const response = await api.get('/api/submissions', { params: filters });
  return response.data;
};

// Leaderboard APIs
export const getAllLeaderboards = async (taskType = null) => {
  const params = taskType ? { task_type: taskType } : {};
  const response = await api.get('/api/leaderboard', { params });
  return response.data;
};

export const getLeaderboard = async (datasetId, includeInternal = true) => {
  const response = await api.get(`/api/leaderboard/${datasetId}`, {
    params: { include_internal: includeInternal }
  });
  return response.data;
};

// Admin/Data Management APIs
export const seedSampleData = async () => {
  const response = await api.post('/api/admin/seed-data');
  return response.data;
};

export const importFromHuggingFace = async (datasetName, config = 'default', split = 'test', numSamples = 100) => {
  const response = await api.post('/api/admin/import-huggingface', null, {
    params: { dataset_name: datasetName, config, split, num_samples: numSamples }
  });
  return response.data;
};

// Health check
export const healthCheck = async () => {
  const response = await api.get('/health');
  return response.data;
};

// Metrics info APIs
export const getMetricInfo = async (metricName) => {
  const response = await api.get(`/api/metrics/${metricName}`);
  return response.data;
};

export const getTaskMetrics = async (taskType) => {
  const response = await api.get(`/api/metrics/task/${taskType}`);
  return response.data;
};

export default api;

