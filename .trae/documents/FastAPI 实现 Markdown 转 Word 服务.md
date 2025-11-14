## 功能概述
- 提供一个 POST 接口，输入 `markdown` 文本与目标 `filename`（不含或含 `.docx`）。
- 将 Markdown 转为 Word（`.docx`）并保存到服务器可公开访问的目录。
- 返回 JSON：包含最终生成的 `filename` 与可下载的绝对链接 `url`。

## 技术选型
- Web 框架：FastAPI + Uvicorn。
- Markdown→HTML：`markdown`（或 `markdown-it-py`，二选一）。
- HTML→DOCX：`html2docx` + `python-docx`。
- 静态文件服务：FastAPI `StaticFiles` 挂载公开目录。

## API 设计
- POST `/convert`
  - 请求体（JSON）：`{ "markdown": "# 标题...", "filename": "报告.docx" }`
  - 校验：`markdown` 非空、长度限制（例如 ≤ 1MB）；`filename` 规范化。
  - 响应（JSON）：`{ "filename": "报告_20251114.docx", "url": "http://host/files/converted/报告_20251114.docx" }`
- 静态下载：挂载 `GET /files/*` 指向 `storage/converted`，浏览器可直接下载。

## 存储与文件名策略
- 输出目录：`storage/converted/`（启动时确保存在）。
- 文件名规范化：
  - 移除非法字符（如 `\\/:*?"<>|`）。
  - 统一追加扩展名 `.docx`。
  - 为避免冲突，追加日期戳或 `uuid`（如：`原名_YYYYMMDD.docx`）。
- 可选清理策略：定期清理过期文件（后续迭代）。

## 校验与安全
- 限制文本大小（如 1MB）与请求体大小；返回 413 超限。
- 防止路径穿越（仅允许文件名，不允许路径）。
- 设置响应 `Content-Type` 为 `application/json`；下载由静态文件服务处理。

## 错误处理
- 400：参数缺失或格式错误（Pydantic 校验）。
- 413：文本过大。
- 500：转换失败（捕获异常并返回统一错误对象）。

## 依赖
- `fastapi`, `uvicorn`
- `markdown` 或 `markdown-it-py`
- `html2docx`, `python-docx`
- `pydantic`

## 项目结构
- `app/main.py`：FastAPI 应用入口、路由与静态挂载。
- `app/converter.py`：`markdown_to_docx(markdown_text, output_path)` 转换逻辑。
- `app/utils.py`：`normalize_filename`、`build_download_url` 等辅助函数。
- `storage/converted/`：输出目录。
- `tests/test_convert.py`：核心用例测试（使用 `TestClient`）。

## 实现步骤
1. 创建 FastAPI 应用并在启动时确保 `storage/converted` 存在；挂载 `StaticFiles` 到 `/files`。
2. 编写 `normalize_filename`（清理非法字符、追加扩展名、加日期或 `uuid`）。
3. 编写 `markdown_to_docx`：
   - 使用 `markdown` 将输入转为 HTML。
   - 使用 `html2docx` 将 HTML 渲染到 `python-docx` 文档并保存到目标路径。
4. 实现 POST `/convert`：
   - 读取并校验请求体；限制大小。
   - 生成最终文件名与输出路径；调用转换函数。
   - 通过 `Request` 构建绝对下载 URL（`request.url_for` 与路径拼接）。
   - 返回 JSON（`filename`, `url`）。
5. 编写测试：
   - 成功转换并断言文件存在与响应字段。
   - 危险文件名被规范化。
   - 缺失字段或超限返回相应错误码。

## 示例（伪代码/关键逻辑）
```python
# app/converter.py
from markdown import markdown
from html2docx import html2docx

def markdown_to_docx(md_text: str, output_path: str):
    html = markdown(md_text, output_format="html5")
    html2docx(html, output_path)

# app/utils.py
import re, uuid, datetime

def normalize_filename(name: str) -> str:
    base = re.sub(r'[\\/:*?"<>|]', '', name).strip()
    if not base.lower().endswith('.docx'):
        base += '.docx'
    stamp = datetime.datetime.now().strftime('%Y%m%d')
    return f"{base[:-5]}_{stamp}.docx"
```

## 运行方式
- 安装依赖：`pip install fastapi uvicorn markdown html2docx python-docx pydantic`
- 启动：`uvicorn app.main:app --reload`
- 调用示例：
```bash
curl -X POST http://localhost:8000/convert \
  -H "Content-Type: application/json" \
  -d '{"markdown":"# 标题\n正文...","filename":"报告.docx"}'
```
返回 JSON 含文件名与可下载链接。

## 注意与扩展
- Markdown 支持度由 `html2docx` 的 HTML 支持决定；复杂表格、代码高亮等可逐步增强（引入 `mdx`、代码高亮 CSS 与更强 HTML→DOCX 处理）。
- 远程图片：如需支持，可在转换前抓取 `img` 的 `src` 并下载到临时文件再插入；初版可不支持或仅支持本地图片。
- 可加鉴权、速率限制与持久化存储（如 S3/OSS）以适配生产环境。