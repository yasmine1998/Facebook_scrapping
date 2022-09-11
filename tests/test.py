from fastapi.testclient import TestClient
from database import *
from bson import ObjectId
import unittest
from main import app

client = TestClient(app)

class ProfileInfo(unittest.TestCase):
    def test_profile_saved(self):
        print("response")
        response = client.post("/scrapPublicPage/",
        json={"url":"https://www.facebook.com/barackobama/"}) 
       
        assert response.status_code == 201
        
