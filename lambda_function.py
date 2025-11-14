import json
import boto3
import urllib.parse
from datetime import datetime
import time

s3 = boto3.client('s3')
textract = boto3.client('textract')
dynamodb = boto3.resource('dynamodb')

TABLE_NAME = "DocumentRecords"
table = dynamodb.Table(TABLE_NAME)

def lambda_handler(event, context):
    try:
        record = event['Records'][0]
        bucket = record['s3']['bucket']['name']
        key = urllib.parse.unquote_plus(record['s3']['object']['key'])

        print(f"Processing: {bucket}/{key}")

        # Check file extension
        if key.lower().endswith(".pdf"):
            print("PDF detected — starting async Textract job")
            
            # Start async job
            response = textract.start_document_text_detection(
                DocumentLocation={
                    'S3Object': {
                        'Bucket': bucket,
                        'Name': key
                    }
                }
            )

            job_id = response["JobId"]
            print("JobId:", job_id)

            # Poll until job completes
            while True:
                result = textract.get_document_text_detection(JobId=job_id)
                status = result["JobStatus"]
                print("Status:", status)

                if status in ["SUCCEEDED", "FAILED"]:
                    break
                
                time.sleep(1)

            # Extract text
            lines = []
            for block in result["Blocks"]:
                if block["BlockType"] == "LINE":
                    lines.append(block["Text"])

            extracted_text = "\n".join(lines)

        else:
            print("Image detected — using sync API")
            response = textract.detect_document_text(
                Document={'S3Object': {'Bucket': bucket, 'Name': key}}
            )

            lines = []
            for block in response.get('Blocks', []):
                if block['BlockType'] == 'LINE':
                    lines.append(block['Text'])

            extracted_text = "\n".join(lines)

        now = datetime.utcnow().isoformat()

        table.put_item(Item={
            'DocumentName': key,
            'UploadedAt': now,
            'ExtractedText': extracted_text
        })

        print("Saved to DynamoDB")
        return {"statusCode": 200, "body": "done"}

    except Exception as e:
        print("ERROR:", e)
        raise
