<div align="center">

# NotebookLM CLI Skill (Fork)

**A robust, maintained fork of the [NotebookLM Claude Code Skill](https://github.com/PleasePrompto/notebooklm-skill)**

** optimized for Windows, Gemini CLI, and general automation**

> interact with Google NotebookLM directly from your terminal or AI agents. Query your notebooks for source-grounded, citation-backed answers. Features improved timeout handling, robust authentication, and Windows compatibility.

</div>

---

## 🚀 Why This Fork?

The original tool was designed specifically for "Claude Code" on macOS/Linux. This fork extends the functionality to be:
1.  **Windows Compatible:** Optimized paths, environment handling, and UTF-8 encoding for Windows.
2.  **Agent Agnostic:** Works with **Gemini CLI**, standard Python scripts, or any tool that can run shell commands.
3.  **More Robust:** Increased timeouts, better error handling, and **Async Architecture** for modern agent loops.
4.  **Flexible Auth:** Supports manual cookie injection for when automated browser login fails.

---

## 🛠️ Usage

### Prerequisites
*   Python 3.10+
*   Google Chrome (or Chromium will be installed automatically)

### Installation

```bash
git clone https://github.com/jpeirce/notebooklm-skill
cd notebooklm-skill
```

### 1. Setup & Authentication

The tool needs to log in to your Google account.

**Automatic Method (Try this first):**
```bash
python scripts/run.py auth_manager.py setup
```
*A browser window will open. Log in to Google, then close the window.*

**Manual Cookie Method (If automation fails):**
1.  Log in to [NotebookLM](https://notebooklm.google.com) in your regular browser (Firefox/Chrome).
2.  Open Developer Tools (F12) -> Console.
3.  Run the script found in `sourced/js.txt` (or below).
4.  Save the JSON output to `data/browser_state/state.json`.

```javascript
(function() {
  const cookies = document.cookie.split(';').map(c => {
    const [name, value] = c.trim().split('=');
    return { name, value, domain: '.google.com', path: '/', expires: 1798132881, httpOnly: false, secure: true, sameSite: 'Lax' };
  });
  copy(JSON.stringify({ cookies, origins: [] }));
  console.log("Copied to clipboard!");
})();
```

### 2. Manage Notebooks

**List Notebooks:**
```bash
python scripts/run.py notebook_manager.py list
```

**Add a Notebook:**
```bash
python scripts/run.py notebook_manager.py add \
  --url "https://notebooklm.google.com/notebook/..." \
  --name "My Docs" \
  --description "Project documentation" \
  --topics "docs,project"
```

### 3. Query NotebookLM

```bash
python scripts/run.py ask_question.py \
  --question "What does the documentation say about the API?" \
  --notebook-id "my-docs"
```

---

## 🤖 Integration with AI Agents

This tool is designed to be a **Skill** for AI agents.

**For Gemini CLI / Generic Agents:**
Add these instructions to your agent's system prompt or `GEMINI.md`:

```markdown
## NotebookLM Integration
This vault is integrated with Google NotebookLM for advanced query and retrieval.

### Workflows
*   **Querying:** `python scripts/run.py ask_question.py --question "Your question here"`
*   **Library Management:** `python scripts/run.py notebook_manager.py list`
```

**For Claude Code:**
Follow the original instructions in `SKILL.md` (included in this repo).

---

## ⚠️ Disclaimer

This tool uses browser automation (Patchright/Playwright) to interact with Google services.
*   **Use at your own risk.** Automated interaction with Google services *can* theoretically lead to account flagging, though this tool uses stealth techniques to mimic human behavior.
*   **Rate Limits:** NotebookLM has rate limits (approx 50 queries/day for free accounts).
*   **Session Cookies:** Your session cookies are stored locally in `data/browser_state/state.json`. **Never commit this file.**

---

## Credits

*   Original Author: [PleasePrompto](https://github.com/PleasePrompto/notebooklm-skill)
*   Fork Maintainer: [jpeirce](https://github.com/jpeirce)

```