import asyncio
import uuid
from app.services.provider import fetch_price
from app.models.polling_job import PollingJob
from app.core.config import SessionLocal


async def start_polling_job_logic(request):
    job_id = f"poll_{uuid.uuid4().hex[:8]}"

    # Save job to DB
    db = SessionLocal()
    try:
        job = PollingJob(
            job_id=job_id,
            symbols=request.symbols,
            interval=request.interval,
            provider=request.provider,
            max_runs=request.max_runs or 10,
            status="running",
        )
        db.add(job)
        db.commit()
        db.refresh(job)
    except Exception as e:
        db.rollback()
        raise
    finally:
        db.close()

    # Polling logic
    async def poll_task():
        run_count = 0
        while run_count < request.max_runs:
            for symbol in request.symbols:
                try:
                    await fetch_price(symbol, request.provider)
                except Exception as e:
                    print(f"Polling error: {e}")
            run_count += 1
            await asyncio.sleep(request.interval)
        print(f"Job {job_id} completed.")

    asyncio.create_task(poll_task())
    return job_id
