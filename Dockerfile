# 使用 Debian Trixie Slim 作为基础镜像
FROM debian:trixie-slim

# 创建工作目录
WORKDIR /app

# 添加 RUN 指令
RUN apt-get update \
 && apt-get install -y --no-install-recommends \
    # 添加 libxml2 到标准安装列表
    libxml2 \
    python3 \
    python3-pip \
    python3-venv \
    build-essential \
    libjpeg-dev \
    zlib1g-dev \
    libgl1 \
    libsm6 \
    libxrender1 \
    libxext6 \
 && rm -rf /var/lib/apt/lists/*

# 创建 Python 虚拟环境
RUN python3 -m venv /opt/venv
# 将 venv 的 bin 目录添加到 PATH，这样后续命令可以直接调用 venv 中的可执行文件
ENV PATH="/opt/venv/bin:$PATH"

# 复制依赖文件并安装 Python 包到虚拟环境中
COPY requirements.txt .
# 使用虚拟环境中的 pip 安装
RUN python -m pip install --no-cache-dir -r requirements.txt

# 复制源代码
COPY . .

# 设置环境变量（API密钥通过运行时注入）
ENV QWEN_API_KEY=""

# 暴露端口
EXPOSE 8502

# 启动命令 (现在会使用 venv 中的 streamlit)
CMD ["streamlit", "run", "--server.port=8502", "app.py"]