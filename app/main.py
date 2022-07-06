import json
import sys
from datetime import timedelta
import time
import redis
from fastapi import Depends, FastAPI
from sqlalchemy import select
from sqlmodel import Session
import joblib
from app.db import init_db, get_session
from app.models import  OptimizationRun, OptimizationResult, FXRate, FXRateRead, FXRateCreate
from app.optimization import _optimization_result
import uuid

def redis_connect() -> redis.client.Redis:
    """Connect to redis server."""
    try:
        # TODO: When running inside docker change this to redis://redis:6379
        client = redis.Redis(
            host="redis",
            port=6379,
            password="ubuntu",
            db=0,
            socket_timeout=5,
        )
        ping = client.ping()
        if ping is True:
            return client
    except redis.AuthenticationError:
        print("AuthenticationError")
        sys.exit(1)


client = redis_connect()

def optimization_result_from_cache(key: str) -> str:
    """Check cache for a given key.

    Args:
        key (str): md5 hash of the payload.

    Returns:
        str: value stored in cache against the key.
    """
    val = client.get(key)
    return val


def optimization_result_to_cache(key: str, value: dict) -> bool:
    """Store value in cache against the key."""
    state = client.setex(key, timedelta(seconds=3600), value=value,)
    return state

def get_optimization_result(payload: dict, session: Session) -> dict:
    """Get optimization result from cache or call optimization function."""
    key = str(joblib.hash(payload))
    data = optimization_result_from_cache(key=key)
    if data is not None:
        data = data.decode("UTF-8")
        data = json.loads(data)
        data["cache"] = True
        data["cached_from"] = "redis"
        return data
    else:
        statement = select(OptimizationResult).where(OptimizationResult.payload_hash == key)
        results = session.exec(statement)
        data = results.first()
        if data:
            data = json.loads(data.result)
            data["cache"] = True
            data["cached_from"] = "DB"
            return data
        else:
            data = _optimization_result(payload)
            data["cache"] = False
            data["cached_from"] = "NA"
            data = json.dumps(data)
            optimization_result_obj = OptimizationResult(id = uuid.uuid4(), task_id=str(uuid.uuid4()), payload_hash=key, payload = payload, result=data)
            session.add(optimization_result_obj)
            session.commit()
            session.refresh(optimization_result_obj)
            state = optimization_result_to_cache(key=key, value=data)
            if state:
                return json.loads(data)
        return data

app = FastAPI()

@app.on_event("startup")
def on_startup():
    init_db()

@app.get("/ping")
async def pong():
    return {"ping": "pong!"}

@app.post("/run_optimization/")
def run_optimization(optimization_run: OptimizationRun, session: Session = Depends(get_session)) -> dict:
    optimization_result_response =  get_optimization_result(optimization_run.dict(), session=session)
    return optimization_result_response


@app.get("/fx_rate/{country}/{year}")
def get_fx_rate(country: str, year: int, session: Session = Depends(get_session)):
    statement = select(FXRate).where(FXRate.country == country).where(FXRate.year == year)
    results = session.exec(statement)
    data = results.first()
    return data["FXRate"]

@app.post("/fx_rate/", response_model=FXRateRead)
def create_team(*, session: Session = Depends(get_session), fx_rate: FXRateCreate):
    db_fx_rate = FXRate.from_orm(fx_rate)
    session.add(db_fx_rate)
    session.commit()
    session.refresh(db_fx_rate)
    return db_fx_rate