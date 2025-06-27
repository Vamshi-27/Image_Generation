# 🌟 DreamForge Studio

**Where imagination meets Creativity**

Transform your creative ideas into stunning visual art with the power of AI. DreamForge Studio is a beautiful, modern web interface for Stable Diffusion that runs seamlessly on CPU-only systems.

![DreamForge Studio](https://img.shields.io/badge/AI-Image%20Generation-blue?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.8%2B-green?style=for-the-badge)
![Gradio](https://img.shields.io/badge/Interface-Gradio-orange?style=for-the-badge)
![CPU Compatible](https://img.shields.io/badge/CPU-Compatible-red?style=for-the-badge)

## ✨ Features

- 🎨 **Beautiful Modern Interface** - Glass morphism design with smooth animations
- 🖼️ **High-Quality Image Generation** - Powered by Stable Diffusion v1.5
- 🎭 **Style Presets** - Photorealistic, Artistic, Cinematic, Fantasy, and more
- 💻 **CPU Optimized** - No GPU required, runs on any system
- 🚀 **One-Click Launch** - Simple startup scripts for instant access
- 📱 **Responsive Design** - Works on desktop, tablet, and mobile
- 🎯 **Smart Prompt Enhancement** - Automatic quality improvements
- 💾 **Auto-Save** - All generated images saved automatically

## 🚀 Quick Start

### 🪟 Windows Users

**First-time setup:**
```cmd
# Option 1: Double-click setup.bat
setup.bat

# Option 2: PowerShell (recommended)
setup.ps1

# Option 3: Manual setup
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

**Run the application:**
```cmd
# Double-click to run
run.bat

# Or manually
venv\Scripts\activate
python app.py
```

### 🐧 Linux/Mac Users
```bash
# First-time setup
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Run the application
chmod +x run.sh
./run.sh
```

### 🌐 Web Demo Version
```bash
# Run the lightweight web demo
python app_vercel.py
```

## 🌐 Access Your Studio

Once started, DreamForge Studio will be available at:
**http://localhost:7860**

The interface will automatically open in your browser!

## 🎨 How to Use

1. **Enter Your Vision** - Describe what you want to create in the text box
2. **Choose a Style** - Select from our preset styles or go with "None"
3. **Adjust Settings** - Fine-tune dimensions and quality in Advanced Controls
4. **Create Magic** - Hit the "Create Magic" button and watch AI bring your vision to life!

### 💡 Pro Tips for Better Results

- **Be Specific**: Include details about lighting, colors, mood, and style
- **Use Quality Keywords**: "high quality", "detailed", "4k", "professional"
- **Set the Mood**: "dramatic", "peaceful", "vibrant", "cinematic"
- **Specify Style**: "photorealistic", "oil painting", "digital art"
- **Technical Terms**: "golden hour", "studio lighting", "shallow depth of field"

## 🎭 Style Presets

| Style | Description |
|-------|-------------|
| 📸 **Photorealistic** | Realistic, detailed photography style |
| 🎨 **Artistic** | Creative, expressive artistic style |
| 🌟 **Cinematic** | Movie-like, dramatic lighting |
| ✨ **Fantasy** | Magical, ethereal, mystical themes |
| 🔮 **Sci-Fi** | Futuristic, high-tech, cyberpunk |
| 🏞️ **Landscape** | Natural scenery, scenic views |
| 👤 **Portrait** | People, faces, headshots |
| 🎭 **Vintage** | Retro, classic, nostalgic feel |

## 🔧 Advanced Controls

- **Width/Height**: Control image dimensions (256-1024px)
- **Quality Steps**: Higher values = better quality (10-50)
- **Auto-Enhance**: Automatically improve prompts for better results

## 📁 Project Structure

```
DreamForge Studio/
├── 🎨 app.py              # Main application
├── 📋 requirements.txt    # Python dependencies
├── 🚀 run.sh             # Linux/Mac launcher
├── 🚀 run.bat            # Windows launcher
├── 📖 README.md          # This file
├── � Report.pdf         # Comprehensive project report
├── 📄 Report.html        # HTML version of report
├── 📄 .gitignore         # Git ignore rules
├── �📁 venv/              # Virtual environment
└── 📁 outputs/           # Generated images
```

## 🛠️ Technical Details

- **AI Model**: Stable Diffusion v1.5
- **Interface**: Gradio with custom CSS
- **Python**: 3.8+ required
- **Dependencies**: PyTorch, Diffusers, Gradio, PIL
- **CPU Optimized**: No CUDA/GPU requirements
- **Memory**: ~4GB RAM recommended

## 🎯 System Requirements

- **Operating System**: Windows 10+, macOS 10.14+, or Linux
- **Python**: 3.8 or higher
- **Memory**: 4GB RAM minimum, 8GB recommended
- **Storage**: 5GB free space (for model and generated images)
- **Internet**: Required for initial model download (~2GB)


## 🎨 Example Prompts

Try these creative prompts to get started:

```
A serene Japanese garden with cherry blossoms in full bloom, morning mist, peaceful atmosphere, high quality, detailed

Cyberpunk cityscape at night, neon lights reflecting on wet streets, futuristic architecture, dramatic lighting, 4k

Majestic dragon perched on ancient castle towers, sunset sky, fantasy art, epic composition, detailed scales

Cozy coffee shop interior, warm lighting, wooden furniture, books on shelves, peaceful atmosphere, artistic style
```

## 📞 Support

Having issues?

1. Restart the application
2. Check system requirements
3. Verify internet connection for model downloads
4. Ensure sufficient disk space

## 🎉 Enjoy Creating!

DreamForge Studio is designed to make AI art generation accessible, beautiful, and fun. Whether you're an artist, designer, or just curious about AI, start creating amazing images today!

---

**Made with ❤️ and AI** | **DreamForge Studio v1.0** | **2025**
