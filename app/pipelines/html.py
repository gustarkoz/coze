import os
from app.render import render_html

def markdown_to_html(md_text: str, output_path: str) -> None:
    title = os.path.splitext(os.path.basename(output_path))[0]
    html = render_html(md_text, title)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)
