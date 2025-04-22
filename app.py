import streamlit as st
import base64
import io
import csv
import json  # Import json
import pandas as pd  # Import pandas
from openai import OpenAI
from PIL import Image
import concurrent.futures  # Import for parallel processing
import os  # Import os module

# --- Configuration ---
# WARNING: Hardcoding API keys is insecure. Consider using Streamlit secrets or environment variables.

# Get API Key from environment variable
QWEN_API_KEY = os.getenv("QWEN_API_KEY")
if not QWEN_API_KEY:
    st.error("错误：QWEN_API_KEY 环境变量未设置。请在运行 Docker 容器前设置该变量。")
    st.stop()  # Stop execution if key is missing

QWEN_BASE_URL = "https://dashscope.aliyuncs.com/compatible-mode/v1"
QWEN_MODEL = "qwen-vl-max-latest"  # Or "qwen-vl-plus"
MAX_WORKERS = 100  # Number of parallel API calls


# --- Helper Functions ---
def encode_image_bytes(image_bytes):
    """Encodes image bytes to base64."""
    return base64.b64encode(image_bytes).decode("utf-8")


def get_qwen_completion(image_bytes, filename=""):  # Add filename for error reporting
    """Calls the Qwen VL API and returns the completion result."""
    try:
        client = OpenAI(
            api_key=QWEN_API_KEY,
            base_url=QWEN_BASE_URL,
        )

        base64_image = encode_image_bytes(image_bytes)

        # --- Modified Prompt for English Output ---
        english_prompt = """You are a professional image data processing assistant responsible for extracting information from the provided invoice image and converting it into standardized CSV format using English.

Please analyze the following image and perform these tasks:

1.  **Identify Key Information**: Find the following invoice details in the image:
    *   Invoice Date
    *   Amount
    *   Invoice Number
    *   Vehicle Number

2.  **Standardize Output**: Organize the extracted information into CSV format with the following field order and format requirements:
    *   Invoice Date (Format: YYYY-MM-DD)
    *   Amount (Unit: Yuan, two decimal places)
    *   Invoice Number
    *   Vehicle Number (Format: XX-XXXXXX, if applicable)

3.  **Handle Missing Values**:
    *   If the Invoice Date is not found, fill the corresponding CSV position with "NULL".
    *   If the Amount is not found, fill the corresponding CSV position with "NULL".
    *   If the Invoice Number is not found, fill the corresponding CSV position with "NULL".
    *   If the Vehicle Number is not found, fill the corresponding CSV position with "NULL".

4.  **Output Format Example**:
    ```csv
    Invoice Date,Amount,Invoice Number,Vehicle Number
    YYYY-MM-DD,XX.XX,XXXXXXXX,XX-XXXXXX
    ```
    Please output ONLY the CSV data row, without the header row.

5. **Important Note**:
    If both pre-tax and post-tax amounts are present, use the post-tax amount.

Process the invoice information in the image according to these rules. Output should be in English."""

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

        completion = client.chat.completions.create(
            model=QWEN_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": [
                        {
                            "type": "text",
                            "text": "You are a helpful assistant processing invoices.",
                        }
                    ],
                },
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            },
                        },
                        {
                            "type": "text",
                            "text": chinese_prompt,  # Use the Chinese prompt
                        },
                    ],
                },
            ],
            # stream=True # Streaming might require different handling
        )
        # Extract the content directly
        if completion and completion.choices:
            model_output = completion.choices[0].message.content
            parsed_data, _ = parse_csv_output(model_output)  # Parse here
            return parsed_data  # Return parsed data directly
        else:
            raise ValueError("API did not return expected choices.")

    except Exception as e:
        # Raise exception to be caught by the batch processor
        raise Exception(f"Error processing {filename}: {e}")


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
