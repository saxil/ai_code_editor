"""
🚀 Advanced AI Code Editor with Enhanced GUI - Fixed Version
A comprehensive PyQt5-based code editor with simulated AI functionality,
modern UI components, and professional styling.
"""

import sys
import os
import json
import logging
from typing import Dict, List, Optional, Tuple
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTextEdit, QSplitter, QTreeWidget, QTreeWidgetItem, QPushButton,
    QLabel, QComboBox, QSlider, QCheckBox, QGroupBox, QScrollArea,
    QMenuBar, QMenu, QAction, QToolBar, QStatusBar, QFileDialog,
    QMessageBox, QProgressBar, QDialog, QDialogButtonBox, QTabWidget,
    QFrame, QGridLayout, QFormLayout, QSpinBox, QLineEdit
)
from PyQt5.QtCore import Qt, QTimer, QThread, pyqtSignal, QSize
from PyQt5.QtGui import QFont, QColor, QPalette, QIcon

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ModernButton(QPushButton):
    """Custom button with modern styling and hover effects"""
    
    def __init__(self, text="", icon_text="", parent=None):
        super().__init__(parent)
        self.setText(f"{icon_text} {text}".strip())
        self.setMinimumHeight(40)
        self.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #4CAF50, stop:1 #45a049);
                border: none;
                border-radius: 8px;
                color: white;
                font-weight: bold;
                font-size: 13px;
                padding: 8px 16px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #5CBF60, stop:1 #4CAF50);
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #45a049, stop:1 #3d8b40);
            }
            QPushButton:disabled {
                background-color: #666666;
                color: #999999;
            }
        """)


class AIResponseWidget(QWidget):
    """Widget for displaying AI chat responses with formatting"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        
        # Create scroll area for messages
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setStyleSheet("""
            QScrollArea {
                border: 2px solid #4CAF50;
                border-radius: 8px;
                background-color: #1e1e1e;
            }
        """)
        
        # Content widget for messages
        self.content_widget = QWidget()
        self.content_layout = QVBoxLayout(self.content_widget)
        self.content_layout.setAlignment(Qt.AlignTop)
        
        self.scroll_area.setWidget(self.content_widget)
        layout.addWidget(self.scroll_area)
        
        # Input area
        input_layout = QHBoxLayout()
        
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Ask AI anything about your code...")
        self.input_field.setStyleSheet("""
            QLineEdit {
                background-color: #2b2b2b;
                border: 2px solid #4CAF50;
                border-radius: 8px;
                padding: 12px;
                font-size: 13px;
                color: #ffffff;
            }
            QLineEdit:focus {
                border: 2px solid #5CBF60;
            }
        """)
        self.input_field.returnPressed.connect(self.send_message)
        
        self.send_button = ModernButton("Send", "📤")
        self.send_button.clicked.connect(self.send_message)
        
        input_layout.addWidget(self.input_field)
        input_layout.addWidget(self.send_button)
        layout.addLayout(input_layout)
        
    def add_message(self, sender: str, message: str, msg_type: str = "user"):
        """Add a message to the chat display"""
        message_widget = QFrame()
        message_layout = QVBoxLayout(message_widget)
        
        # Sender label
        sender_label = QLabel(f"🤖 {sender}" if msg_type == "ai" else f"👤 {sender}")
        sender_label.setStyleSheet("""
            QLabel {
                font-weight: bold;
                font-size: 12px;
                color: #4CAF50;
                margin-bottom: 5px;
            }
        """)
        
        # Message content
        message_label = QLabel(message)
        message_label.setWordWrap(True)
        message_label.setStyleSheet(f"""
            QLabel {{
                background-color: {'#2d4a2d' if msg_type == 'ai' else '#2d2d4a'};
                border-radius: 8px;
                border-left: 4px solid {'#4CAF50' if msg_type == 'ai' else '#2196F3'};
                padding: 12px;
                font-size: 13px;
                color: #ffffff;
                line-height: 1.4;
            }}
        """)
        
        message_layout.addWidget(sender_label)
        message_layout.addWidget(message_label)
        
        self.content_layout.addWidget(message_widget)
        
        # Auto-scroll to bottom
        QTimer.singleShot(100, self.scroll_to_bottom)
        
    def scroll_to_bottom(self):
        """Scroll to the bottom of the message area"""
        scrollbar = self.scroll_area.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())
        
    def send_message(self):
        """Send a message to AI (simulated)"""
        message = self.input_field.text().strip()
        if not message:
            return
            
        # Add user message
        self.add_message("You", message, "user")
        self.input_field.clear()
        
        # Simulate AI response
        QTimer.singleShot(1000, lambda: self.simulate_ai_response(message))
        
    def simulate_ai_response(self, user_message: str):
        """Simulate an AI response based on user input"""
        responses = {
            "help": "I can help you with code generation, optimization, debugging, and explanations. What would you like to work on?",
            "function": "Here's a sample function template:\n\ndef example_function(param):\n    '''Function docstring'''\n    return param * 2",
            "class": "Here's a sample class template:\n\nclass ExampleClass:\n    def __init__(self, value):\n        self.value = value\n    \n    def get_value(self):\n        return self.value",
            "debug": "To debug your code, I'd recommend adding print statements or using a debugger. Can you share the specific issue?",
            "optimize": "Code optimization depends on the specific code. Generally: use efficient algorithms, avoid unnecessary loops, and use built-in functions when possible."
        }
        
        # Simple keyword matching for demo
        response = "I understand you're asking about programming. Could you be more specific about what you need help with?"
        for keyword, default_response in responses.items():
            if keyword in user_message.lower():
                response = default_response
                break
                
        self.add_message("AI Assistant", response, "ai")


class FileExplorer(QTreeWidget):
    """Enhanced file explorer with modern styling"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        self.populate_sample_structure()
        
    def setup_ui(self):
        self.setHeaderLabel("📁 Project Explorer")
        self.setStyleSheet("""
            QTreeWidget {
                background-color: #1e1e1e;
                color: #ffffff;
                border: 2px solid #4CAF50;
                border-radius: 8px;
                padding: 5px;
                font-size: 13px;
            }
            QTreeWidget::item {
                padding: 8px;
                border-radius: 4px;
                margin: 2px;
            }
            QTreeWidget::item:selected {
                background-color: #4CAF50;
                color: #ffffff;
            }
            QTreeWidget::item:hover {
                background-color: #333333;
            }
        """)
        
    def populate_sample_structure(self):
        """Create a sample project structure"""
        # Root items
        src_item = QTreeWidgetItem(self, ["📂 src"])
        tests_item = QTreeWidgetItem(self, ["📂 tests"])
        docs_item = QTreeWidgetItem(self, ["📂 docs"])
        config_item = QTreeWidgetItem(self, ["⚙️ requirements.txt"])
        readme_item = QTreeWidgetItem(self, ["📄 README.md"])
        
        # Source files
        QTreeWidgetItem(src_item, ["🐍 main.py"])
        QTreeWidgetItem(src_item, ["🐍 models.py"])
        QTreeWidgetItem(src_item, ["🐍 utils.py"])
        QTreeWidgetItem(src_item, ["🐍 config.py"])
        
        # Test files
        QTreeWidgetItem(tests_item, ["🧪 test_main.py"])
        QTreeWidgetItem(tests_item, ["🧪 test_models.py"])
        
        # Documentation
        QTreeWidgetItem(docs_item, ["📖 API.md"])
        QTreeWidgetItem(docs_item, ["📖 GUIDE.md"])
        
        # Expand all items
        self.expandAll()


class CodeEditor(QTextEdit):
    """Enhanced code editor with syntax highlighting simulation"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        self.load_sample_code()
        
    def setup_ui(self):
        # Set font
        font = QFont("Consolas", 12)
        font.setFixedPitch(True)
        self.setFont(font)
        
        # Styling
        self.setStyleSheet("""
            QTextEdit {
                background-color: #1e1e1e;
                color: #ffffff;
                border: 2px solid #4CAF50;
                border-radius: 8px;
                padding: 15px;
                font-family: 'Consolas', 'Monaco', monospace;
                font-size: 13px;
                line-height: 1.6;
                selection-background-color: #4CAF50;
            }
            QScrollBar:vertical {
                background-color: #2b2b2b;
                width: 12px;
                border-radius: 6px;
            }
            QScrollBar::handle:vertical {
                background-color: #4CAF50;
                border-radius: 6px;
                min-height: 20px;
            }
            QScrollBar::handle:vertical:hover {
                background-color: #45a049;
            }
        """)
        
    def load_sample_code(self):
        """Load sample code with syntax highlighting simulation"""
        sample_code = '''# 🚀 Welcome to Advanced AI Code Editor
# This is a demonstration of the enhanced GUI

import os
import sys
from typing import List, Dict, Optional

class AICodeAssistant:
    """
    Advanced AI-powered code assistant with comprehensive functionality
    """
    
    def __init__(self, model_name: str = "gpt-4"):
        self.model_name = model_name
        self.history: List[Dict] = []
        
    def generate_code(self, prompt: str) -> str:
        """Generate code based on user prompt"""
        print(f"🤖 Generating code for: {prompt}")
        
        # Simulate AI processing
        if "function" in prompt.lower():
            return self.create_function_template()
        elif "class" in prompt.lower():
            return self.create_class_template()
        else:
            return "# AI-generated code would appear here"
            
    def create_function_template(self) -> str:
        """Generate a function template"""
        template = [
            "def ai_generated_function(param1: str, param2: int = 0) -> bool:",
            "    '''",
            "    AI-generated function template",
            "    '''",
            "    try:",
            "        # Your implementation here",
            "        result = param1 + str(param2)",
            "        return len(result) > 0",
            "    except Exception as e:",
            "        print(f'Error: {e}')",
            "        return False"
        ]
        return "\\n".join(template)

    def create_class_template(self) -> str:
        """Generate a class template"""
        template = [
            "class AIGeneratedClass:",
            "    '''",
            "    AI-generated class template",
            "    '''",
            "    ",
            "    def __init__(self, name: str):",
            "        self.name = name",
            "        self.data = {}",
            "    ",
            "    def process_data(self, data: Dict) -> bool:",
            "        '''Process the provided data'''",
            "        try:",
            "            self.data.update(data)",
            "            return True",
            "        except Exception as e:",
            "            print(f'Error processing data: {e}')",
            "            return False"
        ]
        return "\\n".join(template)

    def optimize_code(self, code: str) -> Dict[str, str]:
        """Analyze and optimize the provided code"""
        suggestions = {
            "performance": "Consider using list comprehensions",
            "readability": "Add type hints and docstrings",
            "security": "Validate input parameters"
        }
        return suggestions

    def explain_code(self, code: str) -> str:
        """Explain what the code does"""
        return "This code defines a class with methods for data processing and error handling."

# Example usage
if __name__ == "__main__":
    assistant = AICodeAssistant()
    code = assistant.generate_code("create a function")
    print("Generated code:", code)
    
    # Demonstrate optimization
    suggestions = assistant.optimize_code(code)
    for category, suggestion in suggestions.items():
        print(f"{category.title()}: {suggestion}")
'''
        
        self.setPlainText(sample_code)


class AIControlPanel(QWidget):
    """Advanced AI control panel with multiple options"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        # AI Model Selection
        model_group = QGroupBox("🤖 AI Model")
        model_layout = QVBoxLayout(model_group)
        
        self.model_combo = QComboBox()
        self.model_combo.addItems(["GPT-4", "Claude-3", "CodeLlama", "Local Model"])
        self.model_combo.setStyleSheet("""
            QComboBox {
                background-color: #2b2b2b;
                border: 2px solid #4CAF50;
                border-radius: 8px;
                padding: 8px;
                color: #ffffff;
                font-size: 13px;
                min-height: 25px;
            }
            QComboBox::drop-down {
                border: none;
                width: 30px;
            }
            QComboBox::down-arrow {
                width: 12px;
                height: 12px;
                image: none;
                border-left: 6px solid transparent;
                border-right: 6px solid transparent;
                border-top: 6px solid #4CAF50;
            }
            QComboBox QAbstractItemView {
                background-color: #2b2b2b;
                border: 2px solid #4CAF50;
                border-radius: 8px;
                color: #ffffff;
                selection-background-color: #4CAF50;
            }
        """)
        model_layout.addWidget(self.model_combo)
        layout.addWidget(model_group)
        
        # Temperature Control
        temp_group = QGroupBox("🌡️ Temperature")
        temp_layout = QVBoxLayout(temp_group)
        
        self.temp_slider = QSlider(Qt.Horizontal)
        self.temp_slider.setRange(0, 100)
        self.temp_slider.setValue(70)
        self.temp_slider.setStyleSheet("""
            QSlider::groove:horizontal {
                border: 2px solid #4CAF50;
                height: 8px;
                background: #2b2b2b;
                border-radius: 6px;
            }
            QSlider::handle:horizontal {
                background: #4CAF50;
                border: 2px solid #45a049;
                width: 20px;
                height: 20px;
                border-radius: 12px;
                margin: -8px 0;
            }
            QSlider::handle:horizontal:hover {
                background: #5CBF60;
            }
        """)
        
        self.temp_label = QLabel("0.7")
        self.temp_label.setAlignment(Qt.AlignCenter)
        self.temp_label.setStyleSheet("color: #4CAF50; font-weight: bold;")
        
        self.temp_slider.valueChanged.connect(
            lambda v: self.temp_label.setText(f"{v/100:.1f}")
        )
        
        temp_layout.addWidget(self.temp_slider)
        temp_layout.addWidget(self.temp_label)
        layout.addWidget(temp_group)
        
        # AI Features
        features_group = QGroupBox("⚡ AI Features")
        features_layout = QVBoxLayout(features_group)
        
        features = [
            ("Auto-complete", True),
            ("Error Detection", True),
            ("Code Suggestions", False),
            ("Documentation", True),
            ("Refactoring", False)
        ]
        
        for feature, checked in features:
            cb = QCheckBox(feature)
            cb.setChecked(checked)
            cb.setStyleSheet("""
                QCheckBox {
                    color: #ffffff;
                    font-size: 13px;
                    spacing: 8px;
                }
                QCheckBox::indicator {
                    width: 18px;
                    height: 18px;
                    border: 2px solid #4CAF50;
                    border-radius: 4px;
                    background-color: #2b2b2b;
                }
                QCheckBox::indicator:checked {
                    background-color: #4CAF50;
                    image: none;
                }
                QCheckBox::indicator:hover {
                    border: 2px solid #5CBF60;
                }
            """)
            features_layout.addWidget(cb)
            
        layout.addWidget(features_group)
        
        # Action Buttons
        actions_group = QGroupBox("🎯 Quick Actions")
        actions_layout = QVBoxLayout(actions_group)
        
        self.ask_button = ModernButton("Ask AI", "💬")
        self.generate_button = ModernButton("Generate Code", "⚡")
        self.explain_button = ModernButton("Explain Code", "📖")
        self.optimize_button = ModernButton("Optimize", "🚀")
        
        actions_layout.addWidget(self.ask_button)
        actions_layout.addWidget(self.generate_button)
        actions_layout.addWidget(self.explain_button)
        actions_layout.addWidget(self.optimize_button)
        
        layout.addWidget(actions_group)


class ImprovedAICodeEditor(QMainWindow):
    """Main application window with enhanced UI"""
    
    def __init__(self):
        super().__init__()
        self.current_file = None
        self.init_ui()
        self.setup_connections()
        
    def init_ui(self):
        """Initialize the user interface"""
        self.setWindowTitle("🚀 Advanced AI Code Editor")
        self.setGeometry(100, 100, 1400, 900)
        self.setMinimumSize(1000, 700)
        
        # Set application-wide dark theme
        self.setStyleSheet("""
            QMainWindow {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #1a1a1a, stop:1 #2d2d2d);
                color: #ffffff;
            }
            QMenuBar {
                background-color: #1e1e1e;
                color: #ffffff;
                border-bottom: 2px solid #4CAF50;
                padding: 4px;
                font-size: 13px;
            }
            QMenuBar::item:selected {
                background-color: #4CAF50;
                border-radius: 4px;
            }
            QMenu {
                background-color: #2b2b2b;
                color: #ffffff;
                border: 2px solid #4CAF50;
                border-radius: 8px;
            }
            QMenu::item:selected {
                background-color: #4CAF50;
            }
            QToolBar {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #2b2b2b, stop:1 #1e1e1e);
                border: none;
                border-bottom: 2px solid #4CAF50;
                spacing: 5px;
                padding: 8px;
            }
            QStatusBar {
                background-color: #1e1e1e;
                color: #4CAF50;
                border-top: 2px solid #4CAF50;
                font-weight: bold;
            }
            QGroupBox {
                color: #ffffff;
                border: 2px solid #4CAF50;
                border-radius: 8px;
                margin-top: 1ex;
                font-weight: bold;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
                color: #4CAF50;
            }
        """)
        
        # Create central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)
        
        # Create toolbar
        self.create_toolbar()
        
        # Create main splitter
        main_splitter = QSplitter(Qt.Horizontal)
        
        # Left panel (File Explorer + AI Controls)
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        left_layout.setContentsMargins(5, 5, 5, 5)
        
        # File explorer
        self.file_explorer = FileExplorer()
        left_layout.addWidget(self.file_explorer)
        
        # AI Control Panel
        self.ai_control_panel = AIControlPanel()
        left_layout.addWidget(self.ai_control_panel)
        
        left_panel.setMaximumWidth(350)
        left_panel.setMinimumWidth(250)
        
        # Center panel (Code Editor)
        self.code_editor = CodeEditor()
        
        # Right panel (AI Chat)
        self.ai_response_widget = AIResponseWidget()
        
        # Add panels to splitter
        main_splitter.addWidget(left_panel)
        main_splitter.addWidget(self.code_editor)
        main_splitter.addWidget(self.ai_response_widget)
        
        # Set splitter proportions
        main_splitter.setSizes([300, 700, 400])
        
        # Add splitter to main layout
        main_layout.addWidget(main_splitter)
        
        # Create menu bar
        self.create_menu_bar()
        
        # Create status bar
        self.create_status_bar()
        
    def create_toolbar(self):
        """Create the application toolbar"""
        toolbar = self.addToolBar("Main")
        toolbar.setMovable(False)
        
        # File operations
        new_action = toolbar.addAction("📄 New")
        new_action.triggered.connect(self.new_file)
        
        open_action = toolbar.addAction("📁 Open")
        open_action.triggered.connect(self.open_file)
        
        save_action = toolbar.addAction("💾 Save")
        save_action.triggered.connect(self.save_file)
        
        toolbar.addSeparator()
        
        # AI operations
        ai_ask_action = toolbar.addAction("🤖 Ask AI")
        ai_ask_action.triggered.connect(self.ask_ai)
        
        ai_generate_action = toolbar.addAction("⚡ Generate")
        ai_generate_action.triggered.connect(self.generate_code)
        
        ai_explain_action = toolbar.addAction("📖 Explain")
        ai_explain_action.triggered.connect(self.explain_code)
        
        toolbar.addSeparator()
        
        # View operations
        zoom_in_action = toolbar.addAction("🔍+ Zoom In")
        zoom_in_action.triggered.connect(self.zoom_in)
        
        zoom_out_action = toolbar.addAction("🔍- Zoom Out")
        zoom_out_action.triggered.connect(self.zoom_out)
        
    def create_menu_bar(self):
        """Create the application menu bar"""
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu("📁 File")
        file_menu.addAction("📄 New", self.new_file)
        file_menu.addAction("📁 Open", self.open_file)
        file_menu.addAction("💾 Save", self.save_file)
        file_menu.addAction("💾 Save As", self.save_as_file)
        file_menu.addSeparator()
        file_menu.addAction("❌ Exit", self.close)
        
        # Edit menu
        edit_menu = menubar.addMenu("✏️ Edit")
        edit_menu.addAction("↩️ Undo", self.code_editor.undo)
        edit_menu.addAction("↪️ Redo", self.code_editor.redo)
        edit_menu.addSeparator()
        edit_menu.addAction("✂️ Cut", self.code_editor.cut)
        edit_menu.addAction("📋 Copy", self.code_editor.copy)
        edit_menu.addAction("📄 Paste", self.code_editor.paste)
        
        # AI menu
        ai_menu = menubar.addMenu("🤖 AI Assistant")
        ai_menu.addAction("💬 Ask AI", self.ask_ai)
        ai_menu.addAction("⚡ Generate Code", self.generate_code)
        ai_menu.addAction("📖 Explain Code", self.explain_code)
        ai_menu.addAction("🚀 Optimize Code", self.optimize_code)
        
        # View menu
        view_menu = menubar.addMenu("👁️ View")
        view_menu.addAction("🔍+ Zoom In", self.zoom_in)
        view_menu.addAction("🔍- Zoom Out", self.zoom_out)
        
    def create_status_bar(self):
        """Create the application status bar"""
        status_bar = self.statusBar()
        status_bar.showMessage("🚀 Advanced AI Code Editor - Ready")
        
        # Add permanent widgets
        self.line_col_label = QLabel("Line: 1, Col: 1")
        self.line_col_label.setStyleSheet("color: #4CAF50; font-weight: bold;")
        status_bar.addPermanentWidget(self.line_col_label)
        
        self.file_type_label = QLabel("Python")
        self.file_type_label.setStyleSheet("color: #4CAF50; font-weight: bold;")
        status_bar.addPermanentWidget(self.file_type_label)
        
    def setup_connections(self):
        """Setup signal connections"""
        # Connect AI control panel buttons
        self.ai_control_panel.ask_button.clicked.connect(self.ask_ai)
        self.ai_control_panel.generate_button.clicked.connect(self.generate_code)
        self.ai_control_panel.explain_button.clicked.connect(self.explain_code)
        self.ai_control_panel.optimize_button.clicked.connect(self.optimize_code)
        
        # Connect editor cursor position changes
        self.code_editor.cursorPositionChanged.connect(self.update_cursor_position)
        
    def update_cursor_position(self):
        """Update cursor position in status bar"""
        cursor = self.code_editor.textCursor()
        line = cursor.blockNumber() + 1
        col = cursor.columnNumber() + 1
        self.line_col_label.setText(f"Line: {line}, Col: {col}")
        
    # File operations
    def new_file(self):
        """Create a new file"""
        self.code_editor.clear()
        self.current_file = None
        self.setWindowTitle("🚀 Advanced AI Code Editor - New File")
        self.statusBar().showMessage("📄 New file created")
        
    def open_file(self):
        """Open an existing file"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Open File", "", "Python Files (*.py);;All Files (*)"
        )
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()
                    self.code_editor.setPlainText(content)
                    self.current_file = file_path
                    self.setWindowTitle(f"🚀 Advanced AI Code Editor - {os.path.basename(file_path)}")
                    self.statusBar().showMessage(f"📁 Opened: {file_path}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to open file:\\n{str(e)}")
                
    def save_file(self):
        """Save the current file"""
        if self.current_file:
            try:
                with open(self.current_file, 'w', encoding='utf-8') as file:
                    file.write(self.code_editor.toPlainText())
                    self.statusBar().showMessage(f"💾 Saved: {self.current_file}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to save file:\\n{str(e)}")
        else:
            self.save_as_file()
            
    def save_as_file(self):
        """Save the current file with a new name"""
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Save File", "", "Python Files (*.py);;All Files (*)"
        )
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as file:
                    file.write(self.code_editor.toPlainText())
                    self.current_file = file_path
                    self.setWindowTitle(f"🚀 Advanced AI Code Editor - {os.path.basename(file_path)}")
                    self.statusBar().showMessage(f"💾 Saved as: {file_path}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to save file:\\n{str(e)}")
                
    # AI operations
    def ask_ai(self):
        """Open AI chat for questions"""
        self.ai_response_widget.input_field.setFocus()
        self.statusBar().showMessage("💬 AI Assistant ready for your questions")
        
    def generate_code(self):
        """Generate code using AI"""
        cursor = self.code_editor.textCursor()
        selected_text = cursor.selectedText()
        
        if selected_text:
            prompt = f"Generate code for: {selected_text}"
        else:
            prompt = "Generate a sample function"
            
        # Simulate AI code generation
        generated_code = self.simulate_code_generation(prompt)
        
        if generated_code:
            cursor.insertText(generated_code)
            self.ai_response_widget.add_message(
                "AI Assistant", 
                f"Generated code based on: {prompt}",
                "ai"
            )
            self.statusBar().showMessage("⚡ Code generated successfully")
            
    def explain_code(self):
        """Explain selected code using AI"""
        cursor = self.code_editor.textCursor()
        selected_text = cursor.selectedText()
        
        if not selected_text:
            selected_text = self.get_current_line()
            
        explanation = self.simulate_code_explanation(selected_text)
        self.ai_response_widget.add_message(
            "AI Assistant",
            f"Code explanation:\\n{explanation}",
            "ai"
        )
        self.statusBar().showMessage("📖 Code explanation generated")
        
    def optimize_code(self):
        """Optimize selected code using AI"""
        cursor = self.code_editor.textCursor()
        selected_text = cursor.selectedText()
        
        if not selected_text:
            QMessageBox.information(
                self, "Info", "Please select code to optimize"
            )
            return
            
        optimization = self.simulate_code_optimization(selected_text)
        self.ai_response_widget.add_message(
            "AI Assistant",
            f"Code optimization suggestions:\\n{optimization}",
            "ai"
        )
        self.statusBar().showMessage("🚀 Code optimization suggestions generated")
        
    # AI simulation methods
    def simulate_code_generation(self, prompt: str) -> str:
        """Simulate AI code generation"""
        if "function" in prompt.lower():
            return """
def generated_function(param1, param2=None):
    '''Generated function based on your request'''
    try:
        result = param1 if param2 is None else param1 + param2
        return result
    except Exception as e:
        print(f"Error: {e}")
        return None
"""
        elif "class" in prompt.lower():
            return """
class GeneratedClass:
    '''Generated class based on your request'''
    
    def __init__(self, name):
        self.name = name
        self.data = {}
    
    def process(self, data):
        '''Process data method'''
        self.data.update(data)
        return True
"""
        else:
            return """
# Generated code snippet
result = []
for i in range(10):
    result.append(i * 2)
print(result)
"""
            
    def simulate_code_explanation(self, code: str) -> str:
        """Simulate AI code explanation"""
        if not code.strip():
            return "No code selected to explain."
            
        explanations = [
            f"This code appears to define functionality related to: {code[:50]}...",
            "The selected code implements a programming pattern that:",
            "• Follows Python best practices",
            "• Uses appropriate data structures",
            "• Includes error handling where needed",
            "• Is designed for maintainability"
        ]
        
        return "\\n".join(explanations)
        
    def simulate_code_optimization(self, code: str) -> str:
        """Simulate AI code optimization"""
        suggestions = [
            "💡 Performance Optimizations:",
            "• Consider using list comprehensions for better performance",
            "• Use built-in functions when possible",
            "• Avoid unnecessary loops",
            "",
            "🔧 Code Quality Improvements:",
            "• Add type hints for better code documentation",
            "• Include docstrings for functions and classes",
            "• Use meaningful variable names",
            "",
            "🛡️ Security Considerations:",
            "• Validate input parameters",
            "• Handle exceptions appropriately",
            "• Use secure coding practices"
        ]
        
        return "\\n".join(suggestions)
        
    def get_current_line(self) -> str:
        """Get the current line of code"""
        cursor = self.code_editor.textCursor()
        cursor.select(cursor.LineUnderCursor)
        return cursor.selectedText()
        
    # Utility methods
    def zoom_in(self):
        """Increase editor font size"""
        font = self.code_editor.font()
        size = font.pointSize()
        if size < 24:
            font.setPointSize(size + 1)
            self.code_editor.setFont(font)
            self.statusBar().showMessage(f"🔍+ Font size: {size + 1}")
            
    def zoom_out(self):
        """Decrease editor font size"""
        font = self.code_editor.font()
        size = font.pointSize()
        if size > 8:
            font.setPointSize(size - 1)
            self.code_editor.setFont(font)
            self.statusBar().showMessage(f"🔍- Font size: {size - 1}")


def main():
    """Main application entry point"""
    app = QApplication(sys.argv)
    app.setApplicationName("Advanced AI Code Editor")
    app.setApplicationVersion("1.0.0")
    
    # Create and show main window
    editor = ImprovedAICodeEditor()
    editor.show()
    
    # Start the application
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
