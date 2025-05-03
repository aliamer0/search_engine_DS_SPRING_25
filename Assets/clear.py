from Assets.db import conn, cursor
import redis
r = redis.Redis(host='localhost', port=6379, db=0)
r.flushdb()
cursor.execute("DELETE FROM crawled_pages;")
conn.commit()
