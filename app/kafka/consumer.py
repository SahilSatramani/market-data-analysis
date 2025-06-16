from confluent_kafka import Consumer
import json
from sqlalchemy.orm import Session
from app.core.config import SessionLocal
from app.models.symbol_average import SymbolAverage
from app.models.raw_market_data import RawMarketData


def calculate_moving_average(prices: list[float]) -> float:
    return round(sum(prices) / len(prices), 2)


def get_last_5_prices(db: Session, symbol: str) -> list[float]:
    records = (
        db.query(RawMarketData)
        .filter(RawMarketData.symbol == symbol)
        .order_by(RawMarketData.timestamp.desc())
        .limit(5)
        .all()
    )
    return [r.price for r in records]


def upsert_symbol_average(db: Session, symbol: str, average: float):
    existing = db.query(SymbolAverage).filter_by(symbol=symbol).first()
    if existing:
        existing.average_price = average
    else:
        existing = SymbolAverage(symbol=symbol, average_price=average)
        db.add(existing)
    db.commit()
    print(f"Upserted moving average for {symbol}: {average}")


def consume_price_events():

    consumer = Consumer(
        {
            "bootstrap.servers": "kafka:29092",
            "group.id": "ma-consumer-group",
            "auto.offset.reset": "earliest",
        }
    )

    consumer.subscribe(["price-events"])
    print("Listening for price events to calculate moving average")

    try:
        while True:
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                print("Error:", msg.error())
                continue

            try:
                event = json.loads(msg.value().decode("utf-8"))
                symbol = event["symbol"]
                db = SessionLocal()

                prices = get_last_5_prices(db, symbol)
                if len(prices) < 5:
                    print(f"Not enough data for {symbol} (only {len(prices)} prices)")
                    continue

                average = calculate_moving_average(prices)
                upsert_symbol_average(db, symbol, average)
                print(f"Received message: {msg.value().decode('utf-8')}")

            except Exception as e:
                print("Error processing message:", e)
            finally:
                db.close()

    except KeyboardInterrupt:
        print("Stopping MA consumer...")
    finally:
        consumer.close()


if __name__ == "__main__":
    consume_price_events()
