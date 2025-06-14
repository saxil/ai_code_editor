# === Ollama PyQt5 Code Editor ===
#
# Description:
# This script creates a simple desktop application using PyQt5 that provides a basic
# code editor interface to send code/prompts to an Ollama API endpoint and display
# the response. It's a standalone alternative to a web-based UI for interacting
# with local Ollama models.
#
# --- Python Environment Setup ---
# You need to have Python installed. Then, install the necessary libraries:
#   pip install PyQt5
#   pip install requests
#
# --- Ollama Setup ---
# 1. Install and run Ollama:
#    - Download and install Ollama from https://ollama.com/
#    - Ensure the Ollama service is running. You can usually start it by running
#      `ollama serve` in your terminal or by launching the Ollama Desktop application.
# 2. Verify Ollama API accessibility:
#    - By default, Ollama's API is accessible at http://localhost:11434.
#    - You can test this by opening this URL in your browser or using a tool like curl.
#      (e.g., `curl http://localhost:11434/api/tags`)
#
# --- Configuration ---
# 1. Model Name:
#    - Open this script (`main_qt.py`) in a text editor.
#    - Locate the `on_run_button_clicked` method within the `CodeEditorWindow` class.
#    - Find the line:
#      `ollama_response = send_code_to_ollama(code_to_send, model_name="your-ollama-coding-model-name")`
#    - Change `"your-ollama-coding-model-name"` to the actual name of the Ollama model
#      you have pulled and wish to use (e.g., "codellama:7b", "llama3", "mistral").
#    - You can list your available models by running `ollama list` in your terminal.
#
# 2. Ollama API URL (Optional):
#    - If your Ollama instance is running on a different host or port, you'll need to
#      update the `ollama_api_url` variable inside the `send_code_to_ollama` function.
#      Default: `ollama_api_url = "http://localhost:11434/api/generate"`
#
# --- Running the Script ---
# Save this file as `main_qt.py` (or any other .py name).
# Open your terminal or command prompt, navigate to the directory where you saved the file,
# and run the script using Python:
#   python main_qt.py
#
# --- Packaging (Optional Summary) ---
# To create a standalone executable from this script, you can use PyInstaller:
# 1. Install PyInstaller: `pip install pyinstaller`
# 2. Run PyInstaller from your terminal in the same directory as the script:
#    `pyinstaller --onefile --windowed --name OllamaCodeEditor main_qt.py`
#    - `--onefile`: Creates a single executable file.
#    - `--windowed`: Prevents a console window from appearing when running the GUI.
#    - `--name OllamaCodeEditor`: Sets the name of your executable.
# The executable will be found in a `dist` subdirectory.
# Note: Packaging can sometimes be complex, especially with libraries like PyQt5.
# Additional hooks or configurations might be needed for PyInstaller in some cases.
#
# === End of Instructions ===

import sys
import os
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QTextEdit, QPushButton, QHBoxLayout, QSplitter, 
                             QLabel, QComboBox, QStatusBar, QFrame)
from PyQt5.QtGui import QIcon, QFont, QSyntaxHighlighter, QTextCharFormat, QColor, QPalette
from PyQt5.QtCore import QRegExp, Qt
from PyQt5.Qsci import QsciScintilla, QsciLexerPython
import requests # For making HTTP requests
import json     # For handling JSON data

# --- Explanation of Core PyQt5 Concepts ---
# QApplication: Manages the GUI application's control flow and main settings.
#               Every PyQt5 application must have exactly one QApplication instance.
# QMainWindow: Represents the main window of the application. It can have menus, toolbars, a status bar, and a central widget.
# QWidget: The base class for all user interface objects. If you're creating a custom UI component or a simple window without QMainWindow features, you might use QWidget directly.
# QVBoxLayout: A layout manager that arranges widgets vertically. PyQt5 uses layouts to manage the size and position of widgets within a window.
# ---

# --- Explanation of PyQt5 Signals and Slots ---
# Signals and Slots are a core feature of PyQt5 (and Qt) for communication between objects.
# - A signal is emitted when a particular event occurs (e.g., a button is clicked).
# - A slot is a function (or method) that can be connected to a signal. When the signal is emitted, the connected slot is called.
# Example: self.runButton.clicked.connect(self.on_run_button_clicked)
#   - `self.runButton.clicked` is a signal emitted when the button is clicked.
#   - `self.on_run_button_clicked` is the slot (a method we will define) that will be executed.
# ---

# --- Explanation of PyQt5 Stylesheets ---
# PyQt5 allows styling widgets using stylesheets, similar to CSS.
# - You can apply stylesheets to the entire application, specific windows, or individual widgets.
# - Stylesheets are strings containing style rules.
# - Rules consist of a selector (e.g., 'QWidget', 'QPushButton', '#myWidgetId') and declarations (e.g., 'background-color: blue; color: white;').
# - Common properties include: background-color, color, font-size, border, padding, margin.
# - To apply a stylesheet to a widget: widget.setStyleSheet("your style rules")
# - To apply to the whole application: app.setStyleSheet("your style rules")
# ---

class PythonSyntaxHighlighter(QSyntaxHighlighter):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Define syntax highlighting rules
        self.highlighting_rules = []
        
        # Keywords
        keyword_format = QTextCharFormat()
        keyword_format.setColor(QColor(86, 156, 214))  # VS Code blue
        keyword_format.setFontWeight(QFont.Bold)
        keywords = ['and', 'as', 'assert', 'break', 'class', 'continue', 'def',
                   'del', 'elif', 'else', 'except', 'exec', 'finally', 'for',
                   'from', 'global', 'if', 'import', 'in', 'is', 'lambda',
                   'not', 'or', 'pass', 'print', 'raise', 'return', 'try',
                   'while', 'with', 'yield']
        for word in keywords:
            pattern = QRegExp(r'\b' + word + r'\b')
            self.highlighting_rules.append((pattern, keyword_format))
        
        # Strings
        string_format = QTextCharFormat()
        string_format.setColor(QColor(206, 145, 120))  # VS Code orange
        self.highlighting_rules.append((QRegExp(r'".*"'), string_format))
        self.highlighting_rules.append((QRegExp(r"'.*'"), string_format))
        
        # Comments
        comment_format = QTextCharFormat()
        comment_format.setColor(QColor(106, 153, 85))  # VS Code green
        comment_format.setFontItalic(True)
        self.highlighting_rules.append((QRegExp(r'#.*'), comment_format))
        
        # Numbers
        number_format = QTextCharFormat()
        number_format.setColor(QColor(181, 206, 168))  # VS Code light green
        self.highlighting_rules.append((QRegExp(r'\b\d+\b'), number_format))
    
    def highlightBlock(self, text):
        for pattern, format in self.highlighting_rules:
            expression = QRegExp(pattern)
            index = expression.indexIn(text)
            while index >= 0:
                length = expression.matchedLength()
                self.setFormat(index, length, format)
                index = expression.indexIn(text, index + length)


class ModernCodeEditor(QsciScintilla):
    def __init__(self):
        super().__init__()
        
        # Set lexer for Python syntax highlighting
        lexer = QsciLexerPython()
        self.setLexer(lexer)
        
        # Set font
        font = QFont('Consolas', 12)
        font.setFamily('Consolas')
        font.setFixedPitch(True)
        font.setPointSize(12)
        self.setFont(font)
        
        # Set margin for line numbers
        self.setMarginType(0, QsciScintilla.NumberMargin)
        self.setMarginWidth(0, "0000")
        self.setMarginLineNumbers(0, True)
        self.setMarginsBackgroundColor(QColor(30, 30, 30))
        self.setMarginsForegroundColor(QColor(128, 128, 128))
        
        # Current line highlighting
        self.setCaretLineVisible(True)
        self.setCaretLineBackgroundColor(QColor(45, 45, 45))
        
        # Set selection colors
        self.setSelectionBackgroundColor(QColor(38, 79, 120))
        
        # Enable brace matching
        self.setBraceMatching(QsciScintilla.SloppyBraceMatch)
        
        # Set colors for dark theme
        self.setColor(QColor(212, 212, 212))  # Text color
        self.setPaper(QColor(30, 30, 30))     # Background color
        
        # Set indentation
        self.setIndentationsUseTabs(False)
        self.setIndentationWidth(4)
        self.setTabWidth(4)
        self.setAutoIndent(True)


class CodeEditorWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Ollama Code Editor - VS Code Style")
        self.setGeometry(100, 100, 1200, 800)
        
        # Set window icon
        icon_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "app_icon.png")
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))

        # Set up the UI
        self.init_ui()
        self.apply_dark_theme()

    def init_ui(self):
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main vertical layout
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)
        
        # Top toolbar
        toolbar_layout = QHBoxLayout()
        
        # Model selection
        model_label = QLabel("Model:")
        model_label.setStyleSheet("color: #ffffff; font-weight: bold;")
        self.model_combo = QComboBox()
        self.model_combo.addItems(["codellama:7b", "llama3", "mistral", "deepseek-coder"])
        self.model_combo.setCurrentText("codellama:7b")
        self.model_combo.setStyleSheet("""
            QComboBox {
                background-color: #3c3c3c;
                color: white;
                border: 1px solid #555;
                padding: 5px;
                border-radius: 3px;
            }
            QComboBox::drop-down {
                border: none;
            }
            QComboBox::down-arrow {
                border: none;
            }
        """)
        
        toolbar_layout.addWidget(model_label)
        toolbar_layout.addWidget(self.model_combo)
        toolbar_layout.addStretch()
        
        # Run button in toolbar
        self.runButton = QPushButton("▶ Run Code")
        self.runButton.setObjectName("runButton")
        self.runButton.clicked.connect(self.on_run_button_clicked)
        toolbar_layout.addWidget(self.runButton)
        
        main_layout.addLayout(toolbar_layout)
        
        # Create splitter for resizable panes
        splitter = QSplitter(Qt.Horizontal)
        
        # Left pane - Code input
        left_pane = QWidget()
        left_layout = QVBoxLayout()
        left_pane.setLayout(left_layout)
        
        input_label = QLabel("Code Input")
        input_label.setStyleSheet("color: #ffffff; font-weight: bold; padding: 5px;")
        left_layout.addWidget(input_label)
        
        # Use modern code editor
        self.codeInput = ModernCodeEditor()
        self.codeInput.setText("# Enter your Python code here\nprint('Hello, Ollama!')")
        left_layout.addWidget(self.codeInput)
        
        # Right pane - Output
        right_pane = QWidget()
        right_layout = QVBoxLayout()
        right_pane.setLayout(right_layout)
        
        output_label = QLabel("AI Response")
        output_label.setStyleSheet("color: #ffffff; font-weight: bold; padding: 5px;")
        right_layout.addWidget(output_label)
        
        self.outputArea = QTextEdit()
        self.outputArea.setReadOnly(True)
        self.outputArea.setPlaceholderText("Ollama's response will appear here...")
        right_layout.addWidget(self.outputArea)
        
        # Add panes to splitter
        splitter.addWidget(left_pane)
        splitter.addWidget(right_pane)
        splitter.setSizes([600, 600])  # Equal split initially
        
        main_layout.addWidget(splitter)
        
        # Status bar
        self.status_bar = QStatusBar()
        self.status_bar.showMessage("Ready - Select a model and enter your code")
        self.setStatusBar(self.status_bar)

    def apply_dark_theme(self):
        """Apply VS Code-like dark theme"""
        self.setStyleSheet("""
            QMainWindow {
                background-color: #1e1e1e;
                color: #ffffff;
            }
            QWidget {
                background-color: #1e1e1e;
                color: #ffffff;
            }
            QTextEdit {
                background-color: #1e1e1e;
                color: #d4d4d4;
                border: 1px solid #3c3c3c;
                font-family: 'Consolas', 'Monaco', monospace;
                font-size: 14px;
                padding: 10px;
            }
            QPushButton#runButton {
                background-color: #0e639c;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton#runButton:hover {
                background-color: #1177bb;
            }
            QPushButton#runButton:pressed {
                background-color: #0d5a87;
            }
            QStatusBar {
                background-color: #007acc;
                color: white;
                border: none;
            }
            QSplitter::handle {
                background-color: #3c3c3c;
                width: 2px;
            }
            QSplitter::handle:hover {
                background-color: #007acc;
            }
        """)
    
    def on_run_button_clicked(self):
        """Send code to Ollama and display response"""
        code_to_send = self.codeInput.text()
        if not code_to_send.strip():
            self.outputArea.setText("Please enter some code.")
            self.status_bar.showMessage("No code to send")
            return

        self.status_bar.showMessage("Sending to Ollama... Please wait.")
        self.outputArea.setText("🤖 Sending to Ollama... Please wait.")
        QApplication.processEvents()

        model_name = self.model_combo.currentText()
        ollama_response = send_code_to_ollama(code_to_send, model_name=model_name)

        if "error" in ollama_response:
            self.outputArea.setText(f"❌ Error: {ollama_response['error']}")
            self.status_bar.showMessage("Error occurred")
        elif "response" in ollama_response:
            self.outputArea.setText(f"🤖 AI Response:\n\n{ollama_response['response']}")
            self.status_bar.showMessage("Response received successfully")
        else:
            self.outputArea.setText(f"⚠️ Unexpected response from Ollama:\n\n{json.dumps(ollama_response, indent=2)}")
            self.status_bar.showMessage("Unexpected response format")


# --- Explanation of 'requests' library ---
# The 'requests' library is a popular third-party Python library for making HTTP requests.
# It simplifies the process of sending GET, POST, etc., requests and handling responses.
# You'll need to install it if you haven't already: pip install requests
# Key methods used:
#   requests.post(url, json=payload): Sends a POST request to the 'url' with 'payload' formatted as JSON.
#   response.raise_for_status(): Checks if the request was successful (status code 2xx). Raises an HTTPError if not.
#   response.json(): Parses the JSON response content into a Python dictionary.
# ---

def send_code_to_ollama(code_text, model_name="codellama:7b"):
    """
    Sends the given code_text to the Ollama API and returns the response.

    Args:
        code_text (str): The code to send to Ollama.
        model_name (str): The name of the Ollama model to use.

    Returns:
        dict: The JSON response from Ollama as a dictionary, or an error dictionary.
    """
    ollama_api_url = "http://localhost:11434/api/generate"

    payload = {
        "model": model_name,
        "prompt": f"Analyze this code and provide a brief explanation:\n\n```python\n{code_text}\n```",
        "stream": False,
        "options": {
            "temperature": 0.7,
            "num_predict": 300
        }
    }

    try:
        response = requests.post(ollama_api_url, json=payload, timeout=120)  # Increased to 2 minutes
        response.raise_for_status()
        return response.json()
    except requests.exceptions.ConnectionError:
        return {"error": "Connection Error: Could not connect to Ollama. Is it running?"}
    except requests.exceptions.Timeout:
        return {"error": "Timeout: The request to Ollama timed out."}
    except requests.exceptions.HTTPError as e:
        return {"error": f"HTTP Error: {e.response.status_code} - {e.response.text}"}
    except requests.exceptions.RequestException as e:
        return {"error": f"Request Exception: An unexpected error occurred: {e}"}
    except json.JSONDecodeError:
        return {"error": "JSON Decode Error: Failed to parse Ollama's response."}


def main():
    # Create the QApplication instance
    app = QApplication(sys.argv)
    
    # Set application properties
    app.setApplicationName("Ollama Code Editor")
    app.setApplicationVersion("1.0")
    app.setOrganizationName("AI Code Editor")
    
    # Set dark theme for the application
    app.setStyle('Fusion')
    
    # Create dark palette
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(30, 30, 30))
    palette.setColor(QPalette.WindowText, QColor(255, 255, 255))
    palette.setColor(QPalette.Base, QColor(45, 45, 45))
    palette.setColor(QPalette.AlternateBase, QColor(60, 60, 60))
    palette.setColor(QPalette.ToolTipBase, QColor(0, 0, 0))
    palette.setColor(QPalette.ToolTipText, QColor(255, 255, 255))
    palette.setColor(QPalette.Text, QColor(255, 255, 255))
    palette.setColor(QPalette.Button, QColor(60, 60, 60))
    palette.setColor(QPalette.ButtonText, QColor(255, 255, 255))
    palette.setColor(QPalette.BrightText, QColor(255, 0, 0))
    palette.setColor(QPalette.Link, QColor(42, 130, 218))
    palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
    palette.setColor(QPalette.HighlightedText, QColor(0, 0, 0))
    app.setPalette(palette)

    # Create the main window
    editor_window = CodeEditorWindow()
    editor_window.show()

    # Start the application's event loop
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
