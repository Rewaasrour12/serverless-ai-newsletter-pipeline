import json
import boto3
import os
from datetime import datetime

s3 = boto3.client('s3')
bedrock = boto3.client('bedrock-runtime', region_name='us-east-1')

BUCKET_NAME = os.environ['BUCKET_NAME']


# ========================
# Call Claude via Bedrock
# ========================
def call_claude(prompt):
    try:
        response = bedrock.invoke_model(
	       modelId='us.anthropic.claude-haiku-4-5-20251001-v1:0',
            body=json.dumps({
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": 4000,
                "temperature": 0.7,
                "messages": [{"role": "user", "content": prompt}]
            })
        )
        result = json.loads(response['body'].read())
        return result['content'][0]['text']
    except Exception as e:
        print(f"Bedrock error: {str(e)}")
        return f"<div class='card'><p>Error calling Claude via Bedrock: {str(e)}</p></div>"


# ========================
# HTML Generator
# ========================
def generate_html(summary_html, items):
    week_date = datetime.now().strftime("%B %d, %Y")

    # Deduplicate sources
    sources = list(set(i.get('source', 'unknown') for i in items))
    sources_html = ''.join(
        [f'<span class="tag">{s}</span>' for s in sources]
    )

    # Limit to first 20 article links
    links_html = ''.join([
        f'<a href="{i.get("link","#")}" target="_blank" class="link-card">'
        f'<span class="src">{i.get("source","unknown")}</span>'
        f'<span class="ttl">{i.get("title","")}</span></a>'
        for i in items[:20]
    ])

    return f"""<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Data Field Weekly - {week_date}</title>

<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Arabic:wght@300;400;500;600;700&family=Fira+Code:wght@400;500&display=swap" rel="stylesheet">

<style>
:root {{
--bg:#f4f6f9;
--surface:#ffffff;
--surface2:#eef1f6;
--accent:#4a7fa5;
--purple:#8b7aa0;
--text:#2c3a4a;
--muted:#8a97a8;
--border:rgba(74,127,165,0.15);
}}

* {{
margin:0;
padding:0;
box-sizing:border-box;
}}

body {{
font-family:'IBM Plex Sans Arabic',sans-serif;
background:var(--bg);
color:var(--text);
}}

.top-stripe {{
height:3px;
background:linear-gradient(90deg,var(--accent),var(--purple));
}}

header {{
text-align:center;
padding:60px 20px 40px;
border-bottom:1px solid var(--border);
}}

.mono {{
font-family:'Fira Code',monospace;
font-size:11px;
letter-spacing:3px;
color:var(--accent);
text-transform:uppercase;
margin-bottom:16px;
}}

h1 {{
font-size:clamp(26px,5vw,44px);
font-weight:700;
}}

h1 em {{
color:var(--accent);
font-style:normal;
}}

.date {{
display:inline-block;
margin-top:14px;
padding:6px 18px;
border-radius:20px;
background:var(--surface);
border:1px solid var(--border);
font-family:'Fira Code',monospace;
font-size:13px;
color:var(--muted);
}}

.wrap {{
max-width:820px;
margin:0 auto;
padding:0 20px 80px;
}}

.stats {{
display:flex;
gap:16px;
margin:32px 0;
flex-wrap:wrap;
}}

.stat {{
flex:1;
min-width:110px;
background:var(--surface);
border:1px solid var(--border);
border-radius:10px;
padding:18px;
text-align:center;
box-shadow:0 2px 8px rgba(74,127,165,0.07);
}}

.stat-n {{
font-family:'Fira Code',monospace;
font-size:28px;
font-weight:700;
color:var(--accent);
}}

.stat-l {{
font-size:12px;
color:var(--muted);
margin-top:4px;
}}

.tags {{
padding:18px 0;
border-top:1px solid var(--border);
border-bottom:1px solid var(--border);
margin:8px 0 32px;
}}

.tags-l {{
font-family:'Fira Code',monospace;
font-size:10px;
letter-spacing:2px;
color:var(--muted);
text-transform:uppercase;
margin-bottom:10px;
}}

.tag {{
display:inline-block;
background:var(--surface2);
border:1px solid var(--border);
padding:4px 10px;
border-radius:4px;
font-size:12px;
color:var(--muted);
margin:3px;
}}

.section {{
margin:36px 0;
}}

.sec-head {{
display:flex;
align-items:center;
gap:12px;
margin-bottom:16px;
}}

.sec-num {{
font-family:'Fira Code',monospace;
font-size:11px;
color:var(--accent);
background:rgba(74,127,165,0.08);
padding:4px 10px;
border-radius:4px;
}}

.sec-head h2 {{
font-size:19px;
font-weight:600;
}}

.card {{
background:var(--surface);
border:1px solid var(--border);
border-radius:12px;
padding:28px;
line-height:1.85;
font-size:15px;
position:relative;
box-shadow:0 2px 12px rgba(74,127,165,0.07);
}}

.card::before {{
content:'';
position:absolute;
right:0;
top:0;
bottom:0;
width:3px;
border-radius:0 12px 12px 0;
background:linear-gradient(180deg,var(--accent),var(--purple));
}}

.card strong {{
color:var(--accent);
font-weight:600;
}}

.links-sec {{
margin-top:48px;
padding-top:28px;
border-top:1px solid var(--border);
}}

.links-title {{
font-family:'Fira Code',monospace;
font-size:10px;
letter-spacing:2px;
color:var(--muted);
text-transform:uppercase;
margin-bottom:18px;
}}

.link-card {{
display:flex;
gap:12px;
padding:14px;
background:var(--surface);
border:1px solid var(--border);
border-radius:8px;
margin-bottom:8px;
text-decoration:none;
box-shadow:0 1px 6px rgba(74,127,165,0.06);
transition:box-shadow 0.2s;
}}

.link-card:hover {{
box-shadow:0 3px 14px rgba(74,127,165,0.13);
}}

.src {{
font-family:'Fira Code',monospace;
font-size:10px;
color:var(--accent);
background:rgba(74,127,165,0.08);
padding:3px 8px;
border-radius:3px;
white-space:nowrap;
}}

.ttl {{
font-size:14px;
color:var(--text);
font-weight:500;
line-height:1.4;
}}

footer {{
text-align:center;
padding:32px;
border-top:1px solid var(--border);
font-family:'Fira Code',monospace;
font-size:12px;
color:var(--muted);
}}
</style>
</head>

<body>
<div class="top-stripe"></div>

<header>
<div class="wrap">
<div class="mono">// weekly digest</div>
<h1>Data <em>Field</em> Weekly</h1>
<p style="color:var(--muted);font-size:14px;margin-top:10px">
Real info from trusted sources - not LLM hallucinations
</p>
<div class="date">Week of {week_date}</div>
</div>
</header>

<div class="wrap">

<div class="stats">
<div class="stat"><div class="stat-n">{len(items)}</div><div class="stat-l">Articles analyzed</div></div>
<div class="stat"><div class="stat-n">{len(sources)}</div><div class="stat-l">Trusted sources</div></div>
<div class="stat"><div class="stat-n">1</div><div class="stat-l">Weekly digest</div></div>
</div>

<div class="tags">
<div class="tags-l">// sources this week</div>
{sources_html}
</div>

{summary_html}

<div class="links-sec">
<div class="links-title">// read the originals</div>
{links_html}
</div>

</div>

<footer>
Generated every Friday · AWS Lambda + Claude via Bedrock · Real sources only
</footer>

</body>
</html>"""


# ========================
# Lambda Handler
# ========================
def lambda_handler(event, context):

    # Load raw collected data from S3
    obj = s3.get_object(
        Bucket=BUCKET_NAME,
        Key='data/raw_collected.json'
    )

    raw_data = json.loads(obj['Body'].read())
    items = raw_data.get('items', [])

    # Build article list as text for the Claude prompt
    items_text = ""
    for i, item in enumerate(items, 1):
        items_text += f"""
{i}. [{item.get('source','unknown')}] {item.get('title','')}
   {item.get('description','')[:200]}
---
"""

    prompt = f"""
You are the editor of a weekly newsletter on Data Engineering and Analytics.

Here are {len(items)} articles from this week:

{items_text}

Return ONLY valid HTML. No markdown. No explanations. No code blocks.
All content must follow this exact structure:

<div class="section">
<div class="sec-head"><span class="sec-num">01</span><h2>Biggest news this week</h2></div>
<div class="card"><p>[3-4 paragraphs on key developments and practical impact]</p></div>
</div>

<div class="section">
<div class="sec-head"><span class="sec-num">02</span><h2>Tools and tech worth watching</h2></div>
<div class="card"><p>[new tools, frameworks, important updates]</p></div>
</div>

<div class="section">
<div class="sec-head"><span class="sec-num">03</span><h2>Market trends</h2></div>
<div class="card"><p>[community trends and discussions]</p></div>
</div>

<div class="section">
<div class="sec-head"><span class="sec-num">04</span><h2>Deep dive of the week</h2></div>
<div class="card"><p>[one topic explained in depth]</p></div>
</div>

<div class="section">
<div class="sec-head"><span class="sec-num">05</span><h2>Practical takeaways</h2></div>
<div class="card"><p>[3-5 actionable insights]</p></div>
</div>

Use <strong> tags for technical terms.
"""

    # Call Claude via Bedrock
    summary_html = call_claude(prompt)

    # Strip any markdown code fences Claude might have added
    summary_html = summary_html.replace("```html", "").replace("```", "").strip()

    # Build the final HTML page
    full_html = generate_html(summary_html, items)

    # Save the generated page to S3 as the site index
    s3.put_object(
        Bucket=BUCKET_NAME,
        Key='index.html',
        Body=full_html.encode('utf-8'),
        ContentType='text/html; charset=utf-8'
    )

    return {
        'statusCode': 200,
        'body': 'Done'
    }