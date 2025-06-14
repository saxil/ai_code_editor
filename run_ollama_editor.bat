@echo off
cd /d "a:\ml\Projects\ai_code_editor"
call venv\Scripts\activate.bat
python src\ollama_pyqt5_code_editor.py
pause
