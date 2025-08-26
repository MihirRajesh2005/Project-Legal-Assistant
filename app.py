import gradio as gr
import tempfile
import os
import shutil
from response_generator import model_response

def chat_interface(message, history, files):
    """Simple chat function that connects to the backend."""


    file_paths = []
    if files:
        for file in files:
            if file is not None:
                temp_dir = tempfile.mkdtemp()
                temp_path = os.path.join(temp_dir, os.path.basename(file.name))
                shutil.copy2(file.name, temp_path)
                file_paths.append(temp_path)


    backend_message = {
        "text": message or "",
        "files": file_paths if file_paths else None
    }

    try:
        response = model_response(backend_message, history)

        for path in file_paths:
            try:
                os.remove(path)
                os.rmdir(os.path.dirname(path))
            except:
                pass

        return response

    except Exception as e:
        return f"Error: {str(e)}"


css = """
.header-section {
    text-align: center;
    padding: 25px;
    background: linear-gradient(135deg, #1e3a8a 0%, #2563eb 100%);
    color: white;
    border-radius: 12px;
    margin-bottom: 20px;
    box-shadow: 0 4px 12px rgba(30, 58, 138, 0.3);
}

.disclaimer-section {
    background: #fef3c7;
    border: 2px solid #f59e0b;
    border-radius: 8px;
    padding: 15px;
    margin-bottom: 20px;
    font-size: 0.95rem;
}
"""


with gr.Blocks(title="Legal Assistant", css=css) as demo:


    gr.HTML("""
    <div class="header-section">
        <h1 style="margin: 0; font-size: 2.2rem;">⚖️ Legal Assistant</h1>
        <p style="margin: 8px 0 0 0; font-size: 1.1rem;">AI-powered legal information and document analysis</p>
    </div>
    """)


    gr.HTML("""
    <div class="disclaimer-section">
        <strong style="color: #92400e;">⚠️ Important Legal Disclaimer:</strong> 
        This AI provides general legal information only and cannot replace professional legal advice. 
        I am not a lawyer and cannot represent clients or provide legal counsel. 
        For specific legal matters, please consult with a qualified attorney.
    </div>
    """)


    chatbot = gr.Chatbot(
        height=400,
        avatar_images=(None, "⚖️"),
        show_copy_button=True
    )


    with gr.Row():
        msg = gr.Textbox(
            placeholder="Ask about legal terms, rights, or processes...", 
            container=False, 
            scale=4,
            lines=2
        )
        files = gr.File(
            file_count="multiple", 
            file_types=[".pdf", ".txt"],
            scale=1,
            container=True,
            height=60
        )

    # Buttons
    with gr.Row():
        submit = gr.Button("⚖️ Get Legal Information", variant="primary", size="lg")
        clear = gr.Button("🗑️ Clear Chat", variant="secondary")

    # Examples
    gr.Markdown("### 📋 Example Questions")
    examples = gr.Examples(
        examples=[
            ["What is a contract and what makes it legally binding?"],
            ["Explain the difference between civil and criminal law"],
            ["What are my rights during a police stop?"],
            ["How does small claims court work?"]
        ],
        inputs=msg,
        label=""
    )

    # Event handlers
    def handle_chat(message, history, files):
        response = chat_interface(message, history, files)
        history.append([message, response])
        return history, ""

    submit.click(
        handle_chat,
        [msg, chatbot, files],
        [chatbot, msg]
    ).then(lambda: None, outputs=files)

    msg.submit(
        handle_chat,
        [msg, chatbot, files],
        [chatbot, msg] 
    ).then(lambda: None, outputs=files)

    clear.click(lambda: [], outputs=chatbot)

if __name__ == "__main__":
    demo.launch()
