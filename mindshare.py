import os
import time
import random
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

input_file = "project_docs.txt"
type_file = "project_types.txt"
os.makedirs("output", exist_ok=True)

tone_emojis = {
    "technical": ["🧠", "⚙️", "📐"],
    "optimistic": ["🚀", "📈", "💡"],
    "curious": ["👀", "🤔"],
    "community": ["🤝", "💬"],
    "value": ["💸", "💰"],
    "decentralized": ["🌐", "🔁"],
}

def load_project_types(file_path):
    mapping = {}
    if not os.path.exists(file_path):
        return mapping
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            if "→" not in line:
                continue
            project, project_type = [x.strip() for x in line.strip().split("→")]
            mapping[project] = project_type
    return mapping

def scrape_full_text(url):
    try:
        response = requests.get(url, timeout=15)
        soup = BeautifulSoup(response.text, "html.parser")
        paragraphs = soup.find_all("p")
        text = "\n".join(p.get_text() for p in paragraphs)
        return text
    except Exception as e:
        return f"[ERROR scraping {url}]: {str(e)}"

def chunk_for_bullets(text, max=5):
    lines = text.split(". ")
    chunks = []
    for line in lines:
        if len(line.strip()) > 50 and len(chunks) < max:
            chunks.append(line.strip())
    return chunks

def make_bold(text):
    table = str.maketrans(
        "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz",
        "𝗔𝗕𝗖𝗗𝗘𝗙𝗚𝗛𝗜𝗝𝗞𝗟𝗠𝗡𝗢𝗣𝗤𝗥𝗦𝗧𝗨𝗩𝗪𝗫𝗬𝗭"
        "𝗮𝗯𝗰𝗱𝗲𝗳𝗴𝗵𝗶𝗷𝗸𝗹𝗺𝗻𝗼𝗽𝗾𝗿𝘀𝘁𝘂𝘃𝘄𝘅𝘆𝘇"
    )
    return text.translate(table)

def get_closer():
    closers = [
        "Would you use this?",
        "Is this the future?",
        "What would you build with it?",
        "Feels underrated — or not?",
        "Let’s hear thoughts 👇",
        "Would you spin one up?",
        "Try it or skip it?",
    ]
    return random.choice(closers)

def pick_emojis():
    flat = [e for group in tone_emojis.values() for e in group]
    return random.sample(flat, k=2)

def format_kaito_post(project, intro, bullets, tag):
    em1, em2 = pick_emojis()
    post = f"{intro.strip()} {em1}\n\n"
    post += f"Here’s what makes it interesting: 👇\n\n"
    for bullet in bullets:
        if ":" in bullet:
            title, body = bullet.split(":", 1)
        elif "–" in bullet:
            title, body = bullet.split("–", 1)
        else:
            title, body = bullet[:30], bullet
        post += f"➥ {make_bold(title.strip())}\n{body.strip()}\n\n"
    post += f"{get_closer()} {tag} {em2}"
    return post.strip()

def generate_post(project_name, chunk, tag, project_type):
    context = f"{project_name} is a {project_type}." if project_type else ""

    prompt = f"""
You're a Web3 user posting on X.

Write a clean, human-style tweet thread about the project below, in this format:

- 1–2 line intro (why it's cool / what it is)
- 3–5 bullets (each starts with a bold heading + one sentence)
- No hashtags, no @mentions
- NO explanation or preamble — just output the tweet
- Use simple, readable English
- Don't include any title like "Here's a thread" or "my attempt"

Project: {project_name}
{context}

Docs:
\"\"\"{chunk}\"\"\"
"""

    try:
        res = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.85,
            max_tokens=600,
        )
        full = res.choices[0].message.content.strip()

        # Extract intro and bullets from response
        lines = full.splitlines()
        intro_lines = []
        bullet_lines = []

        for line in lines:
            if line.strip().startswith(("•", "-", "–", "*")):
                bullet_lines.append(line.strip("•-*– ").strip())
            elif not bullet_lines:
                intro_lines.append(line.strip())

        intro = " ".join(intro_lines)
        bullets = bullet_lines[:5]

        return format_kaito_post(project_name, intro, bullets, tag)

    except Exception as e:
        return f"[ERROR generating for {project_name}]: {str(e)}"

# MAIN RUNNER
project_types = load_project_types(type_file)

with open(input_file, "r", encoding="utf-8") as f:
    lines = f.readlines()

for line in lines:
    if "→" not in line:
        continue

    project, url = [x.strip() for x in line.strip().split("→")]
    tag = f"g{project.lower().replace(' ', '')} ✨"
    project_type = project_types.get(project, "")

    print(f"\n🔍 Scraping docs for {project}")
    full_text = scrape_full_text(url)

    if "[ERROR" in full_text:
        print(full_text)
        continue

    chunks = chunk_for_bullets(full_text)
    if not chunks:
        print(f"[WARN] Not enough content found for {project}")
        continue

    chunk = " ".join(chunks[:3])
    print(f"🧠 Generating Mindshare post for {project}")
    post = generate_post(project, chunk, tag, project_type)

    with open(f"output/{project}.txt", "w", encoding="utf-8") as out:
        out.write(post + "\n")

    time.sleep(2)

print("\n✅ Kaito-optimized Mindshare posts saved in /output/")
