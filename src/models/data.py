from pydantic import BaseModel


class HeartData(BaseModel):
    timestamp: int
    value: float
