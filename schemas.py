from pydantic import BaseModel

class BadgeBase(BaseModel):
    id: int
    name: str
    description: str
    price: float


