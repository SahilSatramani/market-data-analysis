# Market Data Service – FastAPI Project

This is a production-ready FastAPI microservice that fetches real-time market data from providers like Alpha Vantage. It supports real-time querying, periodic polling, and streaming to Kafka (upcoming). It uses SQLAlchemy for database storage and Pydantic for API schema validation.

---

## Features

- Fetch latest market price via `/prices/latest`
- Connects to real-world market APIs (Alpha Vantage)
- Environment-based API key loading (`.env`)
- Pydantic response validation
- Ready for polling, Kafka streaming, and persistence
- Swagger UI built-in for testing APIs

---

## Project Structure

market-data-service/
├── app/
│   ├── api/            # Route definitions
│   ├── services/       # API calls (Alpha Vantage, etc.)
│   ├── schemas/        # Pydantic response models
│   ├── models/         # (Upcoming) SQLAlchemy models
│   ├── core/           # App config (DB, logging)
│   └── main.py         # Entry point
├── .env                # API key and secrets (NOT committed)
├── requirements.txt    # Python dependencies
└── README.md

---

## How to Run

### 1. Clone the repo and enter the directory

```bash
git clone https://github.com/yourusername/market-data-service.git
cd market-data-service

2. Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate  # For Windows: venv\Scripts\activate

3. Install dependencies
pip install -r requirements.txt

4. Add your .env file
ALPHA_VANTAGE_API_KEY=your_api_key_here