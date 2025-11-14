import os
import sys
from fastapi.testclient import TestClient

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from app.main import app

client = TestClient(app)

def main():
    payload = {
        "markdown": "# 标题\n这是正文\n- 列表1\n- 列表2",
        "filename": "报告.docx",
    }
    r = client.post("/convert", json=payload)
    data = r.json()
    print(data)
    fn = data.get("filename")
    path = os.path.join("storage", "converted", fn)
    print(path, os.path.exists(path))

if __name__ == "__main__":
    main()
