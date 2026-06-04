import boto3
import os
from datetime import datetime

ses = boto3.client('ses', region_name='us-east-1')
YOUR_EMAIL = 'rewaasrour@gmail.com'
BUCKET_NAME = os.environ['BUCKET_NAME']
WEBSITE_URL = f"http://{BUCKET_NAME}.s3-website-us-east-1.amazonaws.com"

def lambda_handler(event, context):
    week_date = datetime.now().strftime("%B %d, %Y")
    html = f"""
<div style="font-family:Georgia,serif;background:#f5f3f0;color:#2d3748;padding:40px 20px;">
  <div style="max-width:560px;margin:0 auto;background:#ffffff;border-radius:16px;overflow:hidden;border:1px solid #dde3ec;box-shadow:0 4px 24px rgba(100,120,160,0.10)">
    <div style="height:4px;background:linear-gradient(90deg,#6b8cba,#b5a4c7)"></div>
    <div style="padding:40px">
      <div style="font-family:monospace;font-size:11px;letter-spacing:3px;color:#7a9bbf;margin-bottom:14px;text-transform:uppercase">// Weekly Digest Ready</div>
      <h1 style="font-size:26px;font-weight:700;margin-bottom:6px;color:#2d3748">Data Engineering <span style="color:#6b8cba">Weekly</span></h1>
      <p style="color:#a0aec0;font-size:14px;margin-bottom:24px">Week of {week_date}</p>
      <p style="color:#718096;line-height:1.8;margin-bottom:28px;font-size:15px">This week's digest is ready — real articles from trusted sources, analyzed and summarized for you.</p>
      <a href="{WEBSITE_URL}" style="display:block;background:linear-gradient(135deg,#6b8cba,#b5a4c7);color:white;text-decoration:none;padding:16px;border-radius:10px;text-align:center;font-weight:600;font-size:16px;margin-bottom:20px;letter-spacing:0.5px">Read This Week's Digest →</a>
      <p style="text-align:center;font-family:monospace;font-size:11px;color:#a0aec0">{WEBSITE_URL}</p>
    </div>
    <div style="text-align:center;padding:20px;border-top:1px solid #edf0f5;font-family:monospace;font-size:11px;color:#b0bec9;background:#fafbfd">Sent every Friday · AWS Lambda + Claude</div>
  </div>
</div>"""
    ses.send_email(
        Source=YOUR_EMAIL,
        Destination={'ToAddresses': [YOUR_EMAIL]},
        Message={
            'Subject': {'Data': f'Data Engineering Weekly - {week_date}', 'Charset': 'UTF-8'},
            'Body': {'Html': {'Data': html, 'Charset': 'UTF-8'}}
        }
    )
    return {'statusCode': 200, 'body': 'Email sent'}
