''' IMPORTING PACKAGES '''

from asyncio.windows_events import NULL
from about import author, version
from re import A
from sre_parse import State
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from winsound import MB_ICONHAND
from db_entries import MainDatabase
from db_groups import Database

''' INITIALIZING DB '''

db_entries = MainDatabase('entries.db')
db_groups = Database('groups.db')

class Pass_Manager:
  global root
  def __init__(self, app):
    global root
    root = app
    root.call('source', 'azure.tcl')
    root.call("set_theme", "light")
    root.title('PassManager')
    root.geometry('800x400')
    root.resizable(0, 0)
    root.option_add('*tearOff', FALSE)

    # Configure the grid
    root.columnconfigure(0, weight=0)
    root.columnconfigure(1, weight=1)

    # App Menu
    menubar = Menu(root)
    menu_file = Menu(menubar)
    menu_edit = Menu(menubar)
    menu_about = Menu(menubar)
    menubar.add_cascade(menu=menu_file, label='File')
    menu_file.add_command(label='New')
    menu_file.add_command(label='Open')
    menu_file.add_command(label='Export')
    menubar.add_cascade(menu=menu_edit, label='Group')
    menu_edit.add_command(label='Add Group')
    menu_edit.add_command(label='Edit Group')
    menu_edit.add_command(label='Delete Group')
    menubar.add_cascade(menu=menu_about, label='About')
    menu_about.add_command(label='Author', command=lambda: self.info_window('Author', author))
    menu_about.add_command(label='Version', command=lambda: self.info_window('Version', version))
    root.config(menu=menubar)

    # Folders DB view
    group_frame = ttk.Frame(root)
    group_frame.grid(row=0, column=0, sticky=W+E)

    # Entries DB view
    entry_frame = ttk.Frame(root)
    entry_frame.grid(row=0, column=1, sticky=W+E)

    # Entry Scrollbars
    scrollbary = ttk.Scrollbar(entry_frame, orient=VERTICAL)
    scrollbarx = ttk.Scrollbar(entry_frame, orient=HORIZONTAL)
    # Entries Treeview
    self.entry_treeview = ttk.Treeview(entry_frame, columns=("c1", "c2", "c3"), show='headings')
    self.entry_treeview.configure(yscrollcommand=scrollbary.set, xscrollcommand=scrollbarx.set)

    scrollbary.config(command=self.entry_treeview.yview)
    scrollbary.pack(side=RIGHT, fill=Y)
    scrollbarx.config(command=self.entry_treeview.xview)
    scrollbarx.pack(side=BOTTOM, fill=X)
    #self.entry_treeview.column("# 1", minwidth=0, width=20, stretch=NO, anchor=CENTER)
    self.entry_treeview.column("#1", anchor=CENTER)
    self.entry_treeview.column("#2", anchor=CENTER)
    self.entry_treeview.column("#3", anchor=CENTER)
    #self.entry_treeview.heading("# 1", text='ID')
    self.entry_treeview.heading("#1", text='Name')
    self.entry_treeview.heading("#2", text='Login')
    self.entry_treeview.heading("#3", text='Password')
    self.entry_treeview.bind('<ButtonRelease-1>', self.select_entry)
    self.entry_treeview.bind('<ButtonRelease-3>', self.add_entry_menu)
    self.entry_treeview.pack()

    # Scrollbar folders
    scrollbar_y = ttk.Scrollbar(group_frame, orient=VERTICAL)
    scrollbar_x = ttk.Scrollbar(group_frame, orient=HORIZONTAL)
    # Folders Treeview
    self.group_treeview = ttk.Treeview(group_frame)
    self.group_treeview.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)
    self.group_treeview.heading("#0", text='DATABASE')

    scrollbar_y.configure(command=self.group_treeview.yview)
    scrollbar_y.pack(side=RIGHT, fill=Y)
    scrollbar_x.configure(command=self.group_treeview.xview)
    scrollbar_x.pack(side=BOTTOM, fill=X)
    self.group_treeview.bind('<ButtonRelease-1>', self.select_group)
    self.group_treeview.bind('<ButtonRelease-3>', self.add_group_menu)
    self.populate_groups()

    # Selected group context menu
    self.group_menu = Menu(group_frame, tearoff = 0)
    self.group_menu.add_command(label ="Add Group", command=lambda: self.group_window('New Group'))
    self.group_menu.entryconfig(0, state=DISABLED)
    self.group_menu.add_command(label ="Delete Group", command=self.delete_group)
    self.group_menu.entryconfig(1, state=DISABLED)
    self.group_menu.add_command(label ="Edit Group", command=lambda: self.group_window('Edit Group'))
    self.group_menu.entryconfig(2, state=DISABLED)
    # self.group_menu.add_separator()

    # Selected entry context menu
    self.entry_menu = Menu(entry_frame, tearoff = 0)
    self.entry_menu.add_command(label ="Add Entry", command=lambda: self.entry_window('New Entry'))
    self.entry_menu.entryconfig(0, state=DISABLED)
    self.entry_menu.add_command(label ="Delete Entry", command=self.delete_entry)
    self.entry_menu.entryconfig(1, state=DISABLED)
    self.entry_menu.add_command(label ="Edit Entry", command=lambda: self.entry_window('Edit Entry'))
    self.entry_menu.entryconfig(2, state=DISABLED)
    # self.entry_menu.add_separator()
    root.mainloop()

  '''Group TreeView Functions'''

  def populate_groups(self):
    self.clear_treeview(self.group_treeview)

    self.group_treeview.pack()
    for row in db_groups.fetch():
      if row[2] == '':
        self.group_treeview.insert('', 'end', row[0], text = row[1])
      else:
        self.group_treeview.insert(row[2], 'end', row[0], text = row[1])

  def select_group(self, event):
    global group_iid, entry_iid, selected_group
    if 'entry_iid' in globals() and len(entry_iid) > 0:
      temp = list(entry_iid)
      temp.clear()
      entry_iid = tuple(temp)
    group_iid = self.group_treeview.selection()
    if self.group_treeview.selection():
      current_group = self.group_treeview.focus()
      selected_group = self.group_treeview.item(current_group)
      if self.group_treeview.identify_element(event.x, event.y) == '':
        for i in self.group_treeview.selection():
          self.group_treeview.selection_remove(i)
        temp = list(group_iid)
        temp.clear()
        group_iid = tuple(temp)

    self.populate_entries()

  def add_group_menu(self, event):
    if 'group_iid' in globals():
      if len(group_iid) > 0:
        self.group_menu.entryconfig(0, state=ACTIVE)
        self.group_menu.entryconfig(1, state=ACTIVE)
        self.group_menu.entryconfig(2, state=ACTIVE)
      else:
        self.group_menu.entryconfig(0, state=ACTIVE)
        self.group_menu.entryconfig(1, state=DISABLED)
        self.group_menu.entryconfig(2, state=DISABLED)
      try:
          self.group_menu.tk_popup(event.x_root , event.y_root)
      finally:
          self.group_menu.grab_release()

  def group_window(self, title):
    global group_window
    command_function = self.add_group
    group_window = Toplevel(root)
    group_window.title(title)
    group_window.geometry('400x180')
    group_window.grid_columnconfigure((0,1), weight=1)

    self.group_label = ttk.Label(group_window, text='Name: ').grid(row=1, column=0, pady=20, sticky=E)
    self.group_text = StringVar()
    self.group_entry = ttk.Entry(group_window, textvariable=self.group_text).grid(row=1, column=1, sticky=W)
    if title == 'Edit Group':
      command_function = self.edit_group
      self.group_text.set(selected_group['text'])
    self.add_button = ttk.Button(group_window, text="OK", width='10', command=command_function).grid(row=2, column=0)
    self.cancel_button = ttk.Button(group_window, text="Cancel", width='10', command=lambda: self.cancel_action(group_window)).grid(row=2, column=1, padx=10)

  def add_group(self):
    folder_id = '';
    if len(group_iid) > 0:
      folder_id = group_iid[0]
    db_groups.insert(self.group_text.get(), folder_id, None)
    self.populate_groups()
    group_window.destroy()

  def delete_group(self):
    db_groups.remove(group_iid[0])
    self.populate_groups()

  def edit_group(self):
    db_groups.update(self.group_text.get(), group_iid[0])
    self.populate_groups()
    group_window.destroy()

  '''Entry TreeView Functions'''

  def populate_entries(self):
    self.clear_treeview(self.entry_treeview)
    if 'group_iid' in globals() and len(group_iid) > 0:
      entries = db_entries.fetch(group_iid[0])
      for row in entries:
        self.entry_treeview.insert('', 'end', values=row[1:4], iid=row[0])

  def select_entry(self, event):
    global entry_iid, selected_entry
    entry_iid = self.entry_treeview.selection()
    selected_entry = {'values': ''}
    if self.entry_treeview.selection():
      current_entry = self.entry_treeview.focus()
      selected_entry = self.entry_treeview.item(current_entry)

  def add_entry_menu(self, event):
    if 'group_iid' in globals():
      if len(group_iid) == 0:
        self.entry_menu.entryconfig(0, state=DISABLED)
        self.entry_menu.entryconfig(1, state=DISABLED)
        self.entry_menu.entryconfig(2, state=DISABLED)
      else:
        if 'entry_iid' in globals():
          if len(entry_iid) > 0:
            self.entry_menu.entryconfig(0, state=DISABLED)
            self.entry_menu.entryconfig(1, state=ACTIVE)
            self.entry_menu.entryconfig(2, state=ACTIVE)
          else:
            self.entry_menu.entryconfig(0, state=ACTIVE)
            self.entry_menu.entryconfig(1, state=DISABLED)
            self.entry_menu.entryconfig(2, state=DISABLED)
        else:
          self.entry_menu.entryconfig(0, state=ACTIVE)
          self.entry_menu.entryconfig(1, state=DISABLED)
          self.entry_menu.entryconfig(2, state=DISABLED)
      try:
          self.entry_menu.tk_popup(event.x_root , event.y_root)
      finally:
          self.entry_menu.grab_release()

  def entry_window(self, title):
    global entry_window
    command_function = self.add_entry
    entry_window = Toplevel(root)
    entry_window.title(title)
    entry_window.geometry('500x250')
    # Frames
    input_frame = ttk.Frame(entry_window)
    input_frame.pack(side=TOP)
    button_frame = ttk.Frame(entry_window)
    button_frame.pack()
    # Create entry input fields
    name_label = ttk.Label(input_frame, text='Name: ')
    name_label.grid(row=1, column=0)
    self.name_text = StringVar()
    name_entry = ttk.Entry(input_frame, textvariable=self.name_text, width='50')
    name_entry.grid(row=1, column=1, pady=5)
    login_label = ttk.Label(input_frame, text='Login: ')
    login_label.grid(row=2, column=0)
    self.login_text = StringVar()
    login_entry = ttk.Entry(input_frame, textvariable=self.login_text, width='50')
    login_entry.grid(row=2, column=1, pady=5)
    password_label = ttk.Label(input_frame, text='Password: ')
    password_label.grid(row=3, column=0)
    self.password_text = StringVar()
    password_entry = ttk.Entry(input_frame, textvariable=self.password_text, width='50')
    password_entry.grid(row=3, column=1, pady=5)

    if title == 'Edit Entry':
      command_function = self.edit_entry
      self.name_text.set(selected_entry['values'][0])
      self.login_text.set(selected_entry['values'][1])
      self.password_text.set(selected_entry['values'][2])

    add_button = ttk.Button(button_frame, text="OK", width='10', command=command_function)
    add_button.grid(row=1, column=0, pady=20, padx=10)
    cancel_button = ttk.Button(button_frame, text="Cancel", width='10', command=lambda: self.cancel_action(entry_window))
    cancel_button.grid(row=1, column=1, padx=10)

  def add_entry(self):
    db_entries.insert(self.name_text.get(), self.login_text.get(), self.password_text.get(), group_iid[0])
    self.populate_entries()
    entry_window.destroy()

  def delete_entry(self):
    db_entries.remove(self.entry_treeview.selection()[0])
    self.populate_entries()

  def edit_entry(self):
    db_entries.update(self.name_text.get(), self.login_text.get(), self.password_text.get(), entry_iid[0])
    self.populate_entries()
    entry_window.destroy()

  '''Generic Functions'''

  def info_window(self, title, content):
    global entry_window
    info_window = Toplevel(root)
    info_window.title(title)
    info_window.geometry('400x200')
    info_window.resizable(0, 0)
    # Frames
    info_frame = ttk.Frame(info_window)
    info_frame.pack(side=TOP)
    info_button_frame = ttk.Frame(info_window)
    info_button_frame.pack()
    # Multiline text
    text = Text(info_frame, height=8, width=50)
    scroll = ttk.Scrollbar(info_frame, orient=VERTICAL)
    text.configure(yscrollcommand=scroll.set)
    text.pack(side=LEFT)
    scroll.config(command=text.yview)
    scroll.pack(side=RIGHT, fill=Y)
    text.insert(END, content)

    info_button = ttk.Button(info_button_frame, text="OK", width='10', command=lambda: self.cancel_action(info_window))
    info_button.pack(pady=10)

  def clear_treeview(self, treeview):
    for item in treeview.get_children():
      treeview.delete(item)

  def cancel_action(self, window):
    window.destroy()

''' MAIN '''
if __name__ == '__main__':
  root = Tk()
  application = Pass_Manager(root)
  # Start
  root.mainloop()
