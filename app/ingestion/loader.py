import os
import pypdf
import docx
import json
from bs4 import BeautifulSoup

SUPPORTED_TYPES = {
    "pdf", "txt", "md", "html", "htm", "xml", "docx", "json"
}


def read_pdf(path: str) -> str:
    reader = pypdf.PdfReader(path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text


def read_txt(path: str) -> str:
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        return f.read()


def read_md(path: str) -> str:
    return read_txt(path)


def read_docx(path: str) -> str:
    doc = docx.Document(path)
    return "\n".join([para.text for para in doc.paragraphs])


def read_html(path: str) -> str:
    html = read_txt(path)
    soup = BeautifulSoup(html, "html.parser")
    return soup.get_text(separator="\n")


def read_xml(path: str) -> str:
    xml = read_txt(path)
    soup = BeautifulSoup(xml, "xml")
    return soup.get_text(separator="\n")


def read_json(path: str) -> str:
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return json.dumps(data, indent=2)
    except:
        return read_txt(path)


def load_file(path: str) -> str:
    ext = path.split(".")[-1].lower()

    if ext == "pdf":
        return read_pdf(path)
    if ext in ("txt",):
        return read_txt(path)
    if ext in ("md",):
        return read_md(path)
    if ext in ("docx",):
        return read_docx(path)
    if ext in ("html", "htm"):
        return read_html(path)
    if ext in ("xml",):
        return read_xml(path)
    if ext in ("json",):
        return read_json(path)

    return ""


def iter_documents(data_dir: str):
    """
    Walks data/ directory and returns:
      { "path": full_path, "content": extracted_text }
    """
    for root, _, files in os.walk(data_dir):
        for f in files:
            ext = f.split(".")[-1].lower()
            if ext in SUPPORTED_TYPES:
                full = os.path.join(root, f)
                content = load_file(full)
                yield {"path": full, "content": content}
