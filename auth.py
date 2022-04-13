import hashlib
from tkinter import *
from tkinter import ttk
from pass_manager import Pass_Manager

class Authentication:
  user = 'admin'
  passw = '8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918'

  def __init__(self, root):
    root.geometry('400x180')
    root.title('Login - PassManger')
    root.grid_columnconfigure((0,1), weight=1)
    root.call('source', 'azure.tcl')
    root.call("set_theme", "light")

    #username label and text entry box
    self.usernameLabel = ttk.Label(root, text="User Name").grid(row=1, column=0, pady=20, sticky=E)
    self.username = StringVar()
    self.usernameEntry = ttk.Entry(root, textvariable=self.username).grid(row=1, column=1, padx=5, sticky=W)

    #password label and password entry box
    self.passwordLabel = ttk.Label(root,text="Password").grid(row=2, column=0, sticky=E)
    self.password = StringVar()
    self.passwordEntry = ttk.Entry(root, textvariable=self.password, show='*').grid(row=2, column=1, padx=5, sticky=W)

    #login button
    self.loginButton = ttk.Button(root, text="Login", command=self.validate_login).grid(row=3, column=1, pady=20, sticky=W)

    #error message
    self.message = ttk.Label(text = '', foreground='Red')
    self.message.grid(row=4, column=0, columnspan=2, pady=10)

  def validate_login(self):
    secured_password = self.hash_password()
    if self.username.get() == self.user and secured_password  == self.passw:
      #Destroy current window
      root.destroy()

      #Open new window
      newroot = Tk()
      application = Pass_Manager(newroot)
      newroot.mainloop()
    else:
      self.message['text'] = 'Username or Password incorrect. Try again!.'

  def hash_password(self):
    plaintext = self.password.get().encode()
    d = hashlib.sha256(plaintext)
    hash = d.hexdigest()
    return hash

if __name__ == '__main__':
  root = Tk()
  application = Authentication(root)
  root.mainloop()
