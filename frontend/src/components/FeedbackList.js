import React, { useState, useEffect } from 'react';
import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

function FeedbackList() {
  const [feedback, setFeedback] = useState([]);
  const [categories, setCategories] = useState([]);
  const [loading, setLoading] = useState(true);
  const [filters, setFilters] = useState({
    sentiment: '',
    category: '',
    days: '7'
  });

  useEffect(() => {
    fetchCategories();
  }, []);

  useEffect(() => {
    fetchFeedback();
  }, [filters]);

  const fetchCategories = async () => {
    try {
      const response = await axios.get(`${API_URL}/categories`);
      setCategories(response.data.categories);
    } catch (error) {
      console.error('Error fetching categories:', error);
    }
  };

  const fetchFeedback = async () => {
    setLoading(true);
    try {
      const params = new URLSearchParams();
      if (filters.sentiment) params.append('sentiment', filters.sentiment);
      if (filters.category) params.append('category', filters.category);
      if (filters.days) params.append('days', filters.days);
      
      const response = await axios.get(`${API_URL}/feedback?${params}`);
      setFeedback(response.data);
    } catch (error) {
      console.error('Error fetching feedback:', error);
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

  const formatDate = (dateString) => {
    const date = new Date(dateString);
    const now = new Date();
    const diffMs = now - date;
    const diffMins = Math.floor(diffMs / 60000);
    const diffHours = Math.floor(diffMs / 3600000);
    const diffDays = Math.floor(diffMs / 86400000);

    if (diffMins < 60) return `${diffMins}m ago`;
    if (diffHours < 24) return `${diffHours}h ago`;
    if (diffDays < 7) return `${diffDays}d ago`;
    return date.toLocaleDateString();
  };

  return (
    <div>
      <div className="card">
        <h2>Explore Feedback</h2>
        <div className="filters">
          <select name="days" value={filters.days} onChange={handleFilterChange}>
            <option value="">All Time</option>
            <option value="1">Last 24 Hours</option>
            <option value="7">Last 7 Days</option>
            <option value="30">Last 30 Days</option>
          </select>

          <select name="sentiment" value={filters.sentiment} onChange={handleFilterChange}>
            <option value="">All Sentiments</option>
            <option value="positive">Positive</option>
            <option value="negative">Negative</option>
            <option value="mixed">Mixed</option>
            <option value="neutral">Neutral</option>
          </select>

          <select name="category" value={filters.category} onChange={handleFilterChange}>
            <option value="">All Categories</option>
            {categories.map(cat => (
              <option key={cat} value={cat}>
                {cat.replace('_', ' ').toUpperCase()}
              </option>
            ))}
          </select>
        </div>

        <div style={{color: '#666', marginBottom: '1rem'}}>
          Showing {feedback.length} feedback items
        </div>
      </div>

      {loading ? (
        <div className="loading">Loading feedback...</div>
      ) : feedback.length === 0 ? (
        <div className="empty-state">
          No feedback found for the selected filters.
        </div>
      ) : (
        <div>
          {feedback.map(item => (
            <div key={item.id} className="feedback-item">
              <div className="feedback-header">
                <div className="feedback-meta">
                  <span className="source-badge">{item.source.replace('_', ' ')}</span>
                  <span>{formatDate(item.created_at)}</span>
                </div>
                <span className={`sentiment-badge sentiment-${item.sentiment}`}>
                  {item.sentiment}
                </span>
              </div>
              <div className="feedback-content">{item.content}</div>
              {item.category && (
                <div style={{marginTop: '0.5rem', fontSize: '0.85rem', color: '#888'}}>
                  Category: {item.category.replace('_', ' ')}
                </div>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default FeedbackList;