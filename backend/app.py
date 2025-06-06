from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os
import requests
from datetime import datetime
from dateutil import parser
import openai
from textblob import TextBlob

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# Configure API keys
NEWS_API_KEY = os.getenv('NEWS_API_KEY')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

if OPENAI_API_KEY:
    openai.api_key = OPENAI_API_KEY

# News API endpoint
NEWS_API_URL = "https://newsapi.org/v2/top-headlines"

def format_date(date_str):
    try:
        dt = parser.parse(date_str)
        return dt.strftime("%B %d, %Y")
    except:
        return date_str

@app.route('/news')
def get_news():
    try:
        category = request.args.get('category', 'general')
        
        params = {
            'apiKey': NEWS_API_KEY,
            'category': category,
            'language': 'en',
            'pageSize': 10
        }
        
        response = requests.get(NEWS_API_URL, params=params)
        data = response.json()
        
        if response.status_code != 200:
            return jsonify({'error': data.get('message', 'Failed to fetch news')}), 400
        
        articles = []
        for article in data['articles']:
            articles.append({
                'title': article.get('title', ''),
                'description': article.get('description', ''),
                'url': article.get('url', ''),
                'imageUrl': article.get('urlToImage', ''),
                'source': article.get('source', {}).get('name', ''),
                'publishedAt': format_date(article.get('publishedAt', '')),
                'content': article.get('content', '')
            })
        
        return jsonify({'articles': articles})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def get_summary_using_openai(text):
    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that summarizes news articles concisely."},
                {"role": "user", "content": f"Please summarize this news article in 2-3 sentences:\n\n{text}"}
            ],
            max_tokens=150
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return None

def get_summary_using_textblob(text):
    try:
        blob = TextBlob(text)
        # Get 2-3 most important sentences
        sentences = blob.sentences
        if len(sentences) <= 3:
            return text
        
        # Simple extractive summarization
        sentence_scores = [(str(sentence), sentence.sentiment.polarity + sentence.sentiment.subjectivity) 
                         for sentence in sentences]
        sorted_sentences = sorted(sentence_scores, key=lambda x: x[1], reverse=True)
        summary = ' '.join(sentence[0] for sentence in sorted_sentences[:3])
        return summary
    except:
        return "Unable to generate summary."

@app.route('/summarize', methods=['POST'])
def summarize_article():
    try:
        data = request.json
        text = data.get('content', '')
        
        if not text:
            return jsonify({'error': 'No content provided'}), 400
        
        # Try OpenAI first if API key is available
        if OPENAI_API_KEY:
            summary = get_summary_using_openai(text)
            if summary:
                return jsonify({'summary': summary})
        
        # Fallback to TextBlob
        summary = get_summary_using_textblob(text)
        return jsonify({'summary': summary})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    if not NEWS_API_KEY:
        print("Warning: NEWS_API_KEY not found in environment variables")
    if not OPENAI_API_KEY:
        print("Warning: OPENAI_API_KEY not found in environment variables. Will use TextBlob for summarization.")
    
    app.run(debug=True, port=5000) 