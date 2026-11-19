from booking_db import BookingDB


def test_is_free():
    db = BookingDB(":memory:")
    # Arrange: Ali is in the bay 10:00 → 11:00
    db.conn.execute("""INSERT INTO bookings (client_id, service_id, date, start_time, end_time)
                       VALUES (1, 2, '2026-11-17', '10:00', '11:00')""")

    assert db.is_free("2026-11-17", "11:00", "11:45") == True     # E: starts when Ali leaves
    assert db.is_free("2026-11-17", "09:30", "10:30") == False    # D: overlaps the start
    assert db.is_free("2026-11-17", "10:30", "11:00") == False    # B: inside, ends with Ali
    assert db.is_free("2026-11-17", "09:30", "10:00") == True     # C: ends when Ali arrives
    assert db.is_free("2026-11-18", "10:00", "11:00") == True     # F: another day
    assert db.is_free("2026-11-17", "09:30", "13:00") == False    # G: covers Ali completely
    db.conn.close()


def test_add_booking():
    db = BookingDB(":memory:")
    # Arrange
    db.add_client("Ali", "0151 0000000", "ali@example.com")
    db.add_client("Sara", "0176 0000000", "sara@example.com")
    db.add_service("wash", 30, 25)          # id 1
    db.add_service("full wash", 60, 45)     # id 2

    # Act + Assert
    assert db.add_booking(1, 2, "2026-11-17", "10:00") == "ok"     # 10:00-11:00
    assert db.add_booking(2, 1, "2026-11-17", "10:30") == "taken"  # collides
    assert db.add_booking(2, 1, "2026-11-17", "11:00") == "ok"     # touches only
    assert db.add_booking(2, 2, "2026-11-17", "07:30") == "closed" # before opening
    assert db.add_booking(2, 2, "2026-11-17", "19:45") == "closed" # ends 20:45
    assert db.add_booking(2, 2, "2026-11-17", "19:00") == "ok"     # ends exactly 20:00
    assert db.add_booking(1, 99, "2026-11-17", "12:00") == "unknown_service"   # unknown service

    # check the data too: only the 3 accepted bookings were saved
    count = db.conn.execute("SELECT COUNT(*) FROM bookings").fetchone()[0]
    assert count == 3
    db.conn.close()


def test_bookings_on():
    db = BookingDB(":memory:")
    # Arrange: added in the WRONG order on purpose, to prove ORDER BY works
    db.add_client("Ali", "0151 0000000", "ali@example.com")
    db.add_client("Sara", "0176 0000000", "sara@example.com")
    db.add_service("wash", 30, 25)
    db.add_service("full wash", 60, 45)
    db.add_booking(2, 1, "2026-11-17", "11:00")    # Sara, added first
    db.add_booking(1, 2, "2026-11-17", "10:00")    # Ali, added second

    # Act + Assert
    assert db.bookings_on("2026-11-17") == [
        {"client": "Ali", "service": "full wash", "start": "10:00", "end": "11:00"},
        {"client": "Sara", "service": "wash", "start": "11:00", "end": "11:30"},
    ]
    assert db.bookings_on("2030-01-01") == []      # empty day → empty list, not an error
    db.conn.close()


if __name__ == "__main__":
    test_is_free()
    test_add_booking()
    test_bookings_on()
    print("All tests passed ✅")
