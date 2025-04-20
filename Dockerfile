# 使用官方Streamlit基础镜像
FROM python:3.12.7-slim

# 创建工作目录
WORKDIR /app

# 安装系统依赖（解决PIL等库的编译问题）
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1 libsm6 libxrender1 libxext6 && \
    rm -rf /var/lib/apt/lists/*

# 复制依赖文件并安装
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制源代码
COPY . .

# 设置环境变量（API密钥通过运行时注入）
ENV QWEN_API_KEY=""

# 暴露端口
EXPOSE 8502

# 启动命令
CMD ["streamlit", "run", "--server.port=8502", "app.py"]