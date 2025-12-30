from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import psycopg2
from psycopg2.extras import RealDictCursor
import os
from datetime import datetime, timedelta
from ai_service import AIService

app = FastAPI(title="Feedback Analysis API")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize AI service
ai_service = AIService()

# Database connection
def get_db():
    return psycopg2.connect(
        os.getenv("DATABASE_URL", "postgresql://admin:password@db:5433/feedback"),
        cursor_factory=RealDictCursor
    )

# Models
class Feedback(BaseModel):
    id: int
    source: str
    content: str
    created_at: datetime
    sentiment: Optional[str]
    category: Optional[str]

class SummaryRequest(BaseModel):
    time_range: Optional[str] = "week"  # day, week, month, all
    sentiment: Optional[str] = None
    category: Optional[str] = None

class SummaryResponse(BaseModel):
    summary: str
    total_count: int
    sentiment_breakdown: dict
    top_categories: List[dict]
    time_range: str

class TrendResponse(BaseModel):
    period: str
    positive: int
    negative: int
    mixed: int
    neutral: int

# Endpoints
@app.get("/")
def root():
    return {"message": "Feedback Analysis API", "status": "running"}

@app.get("/feedback", response_model=List[Feedback])
def get_feedback(
    limit: int = 50,
    offset: int = 0,
    sentiment: Optional[str] = None,
    category: Optional[str] = None,
    days: Optional[int] = None
):
    """Get feedback with optional filters"""
    conn = get_db()
    cursor = conn.cursor()
    
    query = "SELECT * FROM feedback WHERE 1=1"
    params = []
    
    if sentiment:
        query += " AND sentiment = %s"
        params.append(sentiment)
    
    if category:
        query += " AND category = %s"
        params.append(category)
    
    if days:
        query += " AND created_at >= %s"
        params.append(datetime.now() - timedelta(days=days))
    
    query += " ORDER BY created_at DESC LIMIT %s OFFSET %s"
    params.extend([limit, offset])
    
    cursor.execute(query, params)
    results = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    return results

@app.post("/analyze/summary", response_model=SummaryResponse)
def analyze_summary(request: SummaryRequest):
    """Generate AI-powered summary of feedback"""
    conn = get_db()
    cursor = conn.cursor()
    
    # Build query based on filters
    query = "SELECT * FROM feedback WHERE 1=1"
    params = []
    
    # Time range filter
    time_map = {
        "day": 1,
        "week": 7,
        "month": 30,
        "all": None
    }
    
    days = time_map.get(request.time_range)
    if days:
        query += " AND created_at >= %s"
        params.append(datetime.now() - timedelta(days=days))
    
    if request.sentiment:
        query += " AND sentiment = %s"
        params.append(request.sentiment)
    
    if request.category:
        query += " AND category = %s"
        params.append(request.category)
    
    query += " ORDER BY created_at DESC"
    
    cursor.execute(query, params)
    feedback_items = cursor.fetchall()
    
    # Get sentiment breakdown
    sentiment_query = """
        SELECT sentiment, COUNT(*) as count 
        FROM feedback 
        WHERE created_at >= %s
        GROUP BY sentiment
    """
    cursor.execute(sentiment_query, [datetime.now() - timedelta(days=days or 365)])
    sentiment_data = cursor.fetchall()
    sentiment_breakdown = {row['sentiment']: row['count'] for row in sentiment_data}
    
    # Get top categories
    category_query = """
        SELECT category, COUNT(*) as count 
        FROM feedback 
        WHERE created_at >= %s
        GROUP BY category 
        ORDER BY count DESC 
        LIMIT 5
    """
    cursor.execute(category_query, [datetime.now() - timedelta(days=days or 365)])
    top_categories = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    # Generate AI summary
    summary = ai_service.generate_summary(feedback_items, request.time_range)
    
    return SummaryResponse(
        summary=summary,
        total_count=len(feedback_items),
        sentiment_breakdown=sentiment_breakdown,
        top_categories=[dict(row) for row in top_categories],
        time_range=request.time_range
    )

@app.get("/analyze/trends", response_model=List[TrendResponse])
def analyze_trends(days: int = 14):
    """Get sentiment trends over time"""
    conn = get_db()
    cursor = conn.cursor()
    
    query = """
        SELECT 
            DATE(created_at) as period,
            sentiment,
            COUNT(*) as count
        FROM feedback
        WHERE created_at >= %s
        GROUP BY DATE(created_at), sentiment
        ORDER BY period DESC
    """
    
    cursor.execute(query, [datetime.now() - timedelta(days=days)])
    results = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    # Organize by period
    trends_dict = {}
    for row in results:
        period = row['period'].isoformat()
        if period not in trends_dict:
            trends_dict[period] = {
                'period': period,
                'positive': 0,
                'negative': 0,
                'mixed': 0,
                'neutral': 0
            }
        
        sentiment = row['sentiment'] or 'neutral'
        trends_dict[period][sentiment] = row['count']
    
    return list(trends_dict.values())

@app.get("/stats/overview")
def get_overview():
    """Get overview statistics"""
    conn = get_db()
    cursor = conn.cursor()
    
    # Total feedback
    cursor.execute("SELECT COUNT(*) as total FROM feedback")
    total = cursor.fetchone()['total']
    
    # Recent feedback (last 7 days)
    cursor.execute("""
        SELECT COUNT(*) as recent 
        FROM feedback 
        WHERE created_at >= %s
    """, [datetime.now() - timedelta(days=7)])
    recent = cursor.fetchone()['recent']
    
    # Sentiment distribution (last 7 days)
    cursor.execute("""
        SELECT sentiment, COUNT(*) as count 
        FROM feedback 
        WHERE created_at >= %s
        GROUP BY sentiment
    """, [datetime.now() - timedelta(days=7)])
    sentiment_dist = {row['sentiment']: row['count'] for row in cursor.fetchall()}
    
    # Top sources
    cursor.execute("""
        SELECT source, COUNT(*) as count 
        FROM feedback 
        GROUP BY source 
        ORDER BY count DESC
    """)
    sources = [dict(row) for row in cursor.fetchall()]
    
    cursor.close()
    conn.close()
    
    return {
        "total_feedback": total,
        "recent_feedback": recent,
        "sentiment_distribution": sentiment_dist,
        "sources": sources
    }

@app.get("/categories")
def get_categories():
    """Get all unique categories"""
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute("SELECT DISTINCT category FROM feedback WHERE category IS NOT NULL ORDER BY category")
    categories = [row['category'] for row in cursor.fetchall()]
    
    cursor.close()
    conn.close()
    
    return {"categories": categories}

class QueryRequest(BaseModel):
    question: str

class QueryResponse(BaseModel):
    answer: str
    relevant_feedback: List[Feedback]
    query_type: str
    filters_applied: dict

@app.post("/query", response_model=QueryResponse)
def natural_language_query(request: QueryRequest):
    """Answer natural language questions about feedback"""
    conn = get_db()
    cursor = conn.cursor()
    
    # Use AI service to parse the question and determine filters
    query_analysis = ai_service.parse_natural_query(request.question)
    
    # Build SQL query based on parsed intent
    query = "SELECT * FROM feedback WHERE 1=1"
    params = []
    
    # Apply time filters
    if query_analysis.get('days'):
        query += " AND created_at >= %s"
        params.append(datetime.now() - timedelta(days=query_analysis['days']))
    
    # Apply sentiment filters
    if query_analysis.get('sentiment'):
        query += " AND sentiment = %s"
        params.append(query_analysis['sentiment'])
    
    # Apply category filters
    if query_analysis.get('category'):
        query += " AND category = %s"
        params.append(query_analysis['category'])
    
    # Apply keyword search
    if query_analysis.get('keywords'):
        keyword_conditions = " OR ".join(["content ILIKE %s"] * len(query_analysis['keywords']))
        query += f" AND ({keyword_conditions})"
        params.extend([f"%{kw}%" for kw in query_analysis['keywords']])
    
    query += " ORDER BY created_at DESC LIMIT 50"
    
    cursor.execute(query, params)
    feedback_items = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    # Generate natural language answer
    answer = ai_service.answer_question(
        request.question, 
        feedback_items, 
        query_analysis
    )
    
    return QueryResponse(
        answer=answer,
        relevant_feedback=feedback_items[:10],  # Return top 10 most relevant
        query_type=query_analysis.get('type', 'general'),
        filters_applied=query_analysis
    )