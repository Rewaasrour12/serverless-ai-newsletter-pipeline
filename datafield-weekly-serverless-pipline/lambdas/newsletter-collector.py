import json
import boto3
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime

s3 = boto3.client('s3')
BUCKET_NAME = 'data-engineer-newsletter'

def fetch_rss(url, source_name, max_items=5):
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=10) as response:
            content = response.read()
        root = ET.fromstring(content)
        items = []
        for item in root.findall('.//item')[:max_items]:
            title = item.findtext('title', '').strip()
            link = item.findtext('link', '').strip()
            description = item.findtext('description', '').strip()
            pub_date = item.findtext('pubDate', '').strip()
            if title and link:
                items.append({
                    'title': title,
                    'link': link,
                    'description': description[:300],
                    'pub_date': pub_date,
                    'source': source_name
                })
        return items
    except Exception as e:
        print(f"Error fetching {source_name}: {e}")
        return []

def fetch_hackernews():
    try:
        url = 'https://hacker-news.firebaseio.com/v0/topstories.json'
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=10) as r:
            story_ids = json.loads(r.read())[:50]
        relevant_stories = []
        keywords = ['pipeline', 'spark', 'kafka', 'dbt', 'airflow', 'warehouse', 'lake', 'streaming', 'analytics', 'engineering', 'sql', 'python']
        for story_id in story_ids:
            if len(relevant_stories) >= 5:
                break
            story_url = f'https://hacker-news.firebaseio.com/v0/item/{story_id}.json'
            req = urllib.request.Request(story_url)
            with urllib.request.urlopen(req, timeout=5) as r:
                story = json.loads(r.read())
            if not story or story.get('type') != 'story':
                continue
            title = story.get('title', '').lower()
            if any(keyword in title for keyword in keywords):
                relevant_stories.append({
                    'title': story.get('title', ''),
                    'link': story.get('url', f"https://news.ycombinator.com/item?id={story_id}"),
                    'description': f"Score: {story.get('score', 0)} | Comments: {story.get('descendants', 0)}",
                    'pub_date': str(datetime.fromtimestamp(story.get('time', 0))),
                    'source': 'Hacker News'
                })
        return relevant_stories
    except Exception as e:
        print(f"Error fetching HN: {e}")
        return []

def lambda_handler(event, context):
    rss_sources = [
        {'url': 'https://aws.amazon.com/blogs/big-data/feed/', 'name': 'AWS Big Data Blog'},
        {'url': 'https://blog.getdbt.com/rss/', 'name': 'dbt Blog'},
        {'url': 'https://engineering.linkedin.com/blog.rss', 'name': 'LinkedIn Engineering'},
        {'url': 'https://netflixtechblog.com/feed', 'name': 'Netflix Tech Blog'},
        {'url': 'https://www.astronomer.io/blog/rss.xml', 'name': 'Astronomer'},
        {'url': 'https://feeds.feedburner.com/oreilly/radar/atom', 'name': "O'Reilly Radar"},
    ]
    all_items = []
    for source in rss_sources:
        items = fetch_rss(source['url'], source['name'])
        all_items.extend(items)
        print(f"Got {len(items)} from {source['name']}")
    hn_items = fetch_hackernews()
    all_items.extend(hn_items)
    result = {
        'collected_at': datetime.now().isoformat(),
        'total_items': len(all_items),
        'items': all_items
    }
    s3.put_object(
        Bucket=BUCKET_NAME,
        Key='data/raw_collected.json',
        Body=json.dumps(result, ensure_ascii=False, indent=2),
        ContentType='application/json'
    )
    print(f"Total collected: {len(all_items)}")
    return {'statusCode': 200, 'body': f'Collected {len(all_items)} items'}
