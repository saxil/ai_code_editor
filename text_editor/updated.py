from tkinter import *
from tkinter import messagebox, filedialog, TclError
import webbrowser
import keyword
import re

class TextEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Simple Text Editor")
        self.root.geometry("800x600")
        self.create_widgets()
        self.text.edit_modified(False)  # Reset modified flag on initialization
        
    def create_widgets(self):
        self.create_menu()
        self.create_text_editor()
        self.create_line_numbers()
        self.create_context_menu()
        
    def create_menu(self):
        menubar = Menu(self.root)
        
        file_menu = Menu(menubar, tearoff=0)
        file_menu.add_command(label="Open...", command=self.open_file, accelerator="Ctrl+O")
        file_menu.add_command(label="Save", command=self.save_file, accelerator="Ctrl+S")
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit, accelerator="Ctrl+W")
        menubar.add_cascade(label="File", menu=file_menu)

        edit_menu = Menu(menubar, tearoff=0)
        edit_menu.add_command(label="Cut", command=self.cut_text, accelerator="Ctrl+X")
        edit_menu.add_command(label="Copy", command=self.copy_text, accelerator="Ctrl+C")
        edit_menu.add_command(label="Paste", command=self.paste_text, accelerator="Ctrl+V")
        edit_menu.add_command(label="Select All", command=self.select_all, accelerator="Ctrl+A")
        edit_menu.add_command(label="Undo", command=self.undo, accelerator="Ctrl+Z")
        edit_menu.add_command(label="Redo", command=self.redo, accelerator="Ctrl+Y")
        menubar.add_cascade(label="Edit", menu=edit_menu)

        help_menu = Menu(menubar, tearoff=0)
        help_menu.add_command(label="Tkinter Help", command=self.open_tkinter_help)
        help_menu.add_command(label="About Tkinter", command=self.about_tkinter)
        menubar.add_cascade(label="Help", menu=help_menu)

        self.root.config(menu=menubar)
        
        self.root.bind_all("<Control-x>", self.cut_text)
        self.root.bind_all("<Control-c>", self.copy_text)
        self.root.bind_all("<Control-v>", self.paste_text)
        self.root.bind_all("<Control-a>", self.select_all)
        self.root.bind_all("<Control-z>", self.undo)
        self.root.bind_all("<Control-y>", self.redo)
    
    def create_text_editor(self):
        self.text_frame = Frame(self.root)
        self.text_frame.pack(side="right", fill="both", expand=True)
        
        self.scrollbar_y = Scrollbar(self.text_frame, orient="vertical")
        self.scrollbar_y.pack(side="right", fill="y")

        self.text = Text(self.text_frame, wrap="none", undo=True, yscrollcommand=self.sync_scroll_y, bg="#2E3440", fg="#D8DEE9", insertbackground="#D8DEE9")
        self.text.pack(side="left", fill="both", expand=True)
        self.scrollbar_y.config(command=self.scroll_y)
        
        # Bind events after creating the text widget
        self.text.bind("<Key>", self.on_text_changed)
        self.text.bind("<MouseWheel>", self.on_text_changed)
    
    def create_line_numbers(self):
        self.line_numbers = Text(self.root, width=4, bg="#3B4252", fg="#D8DEE9", state="disabled", wrap="none")
        self.line_numbers.pack(side="left", fill="y")
        self.update_line_numbers()
    
    def update_line_numbers(self, *args):
        self.line_numbers.config(state="normal")
        self.line_numbers.delete(1.0, "end")
        lines = self.text.get("1.0", "end-1c").split('\n')
        line_numbers_str = '\n'.join(f'{i+1}' for i in range(len(lines)))
        self.line_numbers.insert("1.0", line_numbers_str)
        self.line_numbers.config(state="disabled")
        
    def sync_scroll_y(self, *args):
        self.scrollbar_y.set(*args)
        self.line_numbers.yview_moveto(args[0])
    
    def scroll_y(self, *args):
        self.text.yview(*args)
        self.line_numbers.yview(*args)

    def create_context_menu(self):
        self.context_menu = Menu(self.text, tearoff=0)
        self.context_menu.add_command(label="Cut", command=self.cut_text)
        self.context_menu.add_command(label="Copy", command=self.copy_text)
        self.context_menu.add_command(label="Paste", command=self.paste_text)
        self.context_menu.add_command(label="Select All", command=self.select_all)
        self.context_menu.add_command(label="Undo", command=self.undo)
        self.context_menu.add_command(label="Redo", command=self.redo)
        self.context_menu.add_separator()
        self.context_menu.add_command(label="Save", command=self.save_file, accelerator="Ctrl+S")
        self.text.bind("<Button-3>", self.show_context_menu)
    
    def show_context_menu(self, event):
        self.context_menu.post(event.x_root, event.y_root)
        
    def open_file(self):
        file_path = filedialog.askopenfilename(filetypes=(("Python files", "*.py"), ("Text files", "*.txt"), ("All files", "*.*")))
        if file_path:
            with open(file_path, "r") as file:
                content = file.read()
                self.text.delete('1.0', END)
                self.text.insert('1.0', content)
                self.highlight_syntax()
                self.update_line_numbers()
    
    def save_file(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=(("Python files", "*.py,*.ipynb,*.pyw"), ("Text files", "*.txt"), ("All files", "*.*")))
        if file_path:
            with open(file_path, "w") as file:
                content = self.text.get(1.0, END)
                file.write(content)
    
    def highlight_syntax(self):
        self.text.tag_remove("keyword", "1.0", "end")
        self.text.tag_remove("string", "1.0", "end")
        self.text.tag_remove("comment", "1.0", "end")
        
        keywords_pattern = r'\b(?:' + '|'.join(keyword.kwlist) + r')\b'
        strings_pattern = r'(\".*?\"|\'.*?\')'
        comments_pattern = r'(#.*?$)'

        text = self.text.get("1.0", "end-1c")

        for match in re.finditer(keywords_pattern, text, re.MULTILINE):
            start, end = match.span()
            start_index = f"1.0 + {start} chars"
            end_index = f"1.0 + {end} chars"
            self.text.tag_add("keyword", start_index, end_index)
        
        for match in re.finditer(strings_pattern, text, re.MULTILINE):
            start, end = match.span()
            start_index = f"1.0 + {start} chars"