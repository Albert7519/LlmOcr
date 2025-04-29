# LlmOcr - 发票识别工具 🧾

这是一个使用本地Ollama部署的Qwen2.5-VL-7B-Instruct模型和Streamlit构建的发票信息提取工具。它可以识别发票图片中的关键信息（发票日期、金额、发票号码、车号、上下车时间）并支持批量处理和多种格式下载。

## ✨ 功能特性

*   **关键信息提取**: 自动识别发票图片中的日期、金额、号码、车号和上下车时间。
*   **批量处理**: 支持同时上传和处理多张发票图片。
*   **多种格式下载**: 支持将提取结果下载为 CSV, Excel (.xlsx) 或 JSON 文件。
*   **Web 界面**: 基于 Streamlit 的友好用户界面。
*   **Docker 支持**: 提供 Dockerfile 和 docker-compose.yml，方便容器化部署。
*   **本地模型**: 使用本地部署的Ollama服务，无需远程API密钥。
*   **高分辨率图像支持**: 启用Ollama模型的高分辨率图像处理能力，提高发票识别准确性。

## ⚙️ 先决条件

*   **Ollama服务**: 你需要在本地部署Ollama服务，并加载Qwen2.5-VL-7B-Instruct模型：
    ```bash
    # 安装Ollama（请参考官方文档：https://ollama.com/download）
    # 拉取并加载Qwen2.5-VL-7B-Instruct模型
    ollama pull ZimaBlueAI/Qwen2.5-VL-7B-Instruct
    # 启动Ollama服务
    ollama serve
    ```
*   **Git (可选)**: 用于克隆本仓库。

**对于 Docker 部署:**

*   [Docker Desktop](https://www.docker.com/products/docker-desktop/) (适用于 Windows/Mac) 或 Docker Engine + Docker Compose (适用于 Linux)。
*   确保Ollama服务已在宿主机上启动并运行在默认端口(11434)。

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
    docker pull albert151/llmocr-local:latest
    ```

2.  **运行容器**:
    ```bash
    docker run -d --name LlmOcr_local_run -p 8502:8502 --add-host=host.docker.internal:host-gateway --restart always albert151/llmocr-local:latest
    ```

**选项 B: 使用 `docker-compose` (构建并运行)**

1.  **克隆仓库 (可选)**:
    ```bash
    git clone <仓库地址> # 如果项目在 Git 仓库中
    cd LlmOcrLocal
    ```
    或者直接将项目文件 (`app.py`, `Dockerfile`, `docker-compose.yml`, `requirements.txt`) 下载到本地文件夹。

2.  **构建并启动容器**:
    在项目根目录下打开终端或 PowerShell，运行：
    ```bash
    docker-compose up -d --build
    ```
    *   `--build` 会根据 `Dockerfile` 构建镜像。
    *   `-d` 表示在后台运行。

**访问应用 (两种 Docker 方式通用)**:

*   在你的浏览器中打开 `http://localhost:8502`。

**Docker 故障排除**:

*   **无法访问 `localhost:8502`**:
    *   检查容器日志: `docker logs LlmOcr` (如果使用 compose) 或 `docker logs LlmOcr_local_run` (如果使用 run)。查看是否有错误信息。
    *   确保 Docker Desktop 或 Docker 服务正在运行。
*   **容器无法连接到Ollama服务**:
    *   确保Ollama服务已在宿主机上启动并运行。运行`ollama list`检查模型是否已加载。
    *   检查容器日志中是否有网络连接错误。如果有，确保Docker容器网络配置正确，能够访问宿主机。
*   **同网络其他设备无法访问**:
    *   检查你的防火墙 (如 Windows Defender 防火墙) 是否允许 TCP 端口 8502 的入站连接。
    *   使用你运行 Docker 的电脑的局域网 IP 地址访问，例如 `http://<你的电脑IP>:8502`。

### 方法二：直接配置本地环境

如果你不想使用 Docker，可以手动配置 Python 环境。

1.  **克隆仓库 (可选)**:
    ```bash
    git clone https://github.com/Albert7519/LlmOcrLocal
    cd LlmOcrLocal
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

4.  **确保Ollama服务已启动**:
    ```bash
    # 检查Ollama服务状态
    ollama list
    
    # 如果没有启动，请运行
    ollama serve
    
    # 如果没有安装模型，请运行
    ollama pull ZimaBlueAI/Qwen2.5-VL-7B-Instruct
    ```

5.  **运行应用**:
    确保你的虚拟环境已激活，并且Ollama服务已启动。
    ```bash
    streamlit run app.py
    ```

6.  **访问应用**:
    *   Streamlit 会在终端显示访问地址，通常是 `http://localhost:8502`。在浏览器中打开即可。

### 方法三：以守护进程方式运行（避免终端关闭后应用被杀死）

如果需要在后台长期运行应用而不受终端关闭影响，可以使用各操作系统的守护进程方案：

#### Windows 系统

**选项1：使用 nssm (推荐)**

1. 下载安装 [NSSM (Non-Sucking Service Manager)](https://nssm.cc/download)
2. 打开管理员权限的命令提示符，运行：
   ```cmd
   nssm install LlmOcrService
   ```
3. 在弹出的配置窗口中设置以下内容：
   - Path: 完整路径到 Python 解释器，如 `C:\Python312\python.exe` 或虚拟环境中的 Python
   - Startup directory: 项目目录，如 `E:\CodeProjects\LlmOcrLocal`
   - Arguments: `-m streamlit run app.py`
4. 切换到 "Details" 选项卡，设置服务名称和描述
5. 点击 "Install service"
6. 启动服务：
   ```cmd
   nssm start LlmOcrService
   ```

**选项2：使用 Windows 任务计划程序**

1. 创建一个批处理文件 `start_llmocr.bat`，内容如下：
   ```batch
   @echo off
   cd /d E:\CodeProjects\LlmOcrLocal
   call venv\Scripts\activate
   start /min streamlit run app.py
   ```
2. 打开任务计划程序 (搜索 "Task Scheduler")
3. 创建基本任务 -> 设置名称为 "LlmOcr"
4. 触发器选择 "当计算机启动时"
5. 操作选择 "启动程序"，浏览选择刚创建的批处理文件
6. 勾选 "以最高权限运行" 和 "无论用户是否登录都要运行"

#### Linux 系统

**选项1：使用 Systemd (现代 Linux 发行版)**

1. 创建服务文件：
   ```bash
   sudo nano /etc/systemd/system/llmocr.service
   ```

2. 添加以下内容：
   ```ini
   [Unit]
   Description=LlmOcr Streamlit Application
   After=network.target

   [Service]
   User=<你的用户名>
   WorkingDirectory=/path/to/LlmOcrLocal
   Environment="PATH=/path/to/LlmOcrLocal/venv/bin"
   ExecStart=/path/to/LlmOcrLocal/venv/bin/streamlit run app.py
   Restart=always
   RestartSec=5

   [Install]
   WantedBy=multi-user.target
   ```

3. 启用并启动服务：
   ```bash
   sudo systemctl daemon-reload
   sudo systemctl enable llmocr
   sudo systemctl start llmocr
   ```

4. 查看状态：
   ```bash
   sudo systemctl status llmocr
   ```

**选项2：使用 Screen 或 Tmux**

1. 安装 Screen：
   ```bash
   sudo apt-get install screen  # Debian/Ubuntu
   sudo yum install screen      # CentOS/RHEL
   ```

2. 创建新的 Screen 会话：
   ```bash
   screen -S llmocr
   ```

3. 在会话中激活环境并启动应用：
   ```bash
   cd /path/to/LlmOcrLocal
   source venv/bin/activate
   streamlit run app.py
   ```

4. 分离会话：按 `Ctrl+A` 然后按 `D`
5. 重新连接会话（如需要）：
   ```bash
   screen -r llmocr
   ```

#### macOS 系统

**选项1：使用 launchd (推荐)**

1. 创建 plist 文件：
   ```bash
   nano ~/Library/LaunchAgents/com.user.llmocr.plist
   ```

2. 添加以下内容：
   ```xml
   <?xml version="1.0" encoding="UTF-8"?>
   <!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
   <plist version="1.0">
   <dict>
       <key>Label</key>
       <string>com.user.llmocr</string>
       <key>ProgramArguments</key>
       <array>
           <string>/path/to/LlmOcrLocal/venv/bin/streamlit</string>
           <string>run</string>
           <string>/path/to/LlmOcrLocal/app.py</string>
       </array>
       <key>RunAtLoad</key>
       <true/>
       <key>KeepAlive</key>
       <true/>
       <key>WorkingDirectory</key>
       <string>/path/to/LlmOcrLocal</string>
       <key>StandardErrorPath</key>
       <string>/path/to/LlmOcrLocal/error.log</string>
       <key>StandardOutPath</key>
       <string>/path/to/LlmOcrLocal/output.log</string>
   </dict>
   </plist>
   ```

3. 加载并启动服务：
   ```bash
   launchctl load ~/Library/LaunchAgents/com.user.llmocr.plist
   launchctl start com.user.llmocr
   ```

**选项2：使用 Homebrew 安装 pm2**

1. 安装 pm2：
   ```bash
   brew install node
   npm install -g pm2
   ```

2. 启动并管理应用：
   ```bash
   cd /path/to/LlmOcrLocal
   pm2 start --name "llmocr" venv/bin/streamlit -- run app.py
   pm2 save
   pm2 startup
   ```

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
*   对于高分辨率或复杂的发票图片，已启用Ollama的高分辨率图像处理功能，以提高识别准确率。

## 🔧 常见问题排查

1. **Ollama服务连接问题**
   - 确保Ollama服务已启动：`ollama serve`
   - 检查模型是否已加载：`ollama list`
   - 检查网络端口：确保11434端口没有被防火墙阻止

2. **守护进程运行问题**
   - Windows：检查服务状态 `nssm status LlmOcrService` 或任务计划程序日志
   - Linux：检查systemd日志 `journalctl -u llmocr.service`
   - macOS：检查launchd日志 `cat ~/Library/LaunchAgents/output.log`

3. **图像识别结果不准确**
   - 确保图片清晰度高，无模糊或反光
   - 检查图片大小是否适中（建议小于8MB）
   - 上传原始图片而非截图或二次处理的图片
