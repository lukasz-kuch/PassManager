import sqlite3

class MainDatabase:
  def __init__(self, db):
    self.conn = sqlite3.connect(db)
    self.cur = self.conn.cursor()
    self.cur.execute("CREATE TABLE IF NOT EXISTS credentials (id INTEGER PRIMARY KEY, name text, login text, password text, folder text)")
    self.conn.commit()

  def fetch(self, folder):
    print(folder)
    self.cur.execute("SELECT * FROM credentials WHERE folder=?", (folder,))
    rows = self.cur.fetchall()
    return rows

  def fetch_all(self):
    cursor = self.cur.execute("SELECT * FROM credentials")
    #rows = self.cur.fetchall()
    return cursor

  def insert(self, name, login, password, group):
    self.cur.execute("INSERT INTO credentials VALUES (NULL, ?, ?, ?, ?)", (name, login, password, group))
    self.conn. commit()

  def remove(self, id):
    self.cur.execute("DELETE FROM credentials WHERE id=?", (id,))
    self.conn.commit()

  def update(self, name, login, password, id):
    self.cur.execute("UPDATE credentials SET name = ?, login = ?, password = ? WHERE id = ?",(name, login, password, id))
    self.conn.commit()

  def __del__(self):
    self.conn.close()
