import os
# Disable xformers before importing anything else
os.environ['DISABLE_XFORMERS'] = '1'

import torch
import gradio as gr
import logging
from typing import Optional, Tuple
import time
import json
from datetime import datetime
from PIL import Image
import numpy as np

# Try importing diffusers with error handling
try:
    from diffusers import StableDiffusionPipeline, DPMSolverMultistepScheduler
    DIFFUSERS_AVAILABLE = True
except ImportError as e:
    DIFFUSERS_AVAILABLE = False
    IMPORT_ERROR = str(e)
    print(f"❌ Error importing diffusers: {e}")
    print("🔧 Attempting to fix dependencies...")

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TextToImageGenerator:
    """Text to Image Generation using Stable Diffusion"""
    
    def __init__(self, model_id: str = "runwayml/stable-diffusion-v1-5"):
        """
        Initialize the text-to-image generator
        
        Args:
            model_id: HuggingFace model ID for the Stable Diffusion model
        """
        if not DIFFUSERS_AVAILABLE:
            raise ImportError(f"Diffusers library not available: {IMPORT_ERROR}")
            
        self.model_id = model_id
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.pipeline = None
        self.load_model()
    
    def load_model(self):
        """Load the Stable Diffusion model"""
        try:
            logger.info(f"Loading model {self.model_id} on {self.device}")
            
            # Load the pipeline with CPU-friendly settings
            self.pipeline = StableDiffusionPipeline.from_pretrained(
                self.model_id,
                torch_dtype=torch.float16 if self.device == "cuda" else torch.float32,
                safety_checker=None,
                requires_safety_checker=False,
                variant="fp16" if self.device == "cuda" else None,
                use_safetensors=True
            )
            
            # Use DPM++ scheduler for better quality
            self.pipeline.scheduler = DPMSolverMultistepScheduler.from_config(
                self.pipeline.scheduler.config
            )
            
            # Move to device
            self.pipeline = self.pipeline.to(self.device)
            
            # CPU-specific optimizations
            if self.device == "cpu":
                # Enable attention slicing for lower memory usage
                try:
                    self.pipeline.enable_attention_slicing()
                    logger.info("✅ Attention slicing enabled for CPU efficiency")
                except Exception as e:
                    logger.warning(f"⚠️ Could not enable attention slicing: {e}")
                
                # Enable sequential CPU offload if available
                try:
                    self.pipeline.enable_sequential_cpu_offload()
                    logger.info("✅ Sequential CPU offload enabled")
                except Exception as e:
                    logger.warning(f"⚠️ Could not enable sequential CPU offload: {e}")
            
            # Enable memory efficient attention if using CUDA and xformers is available
            if self.device == "cuda":
                try:
                    self.pipeline.enable_xformers_memory_efficient_attention()
                    logger.info("✅ xformers memory efficient attention enabled")
                except Exception as e:
                    logger.warning(f"⚠️ Could not enable xformers: {e}")
                
                try:
                    # Enable CPU offload to save VRAM
                    self.pipeline.enable_model_cpu_offload()
                    logger.info("✅ Model CPU offload enabled")
                except Exception as e:
                    logger.warning(f"⚠️ Could not enable CPU offload: {e}")
            else:
                logger.info("💻 Running on CPU - skipping GPU optimizations")
            
            logger.info("✅ Model loaded successfully!")
            
        except Exception as e:
            logger.error(f"❌ Error loading model: {e}")
            raise
    
    def generate_image(
        self,
        prompt: str,
        negative_prompt: str = "",
        width: int = 512,
        height: int = 512,
        num_inference_steps: int = 20,
        guidance_scale: float = 7.5,
        seed: Optional[int] = None
    ) -> Tuple[Image.Image, dict]:
        """
        Generate an image from text prompt
        
        Args:
            prompt: Text description of the desired image
            negative_prompt: What you don't want in the image
            width: Image width (must be divisible by 8)
            height: Image height (must be divisible by 8)
            num_inference_steps: Number of denoising steps
            guidance_scale: How closely to follow the prompt
            seed: Random seed for reproducibility
            
        Returns:
            Tuple of (generated_image, generation_info)
        """
        try:
            # Validate dimensions
            width = max(64, min(1024, width // 8 * 8))
            height = max(64, min(1024, height // 8 * 8))
            
            # Set seed for reproducibility
            if seed is not None:
                generator = torch.Generator(device=self.device).manual_seed(int(seed))
            else:
                generator = None
                seed = torch.randint(0, 2**32, (1,)).item()
            
            start_time = time.time()
            
            logger.info(f"🎨 Generating image: '{prompt[:50]}...'")
            
            # Generate image
            with torch.inference_mode():
                result = self.pipeline(
                    prompt=prompt,
                    negative_prompt=negative_prompt or None,
                    width=width,
                    height=height,
                    num_inference_steps=num_inference_steps,
                    guidance_scale=guidance_scale,
                    generator=generator
                )
            
            image = result.images[0]
            generation_time = time.time() - start_time
            
            # Save image
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"generated_{timestamp}_{seed}.png"
            output_path = os.path.join("outputs", filename)
            os.makedirs("outputs", exist_ok=True)
            image.save(output_path)
            
            # Generation info
            info = {
                "prompt": prompt,
                "negative_prompt": negative_prompt,
                "width": width,
                "height": height,
                "steps": num_inference_steps,
                "guidance_scale": guidance_scale,
                "seed": seed,
                "generation_time": round(generation_time, 2),
                "saved_as": filename,
                "model": self.model_id,
                "device": self.device
            }
            
            logger.info(f"✅ Image generated in {generation_time:.2f}s")
            
            return image, info
            
        except Exception as e:
            logger.error(f"❌ Error generating image: {e}")
            raise

# Initialize the generator
print("🚀 Initializing DreamForge Studio...")
generator = TextToImageGenerator()

def enhance_prompt(prompt: str, use_enhancer: bool = True) -> str:
    """Enhance the prompt with style and quality modifiers"""
    if not use_enhancer or not prompt.strip():
        return prompt
    
    # Add quality and style enhancers
    enhancers = [
        "high quality", "detailed", "professional", "artistic",
        "4k resolution", "sharp focus", "well-composed"
    ]
    
    # Check if prompt already has quality terms
    prompt_lower = prompt.lower()
    missing_enhancers = [e for e in enhancers if e not in prompt_lower]
    
    if missing_enhancers:
        # Add a few key enhancers
        selected_enhancers = missing_enhancers[:3]
        enhanced = f"{prompt}, {', '.join(selected_enhancers)}"
        return enhanced
    
    return prompt

def generate_image_gradio(
    prompt,
    negative_prompt,
    style_preset,
    width,
    height,
    steps,
    use_enhancer
):
    """Gradio interface function for image generation"""
    try:
        if not prompt or not prompt.strip():
            return None
        
        # Apply style preset
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
        
        # Enhance prompt if requested
        enhanced_prompt = enhance_prompt(prompt, use_enhancer)
        
        # Generate image
        image, info = generator.generate_image(
            prompt=enhanced_prompt,
            negative_prompt=negative_prompt,
            width=int(width),
            height=int(height),
            num_inference_steps=int(steps),
            guidance_scale=7.5,  # Default guidance scale
            seed=None  # Random seed
        )
        
        # Image generated successfully, just return the image
        return image
        
    except Exception as e:
        error_msg = f"❌ Error generating image: {str(e)}"
        logger.error(error_msg)
        return None

def create_gradio_interface():
    """Create the Gradio web interface"""
    
    # Custom CSS for beautiful styling
    custom_css = """
    /* Global Styles */
    .gradio-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 25%, #f093fb 50%, #f5576c 75%, #4facfe 100%);
        min-height: 100vh;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    /* Main container styling */
    .main-container {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 30px;
        margin: 20px;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    /* Header styling */
    .header-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 15px;
        padding: 40px 30px;
        text-align: center;
        margin-bottom: 30px;
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
        position: relative;
        overflow: hidden;
    }
    
    .header-container::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
        animation: shimmer 3s ease-in-out infinite;
    }
    
    @keyframes shimmer {
        0%, 100% { transform: rotate(0deg); }
        50% { transform: rotate(180deg); }
    }
    
    .header-title {
        color: white;
        font-size: 3.5em;
        font-weight: 700;
        margin: 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        letter-spacing: -1px;
        position: relative;
        z-index: 1;
    }
    
    .header-subtitle {
        color: rgba(255,255,255,0.9);
        font-size: 1.3em;
        margin: 15px 0 0 0;
        font-weight: 300;
        position: relative;
        z-index: 1;
    }
    
    /* Glass card effect */
    .glass-card {
        background: rgba(255, 255, 255, 0.85);
        backdrop-filter: blur(15px);
        border-radius: 20px;
        padding: 30px;
        border: 1px solid rgba(255, 255, 255, 0.3);
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.1);
        margin: 20px 0;
        transition: all 0.3s ease;
    }
    
    .glass-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 50px rgba(0, 0, 0, 0.15);
    }
    
    /* Input styling */
    .input-group textarea, .input-group input, .input-group select {
        border-radius: 15px !important;
        border: 2px solid rgba(102, 126, 234, 0.3) !important;
        padding: 15px 20px !important;
        font-size: 16px !important;
        transition: all 0.3s ease !important;
        background: rgba(255, 255, 255, 0.9) !important;
        box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1) !important;
    }
    
    .input-group textarea:focus, .input-group input:focus, .input-group select:focus {
        border-color: #667eea !important;
        box-shadow: 0 0 25px rgba(102, 126, 234, 0.3) !important;
        transform: translateY(-2px) !important;
        background: rgba(255, 255, 255, 1) !important;
    }
    
    /* Button styling */
    .generate-btn button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        border: none !important;
        border-radius: 20px !important;
        padding: 18px 40px !important;
        font-size: 18px !important;
        font-weight: 700 !important;
        color: white !important;
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.4) !important;
        transition: all 0.3s ease !important;
        text-transform: uppercase !important;
        letter-spacing: 1px !important;
        cursor: pointer !important;
    }
    
    .generate-btn button:hover {
        transform: translateY(-3px) !important;
        box-shadow: 0 15px 40px rgba(102, 126, 234, 0.6) !important;
        background: linear-gradient(135deg, #764ba2 0%, #667eea 100%) !important;
    }
    
    /* Slider styling */
    .slider-container .gr-slider {
        background: linear-gradient(to right, #667eea, #764ba2) !important;
        border-radius: 15px !important;
        overflow: hidden !important;
    }
    
    /* Image output styling */
    .image-output {
        border-radius: 20px !important;
        overflow: hidden !important;
        box-shadow: 0 15px 40px rgba(0, 0, 0, 0.2) !important;
        border: 3px solid rgba(102, 126, 234, 0.3) !important;
        transition: all 0.3s ease !important;
    }
    
    .image-output:hover {
        transform: scale(1.02);
        box-shadow: 0 20px 50px rgba(0, 0, 0, 0.3) !important;
    }
    
    /* Section headers */
    .section-header {
        color: #4a5568;
        font-size: 2em;
        font-weight: 700;
        margin-bottom: 25px;
        text-align: center;
        position: relative;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
    }
    
    .section-header::after {
        content: '';
        position: absolute;
        bottom: -10px;
        left: 50%;
        transform: translateX(-50%);
        width: 100px;
        height: 4px;
        background: linear-gradient(135deg, #667eea, #764ba2);
        border-radius: 2px;
    }
    
    /* Accordion styling */
    .accordion-container {
        background: rgba(102, 126, 234, 0.1) !important;
        border-radius: 15px !important;
        border: 2px solid rgba(102, 126, 234, 0.2) !important;
        margin: 20px 0 !important;
        overflow: hidden !important;
    }
    
    /* Footer styling */
    .footer-container {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        border-radius: 20px;
        padding: 30px;
        text-align: center;
        margin-top: 50px;
        box-shadow: 0 15px 40px rgba(240, 147, 251, 0.4);
        position: relative;
        overflow: hidden;
    }
    
    .footer-container::before {
        content: '';
        position: absolute;
        top: -2px;
        left: -2px;
        right: -2px;
        bottom: -2px;
        background: linear-gradient(45deg, #667eea, #764ba2, #f093fb, #f5576c);
        border-radius: 22px;
        z-index: -1;
        animation: borderGlow 3s ease-in-out infinite;
    }
    
    @keyframes borderGlow {
        0%, 100% { opacity: 0.7; }
        50% { opacity: 1; }
    }
    
    .footer-text {
        color: #000000;
        font-size: 1.2em;
        font-weight: 600;
        margin: 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        position: relative;
        z-index: 1;
    }
    
    /* Gradio footer styling */
    .gradio-container .footer {
        color: #000000 !important;
    }
    
    .gradio-container .footer a {
        color: #000000 !important;
    }
    
    .gradio-container .footer span {
        color: #000000 !important;
    }
    
    /* Target specific footer elements */
    footer, .footer, [class*="footer"] {
        color: #000000 !important;
    }
    
    footer a, .footer a, [class*="footer"] a {
        color: #000000 !important;
    }
    
    footer span, .footer span, [class*="footer"] span {
        color: #000000 !important;
    }
    
    /* Animations */
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .animate-fade-in {
        animation: fadeInUp 0.6s ease-out;
    }
    
    @keyframes pulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.05); }
    }
    
    .pulse-animation {
        animation: pulse 2s ease-in-out infinite;
    }
    
    /* Responsive design */
    @media (max-width: 768px) {
        .header-title {
            font-size: 2.5em;
        }
        .glass-card {
            margin: 15px 0;
            padding: 20px;
        }
        .section-header {
            font-size: 1.6em;
        }
    }
    """
    
    with gr.Blocks(title="🌟 DreamForge Studio", theme=gr.themes.Soft(), css=custom_css) as interface:
        
        # Header with enhanced styling
        gr.HTML("""
        <div class="header-container">
            <h1 class="header-title">🌟 DreamForge Studio</h1>
            <p class="header-subtitle">Where imagination meets Reality</p>
        </div>
        """)
        
        with gr.Row():
            # Input controls with glass card effect
            with gr.Column(scale=1, elem_classes="glass-card"):
                gr.HTML('<div class="section-header">🎯 Forge Your Vision</div>')
                
                prompt_input = gr.Textbox(
                    label="✨ Describe your masterpiece",
                    lines=4,
                    value="A breathtaking sunset over a mystical mountain range with ancient ruins",
                    elem_classes="input-group"
                )
                
                style_preset = gr.Dropdown(
                    label="🎨 Choose Your Style",
                    choices=[
                        "None", "📸 Photorealistic", "🎨 Artistic", "🌟 Cinematic",
                        "✨ Fantasy", "🔮 Sci-Fi", "🏞️ Landscape", "👤 Portrait", "🎭 Vintage"
                    ],
                    value="📸 Photorealistic",
                    elem_classes="input-group"
                )
                
                negative_prompt = gr.Textbox(
                    label="🚫 What to avoid",
                    lines=2,
                    value="low quality, blurry, distorted, deformed, ugly",
                    elem_classes="input-group"
                )
                
                with gr.Accordion("🔧 Advanced Controls", open=False, elem_classes="accordion-container"):
                    with gr.Row():
                        width_slider = gr.Slider(
                            minimum=256, maximum=1024, value=512, step=64,
                            label="📏 Width",
                            elem_classes="slider-container"
                        )
                        height_slider = gr.Slider(
                            minimum=256, maximum=1024, value=512, step=64,
                            label="📏 Height",
                            elem_classes="slider-container"
                        )
                    
                    steps_slider = gr.Slider(
                        minimum=10, maximum=50, value=25, step=1,
                        label="🔄 Quality Steps (Higher = Better Quality)",
                        elem_classes="slider-container"
                    )
                
                use_enhancer = gr.Checkbox(
                    label="✨ Auto-enhance prompts for better results",
                    value=True,
                    elem_classes="input-group"
                )
                
                generate_btn = gr.Button(
                    "🎨 Create Magic",
                    variant="primary",
                    size="lg",
                    elem_classes="generate-btn"
                )
            
            # Output display with enhanced styling
            with gr.Column(scale=2, elem_classes="glass-card"):
                gr.HTML('<div class="section-header">🖼️ Your Masterpiece</div>')
                
                image_output = gr.Image(
                    label="Generated Artwork",
                    type="pil",
                    elem_classes="image-output"
                )
        
        # Set up the generate button click
        generate_btn.click(
            fn=generate_image_gradio,
            inputs=[
                prompt_input, negative_prompt, style_preset,
                width_slider, height_slider, steps_slider,
                use_enhancer
            ],
            outputs=[image_output]
        )
        
        # Enhanced Footer
        gr.HTML("""
        <div class="footer-container">
            <p class="footer-text">🌟 DreamForge Studio | Crafting Dreams into Reality</p>
        </div>
        """)
    
    return interface

if __name__ == "__main__":
    print("🌟 Creating DreamForge Studio interface...")
    interface = create_gradio_interface()
    
    print("🚀 Starting the web server...")
    print("📱 Access DreamForge Studio at:")
    print("   🌐 Primary:    http://localhost:7860")
    print("   🌐 Alternative: http://127.0.0.1:7860")
    print("🔄 The interface will automatically open in your browser")
    print("💡 Tip: Be creative and detailed in your prompts!")
    print("⚠️  Windows users: Use localhost:7860 (not 0.0.0.0:7860)")
    print("⏹️  Press Ctrl+C to stop the server")
    print("=" * 70)
    
    # Launch the interface
    # Try multiple ports if 7860 is busy
    import socket
    
    def find_free_port(start_port=7860, max_port=7870):
        """Find a free port starting from start_port"""
        for port in range(start_port, max_port + 1):
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.bind(('127.0.0.1', port))
                    return port
            except OSError:
                continue
        return None
    
    # Find an available port
    available_port = find_free_port()
    if available_port:
        print(f"🔄 Port 7860 busy, using port {available_port}")
        print(f"📱 Updated URL: http://localhost:{available_port}")
    else:
        available_port = 7860  # Fallback to original
    
    interface.launch(
        server_name="127.0.0.1",  # Changed from 0.0.0.0 for Windows compatibility
        server_port=available_port,
        share=False,
        debug=False,
        show_error=True,
        inbrowser=True  # Automatically open browser
    )
