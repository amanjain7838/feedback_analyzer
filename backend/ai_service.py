import random
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
