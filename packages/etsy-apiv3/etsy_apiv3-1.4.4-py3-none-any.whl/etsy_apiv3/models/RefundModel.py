import pydantic
from . import Price


class Refund(pydantic.BaseModel):
    amount: Price
    created_timestamp: int
    reason: str
    note_from_issuer: str
    status: str
    