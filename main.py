from typing import Union
import os
from fastapi import FastAPI
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
import selenium.webdriver
from pydantic import BaseModel
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
import cruds, models
from database import SessionLocal, engine

chrome_options = selenium.webdriver.ChromeOptions()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class Page(BaseModel):
    url: str = 'https://www.facebook.com/barackobama/'
   
@app.post("/scrapPublicPage/")
async def scrapPublicPage(profileURL:Page ,db: Session = Depends(get_db)): 
    name = profileURL.url[25:-1]
    #driver = webdriver.Chrome(r"/code/chromedriver") # in case you are chrome
    driver = selenium.webdriver.Chrome(options=chrome_options)
    driver.get(profileURL.url)
    data = {}
    content = driver.page_source
    soup = BeautifulSoup(content,features="lxml")
    
    try :
      data['name'] = soup.find('h1', attrs ={'class':'jxuftiz4 jwegzro5 hl4rid49 icdlwmnq'}).getText().strip()
      data['followers'] = soup.find('a',attrs={'href':"https://www.facebook.com/"+ name +"/followers/"}).getText()
      data['following'] = soup.find('a',attrs={'href':'https://www.facebook.com/'+ name +'/following/'}).getText()
      data['intro'] = soup.find('div', attrs ={'class':'hsphh064 ez8dtbzv mfycix9x'}).getText()
      data['page_type'] = soup.find('span', attrs ={'class':'gvxzyvdx aeinzg81 t7p7dqev gh25dzvf ocv3nf92 k1z55t6l oog5qr5w tes86rjd pbevjfx6'}).getText().split(' · ')[1]
      data['phone_number'] = soup.find_all('div', attrs ={'class':'bdao358l om3e55n1 g4tp4svg alzwoclg cqf1kptm gvxzyvdx aeinzg81 jg3vgc78 cgu29s5g i15ihif8 gb2oqlaf i5oewl5a nnzkd6d7 bmgto6uh f9xcifuu'})[1].getText()
      data['website'] = soup.find_all('div', attrs ={'class':'bdao358l om3e55n1 g4tp4svg alzwoclg cqf1kptm gvxzyvdx aeinzg81 jg3vgc78 cgu29s5g i15ihif8 gb2oqlaf i5oewl5a nnzkd6d7 bmgto6uh f9xcifuu'})[2].getText()
    
      return cruds.addProfile(db=db, data=data)
    except:
        print('unexpected error happened')
