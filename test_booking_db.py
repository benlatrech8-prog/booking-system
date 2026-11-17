from booking_db import BookingDB

def test_is_free():
    db = BookingDB(":memory:")
    db.conn.execute("""INSERT INTO bookings (client_id, service_id, date, start_time, end_time)
         VALUES (1, 2, '2026-11-17', '10:00', '11:00')
    """)

    assert db.is_free("2026-11-17", "11:00", "11:45") == True
    assert db.is_free("2026-11-17", "09:30", "10:30") == False
    assert db.is_free("2026-11-17", "11:00", "12:00") == True
    assert db.is_free("2026-11-17", "09:30", "10:00") == True
    assert db.is_free("2026-11-18", "10:00", "11:00") == True
    assert db.is_free("2026-11-17", "09:30", "13:00") == False

def test_add_booking():
    db = BookingDB(":memory:")
    db.add_client("nedjem", "+300000835", "ben@example.com")
    db.add_client("mays", "+49100000775", "a@example.com")
    db.add_service("wash", 30, 25)
    db.add_service("full wash", 60, 45)
    assert db.add_booking(1, 2, "2026-11-17", "10:00") == True
    assert db.add_booking(2, 1, "2026-11-17", "10:30") == False
    assert db.add_booking(2, 1, "2026-11-17", "11:00")  == True
    count = db.conn.execute("SELECT COUNT(*) FROM bookings").fetchone()[0]
    assert count == 2
if __name__ =="__main__":
    test_is_free()
    test_add_booking()
    print("Tests done")
