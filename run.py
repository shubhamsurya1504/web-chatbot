import os
from src.app import create_app

if __name__ == "__main__":
    GOOGLE_API_KEY = "put_api_key_here"  # Replace with your API key
    demo = create_app(GOOGLE_API_KEY)
    demo.launch(share=True)