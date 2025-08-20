# ui.py
import os, json
import gradio as gr
from response_generator import model_response

BRANDING_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "branding.json"))
with open(BRANDING_PATH, "r", encoding="utf-8") as f:
    branding = json.load(f)["brand"]


with gr.Blocks(theme=gr.themes.Ocean(),  
               title="LegalAI - Sort your Legal Queries") as demo:
    gr.HTML(
       f"""<div style="display: flex; justify-content: center; margin-bottom: 20px;">
        <img src="{branding["logo"]["title"]}" alt="{"Here And Now AI"}" style="height: 100px;">
        </div>"""
        )
    gr.ChatInterface(
    fn=model_response,
    type="messages",
    title="LegalAI - Sort your Legal Queries",
    description="Your legal assistant, built to answer your legal queries.",
    multimodal=True,
    textbox=gr.MultimodalTextbox(
        file_count="single",
        file_types=[".txt",".pdf"],
        placeholder="Ask a legal question or upload TXT/PDF..."
    ),
    examples=["What is a PIL?", "Why is it important to read contracts properly?"]
)

if __name__ == "__main__":
    demo.launch()
