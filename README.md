# 📘 AWS Serverless Document Analysis System (Textract + Lambda + S3 + DynamoDB)

This project is a fully serverless, cloud-based Document OCR (Optical Character Recognition) system built using Amazon Web Services.  
Users upload a **PDF or image** from a simple frontend, and the system automatically extracts text using **Amazon Textract**, stores the result in **DynamoDB**, and displays it back to the user.

This project demonstrates real-world serverless architecture, automation, and AI-driven document processing.

---

## 🚀 Features

- Upload **PDF or image files** (JPG, PNG, JPEG, PDF)
- Automatic upload to **Amazon S3**
- Event-driven processing using **AWS Lambda**
- Text extraction using **Amazon Textract**
- Process **multi-page PDFs** using Textract Async APIs
- Store results in **DynamoDB**
- Display extracted text in a simple Streamlit-based UI
- Fully serverless, scalable, and cost-efficient

---

## 🧱 Architecture Overview


---

## 🛠️ Technology Stack

### **Frontend**
- Streamlit (Python UI)

### **Backend**
- AWS Lambda (Python 3.10)

### **Cloud Services**
- Amazon S3
- Amazon Textract  
- Amazon DynamoDB  
- CloudWatch Logs  
- IAM Roles  
- AWS SDK (boto3)

---

## 📂 Project Structure
📦 project-root

├── 📄 app.py                # Streamlit frontend application

├── 📄 lambda_function.py    # AWS Lambda code for Textract processing

├── 📄 requirements.txt      # Python dependencies

└── 📄 README.md             # Project documentation



---

## ⚙️ AWS Configuration Steps

### **1. Create S3 Bucket**
- `vishal-documents-us-east-1`

### **2. Create DynamoDB Table**
- Table name: `DocumentRecords`
- Partition key: `DocumentName` (String)
- Sort key: `UploadedAt` (String)

### **3. Create IAM Role for Lambda**
Role name: `TextractDocumentProcessorRole`

Attach:
- AWSLambdaBasicExecutionRole
- Inline policy (Textract + S3 + DynamoDB permissions)

### **4. Create Lambda Function**
Function name: `textract_processor`  
Runtime: Python 3.10  
Trigger: S3 `ObjectCreated` event

### **5. Add Trigger**
S3 → Upload bucket → Events → "All object create events"

---

## 🧩 Lambda Code (Core Logic)

The Lambda function does:
- Detect PDF or Image format
- Uses **Async Textract** for PDF  
- Uses **Sync Textract** for images  
- Saves extracted text to DynamoDB

(Your lambda_function.py goes here.)

---

## 💻 Running the Frontend Locally

### **Install dependencies**
pip install -r requirements.txt


### **Run Streamlit**


python -m streamlit run app.py


### App opens at:


http://localhost:8501


---

## 📸 Screenshots (Add your images)

Add your screenshots here:


<img width="1431" height="787" alt="Screenshot 2025-11-14 100746" src="https://github.com/user-attachments/assets/0251cc59-e621-477c-b471-1735b2fb0e4e" />
<img width="1440" height="794" alt="Screenshot 2025-11-14 101040" src="https://github.com/user-attachments/assets/99098b8a-ef6c-4146-a93d-6f254b76555c" />
<img width="1437" height="760" alt="Screenshot 2025-11-14 101009" src="https://github.com/user-attachments/assets/d4310f39-83a3-47ab-acd8-b2c3907331e4" />
<img width="1435" height="782" alt="Screenshot 2025-11-14 100948" src="https://github.com/user-attachments/assets/a42b3bac-6065-4464-a715-77700ab2231a" />
<img width="1433" height="775" alt="Screenshot 2025-11-14 100915" src="https://github.com/user-attachments/assets/77c70aed-a532-44d9-9e2a-b694de2600bc" />
<img width="1438" height="790" alt="Screenshot 2025-11-14 100859" src="https://github.com/user-attachments/assets/d947a0f4-e129-4a8c-9043-3f8d8c1212b6" />
<img width="1432" height="778" alt="Screenshot 2025-11-14 100820" src="https://github.com/user-attachments/assets/e3036091-64f2-4d7c-8c46-e7face2d3287" />


---

## 🔮 Future Enhancements

- Extract **tables** and **key-value pairs** from forms
- Add **invoice/ID extraction mode**
- Add **AI-powered summarization** (OpenAI / Bedrock)
- Add **email alerts** after processing
- Add **user authentication** (Cognito)
- Deploy frontend using **S3 + CloudFront**

---

## 👨‍💻 Author

**Vishal** 

---

## 📄 License  
This project is open-source under the MIT License.




