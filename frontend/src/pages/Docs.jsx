import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

const Docs = () => {
  const navigate = useNavigate();
  const [activeTab, setActiveTab] = useState('api');

  const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

  const tabs = [
    { id: 'api', label: 'API Reference', icon: '📡' },
    { id: 'architecture', label: 'Architecture', icon: '🏗️' },
    { id: 'contributing', label: 'Contributing', icon: '🤝' },
    { id: 'interactive', label: 'Interactive Docs', icon: '⚡' },
  ];

  return (
    <div className="min-h-screen bg-gray-900 py-8 px-3">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="mb-6 flex justify-between items-center">
          <button
            onClick={() => navigate('/')}
            className="text-blue-400 hover:text-blue-300"
          >
            ← Back to Leaderboards
          </button>
        </div>

        <h1 className="text-4xl font-bold text-white mb-2">Documentation</h1>
        <p className="text-gray-400 mb-8">
          Complete guides for using, extending, and contributing to the Anote Leaderboard
        </p>

        {/* Tab Navigation */}
        <div className="flex space-x-2 mb-6 border-b border-gray-800 overflow-x-auto">
          {tabs.map((tab) => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={`px-4 py-3 text-sm font-medium whitespace-nowrap transition-colors border-b-2 ${
                activeTab === tab.id
                  ? 'text-blue-400 border-blue-400'
                  : 'text-gray-400 border-transparent hover:text-gray-300'
              }`}
            >
              <span className="mr-2">{tab.icon}</span>
              {tab.label}
            </button>
          ))}
        </div>

        {/* Content */}
        <div className="bg-gray-950 rounded-lg border border-gray-800 p-6">
          {activeTab === 'api' && (
            <div className="prose prose-invert max-w-none">
              <div className="mb-6 p-4 bg-blue-900/20 border border-blue-800 rounded-lg">
                <p className="text-blue-300 text-sm mb-2">
                  📖 This is a summary. For the complete API reference with all endpoints, examples, and schemas:
                </p>
                <a
                  href="https://github.com/yourusername/anoteleaderboard/blob/master/docs/API.md"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-blue-400 hover:text-blue-300 underline text-sm"
                >
                  View full API.md on GitHub →
                </a>
              </div>

              <h2 className="text-2xl font-bold text-white mb-4">API Quick Reference</h2>
              
              <div className="space-y-6 text-gray-300">
                <div>
                  <h3 className="text-xl font-semibold text-white mb-2">Base URL</h3>
                  <code className="bg-gray-900 px-3 py-2 rounded text-emerald-400 block">
                    {API_BASE_URL}
                  </code>
                </div>

                <div>
                  <h3 className="text-xl font-semibold text-white mb-2">Key Endpoints</h3>
                  <ul className="space-y-2 list-none">
                    <li className="bg-gray-900 p-3 rounded">
                      <span className="text-green-400 font-mono font-semibold">GET</span>
                      <code className="ml-3 text-gray-300">/api/leaderboard</code>
                      <p className="text-sm text-gray-400 mt-1 ml-14">Get all leaderboards</p>
                    </li>
                    <li className="bg-gray-900 p-3 rounded">
                      <span className="text-blue-400 font-mono font-semibold">POST</span>
                      <code className="ml-3 text-gray-300">/api/submissions</code>
                      <p className="text-sm text-gray-400 mt-1 ml-14">Submit model predictions</p>
                    </li>
                    <li className="bg-gray-900 p-3 rounded">
                      <span className="text-green-400 font-mono font-semibold">GET</span>
                      <code className="ml-3 text-gray-300">/api/datasets</code>
                      <p className="text-sm text-gray-400 mt-1 ml-14">List all datasets</p>
                    </li>
                    <li className="bg-gray-900 p-3 rounded">
                      <span className="text-green-400 font-mono font-semibold">GET</span>
                      <code className="ml-3 text-gray-300">/api/metrics</code>
                      <p className="text-sm text-gray-400 mt-1 ml-14">Get metric information</p>
                    </li>
                  </ul>
                </div>

                <div>
                  <h3 className="text-xl font-semibold text-white mb-2">Rate Limits</h3>
                  <ul className="space-y-1 text-sm">
                    <li>• General API: <span className="text-emerald-400">100/minute</span></li>
                    <li>• Submissions: <span className="text-yellow-400">10/minute</span></li>
                    <li>• Admin: <span className="text-red-400">5/minute</span></li>
                    <li>• Leaderboards: <span className="text-blue-400">200/minute</span></li>
                  </ul>
                </div>

                <div>
                  <h3 className="text-xl font-semibold text-white mb-2">Quick Example</h3>
                  <pre className="bg-gray-900 p-4 rounded overflow-x-auto text-sm">
{`curl -X POST ${API_BASE_URL}/api/submissions \\
  -H "Content-Type: application/json" \\
  -d '{
    "dataset_id": "uuid",
    "model_name": "My Model",
    "predictions": [
      {"id": "1", "prediction": "answer"}
    ]
  }'`}
                  </pre>
                </div>
              </div>
            </div>
          )}

          {activeTab === 'architecture' && (
            <div className="prose prose-invert max-w-none">
              <div className="mb-6 p-4 bg-purple-900/20 border border-purple-800 rounded-lg">
                <p className="text-purple-300 text-sm mb-2">
                  🏗️ This is a summary. For the complete architecture documentation:
                </p>
                <a
                  href="https://github.com/yourusername/anoteleaderboard/blob/master/docs/ARCHITECTURE.md"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-purple-400 hover:text-purple-300 underline text-sm"
                >
                  View full ARCHITECTURE.md on GitHub →
                </a>
              </div>

              <h2 className="text-2xl font-bold text-white mb-4">System Architecture</h2>
              
              <div className="space-y-6 text-gray-300">
                <div>
                  <h3 className="text-xl font-semibold text-white mb-3">Tech Stack</h3>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div className="bg-gray-900 p-4 rounded">
                      <h4 className="font-semibold text-emerald-400 mb-2">Backend</h4>
                      <ul className="text-sm space-y-1">
                        <li>• FastAPI (Python 3.12)</li>
                        <li>• SQLAlchemy ORM</li>
                        <li>• SQLite / PostgreSQL</li>
                        <li>• Pydantic validation</li>
                        <li>• pytest testing</li>
                      </ul>
                    </div>
                    <div className="bg-gray-900 p-4 rounded">
                      <h4 className="font-semibold text-blue-400 mb-2">Frontend</h4>
                      <ul className="text-sm space-y-1">
                        <li>• React 18</li>
                        <li>• Vite build tool</li>
                        <li>• TailwindCSS</li>
                        <li>• React Router</li>
                        <li>• Axios HTTP client</li>
                      </ul>
                    </div>
                  </div>
                </div>

                <div>
                  <h3 className="text-xl font-semibold text-white mb-3">Key Components</h3>
                  <ul className="space-y-2 text-sm">
                    <li className="bg-gray-900 p-3 rounded">
                      <strong className="text-white">Evaluators:</strong> Task-specific evaluation logic (classification, NER, QA, retrieval)
                    </li>
                    <li className="bg-gray-900 p-3 rounded">
                      <strong className="text-white">Cache Layer:</strong> 5-minute TTL for leaderboard queries
                    </li>
                    <li className="bg-gray-900 p-3 rounded">
                      <strong className="text-white">Rate Limiter:</strong> Per-IP limits to prevent abuse
                    </li>
                    <li className="bg-gray-900 p-3 rounded">
                      <strong className="text-white">HF Importer:</strong> Bulk import from HuggingFace datasets
                    </li>
                  </ul>
                </div>

                <div>
                  <h3 className="text-xl font-semibold text-white mb-3">Supported Task Types</h3>
                  <div className="grid grid-cols-1 sm:grid-cols-2 gap-2 text-sm">
                    <span className="bg-gray-900 px-3 py-2 rounded">📝 Text Classification</span>
                    <span className="bg-gray-900 px-3 py-2 rounded">🏷️ Named Entity Recognition</span>
                    <span className="bg-gray-900 px-3 py-2 rounded">📚 Document Q&A</span>
                    <span className="bg-gray-900 px-3 py-2 rounded">💬 Line Q&A</span>
                    <span className="bg-gray-900 px-3 py-2 rounded">🔍 Retrieval</span>
                  </div>
                </div>
              </div>
            </div>
          )}

          {activeTab === 'contributing' && (
            <div className="prose prose-invert max-w-none">
              <div className="mb-6 p-4 bg-green-900/20 border border-green-800 rounded-lg">
                <p className="text-green-300 text-sm mb-2">
                  🤝 Want to contribute? Check out the full guide:
                </p>
                <a
                  href="https://github.com/yourusername/anoteleaderboard/blob/master/docs/CONTRIBUTING.md"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-green-400 hover:text-green-300 underline text-sm"
                >
                  View full CONTRIBUTING.md on GitHub →
                </a>
              </div>

              <h2 className="text-2xl font-bold text-white mb-4">Contributing Guide</h2>
              
              <div className="space-y-6 text-gray-300">
                <div>
                  <h3 className="text-xl font-semibold text-white mb-3">Getting Started</h3>
                  <ol className="space-y-2 list-decimal list-inside text-sm">
                    <li>Fork the repository on GitHub</li>
                    <li>Clone your fork locally</li>
                    <li>Create a new branch: <code className="bg-gray-900 px-2 py-1 rounded text-blue-400">git checkout -b feature/my-feature</code></li>
                    <li>Make your changes and write tests</li>
                    <li>Run the test suite: <code className="bg-gray-900 px-2 py-1 rounded text-emerald-400">pytest</code></li>
                    <li>Push and create a Pull Request</li>
                  </ol>
                </div>

                <div>
                  <h3 className="text-xl font-semibold text-white mb-3">Development Setup</h3>
                  <pre className="bg-gray-900 p-4 rounded overflow-x-auto text-sm">
{`# Backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload

# Frontend
cd frontend
npm install
npm run dev`}
                  </pre>
                </div>

                <div>
                  <h3 className="text-xl font-semibold text-white mb-3">What to Contribute</h3>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-3 text-sm">
                    <div className="bg-gray-900 p-3 rounded">
                      <strong className="text-emerald-400">New Datasets</strong>
                      <p className="text-gray-400 mt-1">Add domain-specific benchmarks</p>
                    </div>
                    <div className="bg-gray-900 p-3 rounded">
                      <strong className="text-blue-400">New Metrics</strong>
                      <p className="text-gray-400 mt-1">Implement additional evaluation metrics</p>
                    </div>
                    <div className="bg-gray-900 p-3 rounded">
                      <strong className="text-purple-400">Bug Fixes</strong>
                      <p className="text-gray-400 mt-1">Fix issues and improve stability</p>
                    </div>
                    <div className="bg-gray-900 p-3 rounded">
                      <strong className="text-yellow-400">Documentation</strong>
                      <p className="text-gray-400 mt-1">Improve guides and examples</p>
                    </div>
                  </div>
                </div>

                <div>
                  <h3 className="text-xl font-semibold text-white mb-3">Code Style</h3>
                  <ul className="space-y-1 text-sm">
                    <li>• Python: Follow PEP 8, use Black formatter</li>
                    <li>• JavaScript: Airbnb style guide, use Prettier</li>
                    <li>• Write tests for all new features</li>
                    <li>• Add docstrings to public functions</li>
                  </ul>
                </div>
              </div>
            </div>
          )}

          {activeTab === 'interactive' && (
            <div className="text-center py-12">
              <div className="mb-6">
                <h2 className="text-2xl font-bold text-white mb-4">Interactive API Documentation</h2>
                <p className="text-gray-400 mb-6">
                  Test API endpoints directly in your browser with Swagger UI
                </p>
              </div>
              
              <div className="flex flex-col items-center space-y-4">
                <a
                  href={`${API_BASE_URL}/docs`}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="inline-flex items-center px-8 py-4 bg-gradient-to-r from-blue-600 to-blue-700 hover:from-blue-700 hover:to-blue-800 text-white rounded-lg text-lg font-semibold shadow-lg hover:shadow-xl transition-all"
                >
                  <svg className="w-6 h-6 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
                  </svg>
                  Open Swagger UI
                </a>

                <a
                  href={`${API_BASE_URL}/redoc`}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="inline-flex items-center px-8 py-4 bg-gray-800 hover:bg-gray-700 text-white rounded-lg font-semibold border border-gray-700 transition-all"
                >
                  <svg className="w-6 h-6 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                  </svg>
                  Open ReDoc
                </a>
              </div>

              <div className="mt-8 text-sm text-gray-400">
                <p>Swagger UI provides an interactive interface to test all API endpoints</p>
                <p>ReDoc provides a clean, searchable reference documentation</p>
              </div>
            </div>
          )}
        </div>

        {/* Bottom CTA */}
        <div className="mt-8 text-center">
          <div className="inline-block bg-gray-950 border border-gray-800 rounded-lg p-6">
            <h3 className="text-lg font-semibold text-white mb-2">Need Help?</h3>
            <p className="text-gray-400 text-sm mb-4">
              Check out our GitHub repository for issues, discussions, and the latest updates
            </p>
            <a
              href="https://github.com/yourusername/anoteleaderboard"
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex items-center px-6 py-2 bg-gray-800 hover:bg-gray-700 text-white rounded-lg text-sm font-medium border border-gray-700 transition-colors"
            >
              <svg className="w-5 h-5 mr-2" fill="currentColor" viewBox="0 0 24 24">
                <path fillRule="evenodd" d="M12 2C6.477 2 2 6.484 2 12.017c0 4.425 2.865 8.18 6.839 9.504.5.092.682-.217.682-.483 0-.237-.008-.868-.013-1.703-2.782.605-3.369-1.343-3.369-1.343-.454-1.158-1.11-1.466-1.11-1.466-.908-.62.069-.608.069-.608 1.003.07 1.531 1.032 1.531 1.032.892 1.53 2.341 1.088 2.91.832.092-.647.35-1.088.636-1.338-2.22-.253-4.555-1.113-4.555-4.951 0-1.093.39-1.988 1.029-2.688-.103-.253-.446-1.272.098-2.65 0 0 .84-.27 2.75 1.026A9.564 9.564 0 0112 6.844c.85.004 1.705.115 2.504.337 1.909-1.296 2.747-1.027 2.747-1.027.546 1.379.202 2.398.1 2.651.64.7 1.028 1.595 1.028 2.688 0 3.848-2.339 4.695-4.566 4.943.359.309.678.92.678 1.855 0 1.338-.012 2.419-.012 2.747 0 .268.18.58.688.482A10.019 10.019 0 0022 12.017C22 6.484 17.522 2 12 2z" clipRule="evenodd" />
              </svg>
              View on GitHub
            </a>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Docs;

