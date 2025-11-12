import React from 'react';

const LeaderboardCard = ({ leaderboard }) => {
  return (
    <div className="w-full max-w-3xl p-4 bg-gray-950 rounded-lg shadow-lg card-hover">
      <div className="flex justify-between items-center mb-4">
        <div>
          <h2 className="text-xl font-bold text-white">{leaderboard.dataset_name}</h2>
          <p className="text-sm text-gray-400">
            {leaderboard.task_type.replace('_', ' ').toUpperCase()} | Metric: {leaderboard.primary_metric}
          </p>
        </div>
        {leaderboard.url && (
          <a
            href={leaderboard.url}
            className="text-blue-400 hover:text-blue-500 text-sm underline"
            target="_blank"
            rel="noopener noreferrer"
          >
            View Dataset
          </a>
        )}
      </div>
      
      <div className="grid grid-cols-4 text-white font-bold text-center bg-gray-900 p-4 rounded-t-lg">
        <div>Rank</div>
        <div>Model</div>
        <div>Score</div>
        <div>Last Updated</div>
      </div>
      
      <div>
        {leaderboard.entries.length === 0 ? (
          <div className="text-center p-8 text-gray-400">
            No submissions yet
          </div>
        ) : (
          leaderboard.entries.map((entry, index) => (
            <div
              key={entry.submission_id}
              className={`grid grid-cols-4 text-center p-4 ${
                index % 2 === 0 ? 'bg-gray-700 text-white' : 'bg-gray-800 text-white'
              }`}
            >
              <div className="flex items-center justify-center">
                {entry.rank === 1 && <span className="mr-1">🥇</span>}
                {entry.rank === 2 && <span className="mr-1">🥈</span>}
                {entry.rank === 3 && <span className="mr-1">🥉</span>}
                {entry.rank}
              </div>
              <div className="flex items-center justify-center">
                {entry.model_name}
                {entry.is_internal && (
                  <span className="ml-2 px-2 py-1 text-xs bg-blue-500 rounded">Internal</span>
                )}
              </div>
              <div>{entry.score.toFixed(4)}</div>
              <div className="text-sm text-gray-300">{entry.updated_at}</div>
            </div>
          ))
        )}
      </div>
    </div>
  );
};

export default LeaderboardCard;

