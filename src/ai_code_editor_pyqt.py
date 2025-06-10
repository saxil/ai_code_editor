import sys
import os
from PyQt5.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, 
                             QWidget, QPushButton, QTextEdit, QMenuBar, QMenu, 
                             QAction, QFileDialog, QMessageBox, QSplitter, 
                             QLabel, QStatusBar, QToolBar)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QFont, QIcon, QKeySequence
from PyQt5.Qsci import QsciScintilla, QsciLexerPython


class AICodeEditor(QMainWindow):
    def __init__(self):
        super().__init__()
        self.current_file = None
        self.init_ui()
        
    def init_ui(self):
        self.setWindowTitle("AI Code Editor")
        self.setGeometry(100, 100, 1200, 800)
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QHBoxLayout(central_widget)
        
        # Create splitter for resizable panels
        splitter = QSplitter(Qt.Horizontal)
        main_layout.addWidget(splitter)
        
        # Left panel (file explorer - placeholder)
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        left_layout.addWidget(QLabel("File Explorer"))
        left_panel.setMaximumWidth(200)
        left_panel.setStyleSheet("background-color: #f0f0f0; border: 1px solid #ccc;")
        splitter.addWidget(left_panel)
        
        # Center panel (code editor)
        center_widget = QWidget()
        center_layout = QVBoxLayout(center_widget)
        
        # Code editor with syntax highlighting
        self.editor = QsciScintilla()
        self.setup_editor()
        center_layout.addWidget(self.editor)
        
        splitter.addWidget(center_widget)
        
        # Right panel (AI assistant)
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        
        # AI Chat area
        right_layout.addWidget(QLabel("AI Assistant"))
        self.ai_chat = QTextEdit()
        self.ai_chat.setPlaceholderText("AI suggestions and responses will appear here...")
        self.ai_chat.setMaximumHeight(300)
        right_layout.addWidget(self.ai_chat)
        
        # AI input
        self.ai_input = QTextEdit()
        self.ai_input.setPlaceholderText("Ask AI for help with your code...")
        self.ai_input.setMaximumHeight(100)
        right_layout.addWidget(self.ai_input)
        
        # AI buttons
        ai_buttons = QHBoxLayout()
        
        self.ask_ai_btn = QPushButton("Ask AI")
        self.ask_ai_btn.clicked.connect(self.ask_ai)
        ai_buttons.addWidget(self.ask_ai_btn)
        
        self.generate_code_btn = QPushButton("Generate Code")
        self.generate_code_btn.clicked.connect(self.generate_code)
        ai_buttons.addWidget(self.generate_code_btn)
        
        self.explain_code_btn = QPushButton("Explain Code")
        self.explain_code_btn.clicked.connect(self.explain_code)
        ai_buttons.addWidget(self.explain_code_btn)
        
        right_layout.addLayout(ai_buttons)
        
        right_panel.setMaximumWidth(350)
        right_panel.setStyleSheet("background-color: #f8f8f8; border: 1px solid #ccc;")
        splitter.addWidget(right_panel)
        
        # Set splitter proportions
        splitter.setSizes([200, 650, 350])
        
        # Setup menu bar
        self.setup_menu_bar()
        
        # Setup toolbar
        self.setup_toolbar()
        
        # Setup status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Ready")
        
    def setup_editor(self):
        """Setup the code editor with syntax highlighting and features"""
        # Set font
        font = QFont("Consolas", 12)
        font.setFixedPitch(True)
        self.editor.setFont(font)
        
        # Set Python lexer for syntax highlighting
        lexer = QsciLexerPython()
        lexer.setFont(font)
        self.editor.setLexer(lexer)
        
        # Editor settings
        self.editor.setMarginType(0, QsciScintilla.NumberMargin)
        self.editor.setMarginWidth(0, "0000")
        self.editor.setMarginLineNumbers(0, True)
        self.editor.setMarginsBackgroundColor(Qt.lightGray)
        
        # Current line highlighting
        self.editor.setCaretLineVisible(True)
        self.editor.setCaretLineBackgroundColor(Qt.yellow)
        
        # Set selection colors
        self.editor.setSelectionBackgroundColor(Qt.blue)
        
        # Enable brace matching
        self.editor.setBraceMatching(QsciScintilla.SloppyBraceMatch)
        
        # Enable code folding
        self.editor.setFolding(QsciScintilla.BoxedTreeFoldingStyle)
        
        # Auto-indentation
        self.editor.setAutoIndent(True)
        self.editor.setIndentationsUseTabs(False)
        self.editor.setIndentationWidth(4)
        
        # Enable auto-completion
        self.editor.setAutoCompletionSource(QsciScintilla.AcsAll)
        self.editor.setAutoCompletionThreshold(1)
        
        # Set placeholder text
        self.editor.setText("# Welcome to AI Code Editor\\n# Start coding here...\\n\\ndef hello_world():\\n    print('Hello, AI Code Editor!')\\n\\nif __name__ == '__main__':\\n    hello_world()")
        
    def setup_menu_bar(self):
        """Setup the menu bar"""
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu('File')
        
        new_action = QAction('New', self)
        new_action.setShortcut(QKeySequence.New)
        new_action.triggered.connect(self.new_file)
        file_menu.addAction(new_action)
        
        open_action = QAction('Open', self)
        open_action.setShortcut(QKeySequence.Open)
        open_action.triggered.connect(self.open_file)
        file_menu.addAction(open_action)
        
        save_action = QAction('Save', self)
        save_action.setShortcut(QKeySequence.Save)
        save_action.triggered.connect(self.save_file)
        file_menu.addAction(save_action)
        
        save_as_action = QAction('Save As', self)
        save_as_action.setShortcut(QKeySequence.SaveAs)
        save_as_action.triggered.connect(self.save_as_file)
        file_menu.addAction(save_as_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction('Exit', self)
        exit_action.setShortcut(QKeySequence.Quit)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # Edit menu
        edit_menu = menubar.addMenu('Edit')
        
        undo_action = QAction('Undo', self)
        undo_action.setShortcut(QKeySequence.Undo)
        undo_action.triggered.connect(self.editor.undo)
        edit_menu.addAction(undo_action)
        
        redo_action = QAction('Redo', self)
        redo_action.setShortcut(QKeySequence.Redo)
        redo_action.triggered.connect(self.editor.redo)
        edit_menu.addAction(redo_action)
        
        # AI menu
        ai_menu = menubar.addMenu('AI')
        
        ask_ai_action = QAction('Ask AI', self)
        ask_ai_action.triggered.connect(self.ask_ai)
        ai_menu.addAction(ask_ai_action)
        
        generate_code_action = QAction('Generate Code', self)
        generate_code_action.triggered.connect(self.generate_code)
        ai_menu.addAction(generate_code_action)
        
        explain_code_action = QAction('Explain Code', self)
        explain_code_action.triggered.connect(self.explain_code)
        ai_menu.addAction(explain_code_action)
        
    def setup_toolbar(self):
        """Setup the toolbar"""
        toolbar = QToolBar()
        self.addToolBar(toolbar)
        
        # File operations
        new_action = QAction('New', self)
        new_action.triggered.connect(self.new_file)
        toolbar.addAction(new_action)
        
        open_action = QAction('Open', self)
        open_action.triggered.connect(self.open_file)
        toolbar.addAction(open_action)
        
        save_action = QAction('Save', self)
        save_action.triggered.connect(self.save_file)
        toolbar.addAction(save_action)
        
        toolbar.addSeparator()
        
        # AI operations
        ask_ai_action = QAction('Ask AI', self)
        ask_ai_action.triggered.connect(self.ask_ai)
        toolbar.addAction(ask_ai_action)
        
    def new_file(self):
        """Create a new file"""
        self.editor.clear()
        self.current_file = None
        self.setWindowTitle("AI Code Editor - New File")
        self.status_bar.showMessage("New file created")
        
    def open_file(self):
        """Open a file"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Open File", "", 
            "Python Files (*.py);;Text Files (*.txt);;All Files (*)"
        )
        
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()
                    self.editor.setText(content)
                    self.current_file = file_path
                    self.setWindowTitle(f"AI Code Editor - {os.path.basename(file_path)}")
                    self.status_bar.showMessage(f"Opened: {file_path}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Could not open file: {str(e)}")
                
    def save_file(self):
        """Save the current file"""
        if self.current_file:
            try:
                with open(self.current_file, 'w', encoding='utf-8') as file:
                    file.write(self.editor.text())
                    self.status_bar.showMessage(f"Saved: {self.current_file}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Could not save file: {str(e)}")
        else:
            self.save_as_file()
            
    def save_as_file(self):
        """Save the file with a new name"""
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Save File", "", 
            "Python Files (*.py);;Text Files (*.txt);;All Files (*)"
        )
        
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as file:
                    file.write(self.editor.text())
                    self.current_file = file_path
                    self.setWindowTitle(f"AI Code Editor - {os.path.basename(file_path)}")
                    self.status_bar.showMessage(f"Saved: {file_path}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Could not save file: {str(e)}")
                
    def ask_ai(self):
        """Ask AI a question"""
        question = self.ai_input.toPlainText().strip()
        if not question:
            QMessageBox.information(self, "Info", "Please enter a question for the AI.")
            return
            
        # Simulate AI response (replace with actual AI integration)
        self.ai_chat.append(f"You: {question}")
        self.ai_chat.append("AI: I'm a simulated AI response. In a real implementation, this would connect to an AI service like OpenAI's API, local LLM, or other AI models.")
        self.ai_input.clear()
        self.status_bar.showMessage("AI response generated")
        
    def generate_code(self):
        """Generate code based on AI input"""
        prompt = self.ai_input.toPlainText().strip()
        if not prompt:
            QMessageBox.information(self, "Info", "Please enter a code generation prompt.")
            return
            
        # Simulate code generation (replace with actual AI integration)
        generated_code = f"""# Generated code based on: {prompt}
def example_function():
    '''This is a simulated code generation.
    In a real implementation, this would use AI to generate actual code.'''
    print("Generated by AI")
    return "success"

# Call the function
result = example_function()
print(result)
"""
        
        # Insert generated code at cursor position
        cursor_position = self.editor.getCursorPosition()
        self.editor.insertAt(generated_code, cursor_position[0], cursor_position[1])
        
        self.ai_chat.append(f"Generated code for: {prompt}")
        self.ai_input.clear()
        self.status_bar.showMessage("Code generated by AI")
        
    def explain_code(self):
        """Explain selected code"""
        selected_text = self.editor.selectedText()
        if not selected_text:
            QMessageBox.information(self, "Info", "Please select some code to explain.")
            return
            
        # Simulate code explanation (replace with actual AI integration)
        explanation = f"""Code Explanation:
Selected code: {selected_text}

This is a simulated explanation. In a real implementation, 
the AI would analyze the selected code and provide a detailed 
explanation of what it does, how it works, and any potential 
improvements or issues.
"""
        
        self.ai_chat.append(explanation)
        self.status_bar.showMessage("Code explanation generated")


def main():
    app = QApplication(sys.argv)
    editor = AICodeEditor()
    editor.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
