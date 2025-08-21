import sqlite3

conn = sqlite3.connect("football.db")
cursor = conn.cursor()

cursor.execute("DROP TABLE IF EXISTS players")

cursor.execute("""
CREATE TABLE players (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    club TEXT,
    goals INTEGER,
    assists INTEGER
)
""")

players = [
    ("Lionel Messi", "Inter Miami", 20, 12),
    ("Cristiano Ronaldo", "Al Nassr", 25, 5),
    ("Kylian Mbappe", "PSG", 30, 7),
    ("Erling Haaland", "Manchester City", 28, 6),
    ("Kevin De Bruyne", "Manchester City", 10, 20),
    ("Neymar Jr", "Al Hilal", 15, 10),
    ("Fahham Faizal", "Talks and Talks", 7, 3)
]

cursor.executemany("INSERT INTO players (name, club, goals, assists) VALUES (?, ?, ?, ?)", players)

conn.commit()
conn.close()

print("Database created successfully with sample data.")

