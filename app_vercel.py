import os
os.environ['DISABLE_XFORMERS'] = '1'

import gradio as gr
from typing import Optional
import time

# For Vercel deployment, we'll create a demo version
# that shows the interface without actual AI generation
class DemoImageGenerator:
    """Demo version for Vercel deployment"""
    
    def __init__(self):
        self.device = "demo"
        print("🌟 DreamForge Studio - Demo Mode")
        print("Note: This is a demo version for web deployment")
    
    def generate_image(self, prompt: str, **kwargs):
        """Demo image generation - returns placeholder"""
        # Simulate processing time
        time.sleep(2)
        
        # In a real deployment, you would use an API service like:
        # - Hugging Face Inference API
        # - Replicate API
        # - OpenAI DALL-E API
        # - Stability AI API
        
        return None, {
            "prompt": prompt,
            "status": "Demo mode - actual generation requires GPU resources",
            "suggestion": "For full functionality, run locally or use cloud GPU services"
        }

# Initialize demo generator
generator = DemoImageGenerator()

def generate_image_gradio(prompt, negative_prompt, style_preset, width, height, steps, use_enhancer):
    """Demo image generation for Vercel"""
    try:
        if not prompt or not prompt.strip():
            return None
        
        # Add style preset to prompt
        if style_preset != "None":
            style_prompts = {
                "📸 Photorealistic": ", photorealistic, realistic, detailed, high quality",
                "🎨 Artistic": ", artistic, painting style, creative, expressive",
                "🌟 Cinematic": ", cinematic, dramatic lighting, movie scene, epic",
                "✨ Fantasy": ", fantasy art, magical, ethereal, mystical",
                "🔮 Sci-Fi": ", science fiction, futuristic, high-tech, cyberpunk",
                "🏞️ Landscape": ", landscape photography, natural lighting, scenic",
                "👤 Portrait": ", portrait, professional headshot, well-lit face",
                "🎭 Vintage": ", vintage style, retro, classic, nostalgic"
            }
            if style_preset in style_prompts:
                prompt += style_prompts[style_preset]
        
        # For demo, return a message
        demo_message = f"""
🎨 DreamForge Studio - Web Demo

📝 Your prompt: "{prompt[:100]}..."
⚙️ Settings: {width}×{height}, {steps} steps
🎭 Style: {style_preset}

🌐 This is a web demo version. For full AI image generation:
• Download and run locally for CPU generation
• Use cloud GPU services for faster generation
• Integrate with AI APIs for production deployment

🚀 The interface is fully functional - only the AI model 
   requires local resources or cloud GPU for actual generation.
        """
        
        # Create a simple placeholder image (text)
        return gr.update(value=demo_message)
        
    except Exception as e:
        return None

def create_gradio_interface():
    """Create the Gradio web interface for Vercel"""
    
    # Simplified CSS for web deployment
    custom_css = """
    .gradio-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 25%, #f093fb 50%, #f5576c 75%, #4facfe 100%);
        min-height: 100vh;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    .header-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 15px;
        padding: 40px 30px;
        text-align: center;
        margin-bottom: 30px;
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
    }
    
    .header-title {
        color: white;
        font-size: 3.5em;
        font-weight: 700;
        margin: 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .header-subtitle {
        color: rgba(255,255,255,0.9);
        font-size: 1.3em;
        margin: 15px 0 0 0;
        font-weight: 300;
    }
    
    .glass-card {
        background: rgba(255, 255, 255, 0.85);
        backdrop-filter: blur(15px);
        border-radius: 20px;
        padding: 30px;
        border: 1px solid rgba(255, 255, 255, 0.3);
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.1);
        margin: 20px 0;
    }
    
    .section-header {
        color: #4a5568;
        font-size: 2em;
        font-weight: 700;
        margin-bottom: 25px;
        text-align: center;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
    }
    
    .footer-container {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        border-radius: 20px;
        padding: 30px;
        text-align: center;
        margin-top: 50px;
        box-shadow: 0 15px 40px rgba(240, 147, 251, 0.4);
    }
    
    .footer-text {
        color: white;
        font-size: 1.2em;
        font-weight: 600;
        margin: 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    """
    
    with gr.Blocks(title="🌟 DreamForge Studio", theme=gr.themes.Soft(), css=custom_css) as interface:
        
        # Header
        gr.HTML("""
        <div class="header-container">
            <h1 class="header-title">🌟 DreamForge Studio</h1>
            <p class="header-subtitle">Where imagination meets artificial intelligence</p>
            <p style="color: rgba(255,255,255,0.8); font-size: 1em; margin-top: 10px;">
                🌐 Web Demo Version - Download for full AI generation
            </p>
        </div>
        """)
        
        with gr.Row():
            # Input controls
            with gr.Column(scale=1, elem_classes="glass-card"):
                gr.HTML('<div class="section-header">🎯 Forge Your Vision</div>')
                
                prompt_input = gr.Textbox(
                    label="✨ Describe your masterpiece",
                    lines=4,
                    value="A breathtaking sunset over a mystical mountain range with ancient ruins"
                )
                
                style_preset = gr.Dropdown(
                    label="🎨 Choose Your Style",
                    choices=[
                        "None", "📸 Photorealistic", "🎨 Artistic", "🌟 Cinematic",
                        "✨ Fantasy", "🔮 Sci-Fi", "🏞️ Landscape", "👤 Portrait", "🎭 Vintage"
                    ],
                    value="📸 Photorealistic"
                )
                
                negative_prompt = gr.Textbox(
                    label="🚫 What to avoid",
                    lines=2,
                    value="low quality, blurry, distorted, deformed, ugly"
                )
                
                with gr.Accordion("🔧 Advanced Controls", open=False):
                    with gr.Row():
                        width_slider = gr.Slider(
                            minimum=256, maximum=1024, value=512, step=64,
                            label="📏 Width"
                        )
                        height_slider = gr.Slider(
                            minimum=256, maximum=1024, value=512, step=64,
                            label="📏 Height"
                        )
                    
                    steps_slider = gr.Slider(
                        minimum=10, maximum=50, value=25, step=1,
                        label="🔄 Quality Steps"
                    )
                
                use_enhancer = gr.Checkbox(
                    label="✨ Auto-enhance prompts for better results",
                    value=True
                )
                
                generate_btn = gr.Button(
                    "🎨 Create Magic (Demo)",
                    variant="primary",
                    size="lg"
                )
            
            # Output display
            with gr.Column(scale=2, elem_classes="glass-card"):
                gr.HTML('<div class="section-header">🖼️ Demo Output</div>')
                
                demo_output = gr.Textbox(
                    label="Demo Information",
                    lines=12,
                    value="""🌟 Welcome to DreamForge Studio Web Demo!

This is a demonstration of the beautiful interface.

For actual AI image generation, you can:

📥 Download the full version for local use
🚀 Run on your own hardware (CPU compatible)
☁️ Deploy on cloud platforms with GPU support
🔌 Integrate with AI APIs for production use

The complete application includes:
✨ Stable Diffusion AI model
🎨 High-quality image generation  
💻 CPU-optimized performance
🎭 Multiple style presets
📱 Full responsive design

Ready to create amazing AI art!"""
                )
        
        # Set up the generate button click
        generate_btn.click(
            fn=generate_image_gradio,
            inputs=[
                prompt_input, negative_prompt, style_preset,
                width_slider, height_slider, steps_slider,
                use_enhancer
            ],
            outputs=[demo_output]
        )
        
        # Information section
        gr.HTML("""
        <div class="glass-card" style="margin-top: 30px;">
            <h3 style="text-align: center; color: #4a5568;">🚀 Get the Full Version</h3>
            <div style="text-align: center; color: #6c757d; line-height: 1.6;">
                <p><strong>For complete AI image generation capabilities:</strong></p>
                <ul style="text-align: left; max-width: 600px; margin: 0 auto;">
                    <li>🖥️ <strong>Local Installation:</strong> Download and run on your computer</li>
                    <li>☁️ <strong>Cloud Deployment:</strong> Deploy on GPU-enabled cloud platforms</li>
                    <li>🔌 <strong>API Integration:</strong> Connect with Hugging Face, Replicate, or Stability AI</li>
                    <li>🐳 <strong>Docker:</strong> Containerized deployment for production</li>
                </ul>
                <p style="margin-top: 20px;">
                    <strong>GitHub:</strong> <code>github.com/your-username/dreamforge-studio</code>
                </p>
            </div>
        </div>
        """)
        
        # Footer
        gr.HTML("""
        <div class="footer-container">
            <p class="footer-text">🌟 DreamForge Studio | Crafting Dreams into Reality</p>
        </div>
        """)
    
    return interface

# Create and launch the interface
app = create_gradio_interface()

if __name__ == "__main__":
    print("🌐 Starting DreamForge Studio Web Demo...")
    print("📱 Access at: http://localhost:7860")
    print("💡 This is a demo version - download for full AI generation")
    
    app.launch(
        server_name="127.0.0.1",  # Changed from 0.0.0.0 for Windows compatibility
        server_port=7860,
        share=False,
        inbrowser=True  # Automatically open browser
    )
