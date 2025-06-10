import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, 
                             QWidget, QPushButton, QTextEdit, QMenuBar, QMenu, 
                             QAction, QFileDialog, QMessageBox, QSplitter, 
                             QLabel, QStatusBar, QToolBar, QPlainTextEdit)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QKeySequence


class SimpleAICodeEditor(QMainWindow):
    def __init__(self):
        super().__init__()
        self.current_file = None
        self.init_ui()
        
    def init_ui(self):
        self.setWindowTitle("Simple AI Code Editor")
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
        left_layout.addWidget(QLabel("📁 File Explorer"))
        
        # Add some placeholder files
        placeholder_files = QPlainTextEdit()
        placeholder_files.setPlainText("main.py\\nutils.py\\nconfig.py\\nREADME.md")
        placeholder_files.setMaximumHeight(200)
        left_layout.addWidget(placeholder_files)
        
        left_panel.setMaximumWidth(200)
        left_panel.setStyleSheet("background-color: #f0f0f0; border: 1px solid #ccc; padding: 5px;")
        splitter.addWidget(left_panel)
        
        # Center panel (code editor)
        center_widget = QWidget()
        center_layout = QVBoxLayout(center_widget)
        
        # Code editor
        self.editor = QPlainTextEdit()
        self.setup_editor()
        center_layout.addWidget(self.editor)
        
        splitter.addWidget(center_widget)
        
        # Right panel (AI assistant)
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        
        # AI Chat area
        ai_label = QLabel("🤖 AI Assistant")
        ai_label.setStyleSheet("font-weight: bold; font-size: 14px; margin-bottom: 10px;")
        right_layout.addWidget(ai_label)
        
        self.ai_chat = QTextEdit()
        self.ai_chat.setPlaceholderText("AI suggestions and responses will appear here...")
        self.ai_chat.setMaximumHeight(300)
        self.ai_chat.setStyleSheet("border: 1px solid #ddd; border-radius: 4px; padding: 5px;")
        right_layout.addWidget(self.ai_chat)
        
        # AI input
        input_label = QLabel("Ask AI:")
        right_layout.addWidget(input_label)
        
        self.ai_input = QTextEdit()
        self.ai_input.setPlaceholderText("Ask AI for help with your code...")
        self.ai_input.setMaximumHeight(80)
        self.ai_input.setStyleSheet("border: 1px solid #ddd; border-radius: 4px; padding: 5px;")
        right_layout.addWidget(self.ai_input)
        
        # AI buttons
        ai_buttons = QVBoxLayout()
        
        self.ask_ai_btn = QPushButton("💬 Ask AI")
        self.ask_ai_btn.clicked.connect(self.ask_ai)
        self.ask_ai_btn.setStyleSheet("QPushButton { background-color: #4CAF50; color: white; border: none; padding: 8px; border-radius: 4px; } QPushButton:hover { background-color: #45a049; }")
        ai_buttons.addWidget(self.ask_ai_btn)
        
        self.generate_code_btn = QPushButton("⚡ Generate Code")
        self.generate_code_btn.clicked.connect(self.generate_code)
        self.generate_code_btn.setStyleSheet("QPushButton { background-color: #2196F3; color: white; border: none; padding: 8px; border-radius: 4px; } QPushButton:hover { background-color: #1976D2; }")
        ai_buttons.addWidget(self.generate_code_btn)
        
        self.explain_code_btn = QPushButton("📖 Explain Code")
        self.explain_code_btn.clicked.connect(self.explain_code)
        self.explain_code_btn.setStyleSheet("QPushButton { background-color: #FF9800; color: white; border: none; padding: 8px; border-radius: 4px; } QPushButton:hover { background-color: #F57C00; }")
        ai_buttons.addWidget(self.explain_code_btn)
        
        self.optimize_code_btn = QPushButton("🚀 Optimize Code")
        self.optimize_code_btn.clicked.connect(self.optimize_code)
        self.optimize_code_btn.setStyleSheet("QPushButton { background-color: #9C27B0; color: white; border: none; padding: 8px; border-radius: 4px; } QPushButton:hover { background-color: #7B1FA2; }")
        ai_buttons.addWidget(self.optimize_code_btn)
        
        right_layout.addLayout(ai_buttons)
        
        right_panel.setMaximumWidth(350)
        right_panel.setStyleSheet("background-color: #f8f8f8; border: 1px solid #ccc; padding: 10px;")
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
        self.status_bar.showMessage("Ready - Simple AI Code Editor")
        
        # Set application style
        self.setStyleSheet("""
            QMainWindow {
                background-color: #ffffff;
            }
            QMenuBar {
                background-color: #f0f0f0;
                border-bottom: 1px solid #ccc;
            }
            QMenuBar::item:selected {
                background-color: #ddd;
            }
            QToolBar {
                background-color: #f0f0f0;
                border-bottom: 1px solid #ccc;
            }
        """)
        
    def setup_editor(self):
        """Setup the code editor"""
        # Set font
        font = QFont("Consolas", 12)
        font.setFixedPitch(True)
        self.editor.setFont(font)
        
        # Set placeholder text with sample code
        sample_code = """# Welcome to Simple AI Code Editor
# Start coding here...

def hello_world():
    print('Hello, AI Code Editor!')
    return "Welcome to coding with AI assistance!"

def calculate_fibonacci(n):
    if n <= 1:
        return n
    else:
        return calculate_fibonacci(n-1) + calculate_fibonacci(n-2)

# Example usage
if __name__ == '__main__':
    message = hello_world()
    print(message)
    
    # Calculate first 10 Fibonacci numbers
    print("First 10 Fibonacci numbers:")
    for i in range(10):
        print(f"F({i}) = {calculate_fibonacci(i)}")
"""
        
        self.editor.setPlainText(sample_code)
        self.editor.setStyleSheet("border: 1px solid #ddd; border-radius: 4px; padding: 5px;")
        
    def setup_menu_bar(self):
        """Setup the menu bar"""
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu('📁 File')
        
        new_action = QAction('🆕 New', self)
        new_action.setShortcut(QKeySequence.New)
        new_action.triggered.connect(self.new_file)
        file_menu.addAction(new_action)
        
        open_action = QAction('📂 Open', self)
        open_action.setShortcut(QKeySequence.Open)
        open_action.triggered.connect(self.open_file)
        file_menu.addAction(open_action)
        
        save_action = QAction('💾 Save', self)
        save_action.setShortcut(QKeySequence.Save)
        save_action.triggered.connect(self.save_file)
        file_menu.addAction(save_action)
        
        save_as_action = QAction('💾 Save As', self)
        save_as_action.setShortcut(QKeySequence.SaveAs)
        save_as_action.triggered.connect(self.save_as_file)
        file_menu.addAction(save_as_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction('❌ Exit', self)
        exit_action.setShortcut(QKeySequence.Quit)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # Edit menu
        edit_menu = menubar.addMenu('✏️ Edit')
        
        undo_action = QAction('↶ Undo', self)
        undo_action.setShortcut(QKeySequence.Undo)
        undo_action.triggered.connect(self.editor.undo)
        edit_menu.addAction(undo_action)
        
        redo_action = QAction('↷ Redo', self)
        redo_action.setShortcut(QKeySequence.Redo)
        redo_action.triggered.connect(self.editor.redo)
        edit_menu.addAction(redo_action)
        
        edit_menu.addSeparator()
        
        copy_action = QAction('📋 Copy', self)
        copy_action.setShortcut(QKeySequence.Copy)
        copy_action.triggered.connect(self.editor.copy)
        edit_menu.addAction(copy_action)
        
        paste_action = QAction('📄 Paste', self)
        paste_action.setShortcut(QKeySequence.Paste)
        paste_action.triggered.connect(self.editor.paste)
        edit_menu.addAction(paste_action)
        
        # AI menu
        ai_menu = menubar.addMenu('🤖 AI')
        
        ask_ai_action = QAction('💬 Ask AI', self)
        ask_ai_action.triggered.connect(self.ask_ai)
        ai_menu.addAction(ask_ai_action)
        
        generate_code_action = QAction('⚡ Generate Code', self)
        generate_code_action.triggered.connect(self.generate_code)
        ai_menu.addAction(generate_code_action)
        
        explain_code_action = QAction('📖 Explain Code', self)
        explain_code_action.triggered.connect(self.explain_code)
        ai_menu.addAction(explain_code_action)
        
        optimize_code_action = QAction('🚀 Optimize Code', self)
        optimize_code_action.triggered.connect(self.optimize_code)
        ai_menu.addAction(optimize_code_action)
        
    def setup_toolbar(self):
        """Setup the toolbar"""
        toolbar = QToolBar()
        self.addToolBar(toolbar)
        
        # File operations
        new_action = QAction('🆕 New', self)
        new_action.triggered.connect(self.new_file)
        toolbar.addAction(new_action)
        
        open_action = QAction('📂 Open', self)
        open_action.triggered.connect(self.open_file)
        toolbar.addAction(open_action)
        
        save_action = QAction('💾 Save', self)
        save_action.triggered.connect(self.save_file)
        toolbar.addAction(save_action)
        
        toolbar.addSeparator()
        
        # AI operations
        ask_ai_action = QAction('💬 Ask AI', self)
        ask_ai_action.triggered.connect(self.ask_ai)
        toolbar.addAction(ask_ai_action)
        
        generate_action = QAction('⚡ Generate', self)
        generate_action.triggered.connect(self.generate_code)
        toolbar.addAction(generate_action)
        
    def new_file(self):
        """Create a new file"""
        self.editor.clear()
        self.current_file = None
        self.setWindowTitle("Simple AI Code Editor - New File")
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
                    self.editor.setPlainText(content)
                    self.current_file = file_path
                    self.setWindowTitle(f"Simple AI Code Editor - {file_path.split('/')[-1]}")
                    self.status_bar.showMessage(f"Opened: {file_path}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Could not open file: {str(e)}")
                
    def save_file(self):
        """Save the current file"""
        if self.current_file:
            try:
                with open(self.current_file, 'w', encoding='utf-8') as file:
                    file.write(self.editor.toPlainText())
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
                    file.write(self.editor.toPlainText())
                    self.current_file = file_path
                    self.setWindowTitle(f"Simple AI Code Editor - {file_path.split('/')[-1]}")
                    self.status_bar.showMessage(f"Saved: {file_path}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Could not save file: {str(e)}")
                
    def ask_ai(self):
        """Ask AI a question"""
        question = self.ai_input.toPlainText().strip()
        if not question:
            QMessageBox.information(self, "Info", "Please enter a question for the AI.")
            return
            
        # Simulate AI response
        responses = [
            "🤖 AI: That's an interesting question! In a real implementation, I would analyze your code and provide helpful suggestions.",
            "🤖 AI: I can help you with coding best practices, debugging, and optimization techniques.",
            "🤖 AI: For this feature to work with real AI, you would integrate with APIs like OpenAI, Anthropic, or run local models.",
            "🤖 AI: I notice you're working on Python code. Would you like me to suggest some improvements?",
            "🤖 AI: This is a simulated response. In production, I would provide context-aware assistance based on your code."
        ]
        
        import random
        response = random.choice(responses)
        
        self.ai_chat.append(f"👤 You: {question}")
        self.ai_chat.append(response)
        self.ai_chat.append("=" * 50)
        self.ai_input.clear()
        self.status_bar.showMessage("AI response generated")
        
    def generate_code(self):
        """Generate code based on AI input"""
        prompt = self.ai_input.toPlainText().strip()
        if not prompt:
            prompt = "Create a simple function"
            
        # Simulate code generation
        code_templates = [
            f"""# Generated code for: {prompt}
def {prompt.lower().replace(' ', '_')}():
    '''
    This function was generated by AI based on your request.
    Replace this with actual implementation.
    '''
    print("Generated function: {prompt}")
    return True

# Example usage
result = {prompt.lower().replace(' ', '_')}()
print(f"Result: {{result}}")
""",
            f"""# AI Generated Class for: {prompt}
class {prompt.title().replace(' ', '')}:
    def __init__(self):
        self.name = "{prompt}"
        
    def process(self):
        print(f"Processing: {{self.name}}")
        return "success"

# Create instance
instance = {prompt.title().replace(' ', '')}()
result = instance.process()
""",
            f"""# Generated utility function: {prompt}
import datetime

def utility_function():
    '''Generated on {{datetime.datetime.now()}}'''
    # TODO: Implement {prompt}
    pass

utility_function()
"""
        ]
        
        import random
        generated_code = random.choice(code_templates)
        
        # Insert generated code at cursor position
        cursor = self.editor.textCursor()
        cursor.insertText(generated_code)
        
        self.ai_chat.append(f"⚡ Generated code for: {prompt}")
        self.ai_input.clear()
        self.status_bar.showMessage("Code generated by AI")
        
    def explain_code(self):
        """Explain selected code"""
        cursor = self.editor.textCursor()
        selected_text = cursor.selectedText()
        
        if not selected_text:
            QMessageBox.information(self, "Info", "Please select some code to explain.")
            return
            
        # Simulate code explanation
        explanation = f"""📖 Code Explanation:

Selected code:
{selected_text}

🔍 Analysis:
This is a simulated AI explanation. In a real implementation, 
the AI would:

• Analyze the syntax and structure
• Explain what each part does
• Identify potential issues or improvements
• Suggest best practices
• Provide context about the code's purpose

💡 Suggestions:
- Consider adding docstrings for better documentation
- Use type hints for better code clarity
- Follow PEP 8 style guidelines
- Add error handling where appropriate
"""
        
        self.ai_chat.append(explanation)
        self.status_bar.showMessage("Code explanation generated")
        
    def optimize_code(self):
        """Optimize selected code"""
        cursor = self.editor.textCursor()
        selected_text = cursor.selectedText()
        
        if not selected_text:
            selected_text = self.editor.toPlainText()[:200] + "..."
            
        optimization = f"""🚀 Code Optimization Suggestions:

Analyzed code snippet:
{selected_text}

🔧 Optimization recommendations:

1. **Performance**: Use list comprehensions instead of loops where possible
2. **Memory**: Consider using generators for large datasets
3. **Readability**: Add type hints and docstrings
4. **Error Handling**: Implement try-catch blocks for robustness
5. **Security**: Validate inputs and sanitize data

💡 Example optimized pattern:
```python
# Instead of:
result = []
for item in items:
    if condition(item):
        result.append(transform(item))

# Use:
result = [transform(item) for item in items if condition(item)]
```

This is a simulated optimization. Real AI would provide 
specific suggestions based on your actual code.
"""
        
        self.ai_chat.append(optimization)
        self.status_bar.showMessage("Code optimization suggestions generated")


def main():
    app = QApplication(sys.argv)
    
    # Set application properties
    app.setApplicationName("Simple AI Code Editor")
    app.setApplicationVersion("1.0")
    
    editor = SimpleAICodeEditor()
    editor.show()
    
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
