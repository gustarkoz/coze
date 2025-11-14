from markdown import markdown

CSS = """
body{max-width:860px;margin:24px auto;padding:0 16px;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,'Helvetica Neue',Arial,'Noto Sans','Liberation Sans',sans-serif,'Apple Color Emoji','Segoe UI Emoji';color:#24292e}
h1,h2,h3{border-bottom:1px solid #eaecef;padding-bottom:.3em}
code,pre{font-family:ui-monospace,SFMono-Regular,Consolas,'Liberation Mono',Menlo,monospace}
pre{background:#f6f8fa;padding:12px;overflow:auto}
table{border-collapse:collapse;width:100%}
th,td{border:1px solid #d0d7de;padding:6px}
blockquote{color:#57606a;border-left:4px solid #d0d7de;margin:0;padding:0 1em}
img{max-width:100%}
"""

def render_html(md_text: str, title: str) -> str:
    html_body = markdown(md_text, output_format="html5", extensions=["extra"])
    return f"""<!DOCTYPE html><html><head><meta charset='utf-8'><title>{title}</title><style>{CSS}</style></head><body>{html_body}</body></html>"""
