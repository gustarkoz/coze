## 部署目标
- 将现有 FastAPI 转换服务容器化并部署到服务器 `8.136.193.87`。
- 暴露 `8000` 端口（或 `80` 经反向代理），持久化 `storage` 输出目录。
- 保证 Word/Excel/PDF/HTML/PNG 五种转换均可用，Playwright 浏览器在容器内可用。

## 技术方案
- 使用 Playwright 官方 Python 基础镜像（已内置 Chromium）：`mcr.microsoft.com/playwright/python`。
- 通过 `Dockerfile` 打包应用及依赖，并在构建时执行 `python -m playwright install chromium`（确保浏览器可用）。
- 使用 `docker-compose.yml` 管理服务、端口与卷，将主机目录 `./storage` 挂载到容器 `/app/storage`。

## 新增文件
- `requirements.txt`
  - 依赖：`fastapi uvicorn markdown html2docx python-docx jinja2 beautifulsoup4 openpyxl playwright`
- `Dockerfile`
  - 关键步骤：
    1) `FROM mcr.microsoft.com/playwright/python:v1.45.0-jammy`
    2) `WORKDIR /app`
    3) `COPY requirements.txt ./` 并 `pip install -r requirements.txt`
    4) 安装浏览器：`python -m playwright install chromium`
    5) `COPY . .`
    6) `EXPOSE 8000`
    7) CMD：`uvicorn app.main:app --host 0.0.0.0 --port 8000`
- `docker-compose.yml`
  - 服务 `md-converter`：
    - `build: .`
    - `ports: ["8000:8000"]`
    - `volumes: ["./storage:/app/storage"]`
    - `restart: unless-stopped`

## 服务器侧操作（示例命令）
1. 登录服务器并安装 Docker/Compose：
   - Ubuntu：`sudo apt update && sudo apt install -y docker.io docker-compose`
   - 启动：`sudo systemctl enable --now docker`
2. 上传代码到服务器（任选其一）：
   - 使用 `scp`：`scp -r <本地项目目录> user@8.136.193.87:~/md-service`
   - 或在服务器上 `git clone` 仓库到 `~/md-service`
3. 构建与启动：
   - `cd ~/md-service`
   - `sudo docker-compose build`
   - `sudo docker-compose up -d`
4. 放通端口（如需）：
   - `sudo ufw allow 8000/tcp`（或在云平台安全组开放 8000）
5. 验证：
   - 打开 `http://8.136.193.87:8000/docs` 测试各接口
   - 下载链接形如：`http://8.136.193.87:8000/files/<type>/<filename>`

## 可选增强
- 反向代理到 80/443：新增 Nginx + TLS（Let’s Encrypt）。
- 健康检查与监控：在 Compose 中增加 `healthcheck`，采集容器日志。
- 资源限制：给 Playwright 浏览器设置并发与内存限制（后续迭代）。

## 实施步骤
1. 在项目中新增 `requirements.txt`、`Dockerfile`、`docker-compose.yml`。
2. 本地构建镜像并快速验证容器运行（可选）。
3. 将项目上传到服务器并运行上述命令完成部署。
4. 在 `/docs` 完成接口测试，并实际生成各格式文件验证下载可用。

我将按照以上内容创建所需文件，并输出部署所需的命令清单。请确认后我立即开始修改与交付。