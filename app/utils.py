import os
import re
import datetime
from typing import Tuple

def ensure_storage_dirs() -> Tuple[str, str]:
    base_dir = os.path.join("storage")
    for sub in ["converted", "docx", "xlsx", "pdf", "html", "png"]:
        os.makedirs(os.path.join(base_dir, sub), exist_ok=True)
    converted_dir = os.path.join(base_dir, "converted")
    return base_dir, converted_dir

def get_type_dir(type_name: str) -> str:
    base_dir = os.path.join("storage")
    target = os.path.join(base_dir, type_name)
    os.makedirs(target, exist_ok=True)
    return target

def normalize_filename(name: str) -> str:
    base = re.sub(r'[\\/:*?"<>|]', '', name).strip()
    if not base:
        base = "document"
    if not base.lower().endswith('.docx'):
        base += '.docx'
    stamp = datetime.datetime.now().strftime('%Y%m%d')
    root = base[:-5]
    return f"{root}_{stamp}.docx"

def build_download_url(request, relative_path: str) -> str:
    return str(request.url_for("files", path=relative_path))
