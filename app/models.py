from sqlmodel import Field, SQLModel, Column, JSON
from typing import Optional, Dict, Any
import uuid as uuid_pkg

class OptimizationBase(SQLModel):
    iteration: int
    run_time: str

class OptimizationRun(OptimizationBase):
    pass

class OptimizationResult(SQLModel, table=True):
    id: Optional[uuid_pkg.UUID]  = Field(
        primary_key=True,
        index=True
    )
    task_id: Optional[str] = Field(index = True)
    payload_hash: Optional[str] = Field(index = True)
    payload: Dict[Any, Any] = Field(default={}, index = False, sa_column=Column(JSON))
    result:Dict[Any, Any] = Field(default={}, index = False, sa_column=Column(JSON))

    class Config:
        arbitrary_types_allowed = True

class FXRateCreate(SQLModel):
    year: int = Field(index = True)
    country: str = Field(index = True)
    fx_rate: float

class FXRate(FXRateCreate, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

class FXRateRead(FXRateCreate):
    id: int

