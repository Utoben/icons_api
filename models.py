from sqlalchemy import Column, Integer, String, Float
from database import Base

# Модель для значков
class Icon(Base):
    __tablename__ = "icons"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    price = Column(Float)
