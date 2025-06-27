@echo off
REM Beautiful AI Image Generator Startup Script for Windows

echo 🎨 Starting Beautiful AI Image Generator...
echo ==================================================

REM Check if virtual environment exists
if not exist "venv" (
    echo ❌ Virtual environment not found. Please run setup first:
    echo    setup.bat
    pause
    exit /b 1
)

REM Activate virtual environment
echo 🔄 Activating virtual environment...
call venv\Scripts\activate.bat

REM Check if requirements are installed
echo 🔍 Checking dependencies...
python -c "import torch, diffusers, gradio" 2>nul
if errorlevel 1 (
    echo ❌ Dependencies not installed. Installing now...
    pip install -r requirements.txt
)

REM Check system info
echo 💻 System Information:
python -c "import torch; print(f'   Python: {torch.__version__}'); print(f'   PyTorch: {torch.__version__}'); print(f'   CUDA Available: {torch.cuda.is_available()}'); print(f'   GPU: {torch.cuda.get_device_name(0)}' if torch.cuda.is_available() else '   Running on CPU')"

echo.
echo 🚀 Starting the Beautiful Web Interface...
echo    🌐 Web Interface: http://localhost:7860
echo    🌐 Alternative:   http://127.0.0.1:7860
echo    📱 The interface will open automatically in your browser
echo    Press Ctrl+C to stop the server
echo ==================================================
echo.

REM Start the application and open browser
echo Opening browser...
timeout /t 3 /nobreak >nul
start http://localhost:7860
python app.py

pause
