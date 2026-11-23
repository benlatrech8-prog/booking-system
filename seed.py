from booking_db import BookingDB

db = BookingDB("booking.db")
db.add_service("wash", 30, 25)
db.add_service("full wash", 60, 45)
db.add_client("nedjem", "+300000835", "ben@example.com")
db.add_client("mays", "+49100000775", "a@example.com")
db.add_client("mo", "+49134244455", "b@example.com")
db.add_client("modi", "+11134244455", "do@example.com")
print(db.get_services())
