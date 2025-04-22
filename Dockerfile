# 使用 Debian Trixie Slim 作为基础镜像
FROM debian:trixie-slim

# 创建工作目录
WORKDIR /app

# 安装 Python、pip 和系统依赖
# 更新包列表，升级现有包，安装 Python3, pip, 构建工具和必要的库
RUN apt-get update && apt-get upgrade -y && apt-get install -y --no-install-recommends \
    python3 \
    python3-pip \
    python3-venv \
    build-essential \
    libjpeg-dev \
    zlib1g-dev \
    libgl1 \
    libsm6 \
    libxrender1 \
    libxext6 && \
    rm -rf /var/lib/apt/lists/*

# 复制依赖文件并安装 Python 包
COPY requirements.txt .
# 使用 python3 -m pip 确保使用我们安装的 pip 版本
RUN python3 -m pip install --no-cache-dir -r requirements.txt

# 复制源代码
COPY . .

# 设置环境变量（API密钥通过运行时注入）
ENV QWEN_API_KEY=""

# 暴露端口
EXPOSE 8502

# 启动命令
CMD ["streamlit", "run", "--server.port=8502", "app.py"]