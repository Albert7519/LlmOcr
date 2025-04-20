# LlmOcr - 发票识别工具 🧾

这是一个使用通义千问视觉语言模型 (Qwen VL) 和 Streamlit 构建的发票信息提取工具。它可以识别发票图片中的关键信息（发票日期、金额、发票号码、车号）并支持批量处理和多种格式下载。

## ✨ 功能特性

*   **关键信息提取**: 自动识别发票图片中的日期、金额、号码和车号。
*   **批量处理**: 支持同时上传和处理多张发票图片。
*   **多种格式下载**: 支持将提取结果下载为 CSV, Excel (.xlsx) 或 JSON 文件。
*   **Web 界面**: 基于 Streamlit 的友好用户界面。
*   **Docker 支持**: 提供 Dockerfile 和 docker-compose.yml，方便容器化部署。

## ⚙️ 先决条件

*   **通义千问 API 密钥**: 你需要一个有效的阿里云通义千问 API 密钥。请访问[阿里云官网](https://dashscope.console.aliyun.com/apiKey)获取。
*   **Git (可选)**: 用于克隆本仓库。

**对于 Docker 部署:**

*   [Docker Desktop](https://www.docker.com/products/docker-desktop/) (适用于 Windows/Mac) 或 Docker Engine + Docker Compose (适用于 Linux)。

**对于直接环境部署:**

*   Python (推荐 3.12 或更高版本，与 `Dockerfile` 中使用的版本匹配)。
*   pip (Python 包管理器)。

## 🚀 安装与运行

你可以选择以下任一方法来运行此应用：

### 方法一：使用 Docker (推荐)

这是最简单且推荐的运行方式，可以避免环境配置问题。

**选项 A: 使用 `docker run` (拉取预构建镜像)**

如果你不想在本地构建，可以拉取作者预先构建好的镜像。

1.  **拉取镜像**:
    ```bash
    docker pull albert151/llmocr:latest
    ```

2.  **配置 API 密钥**:
    你需要将 API 密钥作为环境变量传递给容器。打开终端或 PowerShell：
    *   **PowerShell (Windows)**:
        ```powershell
        $env:QWEN_API_KEY = "你的实际Qwen API密钥"
        # 然后在同一个窗口运行下面的 docker run 命令
        ```
    *   **CMD (Windows)**:
        ```cmd
        set QWEN_API_KEY=你的实际Qwen API密钥
        # 然后在同一个窗口运行下面的 docker run 命令
        ```
    *   **Linux / macOS**:
        ```bash
        export QWEN_API_KEY="你的实际Qwen API密钥"
        # 然后在同一个 shell 运行下面的 docker run 命令
        ```

**选项 B: 使用 `docker-compose` (构建并运行)**

1.  **克隆仓库 (可选)**:
    ```bash
    git clone <仓库地址> # 如果项目在 Git 仓库中
    cd LlmOcr
    ```
    或者直接将项目文件 (`app.py`, `Dockerfile`, `docker-compose.yml`, `requirements.txt`) 下载到本地文件夹。

2.  **配置 API 密钥**:
    在项目根目录 (与 `docker-compose.yml` 同级) 创建一个名为 `.env` 的文件，并添加以下内容，将 `你的实际Qwen API密钥` 替换为你的真实密钥：
    ```env
    QWEN_API_KEY=你的实际Qwen API密钥
    ```
    **注意**: 请确保 `.env` 文件不会被提交到版本控制系统 (如 Git)。

3.  **构建并启动容器**:
    在项目根目录下打开终端或 PowerShell，运行：
    ```bash
    docker-compose up -d --build
    ```
    *   `--build` 会根据 `Dockerfile` 构建镜像。
    *   `-d` 表示在后台运行。



3.  **运行容器**:
    *   **PowerShell**:
        ```powershell
        docker run -d --name LlmOcr_run -p 8502:8502 -e QWEN_API_KEY=$env:QWEN_API_KEY --restart always albert151/llmocr:latest
        ```
    *   **CMD**: (注意环境变量引用方式不同)
        ```cmd
        docker run -d --name LlmOcr_run -p 8502:8502 -e QWEN_API_KEY=%QWEN_API_KEY% --restart always albert151/llmocr:latest
        ```
    *   **Linux / macOS**:
        ```bash
        docker run -d --name LlmOcr_run -p 8502:8502 -e QWEN_API_KEY="$QWEN_API_KEY" --restart always albert151/llmocr:latest
        ```

**访问应用 (两种 Docker 方式通用)**:

*   在你的浏览器中打开 `http://localhost:8502`。

**Docker 故障排除**:

*   **无法访问 `localhost:8502`**:
    *   检查容器日志: `docker logs LlmOcr` (如果使用 compose) 或 `docker logs LlmOcr_run` (如果使用 run)。查看是否有错误信息，特别是关于 API Key 的。
    *   确保 Docker Desktop 或 Docker 服务正在运行。
*   **同网络其他设备无法访问**:
    *   检查你的防火墙 (如 Windows Defender 防火墙) 是否允许 TCP 端口 8502 的入站连接。
    *   使用你运行 Docker 的电脑的局域网 IP 地址访问，例如 `http://<你的电脑IP>:8502`。

### 方法二：直接配置本地环境

如果你不想使用 Docker，可以手动配置 Python 环境。

1.  **克隆仓库 (可选)**:
    ```bash
    git clone https://github.com/Albert7519/LlmOcr
    cd LlmOcr
    ```
    或者直接将项目文件下载到本地文件夹。

2.  **创建并激活虚拟环境 (推荐)**:
    ```bash
    # 创建虚拟环境 (使用与 Dockerfile 一致的 Python 版本)
    python -m venv venv
    # 激活虚拟环境
    # Windows (CMD/PowerShell)
    venv\Scripts\activate
    # Linux / macOS
    source venv/bin/activate
    ```

3.  **安装依赖**:
    ```bash
    pip install -r requirements.txt
    ```
    *注意：如果遇到 `Pillow` 或其他库的安装问题，可能需要安装相应的系统级编译依赖。Docker 环境已包含这些依赖。*

4.  **配置 API 密钥**:
    将 API 密钥设置为环境变量。
    *   **PowerShell (Windows)**:
        ```powershell
        $env:QWEN_API_KEY = "你的实际Qwen API密钥"
        ```
    *   **CMD (Windows)**:
        ```cmd
        set QWEN_API_KEY=你的实际Qwen API密钥
        ```
    *   **Linux / macOS**:
        ```bash
        export QWEN_API_KEY="你的实际Qwen API密钥"
        ```

5.  **运行应用**:
    确保你的虚拟环境已激活，并且 API 密钥已设置。
    ```bash
    streamlit run app.py
    ```

6.  **访问应用**:
    *   Streamlit 会在终端显示访问地址，通常是 `http://localhost:8502`。在浏览器中打开即可。

## 🛠️ 使用方法

1.  通过浏览器访问运行中的应用 (通常是 `http://localhost:8502`)。
2.  选择你希望下载结果的格式 (CSV, Excel, JSON)。
3.  点击 "上传发票图片" 按钮，选择一张或多张 JPG 或 PNG 格式的发票图片。
4.  上传完成后，图片预览会显示出来。
5.  点击 "✨ 提取信息" 按钮开始处理。
6.  处理完成后，会显示处理统计和提取结果表格。
7.  如果处理成功，会出现 "📥 下载结果" 按钮，点击即可下载相应格式的文件。
8.  如果处理失败，会显示错误信息。

## 📄 注意事项

*   请确保你的 `QWEN_API_KEY` 安全，不要硬编码在代码中或提交到公共仓库。推荐使用 `.env` 文件 (配合 `docker-compose`) 或环境变量。
*   处理速度和准确性依赖于通义千问模型的性能和网络状况。
*   请勿上传包含敏感信息的发票。
