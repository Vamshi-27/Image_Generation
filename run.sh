#!/bin/bash

# Beautiful AI Image Generator Startup Script
echo "🎨 Starting Beautiful AI Image Generator..."
echo "=================================================="

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found. Please run setup first:"
    echo "   chmod +x setup.sh && ./setup.sh"
    exit 1
fi

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source venv/bin/activate

# Check if requirements are installed
echo "🔍 Checking dependencies..."
if ! python -c "import torch, diffusers, gradio" 2>/dev/null; then
    echo "❌ Dependencies not installed. Installing now..."
    pip install -r requirements.txt
fi

# Check system info
echo "💻 System Information:"
python -c "
import torch
print(f'   Python: {torch.__version__}')
print(f'   PyTorch: {torch.__version__}')
print(f'   CUDA Available: {torch.cuda.is_available()}')
if torch.cuda.is_available():
    print(f'   GPU: {torch.cuda.get_device_name(0)}')
    print(f'   VRAM: {torch.cuda.get_device_properties(0).total_memory / 1024**3:.1f} GB')
else:
    print('   Running on CPU')
"

echo ""
echo "🚀 Starting the Beautiful Web Interface..."
echo "   Access the app at: http://localhost:7860"
echo "   Press Ctrl+C to stop the server"
echo "=================================================="
echo ""

# Start the application
python app.py
