# Web3 Project Mindshare Post Generator Bot

## Overview
This Python script automates generating Twitter/X-style “mindshare” posts about Web3 projects. It scrapes documentation from project URLs, analyzes the content using the Groq AI, and creates human-friendly, engaging posts optimized for social engagement.

The script also includes a Google Sheets-based username and passcode authentication to control access.

## Features
- User authentication on backend
- Scrapes paragraphs from project documentation URLs
- Loads project type metadata to tailor generated posts
- Generates structured posts with intro, bullet points, and casual closers
- Uses Groq AI for natural language generation
- Saves each project’s post in `/output` folder as a text file
- Includes emoji tone mapping for varied post styles

## Prerequisites
- Python 3.8 or higher
- `requests`, `beautifulsoup4`, `python-dotenv`, `groq` Python packages

Install dependencies via pip:

```bash
pip install requests beautifulsoup4 python-dotenv groq
```

- A `.env` file containing your Groq API key:
```
GROQ_API_KEY=your_api_key_here
```

## Usage

1. Prepare a file named `project_docs.txt` listing projects and their docs URLs, one per line in same format:
```
ProjectName → https://projectdocs.url
```

2. (Optional) Prepare `project_types.txt` listing project names and types in same format:
```
ProjectName → ProjectType
```

3. Run the script:
```bash
python Twitter-Mindshare.py
```

4. Enter your username and passcode when prompted.

5. The script scrapes project docs, generates posts, and saves results in `/output`.

## Output

- Each project gets a text file named after it, e.g., `output/ProjectName.txt`
- Posts contain a clean intro, 3-5 bullets with bold headers, emojis, and a casual question.

## Notes

- Network connection required for doc scraping and Groq API calls.
- 
- Rate limiting and error handling are basic; adjust as needed for scale.

## ✅ License

- This script is proprietary and provided only for personal or internal use by the original user or team.

- ❌ You may not redistribute, resell, sublicense, or publicly share this code.

- ✅ You may modify it privately for your own workflows.

- 🧠 All intellectual property rights belong to the original creator.

Contact the author if you wish to license this for broader use.

