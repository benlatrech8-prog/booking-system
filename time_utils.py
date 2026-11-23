def add_minutes(time_text, minutes):
    parts = time_text.split(":")
    total = int(parts[0])*60 + int(parts[1]) + minutes
    New_hour = total // 60
    New_min = total % 60
    if New_hour == 24:
        New_hour = 00

    return f"{New_hour:02d}:{New_min:02d}"

assert add_minutes("15:45", 45) == "16:30"
assert add_minutes("12:45", 30) == "13:15"
assert add_minutes("09:45", 60) == "10:45"
assert add_minutes("23:45", 30) == "00:15"
print("Done")
