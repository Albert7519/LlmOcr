import streamlit as st
import base64
import io
import csv
import json  # Import json
import pandas as pd  # Import pandas
from PIL import Image
import concurrent.futures  # Import for parallel processing
import os  # Import os module
import requests  # 导入requests库用于API调用
import socket  # 导入socket库用于检测网络连接

# --- Configuration ---
# 使用Ollama本地部署的Qwen2.5-VL-7B-Instruct模型
OLLAMA_MODEL = "ZimaBlueAI/Qwen2.5-VL-7B-Instruct"  # Ollama模型名称
MAX_WORKERS = 10  # 减少并行调用数量，避免本地模型过载

# 定义可能的Ollama API URLs
DOCKER_API_URL = (
    "http://host.docker.internal:11434/api/generate"  # Docker容器内访问宿主机
)
LOCAL_API_URL = "http://localhost:11434/api/generate"  # 直接在本地运行时使用


# 自动检测使用哪个API URL
def get_ollama_api_url():
    """
    自动检测使用哪个Ollama API URL:
    1. 首先尝试使用localhost
    2. 如果localhost连接失败，尝试使用host.docker.internal (Docker环境)
    3. 如果两者都失败，返回localhost作为默认值
    """
    # 首先尝试localhost
    try:
        response = requests.get("http://localhost:11434/api/version", timeout=1)
        if response.status_code == 200:
            return LOCAL_API_URL
    except requests.exceptions.RequestException:
        pass

    # 尝试Docker网络别名
    try:
        response = requests.get(
            "http://host.docker.internal:11434/api/version", timeout=1
        )
        if response.status_code == 200:
            return DOCKER_API_URL
    except requests.exceptions.RequestException:
        pass

    # 默认返回localhost URL
    return LOCAL_API_URL


# 动态确定要使用的API URL
OLLAMA_API_URL = get_ollama_api_url()


# --- Helper Functions ---
def encode_image_bytes(image_bytes):
    """Encodes image bytes to base64."""
    return base64.b64encode(image_bytes).decode("utf-8")


def get_qwen_completion(image_bytes, filename=""):
    """使用Ollama本地API调用Qwen2.5-VL-7B-Instruct模型处理图像"""
    global OLLAMA_API_URL  # 将全局变量声明移到函数开始处
    
    try:
        base64_image = encode_image_bytes(image_bytes)

        # 构建提示词
        chinese_prompt = """你是一个专业的图像数据处理助手，负责从提供的发票图片中提取信息，并将其转换为标准化的CSV表格格式。

请分析以下图片，并执行以下任务：

1.  **识别关键信息**：从图片中找出以下发票信息：
    *   发票日期
    *   金额
    *   发票号码
    *   车号
    *   上车时间
    *   下车时间

2.  **规范化输出**：将提取的信息整理成CSV格式，字段顺序和格式要求如下：
    *   发票日期 (格式: YYYY-MM-DD)
    *   金额 (单位: 元，保留两位小数)
    *   发票号码
    *   车号 (格式: XX-XXXXXX)
    *   上车时间 (格式: HH:MM)
    *   下车时间 (格式: HH:MM)

3.  **处理缺失值**：
    *   如果图片中找不到发票日期，请在CSV对应位置填写 "NULL"。
    *   如果图片中找不到金额，请在CSV对应位置填写 "NULL"。
    *   如果图片中找不到发票号码，请在CSV对应位置填写 "NULL"。
    *   如果图片中找不到车号，请在CSV对应位置填写 "NULL"。
    *   如果图片中找不到上车时间，请在CSV对应位置填写 "NULL"。
    *   如果图片中找不到下车时间，请在CSV对应位置填写 "NULL"。

4.  **输出格式示例**：
    ```csv
    发票日期,金额,发票号码,车号,上车时间,下车时间
    YYYY-MM-DD,XX.XX,XXXXXXXX,XX-XXXXXX,HH:MM,HH:MM
    ```
    请只输出CSV内容，不要包含表头。

5. **注意事项**：
    如果存在税前价格和税后价格，只统计税后价格。

请根据以上规则处理图片中的发票信息。"""

        # 如果第一次请求失败，尝试另一个URL
        api_url = OLLAMA_API_URL

        # 构建Ollama API请求
        data = {
            "model": OLLAMA_MODEL,
            "prompt": chinese_prompt,
            "images": [base64_image],  # 移除data:image前缀
            "stream": False,
            "options": {
                "vl_high_resolution_images": True  # 启用高分辨率图像处理
            }
        }

        headers = {
            "Content-Type": "application/json"  # 添加请求头
        }

        try:
            # 第一次尝试请求
            response = requests.post(api_url, headers=headers, json=data, timeout=60)
            response.raise_for_status()  # 抛出HTTP错误
        except requests.exceptions.RequestException as e:
            # 如果失败，尝试另一个URL
            alternative_url = (
                LOCAL_API_URL if api_url == DOCKER_API_URL else DOCKER_API_URL
            )
            try:
                response = requests.post(
                    alternative_url, headers=headers, json=data, timeout=60
                )
                response.raise_for_status()
                # 如果成功，更新全局URL
                OLLAMA_API_URL = alternative_url
            except requests.exceptions.RequestException as e2:
                # 两种URL都失败
                error_msg = f"Ollama API请求错误: {str(e2)}"
                if "Connection refused" in str(e2):
                    error_msg += "。请确保Ollama服务已启动，并且可以通过localhost:11434或host.docker.internal:11434访问。"
                raise Exception(error_msg)

        # 解析返回结果
        result = response.json()
        model_output = result.get("response", "")

        if not model_output:
            raise ValueError("模型未返回有效的输出")

        # 解析CSV输出
        parsed_data, _ = parse_csv_output(model_output)
        return parsed_data

    except Exception as e:
        # 将异常传递给批处理器
        raise Exception(f"处理图片 {filename} 时出错: {str(e)}")


def parse_csv_output(model_output):
    """Parses the CSV string output from the model."""
    # Clean potential markdown code blocks
    if model_output.startswith("```csv"):
        model_output = model_output.strip()
        if model_output.startswith("```csv"):
            model_output = model_output[len("```csv") :].strip()
        if model_output.endswith("```"):
            model_output = model_output[: -len("```")].strip()

    # Use io.StringIO to treat the string as a file
    csv_data = io.StringIO(model_output)
    reader = csv.reader(csv_data)
    # Assume the first row is the data we want based on the modified prompt
    try:
        data_row = next(reader)
        # Expected header based on prompt
        header = ["发票日期", "金额", "发票号码", "车号", "上车时间", "下车时间"]
        # Create a list of dictionaries for better display in dataframe
        # Ensure data_row has the same length as header, pad with 'Unknown' if not
        if len(data_row) < len(header):
            data_row.extend(["Unknown"] * (len(header) - len(data_row)))
        elif len(data_row) > len(header):
            data_row = data_row[: len(header)]  # Truncate if too long

        parsed_data = [dict(zip(header, data_row))]
        return parsed_data, header
    except StopIteration:
        # Return empty data but indicate parsing failure upstream if needed
        return [], []
    except Exception as e:
        # Raise exception to be caught by the batch processor
        raise Exception(f"Error parsing CSV output: {e}")


# --- Streamlit App UI ---
st.set_page_config(
    page_title="Invoice OCR",
    page_icon="🧾",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        "Get Help": None,  # 隐藏“Get Help”
        "Report a bug": None,  # 隐藏“Report a bug”
        "About": None,  # 隐藏“About”
    },
)
st.markdown(
    """
    <style>
        .reportview-container {
            margin-top: -2em;
        }
        #MainMenu {visibility: hidden;}
        .stDeployButton {display:none;}
        footer {visibility: hidden;}
        #stDecoration {display:none;}
    </style>
""",
    unsafe_allow_html=True,
)
# Keep UI elements in Chinese as requested
st.title("🧾 发票识别 (支持批量处理)")
st.markdown("上传一张或多张发票图片，提取关键信息。")
st.warning("注意: 请勿上传与公司机密有关文件。")

# Add format selection
download_format = st.radio(
    "选择下载格式:",
    (
        "CSV（注意用CSV导出的结果不可以直接复制到Excel中，若是要复制请选择Excel）",
        "Excel",
        "JSON",
    ),
    horizontal=True,
)

uploaded_files = st.file_uploader(  # Changed variable name
    "上传发票图片 (JPG, PNG)",
    type=["jpg", "jpeg", "png"],
    accept_multiple_files=True,  # Allow multiple files
)

# Define chinese_header in the main scope
chinese_header = [
    "文件名",
    "发票日期",
    "金额",
    "发票号码",
    "车号",
    "上车时间",
    "下车时间",
]

if uploaded_files:  # Check if list is not empty
    st.subheader(f"已上传 {len(uploaded_files)} 张图片:")
    cols = st.columns(min(len(uploaded_files), 10))  # Display up to 10 previews per row
    for idx, uploaded_file in enumerate(uploaded_files):
        with cols[idx % 10]:  # Use modulo 10 to cycle through the 10 columns
            try:
                image = Image.open(uploaded_file)
                st.image(image, caption=uploaded_file.name, use_column_width=True)
            except Exception as e:
                st.error(f"无法显示 {uploaded_file.name}: {e}")

    # Button to trigger processing
    if st.button("✨ 提取信息"):
        results = {}
        errors = {}
        # Use ThreadPoolExecutor for parallel processing
        with st.spinner(f"正在处理 {len(uploaded_files)} 张图片..."):
            with concurrent.futures.ThreadPoolExecutor(
                max_workers=MAX_WORKERS
            ) as executor:
                # Create a future for each uploaded file
                future_to_name = {
                    executor.submit(
                        get_qwen_completion, file.getvalue(), file.name
                    ): file.name
                    for file in uploaded_files
                }

                # Process completed futures
                for future in concurrent.futures.as_completed(future_to_name):
                    filename = future_to_name[future]
                    try:
                        # Get the result (already parsed data with English keys)
                        result_data = future.result()
                        if result_data:  # Check if parsing was successful
                            results[filename] = result_data[
                                0
                            ]  # Store the dict directly
                        else:
                            errors[filename] = "模型未返回有效的CSV数据或解析失败"
                    except Exception as exc:
                        errors[filename] = str(exc)

        # --- Display Results ---
        st.subheader("📊 处理统计")
        st.metric("总计图片", len(uploaded_files))
        st.metric("成功处理", len(results))
        st.metric("处理失败", len(errors))

        if results:
            st.subheader("✅ 提取结果")
            # Combine results into a single list for dataframe display
            all_results_list = []
            for filename, data_dict in results.items():
                # Add filename to the dictionary
                # Ensure the key matches the one in chinese_header
                data_dict_with_filename = {
                    "文件名": filename,
                    **data_dict,
                }
                all_results_list.append(data_dict_with_filename)

            # Display as a single table
            # Create DataFrame first to ensure consistent column order based on chinese_header
            display_df = pd.DataFrame(all_results_list)
            # Reorder columns for display, handling potential missing columns
            display_cols = [col for col in chinese_header if col in display_df.columns]
            st.dataframe(display_df[display_cols], use_container_width=True)

            # --- Download Button Logic ---
            if all_results_list:
                # Ensure download_format is not None before proceeding
                if download_format:
                    # Determine file extension based on format selection
                    if download_format == "Excel":
                        excel_buffer = io.BytesIO()
                        df = pd.DataFrame(all_results_list)
                        # Reorder columns using the globally defined chinese_header
                        cols = [
                            col for col in chinese_header if col in df.columns
                        ]  # Ensure columns exist
                        df = df[cols]  # Use the filtered and ordered columns
                        # Use openpyxl engine for .xlsx format. Ensure openpyxl is installed: pip install openpyxl
                        try:
                            # Change engine to 'openpyxl' and file extension to '.xlsx'
                            df.to_excel(excel_buffer, index=False, engine="openpyxl")
                            download_data = excel_buffer.getvalue()
                            # Update MIME type for .xlsx
                            mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                            # Update file name extension to .xlsx
                            file_name = "invoice_ocr_results.xlsx"
                        except ImportError:
                            # Update error message for openpyxl
                            st.error(
                                "需要安装 'openpyxl' 库才能导出为 .xlsx 格式。请运行: pip install openpyxl"
                            )
                            # Prevent download button rendering if openpyxl is missing
                            download_data = None
                            mime_type = None
                            file_name = None
                        except (
                            Exception
                        ) as e:  # Catch other potential errors during excel writing
                            st.error(f"导出 Excel 文件时出错: {e}")
                            download_data = None
                            mime_type = None
                            file_name = None

                    elif download_format.startswith(
                        "CSV"
                    ):  # Check startswith for the long description
                        # file_extension = "csv" # Not needed here
                        csv_buffer = io.StringIO()
                        # Use the globally defined chinese_header for DictWriter
                        writer = csv.DictWriter(csv_buffer, fieldnames=chinese_header)
                        writer.writeheader()
                        processed_rows = []
                        for row_dict in all_results_list:
                            # Map display keys to expected header keys, handle missing
                            processed_row = {
                                key: row_dict.get(key, "Unknown")
                                for key in chinese_header  # Use global header
                            }
                            processed_rows.append(processed_row)
                        writer.writerows(processed_rows)
                        download_data = csv_buffer.getvalue()
                        mime_type = "text/csv"
                        file_name = (
                            "invoice_ocr_results.csv"  # Explicitly set csv extension
                        )

                    elif download_format == "JSON":
                        # JSON keys will be Chinese based on all_results_list structure
                        download_data = json.dumps(
                            all_results_list, indent=2, ensure_ascii=False
                        )
                        mime_type = "application/json"
                        file_name = (
                            "invoice_ocr_results.json"  # Explicitly set json extension
                        )

                    # Only show download button if data was generated successfully
                    if download_data and mime_type and file_name:
                        # Simplify label text, handle potential missing '（'
                        label_base = (
                            download_format.split("（")[0]
                            if "（" in download_format
                            else download_format
                        )
                        st.download_button(
                            label=f"📥 下载结果 ({label_base})",
                            data=download_data,
                            file_name=file_name,
                            mime=mime_type,
                        )
                else:
                    st.warning(
                        "无法确定下载格式。"
                    )  # Handle case where download_format might be None

        if errors:
            st.subheader("❌ 处理错误")  # Keep UI Chinese
            for filename, error_msg in errors.items():
                st.error(f"**{filename}:** {error_msg}")

else:
    st.info("请上传一张或多张发票图片进行处理。")  # Keep UI Chinese
