from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
import json
from rich.console import Console
from rich.markdown import Markdown

load_dotenv()

console = Console()

model = init_chat_model(
    "google_genai:gemini-3.6-flash"
)

response = model.invoke(
    """
    Explain LangChain simply.

    Format the response using:
    - A short heading
    - Three concise bullet points
    - One practical example
"""
)

console.print(Markdown(response.text))