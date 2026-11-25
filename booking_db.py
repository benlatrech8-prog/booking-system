import sqlite3
from time_utils import add_minutes

class BookingDB():
    def __init__(self,file_name):
        self.conn= sqlite3.connect(file_name, check_same_thread=False)
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
        if rows is None:
            return None
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

    def client_exists(self, client_id):
        cur = self.conn.cursor()
        cur.execute("SELECT name, phone, email FROM clients WHERE clients.id = ?",(client_id,))
        rows = cur.fetchone()
        if rows is None:
            return False
        else :
            return True

    def add_booking(self,client_id, service_id, date, start_time):
        if not self.client_exists(client_id):
            return "unknown_client"
        duration = self.get_duration(service_id)
        if duration is None :
            return "unknown_service"
        end_t = add_minutes(start_time, duration)
        if start_time < "08:00" or end_t > "20:00":
            return "closed"
        free = self.is_free(date,start_time, end_t)
        if not free :
            return "taken"
        cur = self.conn.cursor()
        cur.execute("""INSERT INTO bookings (client_id, service_id, date, start_time, end_time)
            VALUES (?,?,?,?,?)
            """,(client_id, service_id, date, start_time,end_t))
        self.conn.commit()
        return "ok"

    def bookings_on(self, date):
        cur= self.conn.cursor()
        cur.execute("""SELECT clients.name, services.type, bookings.start_time, bookings.end_time
        FROM bookings
        INNER JOIN clients ON bookings.client_id = clients.id
        INNER JOIN services ON bookings.service_id = services.id
        WHERE bookings.date = ?
        ORDER BY bookings.start_time
        """,(date,))
        rows = cur.fetchall()
        result = []
        for name, service, start, end in rows:
            result.append({"client": name, "service": service, "start": start, "end": end })
        return result

    def get_services(self):
        cur = self.conn.cursor()
        cur.execute("SELECT id, type, duration, price FROM services")
        rows = cur.fetchall()
        result = []
        for service_id, name, duration, price in rows:
            result.append({"id": service_id, "name": name, "duration": duration, "price": price})
        return result

    def booking_exists(self, booking_id):
        cur = self.conn.cursor()
        cur.execute("""SELECT client_id, service_id, payment, date, start_time, end_time
            FROM bookings WHERE bookings.id = ?""",(booking_id,))
        rows= cur.fetchone()
        if rows is None:
            return False
        else:
            return True

    def delete_booking(self, booking_id):
        if not self.booking_exists(booking_id):
            return "not_found"

        cur = self.conn.cursor()
        cur.execute("DELETE FROM bookings WHERE bookings.id = ?",(booking_id,))
        self.conn.commit()
        return "ok"

if __name__ == "__main__":
    db = BookingDB(":memory:")
    #print(db.conn.execute("SELECT name FROM sqlite_master").fetchall())
    db.add_client("nedjem", "+300000835", "ben@example.com")
    db.add_client("mays", "+49100000775", "a@example.com")
    db.add_service("wash", 30, 25)
    db.add_service("full wash", 60, 45)
    #print(db.conn.execute("SELECT * FROM clients").fetchall())
    #print(db.conn.execute("SELECT * FROM services").fetchall())
    assert db.get_duration(1) == 30
    assert db.get_duration(2) == 60
    print(db.add_booking(1, 2, "2026-11-17", "10:00"))   # True  ✅ Ali, full wash 10:00-11:00
    print(db.add_booking(2, 1, "2026-11-17", "10:30"))   # False ❌ collides
    print(db.add_booking(2, 1, "2026-11-17", "11:00"))   # True  ✅ touches only
    print(db.add_booking(1, 99, "2026-11-18", "12:00"))
    #print(db.conn.execute("SELECT * FROM bookings").fetchall())
    print(db.bookings_on("2026-11-17"))
    print(db.bookings_on("2030-01-01"))    # → []
    print(db.get_services())
    print("done")

