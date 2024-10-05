from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_signup():
    response = client.get(url="/auth/signup") 
    