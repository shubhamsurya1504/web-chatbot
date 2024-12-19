import os
import gradio as gr
from src.app import create_app

if __name__ == "__main__":
    # Get Google API key from environment
    google_api_key = os.getenv('GOOGLE_API_KEY')
    if not google_api_key:
        raise ValueError("GOOGLE_API_KEY environment variable is required")

    # Create and launch the app
    demo = create_app(google_api_key)
    
    # Launch with Docker-specific settings
    demo.launch(
        server_name="0.0.0.0",  # Required for Docker
        server_port=7860,
        share=True
    )
################### Without Containerization ########################
"""
import os
from src.app import create_app

if __name__ == "__main__":
    GOOGLE_API_KEY = "put_api_key_here"  # Replace with your API key
    demo = create_app(GOOGLE_API_KEY)
    demo.launch(share=True)
"""
