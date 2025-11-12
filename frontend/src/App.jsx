import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import Home from './pages/Home';
import CreateDataset from './pages/CreateDataset';
import Submit from './pages/Submit';

function App() {
  return (
    <Router>
      <div className="min-h-screen bg-gray-900">
        {/* Navigation */}
        <nav className="bg-gray-950 border-b border-gray-800">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="flex justify-between items-center h-16">
              <div className="flex items-center">
                <Link to="/" className="text-white text-xl font-bold">
                  Anote Leaderboard
                </Link>
              </div>
              
              <div className="flex space-x-4">
                <Link
                  to="/"
                  className="text-gray-300 hover:text-white px-3 py-2 rounded-md text-sm font-medium transition-colors"
                >
                  Leaderboards
                </Link>
                <Link
                  to="/create-dataset"
                  className="text-gray-300 hover:text-white px-3 py-2 rounded-md text-sm font-medium transition-colors"
                >
                  Create Dataset
                </Link>
                <Link
                  to="/submit"
                  className="btn-black px-4 py-2 rounded-md text-sm font-medium"
                >
                  Submit Model
                </Link>
              </div>
            </div>
          </div>
        </nav>

        {/* Main Content */}
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/create-dataset" element={<CreateDataset />} />
          <Route path="/submit" element={<Submit />} />
        </Routes>

        {/* Footer */}
        <footer className="bg-gray-950 border-t border-gray-800 mt-20">
          <div className="max-w-7xl mx-auto px-4 py-6 text-center text-gray-400 text-sm">
            <p className="mb-2">
              Built with ❤️ by Anote | <a href="https://anote.ai" className="text-blue-400 hover:text-blue-300">anote.ai</a>
            </p>
            <p>
              <a 
                href="http://localhost:8000/docs" 
                target="_blank" 
                rel="noopener noreferrer"
                className="text-blue-400 hover:text-blue-300"
              >
                API Documentation
              </a>
              {' | '}
              <a 
                href="https://github.com/nv78/Autonomous-Intelligence" 
                target="_blank" 
                rel="noopener noreferrer"
                className="text-blue-400 hover:text-blue-300"
              >
                GitHub
              </a>
            </p>
          </div>
        </footer>
      </div>
    </Router>
  );
}

export default App;

