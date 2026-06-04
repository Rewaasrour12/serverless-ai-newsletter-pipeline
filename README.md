# Serverless AI Newsletter Pipeline

An automated pipeline that runs every Friday. It collects news from the data field — pipelines, warehousing, analytics, and tools — sends it to Claude to summarize, and delivers a clean HTML newsletter to my inbox.

Everything runs on AWS serverless services and No manual work. 

---

## The Problem

Keeping up with the data field is not easy. Every week there are new tools, blog posts, Hacker News threads, and updates from different companies.

I wanted something that collects all of this for me and sends a short summary every Friday morning — without me doing anything.

---

## How It Works

Three Lambda functions, triggered every Friday by EventBridge.

### 1. Collector Lambda

Pulls articles from 6 RSS feeds: AWS Big Data Blog, dbt Blog, Netflix Tech Blog, LinkedIn Engineering, Astronomer, and O'Reilly Radar.

Also scrapes top Hacker News stories and filters by keywords like Kafka, Spark, Airflow, dbt, SQL, and analytics.

All collected data gets saved to S3 as a JSON file.

---

### 2. Summarizer Lambda

Reads the JSON from S3 and sends it to Claude via Amazon Bedrock.

Claude summarizes the articles and generates the HTML newsletter with 5 sections:
- Biggest news this week
- Tools worth watching
- Market trends
- Deep dive of the week
- Practical takeaways

The HTML is saved to S3 as index.html and served as a static website.

---

### 3. Notifier Lambda

Sends an email via Amazon SES with a direct link to the newsletter. One click to open it.

---

## Architecture

```
EventBridge → Controller Lambda → S3 → Summarizer Lambda (Bedrock / Claude) → S3 Static Website → SES Email
```

---

## Stack

| Service | What it does |
|---|---|
| AWS Lambda (Python) | Runs all the functions |
| Amazon S3 | Stores raw data and hosts the website |
| Amazon Bedrock (Claude Haiku) | Summarizes the articles and generates the newsletter |
| Amazon SES | Sends email notifications |
| Amazon EventBridge | Triggers the pipeline every Friday |

---

## Screenshots

### Email Notification
![Email](datafield-weekly-serverless-pipline/Screenshots/Mail.png)

### Newsletter Website
![Newsletter](datafield-weekly-serverless-pipline/Screenshots/Website_1.png)
![Newsletter](datafield-weekly-serverless-pipline/Screenshots/Website_2.png)

### Lambda Functions
![Collector Lambda](datafield-weekly-serverless-pipline/Screenshots/Collector_Lambda.png)
![Summarizer Lambda](datafield-weekly-serverless-pipline/Screenshots/Summarizer_Lambda.png)

### S3 Bucket
![S3 Bucket](datafield-weekly-serverless-pipline/Screenshots/S3_Bucket.png)
![JSON File](datafield-weekly-serverless-pipline/Screenshots/Json_File_S3_Bucket.png)

---

## Project Structure

```text
serverless-ai-newsletter-pipeline/
├── datafield-weekly-serverless-pipline/
│   └── Screenshots/
│       ├── Collector_Lambda.png
│       ├── Json_File_S3_Bucket.png
│       ├── Mail.png
│       ├── Original_Source_1.png
│       ├── S3_Bucket.png
│       ├── Summarizer_Lambda.png
│       ├── Website_1.png
│       └── Website_2.png
├── lambdas/
│   ├── data/
│   │   └── raw_collected.json
│   ├── newsletter-collector.py
│   ├── newsletter-notifier.py
│   └── newsletter-summarizer.py
└── README.md
```
