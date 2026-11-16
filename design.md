clients                services (the menu 📋)       bookings (the ticket 🎫)
─────────              ──────────────────          ──────────────────────
id (PK) INTEGER ◄─┐      id (PK) INTEGER ◄──┐        id (PK) : INTEGER
name    TEXT      │      type      TEXT     │        client_id  (FK) ──┘ → clients : INTEGER
phone   TEXT      │      duration: TEXT     └─────── service_id (FK)    → services : INTEGER
email   TEXT      │      price : INTEGER             payment (cash/card) : TEXT
                  └─────────────────────────────     date : TEXT -- format "YYYY-MM-DD", eg. "2026-11-16"
                                                     start_time : TEXT -- format "HH:MM" (24h), eg. "09:00"
                                                     end_time TEXT -- "HH:MM"

## Business rule: no double booking
A new booking collides with an existing one on the same date when:
    new_start < existing_end  AND  new_end > existing_start
(one car at a time)

## Business rule 2: opening hours
A booking must start at or after 08:00 and end at or before 20:00.
