from tkinter import *
from tkinter import ttk
from pass_manager import Pass_Manager
from functions import *

credentials = load_json()

class Authentication:
  def __init__(self, root):
    if(credentials['login'] != '' and credentials['password'] != ''):
      self.login_window()
      geometry = '400x180'
      title = 'Login'
    else:
      self.register_window()
      geometry = '400x230'
      title = 'Register'

    root.geometry(geometry)
    root.title(f'{title} - PassManger')
    root.grid_columnconfigure((0,1), weight=1)
    root.call('source', 'azure.tcl')
    root.call("set_theme", "dark")

  def login_window(self):
    #username label and text entry box
    usernameLabel = ttk.Label(root, text="User Name")
    usernameLabel.grid(row=1, column=0, pady=20, sticky=E)
    self.username = StringVar()
    usernameEntry = ttk.Entry(root, textvariable=self.username)
    usernameEntry.grid(row=1, column=1, padx=5, sticky=W)

    #password label and password entry box
    passwordLabel = ttk.Label(root, text="Password")
    passwordLabel.grid(row=2, column=0, sticky=E)
    self.password = StringVar()
    passwordEntry = ttk.Entry(root, textvariable=self.password, show='*')
    passwordEntry.grid(row=2, column=1, padx=5, sticky=W)

    #login button
    loginButton = ttk.Button(root, text="Login", command=self.validate_login)
    loginButton.grid(row=4, column=0, columnspan=2, pady=5)

    #error message
    self.message = ttk.Label(root, text='', foreground='Red')
    self.message.grid(row=3, column=0, columnspan=2, pady=5)

  def register_window(self):
    #username label and text entry box
    loginLabel = ttk.Label(root, text="User Name")
    loginLabel.grid(row=1, column=0, pady=20, sticky=E)
    self.login = StringVar()
    loginEntry = ttk.Entry(root, textvariable=self.login)
    loginEntry.grid(row=1, column=1, padx=5, sticky=W)

    #password label and password entry box
    passLabel_1 = ttk.Label(root,text="Password")
    passLabel_1.grid(row=2, column=0, sticky=E)
    self.password_1 = StringVar()
    passwordEntry_1 = ttk.Entry(root, textvariable=self.password_1, show='*')
    passwordEntry_1.grid(row=2, column=1, padx=5, sticky=W)

    passLabel_2 = ttk.Label(root,text="Confirm Password")
    passLabel_2.grid(row=3, column=0, pady=20, sticky=E)
    self.password_2 = StringVar()
    passwordEntry_2 = ttk.Entry(root, textvariable=self.password_2, show='*')
    passwordEntry_2.grid(row=3, column=1, padx=5, sticky=W)

    #login button
    registerButton = ttk.Button(root, text="Register", command=self.register)
    registerButton.grid(row=5, column=0, columnspan=2, pady=5)

    #info message
    self.info_message = ttk.Label(root, text='', foreground='Red')
    self.info_message.grid(row=4, column=0, columnspan=2)

  def validate_login(self):
    secured_password = hash_password(self.password.get())

    if self.username.get() == credentials['login'] and secured_password  == credentials['password']:
      #Destroy current window
      root.destroy()

      #Open new window
      newroot = Tk()
      application = Pass_Manager(newroot)
      newroot.mainloop()
    else:
      self.message['text'] = 'Username or Password incorrect. Try again!.'

  def register(self):
    if self.login.get() == '' or self.password_1.get() == '' or self.password_2.get() == '':
      self.info_message['text'] = 'Please complete all fields!'
    else:
      if self.password_1.get() == self.password_2.get():
        write_json(self.login.get(), self.password_1.get())
        #Destroy current window
        root.destroy()

        #Open new window
        newroot = Tk()
        application = Pass_Manager(newroot)
        newroot.mainloop()
      else:
        self.info_message['text'] = 'Password did not match!'

if __name__ == '__main__':
  root = Tk()
  application = Authentication(root)
  root.mainloop()
