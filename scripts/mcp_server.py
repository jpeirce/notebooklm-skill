from mcp.server.fastmcp import FastMCP
from typing import List, Optional
import sys
import io
from pathlib import Path

# Force UTF-8 encoding for stdout/stderr on Windows to handle emojis
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# Add the scripts directory to the python path so we can import our modules
sys.path.insert(0, str(Path(__file__).parent))

from notebook_manager import NotebookLibrary
from ask_question import ask_notebooklm

# Initialize the MCP server
mcp = FastMCP("NotebookLM Skill")

@mcp.tool()
async def query_notebook(question: str, notebook_id: Optional[str] = None) -> str:
    """
    Ask a question to a Google NotebookLM notebook.
    
    Args:
        question: The question to ask.
        notebook_id: Optional ID of the notebook to query. If not provided, uses the active notebook.
    """
    library = NotebookLibrary()
    
    # Resolve notebook URL
    notebook_url = None
    if notebook_id:
        notebook = library.get_notebook(notebook_id)
        if not notebook:
            return f"Error: Notebook with ID '{notebook_id}' not found."
        notebook_url = notebook['url']
    else:
        active = library.get_active_notebook()
        if not active:
            return "Error: No active notebook selected. Please specify a notebook_id or set an active one."
        notebook_url = active['url']
        
    # Ask the question
    # Note: We run headless by default for the MCP server
    answer = await ask_notebooklm(question, notebook_url, headless=True)
    
    if answer:
        return answer
    else:
        return "Error: Failed to get an answer (Server Updated). Check logs."

@mcp.tool()
def list_notebooks() -> str:
    """
    List all available notebooks in the local library.
    """
    library = NotebookLibrary()
    notebooks = library.list_notebooks()
    
    if not notebooks:
        return "Library is empty. Use add_notebook to add one."
        
    output = ["Notebook Library:"]
    for nb in notebooks:
        active = " [ACTIVE]" if nb['id'] == library.active_notebook_id else ""
        output.append(f"- {nb['name']} (ID: {nb['id']}){active}")
        output.append(f"  Topics: {', '.join(nb['topics'])}")
        
    return "\n".join(output)

@mcp.tool()
def add_notebook(url: str, name: str, description: str, topics: str) -> str:
    """
    Add a new notebook to the library.
    
    Args:
        url: The full URL of the NotebookLM notebook.
        name: A short, descriptive name for the notebook.
        description: A description of the notebook's contents.
        topics: Comma-separated list of topics (e.g. "history, genealogy").
    """
    library = NotebookLibrary()
    topic_list = [t.strip() for t in topics.split(',')]
    
    try:
        notebook = library.add_notebook(
            url=url,
            name=name,
            description=description,
            topics=topic_list
        )
        return f"Successfully added notebook: {notebook['name']} (ID: {notebook['id']})"
    except Exception as e:
        return f"Error adding notebook: {str(e)}"

if __name__ == "__main__":
    # Run the server
    mcp.run()
