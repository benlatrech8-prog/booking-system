import sqlite3

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
if __name__ == "__main__":
    db = BookingDB(":memory:")
    print(db.conn.execute("SELECT name FROM sqlite_master").fetchall())
    db.add_client("nedjem", "+300000835", "ben@gmail.com")
    db.add_client("mays", "+49100000775", "a@gmail.com")
    db.add_service("wash", 30, 25)
    db.add_service("full wash", 60, 45)
    print(db.conn.execute("SELECT * FROM clients").fetchall())
    print(db.conn.execute("SELECT * FROM services").fetchall())
    assert db.get_duration(1) == 30
    assert db.get_duration(2) == 60
    print("done")
