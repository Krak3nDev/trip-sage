# TripSage

TripSage is an AI-powered travel recommendation API that suggests interesting places based on user preferences. It leverages OpenAI's GPT models to generate personalized travel recommendations.

## Features

- Generate personalized travel recommendations based on user queries
- Exclude specific places from recommendations
- Control the number of recommendations returned
- View history of past recommendations
- REST API with JSON responses

## Tech Stack

- **Backend**: FastAPI
- **Database**: SQLite (via SQLAlchemy)
- **AI**: OpenAI GPT models
- **Dependency Injection**: Dishka

## Installation

### Prerequisites

- Python 3.12+
- OpenAI API key

### Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/Krak3nDev/trip-sage.git
   cd trip-sage
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows, use: .venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -e .
   ```

4. Create a `.env` file in the project root with your OpenAI API key:
   ```
   OPENAI_API_KEY=your_openai_api_key
   ```

## Running the Application

Start the development server:

```bash
uvicorn trip_sage.main:create_app --host 0.0.0.0 --port 8000 --reload --factory --use-colors
```

The API will be accessible at `http://localhost:8000`.

## API Documentation

After starting the server, you can access the interactive API documentation:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`
