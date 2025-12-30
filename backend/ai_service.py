import random
import string
from typing import List, Dict
from collections import Counter

class AIService:
    """Mock AI service for feedback analysis"""
    
    def generate_summary(self, feedback_items: List[Dict], time_range: str) -> str:
        """Generate a mock AI summary of feedback"""
        
        if not feedback_items:
            return f"No feedback found for the selected {time_range} period."
        
        # Analyze sentiment distribution
        sentiments = [item.get('sentiment', 'neutral') for item in feedback_items]
        sentiment_counts = Counter(sentiments)
        
        # Analyze categories
        categories = [item.get('category', 'general') for item in feedback_items]
        category_counts = Counter(categories)
        top_categories = category_counts.most_common(3)
        
        # Count negative issues
        negative_items = [item for item in feedback_items if item.get('sentiment') == 'negative']
        
        # Build summary based on patterns
        summary_parts = []
        
        # Opening statement
        total = len(feedback_items)
        summary_parts.append(f"Analysis of {total} feedback items from the past {time_range}:")
        
        # Sentiment overview
        positive_pct = (sentiment_counts.get('positive', 0) / total) * 100
        negative_pct = (sentiment_counts.get('negative', 0) / total) * 100
        mixed_pct = (sentiment_counts.get('mixed', 0) / total) * 100
        
        if positive_pct > 50:
            summary_parts.append(f"\n\n✓ Overall sentiment is positive ({positive_pct:.0f}% positive feedback).")
        elif negative_pct > 40:
            summary_parts.append(f"\n\n⚠ Sentiment is concerning with {negative_pct:.0f}% negative feedback.")
        else:
            summary_parts.append(f"\n\n→ Mixed sentiment: {positive_pct:.0f}% positive, {negative_pct:.0f}% negative, {mixed_pct:.0f}% mixed.")
        
        # Key themes
        if top_categories:
            summary_parts.append(f"\n\nKey themes:")
            for cat, count in top_categories:
                pct = (count / total) * 100
                summary_parts.append(f"\n• {cat.replace('_', ' ').title()}: {count} mentions ({pct:.0f}%)")
        
        # Critical issues
        if negative_items:
            critical_categories = Counter([item.get('category', 'general') for item in negative_items])
            top_issues = critical_categories.most_common(3)
            
            summary_parts.append(f"\n\nTop concerns:")
            for issue, count in top_issues:
                summary_parts.append(f"\n• {issue.replace('_', ' ').title()}: {count} complaints")
        
        # Positive highlights
        positive_items = [item for item in feedback_items if item.get('sentiment') == 'positive']
        if positive_items:
            positive_categories = Counter([item.get('category', 'general') for item in positive_items])
            top_positive = positive_categories.most_common(2)
            
            summary_parts.append(f"\n\nWhat users love:")
            for feature, count in top_positive:
                summary_parts.append(f"\n• {feature.replace('_', ' ').title()}: {count} positive mentions")
        
        # Recommendations
        summary_parts.append("\n\nRecommendations:")
        
        if 'bugs' in [cat for cat, _ in top_categories]:
            summary_parts.append("\n• High priority: Address reported bugs and stability issues")
        
        if 'performance' in [cat for cat, _ in top_categories]:
            summary_parts.append("\n• Investigate performance concerns (speed, battery, memory)")
        
        if negative_pct > 30:
            summary_parts.append("\n• Consider immediate user outreach to understand pain points")
        
        if 'feature_request' in [cat for cat, _ in top_categories]:
            summary_parts.append("\n• Review feature requests for roadmap planning")
        
        # Recent trends
        recent_items = sorted(feedback_items, key=lambda x: x['created_at'], reverse=True)[:10]
        recent_negative = sum(1 for item in recent_items if item.get('sentiment') == 'negative')
        
        if recent_negative >= 5:
            summary_parts.append("\n\n⚠ Alert: Recent spike in negative feedback detected in last 10 submissions.")
        
        return "".join(summary_parts)
    
    def classify_sentiment(self, text: str) -> str:
        """Mock sentiment classification"""
        # In real implementation, this would call an ML model
        negative_keywords = ['crash', 'bug', 'broken', 'terrible', 'awful', 'frustrat', 'annoying', 'expensive']
        positive_keywords = ['love', 'great', 'awesome', 'perfect', 'excellent', 'fantastic', 'smooth']
        
        text_lower = text.lower()
        has_negative = any(kw in text_lower for kw in negative_keywords)
        has_positive = any(kw in text_lower for kw in positive_keywords)
        
        if has_positive and has_negative:
            return 'mixed'
        elif has_positive:
            return 'positive'
        elif has_negative:
            return 'negative'
        else:
            return 'neutral'
    
    def extract_topics(self, feedback_items: List[Dict]) -> List[str]:
        """Mock topic extraction"""
        # In real implementation, this would use NLP/LDA
        all_text = " ".join([item['content'] for item in feedback_items])
        
        common_topics = {
            'performance': ['slow', 'fast', 'speed', 'lag', 'freeze'],
            'bugs': ['crash', 'bug', 'error', 'broken', 'issue'],
            'ui': ['design', 'interface', 'ui', 'layout', 'button'],
            'features': ['feature', 'add', 'need', 'want', 'missing'],
            'pricing': ['price', 'expensive', 'cost', 'subscription', 'cheap']
        }
        
        found_topics = []
        for topic, keywords in common_topics.items():
            if any(kw in all_text.lower() for kw in keywords):
                found_topics.append(topic)
        
        return found_topics[:5]
    
    def parse_natural_query(self, question: str) -> Dict:
        """Parse natural language query into structured filters"""
        question_lower = question.lower()
        analysis = {
            'type': 'general',
            'days': None,
            'sentiment': None,
            'category': None,
            'keywords': []
        }
        
        # Detect time range
        time_patterns = {
            'today': 1,
            'yesterday': 1,
            'this week': 7,
            'last week': 7,
            'past week': 7,
            'this month': 30,
            'last month': 30,
            'past month': 30,
        }
        
        for pattern, days in time_patterns.items():
            if pattern in question_lower:
                analysis['days'] = days
                break
        
        # If asking about "after release" or "recent", use 7 days
        if any(word in question_lower for word in ['after', 'since', 'recent', 'lately']):
            if not analysis['days']:
                analysis['days'] = 7
        
        # Detect sentiment
        if any(word in question_lower for word in ['complain', 'complaint', 'complaints', 'complaining', 'negative', 'issue', 'problem', 'bad']):
            analysis['sentiment'] = 'negative'
            analysis['type'] = 'complaints'
        elif any(word in question_lower for word in ['positive', 'good', 'love', 'praise', 'happy', 'like']):
            analysis['sentiment'] = 'positive'
            analysis['type'] = 'positive_feedback'
        
        # Detect sentiment change questions
        if any(word in question_lower for word in ['change', 'shift', 'trend', 'different']):
            analysis['type'] = 'trend_analysis'
        
        # Detect specific categories from question
        category_keywords = {
            'bugs': ['bug', 'crash', 'broken', 'error'],
            'performance': ['slow', 'fast', 'performance', 'speed', 'battery'],
            'features': ['feature', 'functionality'],
            'ui': ['ui', 'design', 'interface', 'layout'],
            'pricing': ['price', 'cost', 'expensive', 'subscription'],
            'sync': ['sync', 'syncing', 'synchroniz'],
            'search': ['search', 'find', 'finding'],
        }
        
        for category, keywords in category_keywords.items():
            if any(kw in question_lower for kw in keywords):
                analysis['category'] = category
                break
        
        # Extract potential search keywords (remove common words)
        stop_words = {'what', 'are', 'is', 'the', 'about', 'users', 'user', 'people', 
                      'saying', 'this', 'last', 'week', 'month', 'day', 'after', 'before',
                      'did', 'sentiment', 'change', 'can', 'i', 'quickly',
                      'explore', 'feedback', 'without', 'reading', 'hundreds', 'entries'}
        
        words = question_lower.split()
        # Remove punctuation from words and filter
        keywords = [w.strip(string.punctuation) for w in words if w.strip(string.punctuation) not in stop_words and len(w.strip(string.punctuation)) > 3]
        # Only use keywords if no clear sentiment was detected
        if analysis['sentiment']:
            analysis['keywords'] = []  # Skip keywords when sentiment is already clear
        else:
            analysis['keywords'] = keywords[:3]  # Limit to top 3
        
        return analysis
    
    def answer_question(self, question: str, feedback_items: List[Dict], query_analysis: Dict) -> str:
        """Generate natural language answer to user question"""
        
        if not feedback_items:
            return f"I couldn't find any feedback matching your query. Try adjusting your time range or being more specific."
        
        question_lower = question.lower()
        answer_parts = []
        
        # Determine query type and generate appropriate answer
        if query_analysis['type'] == 'complaints':
            # Answer "what are users complaining about"
            negative_items = [item for item in feedback_items if item.get('sentiment') == 'negative']
            
            if not negative_items:
                return f"Good news! I found {len(feedback_items)} feedback items in this period, but none are negative complaints."
            
            categories = Counter([item.get('category', 'general') for item in negative_items])
            top_complaints = categories.most_common(5)
            
            time_str = f"this week" if query_analysis.get('days') == 7 else f"the last {query_analysis.get('days', 30)} days"
            
            answer_parts.append(f"Based on {len(negative_items)} complaints from {time_str}:\n")
            answer_parts.append(f"\n**Top Issues:**")
            
            for category, count in top_complaints:
                pct = (count / len(negative_items)) * 100
                answer_parts.append(f"\n• **{category.replace('_', ' ').title()}**: {count} complaints ({pct:.0f}%)")
                
                # Add example
                example = next((item for item in negative_items if item.get('category') == category), None)
                if example:
                    excerpt = example['content'][:150] + "..." if len(example['content']) > 150 else example['content']
                    answer_parts.append(f"\n  Example: \"{excerpt}\"")
            
            # Add urgency assessment
            if len(negative_items) > len(feedback_items) * 0.4:
                answer_parts.append(f"\n\n⚠️ **Alert**: {(len(negative_items)/len(feedback_items)*100):.0f}% of recent feedback is negative. Consider immediate action.")
        
        elif query_analysis['type'] == 'trend_analysis':
            # Answer "did sentiment change"
            answer_parts.append(f"**Sentiment Analysis:**\n")
            
            sentiments = Counter([item.get('sentiment', 'neutral') for item in feedback_items])
            total = len(feedback_items)
            
            answer_parts.append(f"\nOut of {total} feedback items:")
            for sentiment in ['positive', 'negative', 'mixed', 'neutral']:
                count = sentiments.get(sentiment, 0)
                pct = (count / total) * 100 if total > 0 else 0
                emoji = {'positive': '✓', 'negative': '✗', 'mixed': '~', 'neutral': '○'}[sentiment]
                answer_parts.append(f"\n{emoji} {sentiment.title()}: {count} ({pct:.0f}%)")
            
            # Compare with historical if possible
            answer_parts.append(f"\n\n**Key Changes:**")
            
            # Split into recent vs older
            sorted_items = sorted(feedback_items, key=lambda x: x['created_at'], reverse=True)
            midpoint = len(sorted_items) // 2
            recent = sorted_items[:midpoint]
            older = sorted_items[midpoint:]
            
            recent_neg_pct = sum(1 for item in recent if item.get('sentiment') == 'negative') / len(recent) * 100 if recent else 0
            older_neg_pct = sum(1 for item in older if item.get('sentiment') == 'negative') / len(older) * 100 if older else 0
            
            change = recent_neg_pct - older_neg_pct
            
            if abs(change) > 10:
                direction = "increased" if change > 0 else "decreased"
                answer_parts.append(f"\n• Negative sentiment has {direction} by {abs(change):.0f}% in recent days")
            else:
                answer_parts.append(f"\n• Sentiment has remained relatively stable")
            
            # Identify emerging themes
            recent_categories = Counter([item.get('category') for item in recent])
            older_categories = Counter([item.get('category') for item in older])
            
            for category in recent_categories:
                recent_pct = recent_categories[category] / len(recent) * 100 if recent else 0
                older_pct = older_categories.get(category, 0) / len(older) * 100 if older else 0
                
                if recent_pct - older_pct > 15:
                    answer_parts.append(f"\n• **Spike in '{category}' mentions** (up {recent_pct - older_pct:.0f}%)")
        
        elif query_analysis['type'] == 'positive_feedback':
            # Answer "what do users love"
            positive_items = [item for item in feedback_items if item.get('sentiment') == 'positive']
            
            if not positive_items:
                return f"I found {len(feedback_items)} feedback items, but none are strongly positive. Users may be having a neutral experience."
            
            categories = Counter([item.get('category', 'general') for item in positive_items])
            top_positive = categories.most_common(5)
            
            answer_parts.append(f"**What users love** (based on {len(positive_items)} positive mentions):\n")
            
            for category, count in top_positive:
                pct = (count / len(positive_items)) * 100
                answer_parts.append(f"\n• **{category.replace('_', ' ').title()}**: {count} positive mentions ({pct:.0f}%)")
                
                # Add example
                example = next((item for item in positive_items if item.get('category') == category), None)
                if example:
                    excerpt = example['content'][:150] + "..." if len(example['content']) > 150 else example['content']
                    answer_parts.append(f"\n  \"{excerpt}\"")
        
        else:
            # General exploration answer
            answer_parts.append(f"**Quick Overview:**\n")
            answer_parts.append(f"\nFound {len(feedback_items)} feedback items")
            
            if query_analysis.get('days'):
                answer_parts.append(f" from the last {query_analysis['days']} days")
            
            answer_parts.append(".\n")
            
            # Sentiment breakdown
            sentiments = Counter([item.get('sentiment', 'neutral') for item in feedback_items])
            answer_parts.append(f"\n**Sentiment Breakdown:**")
            for sentiment, count in sentiments.most_common():
                pct = (count / len(feedback_items)) * 100
                answer_parts.append(f"\n• {sentiment.title()}: {count} ({pct:.0f}%)")
            
            # Top categories
            categories = Counter([item.get('category', 'general') for item in feedback_items])
            answer_parts.append(f"\n\n**Top Themes:**")
            for category, count in categories.most_common(3):
                answer_parts.append(f"\n• {category.replace('_', ' ').title()}: {count} mentions")
        
        return "".join(answer_parts)