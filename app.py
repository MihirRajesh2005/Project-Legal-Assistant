import gradio as gr
import os
from response_generator import model_response


custom_css = """
/* Main container styling */
.gradio-container {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    max-width: 1200px;
    margin: 0 auto;
}

/* Header styling with LOCAL background image */
.header-container {
    background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%);
    color: white;
    padding: 3rem 2rem;
    border-radius: 16px;
    margin-bottom: 2rem;
    text-align: center;
    box-shadow: 0 8px 16px rgba(0, 0, 0, 0.15);
    position: relative;
    overflow: hidden;
}

/* Fallback gradient if image doesn't load */
.header-container-fallback {
    background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%);
    color: white;
    padding: 3rem 2rem;
    border-radius: 16px;
    margin-bottom: 2rem;
    text-align: center;
    box-shadow: 0 8px 16px rgba(0, 0, 0, 0.15);
    position: relative;
    overflow: hidden;
}

.header-container::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: radial-gradient(circle at 30% 40%, rgba(255, 255, 255, 0.1) 0%, transparent 50%);
    pointer-events: none;
}

.header-title {
    font-size: 3rem;
    font-weight: 800;
    margin-bottom: 0.75rem;
    text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
    position: relative;
    z-index: 1;
}

.header-subtitle {
    font-size: 1.2rem;
    opacity: 0.95;
    font-weight: 500;
    position: relative;
    z-index: 1;
    text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.2);
}

/* Rest of CSS remains the same as enhanced version */
.legal-icon {
    width: 32px;
    height: 32px;
    display: inline-block;
    margin: 0 8px;
    vertical-align: middle;
}

.section-header {
    display: flex;
    align-items: center;
    gap: 12px;
    margin: 1.5rem 0 1rem 0;
    color: #374151;
    font-weight: 600;
}

.section-icon {
    width: 24px;
    height: 24px;
    opacity: 0.8;
}

/* Chat container styling */
.chat-container {
    border: 1px solid #e5e7eb;
    border-radius: 16px;
    overflow: hidden;
    background: white;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
    position: relative;
}

.chat-container::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 4px;
    background: linear-gradient(90deg, #3b82f6, #1e40af, #3b82f6);
    z-index: 1;
}

/* Input area styling */
.input-container {
    background: linear-gradient(145deg, #f8fafc 0%, #f1f5f9 100%);
    border-top: 1px solid #e5e7eb;
    padding: 1.5rem;
    position: relative;
}

/* Disclaimer styling */
.disclaimer {
    background: linear-gradient(135deg, #fef3cd 0%, #fde68a 100%);
    border: 1px solid #f59e0b;
    border-left: 4px solid #d97706;
    color: #92400e;
    padding: 1.25rem;
    border-radius: 12px;
    margin: 1.5rem 0;
    font-size: 0.95rem;
    line-height: 1.6;
    position: relative;
    box-shadow: 0 2px 8px rgba(217, 119, 6, 0.1);
}

.disclaimer-title {
    font-weight: 700;
    margin-bottom: 0.75rem;
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 1rem;
}

/* Enhanced button styling */
.submit-button {
    background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 0.875rem 2rem !important;
    font-weight: 600 !important;
    font-size: 1rem !important;
    transition: all 0.3s ease !important;
    box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3) !important;
}

.submit-button:hover {
    background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%) !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 16px rgba(59, 130, 246, 0.4) !important;
}

/* Clear button styling */
.clear-button {
    background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 0.75rem 1.5rem !important;
    font-weight: 600 !important;
    transition: all 0.3s ease !important;
    box-shadow: 0 4px 12px rgba(239, 68, 68, 0.3) !important;
}

.clear-button:hover {
    background: linear-gradient(135deg, #dc2626 0%, #b91c1c 100%) !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 16px rgba(239, 68, 68, 0.4) !important;
}

/* Example sections styling */
.example-section {
    background: linear-gradient(145deg, #ffffff 0%, #f8fafc 100%);
    border: 1px solid #e5e7eb;
    border-radius: 12px;
    padding: 1.25rem;
    margin: 0.75rem 0;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
    transition: all 0.3s ease;
}

.example-section:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
    border-color: #3b82f6;
}

/* Footer styling */
.footer {
    text-align: center;
    padding: 2rem 1rem;
    color: #6b7280;
    font-size: 0.9rem;
    border-top: 1px solid #e5e7eb;
    margin-top: 3rem;
    background: linear-gradient(145deg, #f9fafb 0%, #f3f4f6 100%);
    border-radius: 12px 12px 0 0;
}

/* Feature highlights */
.feature-highlight {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 0.75rem;
    background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%);
    border-radius: 8px;
    margin: 0.5rem 0;
    border-left: 3px solid #0891b2;
}

.feature-icon {
    width: 20px;
    height: 20px;
    opacity: 0.8;
}

/* Responsive design */
@media (max-width: 768px) {
    .header-title {
        font-size: 2.2rem;
    }

    .header-subtitle {
        font-size: 1rem;
    }

    .header-container {
        padding: 2rem 1rem;
    }
}
"""

def create_legal_assistant_interface():
    with gr.Blocks(
        css=custom_css,
        title="AI Legal Assistant",
        theme=gr.themes.Soft(
            primary_hue="blue",
            secondary_hue="slate", 
            neutral_hue="slate",
            spacing_size="lg",
            radius_size="lg"
        )
    ) as demo:

        # Header
        gr.HTML("""
            <div class="header-container">
                <h1 class="header-title">⚖️ AI Legal Assistant</h1>
                <p class="header-subtitle">
                    🤖 Powered by AI • 📚 Legal Knowledge Base • 🔒 Confidential & Secure
                </p>
                <div style="margin-top: 1rem; font-size: 0.9rem; opacity: 0.8;">
                    Get clear explanations of legal concepts and basic rights information
                </div>
            </div>
        """)

        gr.HTML("""
            <div class="disclaimer">
                <div class="disclaimer-title">
                    ⚠️ Important Legal Disclaimer
                </div>
                <div style="display: flex; align-items: flex-start; gap: 1rem;">
<div>
                        This AI assistant provides <strong>general legal information</strong> and educational content only. 
                        It is <strong>not a lawyer</strong> and cannot provide legal advice, represent clients, 
                        or substitute for professional legal counsel. For specific legal matters, please consult 
                        with a qualified attorney.
                    </div>
                </div>
            </div>
        """)

        with gr.Column(elem_classes="chat-container"):
            # Feature highlights
            gr.HTML("""
                <div style="padding: 1rem 1.5rem; background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);">
                    <div class="feature-highlight">
                        <span class="feature-icon">📄</span>
                        <span><strong>Document Analysis:</strong> Upload .txt and .pdf files for legal document review</span>
                    </div>
                    <div class="feature-highlight">
                        <span class="feature-icon">🧠</span>
                        <span><strong>AI-Powered:</strong> Advanced legal knowledge with web search capabilities</span>
                    </div>
                    <div class="feature-highlight">
                        <span class="feature-icon">🔒</span>
                        <span><strong>Secure & Private:</strong> Your conversations and documents remain confidential</span>
                    </div>
                </div>
            """)

            chatbot = gr.Chatbot(
                label="Legal Assistant Chat",
                height=500,
                show_label=False,
                bubble_full_width=False,
                show_copy_button=True,
                layout="panel",
                placeholder="👋 Welcome to your AI Legal Assistant! Ask me any legal question or upload a document for analysis...",
                avatar_images=(None, None)
            )

            # Input area
            with gr.Column(elem_classes="input-container"):
                gr.HTML("""
                    <div class="section-header">
<span>Ask a Question or Upload Documents</span>
                    </div>
                """)

                with gr.Row():
                    msg_input = gr.MultimodalTextbox(
                        file_count="multiple",
                        file_types=[".txt", ".pdf"],
                        placeholder="💬 Type your legal question here, or drag & drop documents (.txt, .pdf) for analysis...",
                        container=True,
                        scale=4,
                        show_label=False
                    )

                with gr.Row():
                    submit_btn = gr.Button(
                        "📤 Send Message",
                        variant="primary",
                        elem_classes="submit-button",
                        scale=2
                    )
                    clear_btn = gr.Button(
                        "🗑️ Clear Chat",
                        variant="secondary", 
                        elem_classes="clear-button",
                        scale=1
                    )

        # Example questions
        gr.HTML("""
            <div class="section-header" style="margin-top: 3rem;">
<span>💡 Example Legal Questions</span>
            </div>
        """)

        with gr.Row():
            with gr.Column(scale=1, elem_classes="example-section"):
                gr.HTML("<h4 style='color: #1e40af; margin-bottom: 1rem;'>⚖️ Rights & Procedures</h4>")
                gr.Examples(
                    examples=[
                        ["What are my rights during a police stop?"],
                        ["Explain the difference between civil and criminal law"],
                        ["What is a copyright and how long does it last?"],
                        ["What should I know about Miranda rights?"]
                    ],
                    inputs=[msg_input],
                    label=None
                )

            with gr.Column(scale=1, elem_classes="example-section"):
                gr.HTML("<h4 style='color: #1e40af; margin-bottom: 1rem;'>📋 Contracts & Employment</h4>")
                gr.Examples(
                    examples=[
                        ["What should I know about rental agreements?"],
                        ["Explain the basics of employment law"],
                        ["What are the key elements of a valid contract?"],
                        ["What is wrongful termination?"]
                    ],
                    inputs=[msg_input],
                    label=None
                )

            with gr.Column(scale=1, elem_classes="example-section"):
                gr.HTML("<h4 style='color: #1e40af; margin-bottom: 1rem;'>🏛️ Legal Processes</h4>")
                gr.Examples(
                    examples=[
                        ["How does the small claims court process work?"],
                        ["What is the difference between a will and a trust?"],
                        ["Explain the basics of business formation"],
                        ["What happens during a bankruptcy filing?"]
                    ],
                    inputs=[msg_input],
                    label=None
                )

        # Footer
        gr.HTML("""
            <div class="footer">
                <div style="display: flex; justify-content: center; align-items: center; gap: 2rem; margin-bottom: 1rem;">
                    <div style="display: flex; align-items: center; gap: 0.5rem;">
                        <span>⚖️</span>
                        <span>Built with Gradio</span>
                    </div>
                    <div style="display: flex; align-items: center; gap: 0.5rem;">
                        <span>🎓</span>
                        <span>For Educational Purposes</span>
                    </div>
                    <div style="display: flex; align-items: center; gap: 0.5rem;">
                        <span>👨‍⚖️</span>
                        <span>Consult Real Attorneys</span>
                    </div>
                </div>
                <p style="margin: 0; font-size: 0.85rem; opacity: 0.8;">
                    🔒 Your privacy is protected • 🌐 Powered by OpenAI • 📚 Legal information database
                </p>
            </div>
        """)

        # Chat functionality
        def respond_to_message(message, chat_history):
            if not message["text"] and not message["files"]:
                return chat_history, {"text": "", "files": []}

            try:
                bot_response = model_response(message, chat_history)
                user_msg = message["text"] if message["text"] else ""
                if message["files"]:
                    file_names = [os.path.basename(f) for f in message["files"]]
                    user_msg += f"\n📎 Uploaded files: {', '.join(file_names)}"

                chat_history.append([user_msg, bot_response])
                return chat_history, {"text": "", "files": []}

            except Exception as e:
                error_msg = f"⚠️ I apologize, but I encountered an error processing your request: {str(e)}"
                chat_history.append([message["text"] or "📄 File upload", error_msg])
                return chat_history, {"text": "", "files": []}

        def clear_chat():
            try:
                from response_generator import history
                history.clear()
            except:
                pass
            return []

        # Event handlers
        submit_btn.click(respond_to_message, [msg_input, chatbot], [chatbot, msg_input])
        msg_input.submit(respond_to_message, [msg_input, chatbot], [chatbot, msg_input])
        clear_btn.click(clear_chat, outputs=[chatbot])

    return demo

if __name__ == "__main__":
    demo = create_legal_assistant_interface()
    demo.launch(
        share=False,
        server_name="0.0.0.0",
        server_port=7860,
        show_error=True,
        debug=True
    )