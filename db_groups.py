import sqlite3

class Database:
  def __init__(self, db):
    self.conn = sqlite3.connect(db)
    self.cur = self.conn.cursor()
    self.cur.execute("CREATE TABLE IF NOT EXISTS groups (id INTEGER PRIMARY KEY, name text, parent text, child text)")
    self.conn.commit()

  def fetch(self):
    self.cur.execute("SELECT * FROM groups")
    rows = self.cur.fetchall()
    return rows

  def insert(self, name, parent, child):
    self.cur.execute("INSERT INTO groups VALUES (NULL, ?, ?, ?)", (name, parent, child))
    self.conn. commit()

  def remove(self, id):
    self.cur.execute("DELETE FROM groups WHERE id=?", (id,))
    self.conn.commit()

  def update(self, name, id):
    self.cur.execute("UPDATE groups SET name = ? WHERE id = ?", (name, id))
    self.conn.commit()

  def update_parent(self, parent, id):
    self.cur.execute("UPDATE groups SET parent = ? WHERE id = ?", (parent, id))
    self.conn.commit()

  def __del__(self):
    self.conn.close()
