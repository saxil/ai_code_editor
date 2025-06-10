"""
🚀 Advanced AI Code Editor - Main Entry Point
Launch the improved PyQt5-based AI code editor with enhanced GUI
"""

import sys
import os

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from improved_ai_code_editor_working import main

if __name__ == "__main__":
    main()
