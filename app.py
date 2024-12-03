from flask import Flask, request, jsonify, send_from_directory, render_template
from flask_cors import CORS
from datetime import datetime
import os
from dotenv import load_dotenv
import re
from collections import Counter

load_dotenv()

# Get the absolute path to the static directory
STATIC_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), 'static'))
print(f"Static directory path: {STATIC_DIR}")

app = Flask(__name__, static_folder=STATIC_DIR)
CORS(app)

# Enable debug mode
app.debug = True

TRENDING_HASHTAGS = {
    'instagram': ['#reels', '#trending', '#viral', '#instagram', '#follow'],
    'twitter': ['#trending', '#viral', '#follow', '#news', '#today'],
    'tiktok': ['#fyp', '#viral', '#trending', '#foryou', '#tiktok']
}

@app.route('/', methods=['GET'])
def index():
    try:
        static_file = os.path.join(STATIC_DIR, 'landing.html')
        print(f"Attempting to serve: {static_file}")
        if os.path.exists(static_file):
            print("File exists!")
            return send_from_directory(STATIC_DIR, 'landing.html')
        else:
            print("File not found!")
            return jsonify({"error": "Landing page not found"}), 404
    except Exception as e:
        print(f"Error serving landing page: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/tool')
def tool():
    try:
        return send_from_directory(STATIC_DIR, 'index.html')
    except Exception as e:
        print(f"Error serving tool page: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/static/<path:path>')
def serve_static(path):
    try:
        return send_from_directory(STATIC_DIR, path)
    except Exception as e:
        print(f"Error serving static file {path}: {str(e)}")
        return jsonify({"error": str(e)}), 404

@app.route('/api/analyze', methods=['POST'])
def analyze_content():
    try:
        data = request.json
        content = data.get('content', '')
        platform = data.get('platform', '').lower()
        
        analysis = {
            'content_score': analyze_content_quality(content),
            'hashtag_suggestions': get_hashtag_suggestions(content, platform),
            'engagement_prediction': calculate_engagement_score(content),
            'monetization_potential': estimate_monetization(content),
            'best_posting_times': get_optimal_posting_times(platform),
            'improvements': generate_improvements(content, platform),
            'viral_potential': calculate_viral_potential(content, platform)
        }
        
        return jsonify(analysis)
    
    except Exception as e:
        print(f"Error analyzing content: {str(e)}")
        return jsonify({'error': str(e)}), 500

def analyze_content_quality(content):
    try:
        score = 0
        
        # Length analysis (ideal length varies by platform)
        length = len(content)
        if 50 <= length <= 300:
            score += 25
        elif 300 < length <= 500:
            score += 15
        
        # Emoji presence (engagement booster)
        emoji_count = len(re.findall(r'[\U0001F300-\U0001F9FF]', content))
        score += min(emoji_count * 2, 10)
        
        # URL presence (monetization potential)
        if 'http' in content or 'www.' in content:
            score += 15
        
        # Hashtag quality
        hashtags = re.findall(r'#\w+', content)
        score += min(len(hashtags) * 5, 20)
        
        # Call to action presence
        cta_phrases = ['check out', 'visit', 'buy', 'follow', 'like', 'share', 'comment']
        if any(phrase in content.lower() for phrase in cta_phrases):
            score += 15
        
        return min(score, 100)
    
    except Exception as e:
        print(f"Error analyzing content quality: {str(e)}")
        return 0

def get_hashtag_suggestions(content, platform):
    try:
        existing_hashtags = set(re.findall(r'#\w+', content.lower()))
        platform_trends = TRENDING_HASHTAGS.get(platform, [])
        
        # Filter out already used hashtags
        suggestions = [tag for tag in platform_trends if tag.lower() not in existing_hashtags]
        
        # Add industry-specific hashtags based on content
        keywords = extract_keywords(content)
        for keyword in keywords:
            suggestions.append(f'#{keyword}')
        
        return suggestions[:5]
    
    except Exception as e:
        print(f"Error getting hashtag suggestions: {str(e)}")
        return []

def extract_keywords(content):
    try:
        # Simple keyword extraction
        words = re.findall(r'\w+', content.lower())
        # Remove common words
        stopwords = {'the', 'is', 'at', 'which', 'on', 'a', 'an', 'and', 'or', 'but'}
        keywords = [word for word in words if word not in stopwords and len(word) > 3]
        
        # Get most common words
        word_freq = Counter(keywords)
        return [word for word, _ in word_freq.most_common(3)]
    
    except Exception as e:
        print(f"Error extracting keywords: {str(e)}")
        return []

def calculate_engagement_score(content):
    try:
        score = analyze_content_quality(content) / 10
        return round(score, 1)
    
    except Exception as e:
        print(f"Error calculating engagement score: {str(e)}")
        return 0

def estimate_monetization(content):
    try:
        base_rate = 0.05  # Base rate per engagement
        engagement_score = calculate_engagement_score(content)
        
        # Factors that increase monetization potential
        multiplier = 1.0
        
        # Check for commercial intent
        commercial_keywords = ['buy', 'sale', 'discount', 'offer', 'deal', 'limited', 'exclusive']
        if any(keyword in content.lower() for keyword in commercial_keywords):
            multiplier *= 1.5
        
        # Check for links
        if 'http' in content or 'www.' in content:
            multiplier *= 1.3
        
        # Calculate potential reach based on content quality
        potential_reach = 1000 * (engagement_score / 10)
        
        estimated_earnings = base_rate * potential_reach * multiplier
        return round(estimated_earnings, 2)
    
    except Exception as e:
        print(f"Error estimating monetization: {str(e)}")
        return 0

def get_optimal_posting_times(platform):
    try:
        times = {
            'instagram': ['8:00', '12:00', '17:00', '21:00'],
            'twitter': ['9:00', '12:00', '15:00', '18:00'],
            'tiktok': ['11:00', '15:00', '19:00', '22:00']
        }
        return times.get(platform, ['12:00', '18:00'])
    
    except Exception as e:
        print(f"Error getting optimal posting times: {str(e)}")
        return []

def generate_improvements(content, platform):
    try:
        improvements = []
        
        # Length improvements
        length = len(content)
        if length < 50:
            improvements.append("Add more detail to increase engagement")
        elif length > 500:
            improvements.append("Content might be too long - consider breaking into multiple posts")
        
        # Hashtag improvements
        hashtags = re.findall(r'#\w+', content)
        if not hashtags:
            improvements.append("Add relevant hashtags for better visibility")
        elif len(hashtags) < 3:
            improvements.append("Add more trending hashtags to increase reach")
        
        # Platform-specific improvements
        if platform == 'instagram':
            if len(re.findall(r'[\U0001F300-\U0001F9FF]', content)) < 2:
                improvements.append("Add more emojis for better engagement")
        elif platform == 'twitter':
            if length > 280:
                improvements.append("Shorten content to fit Twitter's character limit")
        elif platform == 'tiktok':
            if not any(word in content.lower() for word in ['trend', 'challenge', 'duet']):
                improvements.append("Reference current trends or challenges for better visibility")
        
        return improvements
    
    except Exception as e:
        print(f"Error generating improvements: {str(e)}")
        return []

def calculate_viral_potential(content, platform):
    try:
        score = 0
        
        # Check for viral indicators
        viral_keywords = ['trending', 'viral', 'challenge', 'breaking', 'exclusive']
        score += sum(5 for keyword in viral_keywords if keyword in content.lower())
        
        # Platform-specific viral factors
        if platform == 'tiktok':
            if any(word in content.lower() for word in ['duet', 'challenge']):
                score += 20
        elif platform == 'twitter':
            if '#' in content and len(content) < 200:
                score += 15
        elif platform == 'instagram':
            if '#reels' in content.lower():
                score += 15
        
        # Engagement factors
        engagement_score = calculate_engagement_score(content)
        score += engagement_score * 2
        
        return min(score, 100)
    
    except Exception as e:
        print(f"Error calculating viral potential: {str(e)}")
        return 0

if __name__ == '__main__':
    app.run(debug=True, port=5000)
