import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const COLORS = {
  positive: '#28a745',
  negative: '#dc3545',
  mixed: '#ffc107',
  neutral: '#6c757d'
};

function Dashboard({ overview }) {
  const [trends, setTrends] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchTrends();
  }, []);

  const fetchTrends = async () => {
    try {
      const response = await axios.get(`${API_URL}/analyze/trends?days=14`);
      setTrends(response.data.reverse());
    } catch (error) {
      console.error('Error fetching trends:', error);
    } finally {
      setLoading(false);
    }
  };

  if (!overview) return <div className="loading">Loading...</div>;

  const sentimentData = Object.entries(overview.sentiment_distribution || {}).map(([key, value]) => ({
    name: key.charAt(0).toUpperCase() + key.slice(1),
    value: value
  }));

  return (
    <div>
      <div className="stats-grid">
        <div className="stat-card">
          <div className="label">Total Feedback</div>
          <div className="value">{overview.total_feedback}</div>
        </div>
        <div className="stat-card">
          <div className="label">Last 7 Days</div>
          <div className="value">{overview.recent_feedback}</div>
        </div>
        <div className="stat-card">
          <div className="label">Positive</div>
          <div className="value" style={{color: '#28a745'}}>
            {overview.sentiment_distribution?.positive || 0}
          </div>
        </div>
        <div className="stat-card">
          <div className="label">Negative</div>
          <div className="value" style={{color: '#dc3545'}}>
            {overview.sentiment_distribution?.negative || 0}
          </div>
        </div>
      </div>

      <div className="card">
        <h2>Sentiment Trends (Last 14 Days)</h2>
        {loading ? (
          <div className="loading">Loading chart...</div>
        ) : (
          <div className="chart-container">
            <ResponsiveContainer width="100%" height={300}>
              <LineChart data={trends}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="period" />
                <YAxis />
                <Tooltip />
                <Legend />
                <Line type="monotone" dataKey="positive" stroke={COLORS.positive} strokeWidth={2} />
                <Line type="monotone" dataKey="negative" stroke={COLORS.negative} strokeWidth={2} />
                <Line type="monotone" dataKey="mixed" stroke={COLORS.mixed} strokeWidth={2} />
              </LineChart>
            </ResponsiveContainer>
          </div>
        )}
      </div>

      <div className="card">
        <h2>Sentiment Distribution (Last 7 Days)</h2>
        <div className="chart-container">
          <ResponsiveContainer width="100%" height={300}>
            <PieChart>
              <Pie
                data={sentimentData}
                cx="50%"
                cy="50%"
                labelLine={false}
                label={({ name, percent }) => `${name}: ${(percent * 100).toFixed(0)}%`}
                outerRadius={80}
                fill="#8884d8"
                dataKey="value"
              >
                {sentimentData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={COLORS[entry.name.toLowerCase()]} />
                ))}
              </Pie>
              <Tooltip />
            </PieChart>
          </ResponsiveContainer>
        </div>
      </div>

      <div className="card">
        <h2>Feedback Sources</h2>
        <div style={{display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '1rem'}}>
          {overview.sources?.map(source => (
            <div key={source.source} style={{padding: '1rem', background: '#f8f9fa', borderRadius: '8px'}}>
              <div style={{fontSize: '0.9rem', color: '#666', marginBottom: '0.25rem'}}>
                {source.source.replace('_', ' ').toUpperCase()}
              </div>
              <div style={{fontSize: '1.5rem', fontWeight: 'bold', color: '#667eea'}}>
                {source.count}
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

export default Dashboard;
