# LlmOcr

[English](README.md) | [中文](README.zh-CN.md)

LlmOcr is a lightweight invoice OCR tool built with Streamlit and the Qwen vision-language model API. It extracts structured fields from invoice images, supports batch processing, and lets users download results as CSV, Excel, or JSON files.

The project is designed for small, practical document-processing workflows where users want a simple web UI, Docker deployment, and reproducible extraction logic.

## Features

- Extracts invoice date, amount, invoice number, vehicle number, pickup time, and drop-off time from invoice images.
- Supports batch uploads for JPG, JPEG, and PNG files.
- Exports results as CSV, Excel (`.xlsx`), or JSON.
- Provides a Streamlit web interface.
- Supports Docker and Docker Compose deployment.
- Reads the Qwen API key from environment variables instead of hardcoding secrets.

## Requirements

### Qwen API

You need a valid Qwen API key from Alibaba Cloud DashScope:

https://dashscope.console.aliyun.com/apiKey

Set it as the `QWEN_API_KEY` environment variable before running the app.

### Docker deployment

- Docker Desktop for Windows/macOS, or Docker Engine with Docker Compose on Linux.

### Local Python deployment

- Python 3.12 or newer is recommended.
- `pip` for installing Python dependencies.

## Quick Start

### Option 1: Docker Compose

1. Clone the repository:

   ```bash
   git clone https://github.com/Albert7519/LlmOcr.git
   cd LlmOcr
   ```

2. Create a local `.env` file:

   ```bash
   cp .env.example .env
   ```

3. Edit `.env` and set your real Qwen API key:

   ```env
   QWEN_API_KEY=your_qwen_api_key_here
   ```

4. Build and start the app:

   ```bash
   docker-compose up -d --build
   ```

5. Open the web app:

   ```text
   http://localhost:8502
   ```

### Option 2: Docker Run

Pull the prebuilt image:

```bash
docker pull albert151/llmocr:latest
```

Set your API key:

```bash
export QWEN_API_KEY="your_qwen_api_key_here"
```

Run the container:

```bash
docker run -d --name LlmOcr_run -p 8502:8502 -e QWEN_API_KEY="$QWEN_API_KEY" --restart always albert151/llmocr:latest
```

For Windows PowerShell:

```powershell
$env:QWEN_API_KEY = "your_qwen_api_key_here"
docker run -d --name LlmOcr_run -p 8502:8502 -e QWEN_API_KEY=$env:QWEN_API_KEY --restart always albert151/llmocr:latest
```

### Option 3: Local Python

1. Clone the repository:

   ```bash
   git clone https://github.com/Albert7519/LlmOcr.git
   cd LlmOcr
   ```

2. Create and activate a virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

   On Windows:

   ```cmd
   venv\Scripts\activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Set your Qwen API key:

   ```bash
   export QWEN_API_KEY="your_qwen_api_key_here"
   ```

5. Run the app:

   ```bash
   streamlit run app.py
   ```

6. Open the local URL shown by Streamlit, usually:

   ```text
   http://localhost:8502
   ```

## Usage

1. Open the running app in a browser.
2. Choose the output format: CSV, Excel, or JSON.
3. Upload one or more invoice images in JPG, JPEG, or PNG format.
4. Preview the uploaded images.
5. Click the extraction button.
6. Review the extracted table and processing statistics.
7. Download the results in the selected format.

## Docker Troubleshooting

- If `http://localhost:8502` is not reachable, check container logs:

  ```bash
  docker logs LlmOcr
  ```

  or, for the `docker run` container:

  ```bash
  docker logs LlmOcr_run
  ```

- Make sure Docker Desktop or Docker Engine is running.
- If another device on the same network cannot access the app, check firewall rules for TCP port `8502`.
- To access from another device, use the host machine's local network IP, for example `http://192.168.x.x:8502`.

## Security and Privacy Notes

- Do not commit API keys or real `.env` files.
- Do not hardcode `QWEN_API_KEY` in source code.
- Be careful when uploading invoices or documents that contain sensitive personal or business information.
- The app sends uploaded images to the configured Qwen API endpoint for inference. Do not use it for documents that cannot be processed by an external API.

## Maintainer Notes

This is currently a single-maintainer open-source project. Issues and pull requests are welcome when they include enough context to reproduce the behavior.

Useful contribution areas include:

- deployment and Docker fixes;
- extraction prompt improvements;
- tests for CSV parsing and export behavior;
- UI improvements for upload, error handling, and result download;
- documentation updates for setup and troubleshooting.

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.
