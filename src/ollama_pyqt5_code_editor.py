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
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QTextEdit, QPushButton, QHBoxLayout
# If not already there: from PyQt5.QtWidgets import QApplication, QMainWindow
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

class CodeEditorWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyQt5 Ollama Code Editor")
        self.setGeometry(100, 100, 850, 650) # Slightly adjusted size for better look

        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Main vertical layout for the central widget
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)

        self.init_ui(main_layout)
        self.apply_styles() # Call a new method to apply styles

    def init_ui(self, main_layout): # Accept main_layout as an argument
        # --- Explanation of Widgets and Layouts ---
        # QTextEdit: A widget that allows multi-line text editing. We'll use one for code input and another for output.
        # QPushButton: A standard command button.
        # QHBoxLayout: Arranges widgets horizontally. We might use this for the button if we want something next to it.
        # QVBoxLayout: Arranges widgets vertically. This will be our main layout and also used to stack input/output areas.
        # ---

        # Code Input Area
        self.codeInput = QTextEdit()
        self.codeInput.setObjectName("codeInput") # Added object name for potential specific styling
        self.codeInput.setPlaceholderText("Enter your code here...")
        main_layout.addWidget(self.codeInput, 1) # The '1' makes it take more space (stretch factor)

        # Output Display Area
        # QTextBrowser is like QTextEdit but read-only by default and can render HTML.
        # For simplicity, we'll start with QTextEdit and can make it read-only.
        self.outputArea = QTextEdit()
        self.outputArea.setObjectName("outputArea") # Added object name
        self.outputArea.setReadOnly(True) # Make it read-only
        self.outputArea.setPlaceholderText("Ollama's output will appear here...")
        main_layout.addWidget(self.outputArea, 1) # The '1' makes it take more space

        # Button to send code
        self.runButton = QPushButton("Run Code")
        self.runButton.setObjectName("runButton") # Added object name
        self.runButton.clicked.connect(self.on_run_button_clicked) # Connect the signal to the slot
        main_layout.addWidget(self.runButton)

        # --- Explanation of Widget Sizing (Stretch Factors) ---
        # When adding widgets to a QVBoxLayout (or QHBoxLayout), the second argument to addWidget (e.g., 1 in main_layout.addWidget(self.codeInput, 1))
        # is a stretch factor. Widgets with higher stretch factors will expand more to fill available space compared to those with lower or zero stretch factors.
        # Here, both QTextEdit widgets are given a stretch factor of 1, so they will share the available vertical space equally after the button gets its preferred size.
        # ---

    def apply_styles(self):
        """Applies basic styling to the application widgets."""
        
        stylesheet = """
            QMainWindow {
                background-color: #f0f0f0;
            }
            QTextEdit#codeInput, QTextEdit#outputArea {
                background-color: #ffffff;
                color: #333333;
                border: 1px solid #cccccc;
                border-radius: 4px;
                font-size: 14px;
                padding: 5px;
            }
            QPushButton#runButton {
                background-color: #007bff;
                color: white;
                border: none;
                padding: 10px 15px;
                border-radius: 4px;
                font-size: 14px;
            }
            QPushButton#runButton:hover {
                background-color: #0056b3;
            }
            QPushButton#runButton:pressed {
                background-color: #004085;
            }
        """
        self.setStyleSheet(stylesheet)
        
    def on_run_button_clicked(self):
        """
        Slot for the runButton's clicked signal.
        Gets code from input, sends to Ollama, and displays the result.
        """
        code_to_send = self.codeInput.toPlainText()
        if not code_to_send.strip():
            self.outputArea.setText("Please enter some code.")
            return

        # Show some feedback that it's working
        self.outputArea.setText("Sending to Ollama... Please wait.")
        QApplication.processEvents() # Allow UI to update

        # IMPORTANT: Remind user they might need to change the model name here or pass it from a UI element eventually
        # For example, model_name = self.modelSelector.currentText() if you add a QComboBox for model selection.
        ollama_response = send_code_to_ollama(code_to_send, model_name="your-ollama-coding-model-name") # Ensure this model name is configured by the user

        if "error" in ollama_response:
            self.outputArea.setText(f"Error: {ollama_response['error']}")
        elif "response" in ollama_response: # This is the expected key for Ollama's non-streaming response
            self.outputArea.setText(ollama_response["response"])
        else:
            # Fallback for unexpected response structure
            self.outputArea.setText(f"Unexpected response from Ollama: {json.dumps(ollama_response, indent=2)}")


# --- Explanation of 'requests' library ---
# The 'requests' library is a popular third-party Python library for making HTTP requests.
# It simplifies the process of sending GET, POST, etc., requests and handling responses.
# You'll need to install it if you haven't already: pip install requests
# Key methods used:
#   requests.post(url, json=payload): Sends a POST request to the 'url' with 'payload' formatted as JSON.
#   response.raise_for_status(): Checks if the request was successful (status code 2xx). Raises an HTTPError if not.
#   response.json(): Parses the JSON response content into a Python dictionary.
# ---

def send_code_to_ollama(code_text, model_name="your-ollama-coding-model-name"):
    """
    Sends the given code_text to the Ollama API and returns the response.

    Args:
        code_text (str): The code to send to Ollama.
        model_name (str): The name of the Ollama model to use.
                          **IMPORTANT**: User needs to change this!

    Returns:
        dict: The JSON response from Ollama as a dictionary, or an error dictionary.
    """
    # IMPORTANT: Remind the user that this endpoint might need to be changed
    # if their Ollama instance is not running on the default location.
    ollama_api_url = "http://localhost:11434/api/generate"

    payload = {
        "model": model_name,
        "prompt": code_text,
        "stream": False  # Keep it simple for now, no streaming
    }

    try:
        # Tell the user that they may need to configure proxies if they are behind one
        response = requests.post(ollama_api_url, json=payload, timeout=20) # Added timeout
        response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)
        return response.json()
    except requests.exceptions.ConnectionError:
        return {"error": "Connection Error: Could not connect to Ollama. Is it running?"}
    except requests.exceptions.Timeout:
        return {"error": "Timeout: The request to Ollama timed out."}
    except requests.exceptions.HTTPError as e:
        return {"error": f"HTTP Error: {e.response.status_code} - {e.response.text}"}
    except requests.exceptions.RequestException as e:
        # For any other requests-related errors
        return {"error": f"Request Exception: An unexpected error occurred: {e}"}
    except json.JSONDecodeError:
        return {"error": "JSON Decode Error: Failed to parse Ollama's response."}


def main():
    # Create the QApplication instance
    app = QApplication(sys.argv)

    # Create the main window
    editor_window = CodeEditorWindow()
    editor_window.show()

    # Start the application's event loop
    # sys.exit(app.exec_()) ensures a clean exit
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
