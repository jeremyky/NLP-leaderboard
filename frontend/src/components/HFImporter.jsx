import React, { useState } from 'react';
import { importFromHuggingFace } from '../services/api';

const HFImporter = ({ onSuccess }) => {
  const [datasetName, setDatasetName] = useState('');
  const [config, setConfig] = useState('default');
  const [split, setSplit] = useState('test');
  const [numSamples, setNumSamples] = useState(100);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(null);

  // Popular HuggingFace datasets
  const popularDatasets = [
    { name: 'ag_news', description: 'AG News Classification (4 classes)' },
    { name: 'sst2', description: 'Stanford Sentiment Treebank (Binary)' },
    { name: 'imdb', description: 'IMDB Movie Reviews (Sentiment)' },
    { name: 'squad', description: 'SQuAD Question Answering' },
    { name: 'conll2003', description: 'CoNLL-2003 (NER)' },
    { name: 'wikitext', description: 'WikiText Language Modeling' },
    { name: 'financial_phrasebank', description: 'Financial Sentiment' },
  ];

  const handleImport = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setSuccess(null);

    try {
      const result = await importFromHuggingFace(datasetName, config, split, numSamples);
      setSuccess(`Successfully imported ${result.data.name}! (${result.data.num_examples} examples)`);
      setDatasetName('');
      if (onSuccess) onSuccess(result.data);
    } catch (err) {
      setError(err.response?.data?.detail || err.message || 'Failed to import dataset');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="bg-gray-800 rounded-lg p-6 border border-gray-700">
      <h3 className="text-xl font-bold text-white mb-4">
        🤗 Import from HuggingFace
      </h3>
      
      {error && (
        <div className="mb-4 p-3 bg-red-900 border border-red-700 text-red-100 rounded text-sm">
          {error}
        </div>
      )}
      
      {success && (
        <div className="mb-4 p-3 bg-green-900 border border-green-700 text-green-100 rounded text-sm">
          {success}
        </div>
      )}

      <form onSubmit={handleImport} className="space-y-4">
        <div>
          <label className="block text-sm font-medium text-gray-300 mb-2">
            Dataset Name *
          </label>
          <input
            type="text"
            value={datasetName}
            onChange={(e) => setDatasetName(e.target.value)}
            required
            className="w-full px-3 py-2 bg-gray-900 border border-gray-700 rounded text-white text-sm focus:outline-none focus:border-blue-500"
            placeholder="e.g., ag_news, sst2, imdb"
          />
          
          {/* Quick select popular datasets */}
          <div className="mt-2 flex flex-wrap gap-2">
            {popularDatasets.map(ds => (
              <button
                key={ds.name}
                type="button"
                onClick={() => setDatasetName(ds.name)}
                className="px-2 py-1 bg-gray-700 hover:bg-gray-600 text-gray-300 text-xs rounded"
                title={ds.description}
              >
                {ds.name}
              </button>
            ))}
          </div>
        </div>

        <div className="grid grid-cols-3 gap-3">
          <div>
            <label className="block text-sm font-medium text-gray-300 mb-2">
              Config
            </label>
            <input
              type="text"
              value={config}
              onChange={(e) => setConfig(e.target.value)}
              className="w-full px-3 py-2 bg-gray-900 border border-gray-700 rounded text-white text-sm focus:outline-none focus:border-blue-500"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-300 mb-2">
              Split
            </label>
            <select
              value={split}
              onChange={(e) => setSplit(e.target.value)}
              className="w-full px-3 py-2 bg-gray-900 border border-gray-700 rounded text-white text-sm focus:outline-none focus:border-blue-500"
            >
              <option value="test">test</option>
              <option value="validation">validation</option>
              <option value="train">train</option>
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-300 mb-2">
              Samples
            </label>
            <input
              type="number"
              value={numSamples}
              onChange={(e) => setNumSamples(parseInt(e.target.value))}
              min="10"
              max="1000"
              className="w-full px-3 py-2 bg-gray-900 border border-gray-700 rounded text-white text-sm focus:outline-none focus:border-blue-500"
            />
          </div>
        </div>

        <button
          type="submit"
          disabled={loading || !datasetName}
          className="w-full px-4 py-2 bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-700 hover:to-blue-700 text-white rounded disabled:opacity-50"
        >
          {loading ? 'Importing...' : 'Import Dataset'}
        </button>
      </form>

      <div className="mt-4 p-3 bg-gray-900 rounded text-xs text-gray-400">
        <p className="font-semibold mb-1">💡 Tips:</p>
        <ul className="list-disc list-inside space-y-1">
          <li>Click any popular dataset name to auto-fill</li>
          <li>Most datasets use "default" config and "test" split</li>
          <li>Start with 100 samples for testing</li>
          <li>Browse datasets at: <a href="https://huggingface.co/datasets" target="_blank" rel="noopener noreferrer" className="text-blue-400 hover:text-blue-300">huggingface.co/datasets</a></li>
        </ul>
      </div>
    </div>
  );
};

export default HFImporter;

