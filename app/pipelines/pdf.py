import os
from playwright.sync_api import sync_playwright
from app.render import render_html

def markdown_to_pdf(md_text: str, output_path: str) -> None:
    title = os.path.splitext(os.path.basename(output_path))[0]
    html = render_html(md_text, title)
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.set_content(html, wait_until='load')
        page.pdf(path=output_path, format='A4', print_background=True, margin={'top':'20mm','bottom':'20mm','left':'16mm','right':'16mm'})
        browser.close()
