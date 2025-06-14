# PowerShell script to run the Ollama PyQt5 Code Editor
Set-Location "a:\ml\Projects\ai_code_editor"

# Activate virtual environment
& ".\venv\Scripts\Activate.ps1"

# Run the application
python "src\ollama_pyqt5_code_editor.py"

# Keep window open
Read-Host "Press Enter to exit"
