import sqlite3

class BookingDB():
    def __init__(self,file_name):
        self.conn= sqlite3.connect("booking.db")
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
if __name__ == "__main__":
    db = BookingDB(":memory:")
    print(db.conn.execute("SELECT name FROM sqlite_master").fetchall())
