import React, { useState } from 'react';
import axios from 'axios';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

function AnalysisSummary() {
  const [summary, setSummary] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [filters, setFilters] = useState({
    time_range: 'week',
    sentiment: '',
    category: ''
  });

  const generateSummary = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await axios.post(`${API_URL}/analyze/summary`, filters);
      setSummary(response.data);
    } catch (err) {
      setError('Failed to generate summary. Please try again.');
      console.error('Error generating summary:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleFilterChange = (e) => {
    setFilters({
      ...filters,
      [e.target.name]: e.target.value
    });
  };

  return (
    <div>
      <div className="card">
        <h2>AI-Powered Analysis</h2>
        <p style={{color: '#666', marginBottom: '1.5rem'}}>
          Generate intelligent summaries and insights from your feedback data
        </p>

        <div className="filters">
          <select name="time_range" value={filters.time_range} onChange={handleFilterChange}>
            <option value="day">Last 24 Hours</option>
            <option value="week">Last Week</option>
            <option value="month">Last Month</option>
            <option value="all">All Time</option>
          </select>

          <select name="sentiment" value={filters.sentiment} onChange={handleFilterChange}>
            <option value="">All Sentiments</option>
            <option value="positive">Positive Only</option>
            <option value="negative">Negative Only</option>
            <option value="mixed">Mixed Only</option>
          </select>

          <button 
            className="button" 
            onClick={generateSummary}
            disabled={loading}
          >
            {loading ? 'Analyzing...' : '✨ Generate AI Summary'}
          </button>
        </div>

        {error && <div className="error">{error}</div>}
      </div>

      {summary && (
        <>
          <div className="card">
            <h2>Summary</h2>
            <div className="summary-text">{summary.summary}</div>
          </div>

          <div className="card">
            <h2>Sentiment Breakdown</h2>
            <div className="chart-container">
              <ResponsiveContainer width="100%" height={300}>
                <BarChart data={Object.entries(summary.sentiment_breakdown || {}).map(([key, value]) => ({
                  name: key.charAt(0).toUpperCase() + key.slice(1),
                  count: value
                }))}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="name" />
                  <YAxis />
                  <Tooltip />
                  <Legend />
                  <Bar dataKey="count" fill="#667eea" />
                </BarChart>
              </ResponsiveContainer>
            </div>
          </div>

          {summary.top_categories && summary.top_categories.length > 0 && (
            <div className="card">
              <h2>Top Categories</h2>
              <div style={{display: 'grid', gap: '1rem'}}>
                {summary.top_categories.map((cat, idx) => (
                  <div key={idx} style={{
                    display: 'flex',
                    justifyContent: 'space-between',
                    alignItems: 'center',
                    padding: '1rem',
                    background: '#f8f9fa',
                    borderRadius: '8px'
                  }}>
                    <span style={{fontWeight: '500'}}>
                      {cat.category.replace('_', ' ').toUpperCase()}
                    </span>
                    <span style={{
                      background: '#667eea',
                      color: 'white',
                      padding: '0.25rem 0.75rem',
                      borderRadius: '12px',
                      fontSize: '0.9rem'
                    }}>
                      {cat.count} mentions
                    </span>
                  </div>
                ))}
              </div>
            </div>
          )}

          <div className="card">
            <h3>Analysis Details</h3>
            <div style={{display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '1rem'}}>
              <div>
                <div style={{color: '#666', fontSize: '0.9rem'}}>Total Items Analyzed</div>
                <div style={{fontSize: '1.5rem', fontWeight: 'bold', color: '#667eea', marginTop: '0.25rem'}}>
                  {summary.total_count}
                </div>
              </div>
              <div>
                <div style={{color: '#666', fontSize: '0.9rem'}}>Time Range</div>
                <div style={{fontSize: '1.5rem', fontWeight: 'bold', color: '#667eea', marginTop: '0.25rem'}}>
                  {summary.time_range}
                </div>
              </div>
            </div>
          </div>
        </>
      )}

      {!summary && !loading && (
        <div className="empty-state">
          Click "Generate AI Summary" to analyze your feedback
        </div>
      )}
    </div>
  );
}

export default AnalysisSummary;
