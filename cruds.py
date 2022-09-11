from sqlalchemy.orm import Session
from models import *

def addProfile(db: Session,data):
  db_user = Profile(name=data['name'], followers=data['followers'] , following=data['following'] , intro = data['intro'] , page_type= data['page_type'],
  phone_number = data['phone_number'] , website = data['website'] )
  db.add(db_user)
  db.commit()
  db.refresh(db_user)
  return db_user