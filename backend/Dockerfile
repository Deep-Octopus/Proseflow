# 使用官方 Python 镜像
FROM python:3.10-slim

# 设置工作目录
WORKDIR /app

# 安装编译依赖，用于某些 Python 包
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# 复制依赖文件并安装
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制所有应用代码
COPY . .

# 暴露端口
EXPOSE 8000

# 默认启动命令 (在 docker-compose 中会被覆盖)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
