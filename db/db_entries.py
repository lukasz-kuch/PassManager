import sqlite3
import scripts.encrypt as encrypt

class Database:
  def __init__(self, db):
    self.conn = sqlite3.connect(db)
    self.cur = self.conn.cursor()
    self.cur.execute("CREATE TABLE IF NOT EXISTS credentials (id INTEGER PRIMARY KEY, name text, login text, password text, folder_id text)")
    self.conn.commit()

  def fetch(self, folder):
    i = 0
    self.cur.execute("SELECT * FROM credentials WHERE folder_id=?", (folder,))
    rows = self.cur.fetchall()
    return rows

  def fetch_all(self):
    cursor = self.cur.execute("SELECT * FROM credentials")
    #rows = self.cur.fetchall()
    return cursor

  def insert(self, name, login, password, folder_id):
    self.cur.execute("INSERT INTO credentials VALUES (NULL, ?, ?, ?, ?)", (name, encrypt.Encrypt(login), encrypt.Encrypt(password), folder_id))
    self.conn. commit()

  def remove(self, id):
    self.cur.execute("DELETE FROM credentials WHERE id=?", (id,))
    self.conn.commit()

  def update(self, name, login, password, id):
    self.cur.execute("UPDATE credentials SET name = ?, login = ?, password = ? WHERE id = ?",(name,  encrypt.Encrypt(login), encrypt.Encrypt(password), id))
    self.conn.commit()

  def __del__(self):
    self.conn.close()
