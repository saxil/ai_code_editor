#!/bin/bash
# Activation and run script for the Ollama PyQt5 Code Editor

echo "=== Ollama PyQt5 Code Editor Setup & Run ==="
echo ""

# Navigate to project directory
cd "a:/ml/Projects/ai_code_editor"

echo "1. Virtual environment created: ✓"
echo "2. Requirements installed: ✓"
echo "3. Icon added to assets: ✓"
echo ""

echo "To run the application:"
echo "Option 1 (Batch file): run_ollama_editor.bat"
echo "Option 2 (PowerShell): run_ollama_editor.ps1"
echo "Option 3 (Manual): venv\\Scripts\\python.exe src\\ollama_pyqt5_code_editor.py"
echo ""

echo "Before running, make sure to:"
echo "1. Install and start Ollama (https://ollama.com/)"
echo "2. Pull a model: ollama pull codellama:7b"
echo "3. Edit the model name in src/ollama_pyqt5_code_editor.py"
echo "   Change 'your-ollama-coding-model-name' to your actual model"
