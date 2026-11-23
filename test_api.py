from fastapi.testclient import TestClient
import main
from main import app
from booking_db import BookingDB

client = TestClient(app)

def test_home():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Car wash API is running"}

def test_services():
    main.db = BookingDB(":memory:")
    main.db.add_service("wash", 30, 25)

    response = client.get("/services")

    assert response.status_code == 200
    assert response.json() == [
  {
    "id": 1,
    "name": "wash",
    "duration": 30,
    "price": 25

  }
]
