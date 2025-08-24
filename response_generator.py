from openai import OpenAI
from dotenv import load_dotenv
from PyPDF2 import PdfReader
import os, io


load_dotenv()
chat_model = "gpt-5-mini"
chat_client = OpenAI(api_key=os.getenv("openai_api_key"))


system_prompt = """
Your mission is to clarify legal terms, explain basic rights, and outline common legal processes.
Use simple language to ensure clarity.
Always provide general legal information and help users understand legal concepts without offering specific legal advice.
Specify that **you are not a lawyer and cannot represent clients or provide legal counsel**.
Use web search whenever necessary to ensure that your information is accurate and up-to-date.
Your tone is always: confident, formal, objective, and informative.
You will **not** identify yourself to the user.
Limit responses to 5 or fewer lines.
"""


def file_processor(files):
    if not files:
        return ""

    content = ""
    for file_name in files:
        try:
            lower = file_name.lower()

            if lower.endswith(".txt"):
                with open(file_name, "r", encoding="utf-8") as f:
                    txt_content = f.read()
                content += f"\n=== {file_name} ===\n{txt_content}\n"

            elif lower.endswith(".pdf"):
                with open(file_name, "rb") as f:
                    pdf_bytes = io.BytesIO(f.read())
                reader = PdfReader(pdf_bytes)
                page_texts = []
                for page in reader.pages:
                    t=page.extract_text() or ""
                    page_texts.append(t.strip())
                pdf_text = "\n".join(page_texts).strip()
                if pdf_text:
                    content += f"\n=== {file_name} ===\n{pdf_text}\n"
                else:
                    content += (
                        f"\n=== {file_name} ===\n"
                        f"(No selectable text found. This PDF may be scanned or image-based. Consider OCR.)\n"
                        )

            else:
                content += f"\nSkipping unsupported file type: {file_name}\n"

        except Exception as e:
            content += f"\nError reading {file_name}: {str(e)}\n"

    return content



history = []

def model_response(message,gradio_history):
    global history
    
    full_message = message["text"] or ""

    file_content = file_processor(message['files']) if message['files'] else None
    if file_content is not None:
        full_message = f"{full_message}\n\nUploaded file content:\n{file_content}"
    
    if len(history)>20:
        history = history[2:]
    
    inputs_for_model = []
    if history:
        inputs_for_model.extend(history)
    
    inputs_for_model.append({"role":"user", "content":full_message})
    
    model_response = chat_client.responses.create(
        model=chat_model, 
        instructions= system_prompt, 
        input= inputs_for_model, 
        store= False, 
        tools=[{"type":"web_search_preview", "search_context_size":"medium"}],
        text={"verbosity":"low"}, 
        reasoning={"effort":"medium"}
    )
    final_response = model_response.output_text.strip()
    history.extend([
        {"role":"user", "content":full_message}, 
        {"role":"assistant","content":final_response}
    ])

    return final_response