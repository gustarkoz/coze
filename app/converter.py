import os
from markdown import markdown
from html2docx import html2docx

def markdown_to_docx(md_text: str, output_path: str) -> None:
    html = markdown(md_text, output_format="html5")
    title = os.path.splitext(os.path.basename(output_path))[0]
    buf = html2docx(html, title=title)
    with open(output_path, "wb") as fp:
        fp.write(buf.getvalue())
