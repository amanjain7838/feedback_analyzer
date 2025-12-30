import React, { useState } from 'react';
import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const EXAMPLE_QUESTIONS = [
  "What are users complaining about this week?",
  "Did sentiment change after the last release?",
  "What do users love about the app?",
  "Show me recent bug reports",
  "What are the main performance issues?",
  "Are people happy with the new features?"
];

function QueryInterface() {
  const [question, setQuestion] = useState('');
  const [response, setResponse] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const askQuestion = async (queryText) => {
    const textToAsk = queryText || question;
    
    if (!textToAsk.trim()) {
      setError('Please enter a question');
      return;
    }

    setLoading(true);
    setError(null);
    setResponse(null);

    try {
      const result = await axios.post(`${API_URL}/query`, {
        question: textToAsk
      });
      setResponse(result.data);
      if (queryText) {
        setQuestion(queryText);
      }
    } catch (err) {
      setError('Failed to process your question. Please try again.');
      console.error('Error asking question:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    askQuestion();
  };

  const handleExampleClick = (exampleQuestion) => {
    setQuestion(exampleQuestion);
    askQuestion(exampleQuestion);
  };

  const formatDate = (dateString) => {
    const date = new Date(dateString);
    return date.toLocaleDateString() + ' ' + date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  };

  return (
    <div>
      <div className="card">
        <h2>🤖 Ask Questions About Your Feedback</h2>
        <p style={{ color: '#666', marginBottom: '1.5rem' }}>
          Ask natural language questions to quickly understand your feedback data
        </p>

        <form onSubmit={handleSubmit}>
          <div style={{ display: 'flex', gap: '1rem', marginBottom: '1rem' }}>
            <input
              type="text"
              value={question}
              onChange={(e) => setQuestion(e.target.value)}
              placeholder="e.g., What are users complaining about this week?"
              style={{
                flex: 1,
                padding: '1rem',
                fontSize: '1rem',
                border: '2px solid #e8ecf1',
                borderRadius: '8px'
              }}
            />
            <button
              type="submit"
              className="button"
              disabled={loading || !question.trim()}
            >
              {loading ? '🤔 Thinking...' : '💬 Ask'}
            </button>
          </div>
        </form>

        {error && <div className="error">{error}</div>}

        <div>
          <div style={{ fontSize: '0.9rem', color: '#666', marginBottom: '0.75rem' }}>
            Try these examples:
          </div>
          <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.5rem' }}>
            {EXAMPLE_QUESTIONS.map((example, idx) => (
              <button
                key={idx}
                onClick={() => handleExampleClick(example)}
                style={{
                  padding: '0.5rem 1rem',
                  border: '1px solid #e8ecf1',
                  background: 'white',
                  borderRadius: '20px',
                  fontSize: '0.85rem',
                  cursor: 'pointer',
                  transition: 'all 0.2s'
                }}
                onMouseEnter={(e) => {
                  e.target.style.background = '#f5f7fa';
                  e.target.style.borderColor = '#667eea';
                }}
                onMouseLeave={(e) => {
                  e.target.style.background = 'white';
                  e.target.style.borderColor = '#e8ecf1';
                }}
              >
                {example}
              </button>
            ))}
          </div>
        </div>
      </div>

      {response && (
        <>
          <div className="card">
            <h2>Answer</h2>
            <div className="summary-text" style={{ marginTop: '1rem' }}>
              {response.answer}
            </div>
            
            <div style={{ 
              marginTop: '1.5rem', 
              padding: '1rem', 
              background: '#f8f9fa', 
              borderRadius: '8px',
              fontSize: '0.9rem'
            }}>
              <strong>Query Analysis:</strong>
              <div style={{ marginTop: '0.5rem', display: 'flex', flexWrap: 'wrap', gap: '0.5rem' }}>
                <span style={{ padding: '0.25rem 0.75rem', background: 'white', borderRadius: '12px' }}>
                  Type: {response.query_type.replace('_', ' ')}
                </span>
                {response.filters_applied.days && (
                  <span style={{ padding: '0.25rem 0.75rem', background: 'white', borderRadius: '12px' }}>
                    Last {response.filters_applied.days} days
                  </span>
                )}
                {response.filters_applied.sentiment && (
                  <span style={{ padding: '0.25rem 0.75rem', background: 'white', borderRadius: '12px' }}>
                    Sentiment: {response.filters_applied.sentiment}
                  </span>
                )}
                {response.filters_applied.category && (
                  <span style={{ padding: '0.25rem 0.75rem', background: 'white', borderRadius: '12px' }}>
                    Category: {response.filters_applied.category}
                  </span>
                )}
              </div>
            </div>
          </div>

          {response.relevant_feedback && response.relevant_feedback.length > 0 && (
            <div className="card">
              <h2>Related Feedback ({response.relevant_feedback.length} items)</h2>
              <div style={{ marginTop: '1rem' }}>
                {response.relevant_feedback.map((item) => (
                  <div key={item.id} className="feedback-item">
                    <div className="feedback-header">
                      <div className="feedback-meta">
                        <span className="source-badge">{item.source.replace('_', ' ')}</span>
                        <span style={{ fontSize: '0.85rem', color: '#888' }}>
                          {formatDate(item.created_at)}
                        </span>
                      </div>
                      <span className={`sentiment-badge sentiment-${item.sentiment}`}>
                        {item.sentiment}
                      </span>
                    </div>
                    <div className="feedback-content">{item.content}</div>
                    {item.category && (
                      <div style={{ marginTop: '0.5rem', fontSize: '0.85rem', color: '#888' }}>
                        Category: {item.category.replace('_', ' ')}
                      </div>
                    )}
                  </div>
                ))}
              </div>
            </div>
          )}
        </>
      )}

      {!response && !loading && (
        <div className="card" style={{ textAlign: 'center', padding: '3rem' }}>
          <div style={{ fontSize: '3rem', marginBottom: '1rem' }}>💭</div>
          <h3>Ask me anything about your feedback</h3>
          <p style={{ color: '#666', marginTop: '0.5rem' }}>
            I can help you understand complaints, track sentiment changes, identify trends, and more
          </p>
        </div>
      )}
    </div>
  );
}

export default QueryInterface;
