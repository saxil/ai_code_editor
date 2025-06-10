from tkinter import *
from tkinter import messagebox
import webbrowser
from tkinter.filedialog import askopenfile, asksaveasfile
root=Tk("Text Editor")
def openfile():
    file=askopenfile(parent=root,title="Select a file",filetypes=(("Text files","*.txt"),("All files","*.*")))
    if file!=None:
        contents=file.read()
        text.insert('1.0',contents)
        file.close()

def save():
    # pass
    file = asksaveasfile(mode='w', defaultextension=".txt",filetypes=(("Text files", "*.txt"), ("All files", "*.*")))
    if file is None:
        return
header=Label(root,text="Simple Text Editor",font=("Arial",20,"bold"))
header.grid(row=0,column=0)
text=Text(root)
text.grid()
# buttonb=Button(root,text="Save",command=save,relief="ridge").grid(row=100,column=0)
# Creating Menubar 
menubar = Menu(root) 
  
# Adding File Menu and commands 
file = Menu(menubar, tearoff = 0) 
menubar.add_cascade(label ='File', menu = file) 
file.add_command(label ='New File', command = None) 
file.add_command(label ='Open...', command = openfile) 
file.add_command(label ='Save', command = save) 
file.add_separator() 
file.add_command(label ='Exit', command = root.destroy) 
  
# Adding Edit Menu and commands 
edit = Menu(menubar, tearoff = 0) 
menubar.add_cascade(label ='Edit', menu = edit) 
edit.add_command(label ='Cut', command = None) 
edit.add_command(label ='Copy', command = None) 
edit.add_command(label ='Paste', command = None) 
edit.add_command(label ='Select All', command = None) 
edit.add_separator() 
edit.add_command(label ='Find...', command = None) 
edit.add_command(label ='Find again', command = None) 
def tk_help():
    webbrowser.open_new(r"https://docs.python.org/3/library/tk.html")
def we():
    messagebox.showinfo("About Tk","Tkinter is the standard GUI library for Python. Python when combined with Tkinter provides a fast and easy way to create GUI applications. Tkinter provides a powerful object-oriented interface to the Tk GUI toolkit.")
# Adding Help Menu 
help_ = Menu(menubar, tearoff = 0) 
menubar.add_cascade(label ='Help', menu = help_) 
help_.add_command(label ='Tk Help', command =tk_help)
# help_.add_command(label ='Demo', command = None) 
help_.add_separator() 
help_.add_command(label ='About Tk', command = we) 
  
# display Menu 
root.config(menu = menubar) 
mainloop() 

root.mainloop()

