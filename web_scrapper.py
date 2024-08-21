from dataclasses import dataclass, field, asdict
from typing import List, Dict, Optional
from bs4 import BeautifulSoup
import os, requests, json


@dataclass
class BlogPost:
    url: str
    post_id: Optional[str] = None
    title: str = ""
    keywords: List[str] = field(default_factory=list)
    thumbnail: Optional[str] = None
    video_duration: Optional[str] = None
    word_count: Optional[int] = None
    lang: Optional[str] = None
    published_date: Optional[str] = None
    last_updated: Optional[str] = None
    description: Optional[str] = None
    author: Optional[str] = None
    classes: List[dict] = field(default_factory=list)
    content: Optional[str] = None


def retrieve_webpage(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        raise Exception(f"Error fetching data from {url}: {e}")


def store_articles(blog_posts):
    if not blog_posts:
        print("No articles to store")
        return

    output_directory = "./blog_posts"
    os.makedirs(output_directory, exist_ok=True)

    first_post = blog_posts[0]
    year, month, *_ = first_post.published_date.split('-')

    file_path = os.path.join(output_directory, f'blog_posts_{year}_{month}.json')
    try:
        with open(file_path, 'w', encoding="utf-8") as file:
            json.dump([asdict(post) for post in blog_posts], file, ensure_ascii=False, indent=4)
        print(f"Articles stored in {file_path}")
    except Exception as e:
        print(f"Error storing articles: {e}")


class SitemapHandler:
    def __init__(self, sitemap_index="https://www.almayadeen.net/sitemaps/all.xml"):
        self.sitemap_index = sitemap_index

    def extract_sitemap_urls(self):
        try:
            content = retrieve_webpage(self.sitemap_index)
            soup = BeautifulSoup(content, "lxml")
            return [element.string for element in soup.find_all("loc")]
        except Exception as e:
            print(f"Error parsing sitemap URLs: {e}")
            return []

    def extract_article_urls(self, sitemap_url):
        try:
            content = retrieve_webpage(sitemap_url)
            soup = BeautifulSoup(content, "lxml")
            return [element.text for element in soup.find_all('loc')]
        except Exception as e:
            print(f"Error parsing article URLs from {sitemap_url}: {e}")
            return []


@dataclass
class ArticleExtractor:

    def extract(self, article_url):
        try:
            content = retrieve_webpage(article_url)
            soup = BeautifulSoup(content, "lxml")
            script = soup.find("script", {"type": "text/tawsiyat"})
            metadata = json.loads(script.string) if script else {}

            full_text = "\n".join(paragraph.text for paragraph in soup.find_all("p"))
            post = BlogPost(
                url=article_url,
                post_id=metadata.get('postid', ''),
                title=metadata.get('title', ''),
                keywords=metadata.get('keywords', '').split(" "),
                thumbnail=metadata.get('thumbnail', ''),
                video_duration=metadata.get('video_duration', ''),
                word_count=metadata.get('word_count', ''),
                lang=metadata.get('lang', ''),
                published_date=metadata.get('published_time', ''),
                last_updated=metadata.get('last_updated', ''),
                description=metadata.get('description', ''),
                author=metadata.get('author', ''),
                classes=metadata.get('classes', []),
                content=full_text
            )
            return post
        except Exception as e:
            print(f"Error extracting article {article_url}: {e}")
            return None


def main():
    max_posts = 10000
    post_count = 1

    sitemap_handler = SitemapHandler()
    sitemap_urls = sitemap_handler.extract_sitemap_urls()

    for sitemap_url in sitemap_urls:
        if post_count > max_posts:
            break
        print(f"Processing {sitemap_url}")
        article_urls = sitemap_handler.extract_article_urls(sitemap_url)
        print(f"Retrieved {len(article_urls)} article URLs")
        posts = []

        extractor = ArticleExtractor()
        for url in article_urls:
            if post_count > max_posts:
                break
            post = extractor.extract(url)
            if post:
                print(f"Extracting article {post_count} from {url}")
                post_count += 1
                posts.append(post)
        store_articles(posts)


if __name__ == "__main__":
    main()
