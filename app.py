import streamlit as st
import boto3
import uuid
import time
from PIL import Image
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import simpleSplit

# ===========================
# AWS CONFIG
# ===========================
REGION = "us-east-1"
BUCKET_NAME = "vishal-documents-us-east-1"
TABLE_NAME = "DocumentRecords"

# AWS Clients
s3 = boto3.client("s3", region_name=REGION)
dynamodb = boto3.resource("dynamodb", region_name=REGION)
table = dynamodb.Table(TABLE_NAME)

# ===========================
# PAGE SETTINGS
# ===========================
st.set_page_config(
    page_title="AWS Textract OCR",
    layout="centered",
    page_icon="📄"
)

st.markdown("""
    <h1 style='text-align:center;'>📄 AWS Textract Document Analyzer</h1>
    <p style='text-align:center;'>Upload an image or PDF and extract text using AWS Textract</p>
""", unsafe_allow_html=True)


# ===========================
# FILE UPLOAD
# ===========================
uploaded_file = st.file_uploader(
    "Choose Image or PDF", 
    type=["png", "jpg", "jpeg", "pdf"]
)

if uploaded_file:

    st.subheader("📎 File Preview")

    # For images, show preview
    if uploaded_file.type != "application/pdf":
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_column_width=True)
    else:
        st.info("PDF Uploaded — Preview not available, but it will be processed.")

    # Unique file key
    file_key = f"{uuid.uuid4()}_{uploaded_file.name}"

    # ===========================
    # UPLOAD TO S3
    # ===========================
    with st.spinner("Uploading to S3..."):
        s3.put_object(
            Bucket=BUCKET_NAME,
            Key=file_key,
            Body=uploaded_file.getvalue(),
            ContentType=uploaded_file.type
        )
    st.success(f"✔ File uploaded as: {file_key}")

    st.info("🔁 Waiting for Lambda + Textract to analyze the document...")

    # ===========================
    # POLL DYNAMODB FOR RESULT
    # ===========================
    extracted_text = None

    for _ in range(20):     # Wait 20 seconds max
        time.sleep(1)

        response = table.scan(
            FilterExpression="DocumentName = :name",
            ExpressionAttributeValues={":name": file_key}
        )

        if response.get("Items"):
            extracted_text = response["Items"][0].get("ExtractedText")
            break

    # ===========================
    # SHOW RESULT
    # ===========================
    if extracted_text:
        st.success("✔ Textract extraction completed!")

        st.subheader("📄 Extracted Text")
        st.text_area("Extracted Text", extracted_text, height=300)
        
        # Download buttons
        col1, col2 = st.columns(2)
        
        with col1:
            st.download_button(
                label="📄 Download as TXT",
                data=extracted_text,
                file_name=f"{uploaded_file.name}_extracted.txt",
                mime="text/plain"
            )
        
        with col2:
            # Create PDF
            pdf_buffer = BytesIO()
            c = canvas.Canvas(pdf_buffer, pagesize=letter)
            width, height = letter
            
            # Split text into lines that fit the page
            lines = []
            for paragraph in extracted_text.split('\n'):
                if paragraph.strip():
                    wrapped_lines = simpleSplit(paragraph, "Helvetica", 12, width - 100)
                    lines.extend(wrapped_lines)
                else:
                    lines.append('')
            
            y = height - 50
            for line in lines:
                if y < 50:  # Start new page
                    c.showPage()
                    y = height - 50
                c.drawString(50, y, line)
                y -= 15
            
            c.save()
            pdf_data = pdf_buffer.getvalue()
            
            st.download_button(
                label="📄 Download as PDF",
                data=pdf_data,
                file_name=f"{uploaded_file.name}_extracted.pdf",
                mime="application/pdf"
            )

    else:
        st.error("❌ Text not found yet. Try again after a few seconds.")