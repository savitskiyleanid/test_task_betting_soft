import uuid
from decimal import Decimal

from pydantic import BaseModel


class BetBase(BaseModel):
    bet: Decimal
    user_id: int
    event_id: uuid.UUID


class BetCreate(BetBase):
    pass


class BetRead(BetBase):
    id: int

    class Config:
        orm_mode = True
