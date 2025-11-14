import os
from fastapi import FastAPI, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from app.utils import ensure_storage_dirs
from app.utils import normalize_filename, build_download_url, get_type_dir
from app.converter import markdown_to_docx
from app.pipelines.excel import markdown_to_xlsx
from app.pipelines.html import markdown_to_html
from app.pipelines.pdf import markdown_to_pdf
from app.pipelines.png import markdown_to_png

app = FastAPI()

ensure_storage_dirs()
app.mount("/files", StaticFiles(directory=os.path.join("storage")), name="files")

class ConvertRequest(BaseModel):
    markdown: str
    filename: str

MAX_MD_BYTES = 1 * 1024 * 1024

@app.post("/convert")
def convert(req: ConvertRequest, request: Request):
    if not req.markdown:
        raise HTTPException(status_code=400, detail="markdown is required")
    if len(req.markdown.encode("utf-8")) > MAX_MD_BYTES:
        raise HTTPException(status_code=413, detail="markdown too large")
    final_name = normalize_filename(req.filename)
    _, converted_dir = ensure_storage_dirs()
    output_path = os.path.join(converted_dir, final_name)
    try:
        markdown_to_docx(req.markdown, output_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    url = build_download_url(request, f"converted/{final_name}")
    return {"filename": final_name, "url": url}

@app.post("/convert/excel")
def convert_excel(req: ConvertRequest, request: Request):
    if not req.markdown:
        raise HTTPException(status_code=400, detail="markdown is required")
    if len(req.markdown.encode("utf-8")) > MAX_MD_BYTES:
        raise HTTPException(status_code=413, detail="markdown too large")
    name = normalize_filename(req.filename)
    name = name[:-5] + '.xlsx'
    dir_path = get_type_dir('xlsx')
    out = os.path.join(dir_path, name)
    try:
        sheets = markdown_to_xlsx(req.markdown, out)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    url = build_download_url(request, f"xlsx/{name}")
    return {"filename": name, "url": url, "sheets": sheets}

@app.post("/convert/pdf")
def convert_pdf(req: ConvertRequest, request: Request):
    if not req.markdown:
        raise HTTPException(status_code=400, detail="markdown is required")
    if len(req.markdown.encode("utf-8")) > MAX_MD_BYTES:
        raise HTTPException(status_code=413, detail="markdown too large")
    name = normalize_filename(req.filename)
    name = name[:-5] + '.pdf'
    dir_path = get_type_dir('pdf')
    out = os.path.join(dir_path, name)
    try:
        markdown_to_pdf(req.markdown, out)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    url = build_download_url(request, f"pdf/{name}")
    return {"filename": name, "url": url}

@app.post("/convert/html")
def convert_html(req: ConvertRequest, request: Request):
    if not req.markdown:
        raise HTTPException(status_code=400, detail="markdown is required")
    if len(req.markdown.encode("utf-8")) > MAX_MD_BYTES:
        raise HTTPException(status_code=413, detail="markdown too large")
    name = normalize_filename(req.filename)
    name = name[:-5] + '.html'
    dir_path = get_type_dir('html')
    out = os.path.join(dir_path, name)
    try:
        markdown_to_html(req.markdown, out)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    url = build_download_url(request, f"html/{name}")
    return {"filename": name, "url": url}

@app.post("/convert/png")
def convert_png(req: ConvertRequest, request: Request):
    if not req.markdown:
        raise HTTPException(status_code=400, detail="markdown is required")
    if len(req.markdown.encode("utf-8")) > MAX_MD_BYTES:
        raise HTTPException(status_code=413, detail="markdown too large")
    name = normalize_filename(req.filename)
    name = name[:-5] + '.png'
    dir_path = get_type_dir('png')
    out = os.path.join(dir_path, name)
    try:
        markdown_to_png(req.markdown, out)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    url = build_download_url(request, f"png/{name}")
    return {"filename": name, "url": url}
