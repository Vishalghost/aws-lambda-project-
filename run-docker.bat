@echo off
echo 🐳 Building and running Docker container...

docker build -t textract-app .
docker run -p 8501:8501 -e AWS_ACCESS_KEY_ID=%AWS_ACCESS_KEY_ID% -e AWS_SECRET_ACCESS_KEY=%AWS_SECRET_ACCESS_KEY% -e AWS_DEFAULT_REGION=us-east-1 textract-app

echo ✅ App running at http://localhost:8501