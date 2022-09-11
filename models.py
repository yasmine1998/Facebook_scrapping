from sqlite3 import Date
from sqlalchemy import Boolean, Column, DATE, Integer, String , DateTime
from sqlalchemy.orm import relationship
from database import Base
import datetime

    
class Profile(Base):
    __tablename__ = "profile"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    followers = Column(String)
    following  = Column(String)
    intro = Column(String)
    page_type = Column(String)
    phone_number =  Column(String)
    website =  Column(String)
    scraping_date = Column(DateTime, default=datetime.datetime.utcnow)
