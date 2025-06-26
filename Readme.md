# 📈 Market Data Analysis Platform

This project is a real-time **market data ingestion and analysis pipeline** built using **FastAPI**, **Kafka**, **PostgreSQL**, and **Docker**. It fetches latest stock prices from Alpha Vantage API, stores raw data in a database, publishes events to Kafka, and computes a **5-point moving average** via a background Kafka consumer.

---

## 🧠 Features

- ⏱ Fetch latest price data from Alpha Vantage via `/prices/latest`
- 💾 Store raw responses into PostgreSQL
- 📤 Publish price events to Kafka (`price-events` topic)
- 🧮 Compute moving averages and update `symbol_averages` table
- 🐳 Fully containerized via Docker Compose
- ✅ CI with GitHub Actions for linting, building, and integration test

---

## 🏗️ Architecture Overview

![alt text](image.png)

---

## How to Run

## ⚙️ Local Setup

Follow these steps to run the project locally using Docker Compose.

### 1. Clone the repository

```bash
1. Clone the repository
git clone https://github.com/your-username/market-data-analysis.git
cd market-data-analysis

2. Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate  # For Windows: venv\Scripts\activate

3. Install dependencies
pip install -r requirements.txt

4. Add your .env file
cat <<EOF > .env
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=marketdata
DATABASE_URL=postgresql://postgres:postgres@db:5432/marketdata
ALPHA_VANTAGE_API_KEY=your_actual_key
KAFKA_BOOTSTRAP_SERVERS=kafka:29092
EOF
```
## Start all services via Docker Compose
```bash
docker-compose up --build
```
## Test the Endpoint
```bash
curl "http://127.0.0.1:8000/prices/latest?symbol=AAPL&provider=alpha_vantage"
```
---

##  Github Actions Include 

- Python linting via flake8
- Docker Compose setup
- Endpoint test (/prices/latest)
- DB migration test


  
---