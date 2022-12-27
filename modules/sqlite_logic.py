import sqlite3 as sq

def start():
    global base, cur
    base = sq.connect("databases/db.db", check_same_thread=False)
    cur = base.cursor()

    if base:
        print('База данных подключена')
    base.execute("""
    CREATE TABLE IF NOT EXISTS
    url(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    url TEXT)""")
    base.commit()

async def create_url(url):
    result = cur.execute("SELECT id FROM url WHERE url = ?", (url,)).fetchall()
    if len(result) == 0:
        cur.execute("INSERT INTO url(url) VALUES (?)", (url,) )
        result = cur.execute("SELECT id FROM url WHERE url = ?", (url,)).fetchall()
        base.commit()
        return result[0][0], True
    else:
        return result[0][0], False

async def remove_url(_id):
    result = cur.execute("SELECT url FROM url WHERE id = ?", (_id,)).fetchall()
    if len(result) == 0:
        return False
    else:
        cur.execute("DELETE FROM url WHERE id = ?", (_id,))
        base.commit()
        return True

async def get_Url():
    result = cur.execute("SELECT id, url FROM url").fetchall()
    return  result

async def get_user_url(_id):
    result = cur.execute("SELECT url FROM url WHERE id = ?", (_id,)).fetchall()
    if len(result) == 0:
        return None, False
    else:
        return result[0][0], True

