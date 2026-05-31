# LlmOcr - 发票识别工具

[English](README.md) | [中文](README.zh-CN.md)

这是一个使用通义千问视觉语言模型 (Qwen VL) 和 Streamlit 构建的轻量发票信息提取工具。它可以识别发票图片中的关键信息，并支持批量处理以及 CSV、Excel、JSON 多种格式下载。

本项目适合小型、实用的文档处理场景：用户可以通过简单 Web 界面上传图片，使用 Docker 部署，并复现完整的信息提取流程。

## 功能特性

- 自动识别发票日期、金额、发票号码、车号、上车时间和下车时间。
- 支持 JPG、JPEG、PNG 图片批量上传。
- 支持将结果导出为 CSV、Excel (`.xlsx`) 或 JSON。
- 提供基于 Streamlit 的 Web 界面。
- 支持 Docker 和 Docker Compose 部署。
- 从环境变量读取 Qwen API Key，避免在代码中硬编码密钥。

## 环境要求

### Qwen API

你需要一个有效的阿里云通义千问 API 密钥：

https://dashscope.console.aliyun.com/apiKey

运行应用前，请将其设置为 `QWEN_API_KEY` 环境变量。

### Docker 部署

- Windows/macOS 可使用 Docker Desktop。
- Linux 可使用 Docker Engine 和 Docker Compose。

### 本地 Python 部署

- 推荐 Python 3.12 或更高版本。
- 需要使用 `pip` 安装 Python 依赖。

## 快速开始

### 方式一：Docker Compose

1. 克隆仓库：

   ```bash
   git clone https://github.com/Albert7519/LlmOcr.git
   cd LlmOcr
   ```

2. 创建本地 `.env` 文件：

   ```bash
   cp .env.example .env
   ```

3. 编辑 `.env`，填入真实的 Qwen API Key：

   ```env
   QWEN_API_KEY=your_qwen_api_key_here
   ```

4. 构建并启动应用：

   ```bash
   docker-compose up -d --build
   ```

5. 打开 Web 应用：

   ```text
   http://localhost:8502
   ```

### 方式二：Docker Run

拉取预构建镜像：

```bash
docker pull albert151/llmocr:latest
```

设置 API Key：

```bash
export QWEN_API_KEY="your_qwen_api_key_here"
```

运行容器：

```bash
docker run -d --name LlmOcr_run -p 8502:8502 -e QWEN_API_KEY="$QWEN_API_KEY" --restart always albert151/llmocr:latest
```

Windows PowerShell：

```powershell
$env:QWEN_API_KEY = "your_qwen_api_key_here"
docker run -d --name LlmOcr_run -p 8502:8502 -e QWEN_API_KEY=$env:QWEN_API_KEY --restart always albert151/llmocr:latest
```

### 方式三：本地 Python

1. 克隆仓库：

   ```bash
   git clone https://github.com/Albert7519/LlmOcr.git
   cd LlmOcr
   ```

2. 创建并激活虚拟环境：

   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

   Windows：

   ```cmd
   venv\Scripts\activate
   ```

3. 安装依赖：

   ```bash
   pip install -r requirements.txt
   ```

4. 设置 Qwen API Key：

   ```bash
   export QWEN_API_KEY="your_qwen_api_key_here"
   ```

5. 运行应用：

   ```bash
   streamlit run app.py
   ```

6. 打开 Streamlit 显示的本地地址，通常是：

   ```text
   http://localhost:8502
   ```

## 使用方法

1. 通过浏览器访问运行中的应用。
2. 选择希望下载的格式：CSV、Excel 或 JSON。
3. 上传一张或多张 JPG、JPEG、PNG 格式的发票图片。
4. 预览上传的图片。
5. 点击提取按钮开始处理。
6. 查看提取结果表格和处理统计。
7. 下载所选格式的结果文件。

## Docker 故障排除

- 如果无法访问 `http://localhost:8502`，请检查容器日志：

  ```bash
  docker logs LlmOcr
  ```

  或者，如果使用 `docker run` 启动：

  ```bash
  docker logs LlmOcr_run
  ```

- 确保 Docker Desktop 或 Docker Engine 正在运行。
- 如果同一局域网内其他设备无法访问应用，请检查防火墙是否允许 TCP 端口 `8502`。
- 局域网访问时，请使用运行 Docker 的主机 IP，例如 `http://192.168.x.x:8502`。

## 安全与隐私说明

- 不要提交 API Key 或真实 `.env` 文件。
- 不要在源代码中硬编码 `QWEN_API_KEY`。
- 上传包含个人或业务敏感信息的发票、票据或文档前请谨慎评估。
- 本应用会将上传图片发送到配置的 Qwen API 端点进行推理，不适合处理不能发送给外部 API 的文档。

## 维护说明

本项目目前由单人维护。欢迎提交 issue 或 pull request，但请尽量提供足够的复现信息。

适合贡献的方向包括：

- Docker 部署和运行问题修复；
- 信息提取提示词改进；
- CSV 解析和导出行为测试；
- 上传、错误提示和结果下载相关的界面改进；
- 安装、运行和故障排除文档完善。

## 开源协议

本项目使用 MIT License。详情见 [LICENSE](LICENSE)。
