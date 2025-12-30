# Feedback Explorer

An AI-powered internal tool for analyzing customer feedback from multiple sources (support tickets, surveys, app store reviews).

## Features

- **Ask Questions** (NEW!): Natural language interface to query feedback - ask "What are users complaining about this week?" and get instant AI-powered answers
- **Dashboard**: Overview of feedback metrics with sentiment trends and distribution charts
- **Explore Feedback**: Filter and browse feedback by time range, sentiment, and category
- **AI Analysis**: Generate intelligent summaries using a mock AI service that identifies key themes, concerns, and recommendations

## Tech Stack

- **Backend**: Python, FastAPI, PostgreSQL
- **Frontend**: React, Recharts (for visualizations)
- **Infrastructure**: Docker Compose

## Project Structure

```
.
├── docker-compose.yml
├── init.sql
├── backend/
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── main.py
│   └── ai_service.py
└── frontend/
    ├── Dockerfile
    ├── package.json
    ├── public/
    │   └── index.html
    └── src/
        ├── App.js
        ├── App.css
        ├── index.js
        └── components/
            ├── Dashboard.js
            ├── FeedbackList.js
            └── AnalysisSummary.js
```

## How to Run

### Prerequisites
- Docker and Docker Compose installed
- Ports 3000, 5432, and 8000 available

### Quick Start

1. Clone or create the project structure as shown above

2. Start all services:
```bash
docker-compose up --build
```

3. Wait for all services to start (takes ~30-60 seconds):
   - PostgreSQL database initializes with seed data
   - Backend API starts on http://localhost:8000
   - Frontend app starts on http://localhost:3000

4. Open your browser to http://localhost:3000

### Verify Services

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000 (check http://localhost:8000/docs for API documentation)
- **Database**: localhost:5432 (credentials: admin/password)

### Stop Services

```bash
docker-compose down
```

To remove volumes (database data):
```bash
docker-compose down -v
```

## Usage

### Ask Questions Tab (NEW!)
Natural language query interface:
- Type questions in plain English like "What are users complaining about this week?"
- Or click example questions to get started
- Get instant AI-powered answers with:
  - Detailed analysis of the query
  - Top issues, themes, or sentiment changes
  - Related feedback items for context
  - Smart filtering based on your question

Example questions:
- "What are users complaining about this week?"
- "Did sentiment change after the last release?"
- "What do users love about the app?"
- "Show me recent bug reports"
- "What are the main performance issues?"

### Dashboard Tab
View high-level metrics including:
- Total feedback count
- Recent feedback (last 7 days)
- Sentiment trends over time
- Sentiment distribution pie chart
- Feedback sources breakdown

### Explore Feedback Tab
Browse and filter feedback:
- Filter by time range (24 hours, 7 days, 30 days, all time)
- Filter by sentiment (positive, negative, mixed, neutral)
- Filter by category (bugs, features, performance, etc.)
- View detailed feedback with metadata

### AI Analysis Tab
Generate intelligent summaries:
1. Select time range and optional sentiment filter
2. Click "Generate AI Summary"
3. View comprehensive analysis including:
   - Overall sentiment assessment
   - Key themes and categories
   - Top concerns and complaints
   - Positive highlights
   - Actionable recommendations
   - Alert for recent negative spikes

## API Endpoints

- `GET /feedback` - List feedback with filters
- `POST /query` - Natural language question answering (NEW!)
- `POST /analyze/summary` - Generate AI summary
- `GET /analyze/trends` - Get sentiment trends
- `GET /stats/overview` - Get overview statistics
- `GET /categories` - Get all categories

Full API documentation available at http://localhost:8000/docs when running.

## Mock AI Service

The AI service (`ai_service.py`) simulates an ML model for demonstration purposes:
- **Natural language understanding**: Parses user questions to extract intent, time ranges, sentiment filters, and keywords
- **Sentiment analysis**: Keyword-based classification
- **Summary generation**: Pattern-based analysis of sentiment, categories, and trends
- **Topic extraction**: Common topic detection
- **Conversational answers**: Generates natural language responses tailored to the question type

In a production environment, this would integrate with real ML models (OpenAI, Claude, Hugging Face, etc.).

## Sample Data

The database is seeded with 30 realistic feedback items covering various scenarios:
- Different sources (app store, support tickets, surveys)
- Various sentiments (positive, negative, mixed, neutral)
- Multiple categories (bugs, features, performance, UX, etc.)
- Distributed across the last 6 days

## Design Decisions

1. **Docker Compose**: Ensures consistent environment across machines with zero manual setup
2. **FastAPI**: Modern, fast Python framework with automatic API documentation
3. **React**: Component-based architecture for maintainable UI
4. **PostgreSQL**: Reliable, scalable database suitable for production
5. **Mock AI**: Demonstrates integration patterns without requiring API keys or external services
6. **Minimal Dependencies**: Only essential libraries to reduce complexity

## Future Enhancements

For a production version, consider:
- Real ML model integration (OpenAI, Claude, or custom models)
- User authentication and role-based access
- Export functionality (CSV, PDF reports)
- Email alerts for sentiment spikes
- Integration with ticketing systems (Zendesk, Intercom)
- Advanced NLP for topic modeling and entity extraction
- Caching layer (Redis) for performance
- Automated feedback ingestion pipelines
- A/B test impact analysis