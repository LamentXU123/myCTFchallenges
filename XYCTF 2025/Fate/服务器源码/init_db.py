import sqlite3

conn = sqlite3.connect("database.db")
conn.execute("""CREATE TABLE FATETABLE (
  NAME TEXT NOT NULL,
  FATE TEXT NOT NULL
);""")
Fate = [
    ('JOHN', '1994-2030 Dead in a car accident'),
    ('JANE', '1990-2025 Lost in a fire'),
    ('SARAH', '1982-2017 Fired by a government official'),
    ('DANIEL', '1978-2013 Murdered by a police officer'),
    ('LUKE', '1974-2010 Assassinated by a military officer'),
    ('KAREN', '1970-2006 Fallen from a cliff'),
    ('BRIAN', '1966-2002 Drowned in a river'),
    ('ANNA', '1962-1998 Killed by a bomb'),
    ('JACOB', '1954-1990 Lost in a plane crash'),
    ('LAMENTXU', r'2024 Send you a flag flag{FAKE}')
]
conn.executemany("INSERT INTO FATETABLE VALUES (?, ?)", Fate)

conn.commit()
conn.close()
