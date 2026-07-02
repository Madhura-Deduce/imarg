import psycopg2
from psycopg2.extras import RealDictCursor, register_hstore

#Geocoding DB
def get_db():
    conn = psycopg2.connect(
        dbname="nominatim_17_4m",
        user="postgres",
        password="imarg@2025",
        host="10.10.6.252",
        port="7051",
        cursor_factory=RealDictCursor
    )
    register_hstore(conn)
    return conn

#Auth,AOI,Downdload DB
def get_db1():
    conn = psycopg2.connect(
        dbname="imargmap",
        user="postgres",
        password="postgres",
        host="10.10.6.83",
        port="5432",
        cursor_factory=RealDictCursor
    )
    register_hstore(conn)
    return conn



#POI DATA DB
def get_db2():
    conn = psycopg2.connect(
        dbname="bindu_v1.7.1",
        user="postgres",
        password="imarg@2025",
        host="10.10.6.252",
        port="7051",
        cursor_factory=RealDictCursor
    )
    register_hstore(conn)
    return conn
