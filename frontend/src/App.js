import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css';
import Dashboard from './components/Dashboard';
import FeedbackList from './components/FeedbackList';
import AnalysisSummary from './components/AnalysisSummary';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

function App() {
  const [activeTab, setActiveTab] = useState('dashboard');
  const [overview, setOverview] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchOverview();
  }, []);

  const fetchOverview = async () => {
    try {
      const response = await axios.get(`${API_URL}/stats/overview`);
      setOverview(response.data);
    } catch (error) {
      console.error('Error fetching overview:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="App">
      <header className="header">
        <h1>📊 Feedback Explorer</h1>
        <p>AI-powered customer feedback analysis</p>
      </header>

      <nav className="nav">
        <button 
          className={activeTab === 'dashboard' ? 'active' : ''}
          onClick={() => setActiveTab('dashboard')}
        >
          Dashboard
        </button>
        <button 
          className={activeTab === 'explore' ? 'active' : ''}
          onClick={() => setActiveTab('explore')}
        >
          Explore Feedback
        </button>
        <button 
          className={activeTab === 'analysis' ? 'active' : ''}
          onClick={() => setActiveTab('analysis')}
        >
          AI Analysis
        </button>
      </nav>

      <main className="main">
        {loading ? (
          <div className="loading">Loading...</div>
        ) : (
          <>
            {activeTab === 'dashboard' && <Dashboard overview={overview} />}
            {activeTab === 'explore' && <FeedbackList />}
            {activeTab === 'analysis' && <AnalysisSummary />}
          </>
        )}
      </main>
    </div>
  );
}

export default App;
