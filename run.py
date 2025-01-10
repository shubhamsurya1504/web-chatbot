import os
import gradio as gr
from src.app import create_app
import dotenv

dotenv.load_dotenv()

if __name__ == "__main__":
    GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')  # Replace with your API key
    if not GOOGLE_API_KEY:
        raise ValueError("GOOGLE_API_KEY environment variable is required")
    
    # Create and launch the app
    demo = create_app(GOOGLE_API_KEY)
    demo.launch(
        server_name="0.0.0.0",  # Listen on all network interfaces
        server_port=7860,       # Explicitly set the port if needed
        share=True              # Enable sharing if necessary
    )
