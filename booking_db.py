import sqlite3
from time_utils import add_minutes

class BookingDB():
    def __init__(self,file_name):
        self.conn= sqlite3.connect(file_name)
        self.create_table()
    def create_table(self):
        cur = self.conn.cursor()
        cur.execute("""CREATE TABLE IF NOT EXISTS clients(
        id INTEGER PRIMARY KEY,
        name TEXT,
        phone TEXT,
        email TEXT)
        """)

        cur.execute("""CREATE TABLE IF NOT EXISTS services(
        id INTEGER PRIMARY KEY,
        type TEXT,
        duration INTEGER,
        price INTEGER)
        """)

        cur.execute("""CREATE TABLE IF NOT EXISTS bookings(
        id INTEGER PRIMARY KEY,
        client_id INTEGER,
        service_id INTEGER,
        payment TEXT,
        date TEXT,
        start_time TEXT,
        end_time TEXT)
        """)
        self.conn.commit()

    def add_client(self, name, phone, email):
        cur = self.conn.cursor()
        cur.execute("INSERT INTO clients (name, phone, email) VALUES (?,?,?) ",(name,phone,email))
        self.conn.commit()
    def add_service(self, name, duration, price):
        cur = self.conn.cursor()
        cur.execute("INSERT INTO services (type, duration, price) VALUES (?,?,?) ",(name, duration, price))
        self.conn.commit()

    def get_duration(self, service_id):
        cur= self.conn.cursor()
        cur.execute("SELECT duration FROM services WHERE id = ?",(service_id,))
        rows = cur.fetchone()
        return rows[0]

    def is_free(self, date,new_start, new_end):
        cur = self.conn.cursor()
        cur.execute("""SELECT COUNT(*) FROM bookings
               WHERE date = ? AND start_time < ? AND end_time > ?""", (date, new_end, new_start))
        rows= cur.fetchone()
        if rows[0] == 0:
            return True
        else:
            return False

    def add_booking(self,client_id, service_id, date, start_time):
        duration = self.get_duration(service_id)
        end_t = add_minutes(start_time, duration)
        free = self.is_free(date,start_time, end_t)
        if not free :
            return False
        cur = self.conn.cursor()
        cur.execute("""INSERT INTO bookings (client_id, service_id, date, start_time, end_time)
            VALUES (?,?,?,?,?)
            """,(client_id, service_id, date, start_time,end_t))
        self.conn.commit()
        return True
if __name__ == "__main__":
    db = BookingDB(":memory:")
    print(db.conn.execute("SELECT name FROM sqlite_master").fetchall())
    db.add_client("nedjem", "+300000835", "ben@example.com")
    db.add_client("mays", "+49100000775", "a@example.com")
    db.add_service("wash", 30, 25)
    db.add_service("full wash", 60, 45)
    print(db.conn.execute("SELECT * FROM clients").fetchall())
    print(db.conn.execute("SELECT * FROM services").fetchall())
    assert db.get_duration(1) == 30
    assert db.get_duration(2) == 60
    print(db.add_booking(1, 2, "2026-11-17", "10:00"))   # True  ✅ Ali, full wash 10:00-11:00
    print(db.add_booking(2, 1, "2026-11-17", "10:30"))   # False ❌ collides
    print(db.add_booking(2, 1, "2026-11-17", "11:00"))   # True  ✅ touches only
    print(db.conn.execute("SELECT * FROM bookings").fetchall())
    print("done")

