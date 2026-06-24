'''from core.database import get_aoi_db

try:
    conn = get_aoi_db()
    print("Database Connected Successfully")

    conn.close()

except Exception as e:
    print(e)'''
'''import psycopg2

try:
    conn = psycopg2.connect(
        dbname="imarg",
        user="postgres",
        password="madhu",
        host="localhost",
        port="5432"
    )

    print("SUCCESS")

    conn.close()

except Exception as e:
    print(e)'''
# test_db.py

'''from core.database import get_db

conn = get_db()
cur = conn.cursor()

cur.execute("""
SELECT table_name
FROM information_schema.tables
WHERE table_name LIKE 'planet_osm%';
""")

for row in cur.fetchall():
    print(row)

cur.close()
conn.close()'''
import psycopg2
from psycopg2.extras import RealDictCursor

def admin_test():
    conn = psycopg2.connect(
        dbname="test_db",
        user="postgres",
        password="madhu",
        host="localhost",
        port="5432",
        cursor_factory=RealDictCursor
    )

    return conn