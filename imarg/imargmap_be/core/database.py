import psycopg2
from psycopg2.extras import RealDictCursor, register_hstore

# Existing DB
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


# def get_auth_db():
#     conn = psycopg2.connect(
#         dbname="auth_db",
#         user="postgres",
#         password="postgres",
#         host="10.10.6.83",
#         port="5432",
#         cursor_factory=RealDictCursor
#     )
#     register_hstore(conn)
#     return conn
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
'''def get_aoi_db():
    conn=psycopg2.connect(
        dbname="imarg",
        user="postgres",
        password="madhu",
        host="localhost",
        port="5432",
        cursor_factory=RealDictCursor
    )
    register_hstore(conn)
    return conn'''
def admin_test():
    conn=psycopg2.connect(
        dbname="test_db",
        user="postgres",
        password="madhu",
        host="localhost",
        port="5432",
        cursor_factory=RealDictCursor
    )
    register_hstore(conn)
    return conn