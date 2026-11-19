from booking_db import BookingDB

db = BookingDB("booking.db")
db.add_service("wash", 30, 25)
db.add_service("full wash", 60, 45)
print(db.get_services())
