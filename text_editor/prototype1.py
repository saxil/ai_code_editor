from tkinter import *
from tkinter import messagebox
import webbrowser
from tkinter.filedialog import askopenfile, asksaveasfile
import keyword

root = Tk()
root.title("Simple Text Editor")
root.resizable(True, True)
root.iconphoto(TRUE, PhotoImage(file='Text_editor\cursor-text.png'))
def openfile():
    file = askopenfile(parent=root, title="Select a file", filetypes=(("Python files", "*.py"), ("All files", "*.*")))
    if file != None:
        filename = file.name
        if filename.endswith('.py'):
            contents = file.read()
            text.insert('1.0', contents)
            highlight_keywords()
        else:
            messagebox.showwarning("Invalid File", "Please select a Python file (.py)")
        file.close()

def save():
    file = asksaveasfile(mode='w', defaultextension=".txt", filetypes=(("Text files", "*.txt"), ("All files", "*.*")))
    if file is None:
        return

def highlight_keywords():
    text.tag_remove("keyword", "1.0", "end")
    for word in text.get("1.0", "end").split():
        if word in keyword.kwlist:
            start = "1.0"
            while True:
                pos = text.search(word, start, stopindex="end")
                if not pos:
                    break
                start = f"{pos}+{len(word)}c"
                text.tag_add("keyword", pos, f"{pos}+{len(word)}c")
            text.tag_config("keyword", foreground="blue")

def cut_text():
    text.event_generate("<<Cut>>")

def copy_text():
    text.event_generate("<<Copy>>")

def paste_text():
    text.event_generate("<<Paste>>")

def select_all():
    text.tag_add("sel", "1.0", "end")

def find_text():
    # Implement your find functionality here
    pass

def find_again():
    # Implement your find again functionality here
    pass

# header = Label(root, text="Simple Text Editor", font=("Arial", 20, "bold"))
# header.grid(row=0, column=0)
text = Text(root)
text.grid()

menubar = Menu(root)
file = Menu(menubar, tearoff=0)
menubar.add_cascade(label='File', menu=file)
file.add_command(label='New File', command=None)
file.add_command(label='Open...', command=openfile)
file.add_command(label='Save', command=save)
file.add_separator()
file.add_command(label='Exit', command=root.destroy)

edit = Menu(menubar, tearoff=0)
menubar.add_cascade(label='Edit', menu=edit)
edit.add_command(label='Cut', command=cut_text)
edit.add_command(label='Copy', command=copy_text)
edit.add_command(label='Paste', command=paste_text)
edit.add_command(label='Select All', command=select_all)
edit.add_separator()
edit.add_command(label='Find...', command=find_text)
edit.add_command(label='Find again', command=find_again)

def tk_help():
    webbrowser.open_new(r"https://docs.python.org/3/library/tk.html")

def we():
    messagebox.showinfo("About Tk", "Tkinter is the standard GUI library for Python. Python when combined with Tkinter provides a fast and easy way to create GUI applications. Tkinter provides a powerful object-oriented interface to the Tk GUI toolkit.")

help_ = Menu(menubar, tearoff=0)
menubar.add_cascade(label='Help', menu=help_)
help_.add_command(label='Tk Help', command=tk_help)
help_.add_separator()
help_.add_command(label='About Tk', command=we)

root.config(menu=menubar)

text.bind("<KeyRelease>", lambda event: highlight_keywords())

mainloop()
