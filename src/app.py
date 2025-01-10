import gradio as gr
from urllib.parse import urlparse
from .crawler import crawl
from .processor import process_text_files
from .qa_system import QASystem
import os
import dotenv

dotenv.load_dotenv()


class PulseQA:
    def __init__(self, google_api_key):
        self.qa_system = QASystem(google_api_key)
        self.domain = None
    
    def initialize_system(self, url):
        try:
            # Crawl the website
            self.domain = crawl(url)
            
            # Process the text files
            df = process_text_files(self.domain)
            
            # Initialize the QA system
            if self.qa_system.initialize_vectorstore(df):
                return f"Successfully initialized system for domain: {self.domain}"
            else:
                return "Failed to initialize the system"
            
        except Exception as e:
            return f"Error initializing system: {str(e)}"
    
    def answer_question(self, question):
        return self.qa_system.get_answer(question)

def create_app(google_api_key):
    pulse_qa = PulseQA(google_api_key)

    with gr.Blocks(theme=gr.themes.Soft(primary_hue="blue")) as demo:
        gr.Markdown(
            """
            # 🔍 Pulse - Help Website Q&A Agent
            
            Crawl any help website and ask questions about its content!
            """
        )
        
        with gr.Row():
            with gr.Column():
                url_input = gr.Textbox(
                    label="Help Website URL",
                    placeholder="Enter the URL of the help website (e.g., https://help.slack.com)",
                    info="The website URL to crawl and analyze"
                )
                initialize_btn = gr.Button("Initialize System", variant="primary")
                status_output = gr.Textbox(label="Status", interactive=False)
                
        with gr.Row():
            with gr.Column():
                question_input = gr.Textbox(
                    label="Your Question",
                    placeholder="Ask a question about the documentation...",
                    info="Ask anything about the help content"
                )
                question_btn = gr.Button("Get Answer", variant="primary")
                answer_output = gr.Markdown(label="Answer")
        
        initialize_btn.click(
            pulse_qa.initialize_system,
            inputs=[url_input],
            outputs=[status_output]
        )
        
        question_btn.click(
            pulse_qa.answer_question,
            inputs=[question_input],
            outputs=[answer_output]
        )
        
        gr.Markdown(
            """
            ### Instructions:
            1. Enter the URL of the help website you want to analyze
            2. Click "Initialize System" and wait for the crawling and processing to complete
            3. Once initialized, you can ask questions about the documentation
            4. Click "Get Answer" to receive responses based on the content
            
            ### Example Questions:
            - What is [product] and how does it work?
            - How do I configure [feature]?
            - What are the system requirements.?
            """
        )
    
    return demo

if __name__ == "__main__":
    GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')  # Replace with your API key
    demo = create_app(GOOGLE_API_KEY)
    demo.launch(share=True)
