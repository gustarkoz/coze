## 功能目标
- 在现有服务基础上新增 4 种转换：Excel（智能识别表格，多 Sheet）、PDF（高质量）、HTML（精美网页）、PNG（高清图片）。
- 统一输入：`markdown` 与 `filename`；按目标格式输出文件名与下载链接。

## 架构与目录
- `app/main.py`：注册路由与静态挂载（`/files`）。
- `app/pipelines/`：各格式转换管线模块：
  - `word.py`（复用现有 html→docx）
  - `excel.py`（HTML 表格→xlsx，多 Sheet）
  - `pdf.py`（HTML→PDF via Playwright）
  - `html.py`（渲染模板→.html）
  - `png.py`（HTML→截图 PNG via Playwright）
- `app/render.py`：Markdown→HTML 渲染（带样式）、公共 CSS、模板。
- 输出目录：`storage/{docx,xlsx,pdf,html,png}/`。

## 转换管线设计
- 通用步骤：
  1) 校验输入大小与安全文件名；
  2) Markdown→HTML（`markdown` 或 `markdown-it-py`，启用 `tables`、`fenced_code`、`toc` 等扩展）；
  3) 按目标格式执行：
- Word（.docx）：`html2docx(html, title)` → 写入 `.docx`。
- Excel（.xlsx）：
  - 使用 `BeautifulSoup` 解析 HTML 中的 `<table>`；
  - Sheet 识别策略：
    - 以最近的上级标题（`<h1>|<h2>|<h3>`）命名 Sheet；若无标题，则 `Table 1/2/...`。
    - 一个标题下若有多张表格：每张表单独 Sheet（避免混排复杂性）。
  - 单元格内容保持原样文本；支持表头行识别（`<th>`）。
  - 写入 `openpyxl`，保证 Excel 兼容性。
- PDF（.pdf）：
  - 用统一样式的 HTML；
  - 通过 Playwright Chromium 渲染：`page.set_content(html); page.pdf()`，设置 A4、页边距、打印背景；
  - 可选页眉页脚（后续迭代）。
- HTML（.html）：
  - 用 Jinja2 模板包裹内容，注入 CSS 与标题；
  - 生成静态 HTML 文件用于直接预览/下载。
- PNG（.png）：
  - 通过 Playwright Chromium 渲染：`page.screenshot(full_page=True)` 生成高清长图；
  - 支持自定义宽度/主题（后续迭代）。

## API 设计
- 路由：
  - `POST /convert/word` 输入：`{ markdown, filename }` → 返回：`{ filename, url }`
  - `POST /convert/excel` 输入：`{ markdown, filename }` → 返回：`{ filename, url, sheets: ["SheetA", "SheetB", ...] }`
  - `POST /convert/pdf` 输入：`{ markdown, filename }` → 返回：`{ filename, url }`
  - `POST /convert/html` 输入：`{ markdown, filename }` → 返回：`{ filename, url }`
  - `POST /convert/png` 输入：`{ markdown, filename }` → 返回：`{ filename, url }`
- 可选统一路由：`POST /convert`，加 `targets: ["docx","xlsx","pdf","html","png"]` 支持一次生成多格式（后续迭代）。

## 依赖与安装
- 通用：`fastapi`, `uvicorn`, `markdown` 或 `markdown-it-py`, `jinja2`, `beautifulsoup4`。
- Word：`html2docx`, `python-docx`。
- Excel：`openpyxl`。
- PDF/PNG：`playwright`（首次需安装浏览器：`playwright install chromium`）。
- 代码高亮（可选）：`pygments`。
- 注意：如选择 WeasyPrint 生成 PDF/PNG，则需安装 Cairo/Pango 等系统库（Windows 较繁琐）；优先使用 Playwright 方案。

## 存储与命名
- 目录：`storage/docx|xlsx|pdf|html|png/`。
- 文件名：清理非法字符、统一扩展名；避免冲突加日期戳或 UUID；中文名保留。
- 下载链接：`/files/<type>/<filename>`。

## 安全与性能
- 输入大小限制（默认 1MB，可调）；
- 路径穿越防护，仅允许文件名；
- Playwright 渲染时限制并发与超时；
- 适度缓存样式模板；
- 后续增加速率限制与鉴权（按需）。

## 测试用例
- Excel 多表识别：含 2 个 H1 与 3 张表，断言生成的 Sheet 名称与单元格数据；
- PDF/PNG：生成文件存在且大小>0；
- HTML：包含标题、代码高亮与表格样式；
- 错误路径：空 markdown、超限、非法文件名返回相应错误码。

## 实施步骤
1. 新增 `app/render.py`（Markdown→HTML + 样式模板）。
2. 实现 `pipelines/word.py`（复用现有逻辑）。
3. 实现 `pipelines/excel.py`（HTML→tables→openpyxl，多 Sheet 规则）。
4. 实现 `pipelines/pdf.py` 与 `pipelines/png.py`（Playwright 渲染）。
5. 新增路由与输出目录挂载；复用现有文件名工具。
6. 编写端到端测试与示例。

## 运行与验证
- 安装：`pip install fastapi uvicorn markdown jinja2 beautifulsoup4 html2docx python-docx openpyxl playwright`
- 浏览器安装（首次）：`playwright install chromium`
- 启动：`uvicorn app.main:app --reload`
- 通过 `/docs` 分别测试 5 个接口；查看 `storage/*` 与返回下载链接是否可访问。

如确认该方案，我将开始按上述步骤实现代码与测试，并确保在本地验证通过后交付。