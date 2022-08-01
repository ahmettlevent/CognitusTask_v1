from sqlalchemy import Column, Integer, String
from database import Base


class LabeledData(Base):
    __tablename__ = "labeled_data"
    id = Column(Integer, primary_key=True,  index=True)
    text = Column(String(255), index=True)
    label = Column(String(255), index=True)