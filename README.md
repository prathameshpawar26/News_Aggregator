# News Aggregator with AI Summaries

A full-stack application that aggregates news articles and provides AI-generated summaries.

## Project Structure
```
news_app/
├── frontend/          # React frontend
└── backend/           # Flask backend
```

## Setup Instructions

### Backend Setup
1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/Scripts/activate  # On Windows
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file with your API keys:
   ```
   NEWS_API_KEY=your_news_api_key
   OPENAI_API_KEY=your_openai_api_key
   ```

5. Run the Flask server:
   ```bash
   python app.py
   ```

### Frontend Setup
1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm start
   ```

## Features
- Browse news articles by category
- View article details including title, description, and image
- Generate AI-powered summaries of articles
- Clean and responsive UI using TailwindCSS

## Technologies Used
- Frontend: React, Axios, TailwindCSS
- Backend: Flask, OpenAI API, NewsAPI 