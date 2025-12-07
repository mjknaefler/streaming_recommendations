# test if postgres connection works

import psycopg2

# TODO: move to env file
HOST = 'localhost'
PORT = '5432'
DATABASE = 'streaming_recommendations'
USER = 'myuser'
PASSWORD = 'mypass'

try:
    conn = psycopg2.connect(
        host=HOST,
        port=PORT,
        database=DATABASE,
        user=USER,
        password=PASSWORD
    )
    print("Connected!")
    
    # simple test query
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM title;")
    count = cur.fetchone()[0]
    print(f"Number of titles: {count}")
    
    cur.close()
    conn.close()
    
except Exception as e:
    print(f"Connection failed: {e}")