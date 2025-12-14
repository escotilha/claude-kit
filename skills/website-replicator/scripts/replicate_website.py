#!/usr/bin/env python3
"""
Website Replicator - Clone websites locally for study purposes.
Downloads HTML, CSS, JS, images, and other assets while preserving structure.
"""

import os
import re
import sys
import hashlib
import argparse
from pathlib import Path
from urllib.parse import urljoin, urlparse, unquote
from concurrent.futures import ThreadPoolExecutor, as_completed

try:
    import requests
    from bs4 import BeautifulSoup
except ImportError:
    print("Installing required packages...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "requests", "beautifulsoup4", "--break-system-packages", "-q"])
    import requests
    from bs4 import BeautifulSoup


class WebsiteReplicator:
    def __init__(self, url: str, output_dir: str, max_depth: int = 2, max_pages: int = 50):
        self.base_url = url.rstrip('/')
        self.parsed_base = urlparse(self.base_url)
        self.domain = self.parsed_base.netloc
        self.output_dir = Path(output_dir)
        self.max_depth = max_depth
        self.max_pages = max_pages
        
        self.visited_urls = set()
        self.downloaded_assets = {}
        self.pages_downloaded = 0
        
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
        })

    def url_to_filepath(self, url: str, is_page: bool = False) -> Path:
        """Convert URL to local file path."""
        parsed = urlparse(url)
        path = unquote(parsed.path) or '/index.html'
        
        if is_page and not path.endswith(('.html', '.htm', '.php', '.asp', '.aspx')):
            if path.endswith('/'):
                path += 'index.html'
            else:
                path += '/index.html'
        
        # Handle query strings by hashing them
        if parsed.query:
            query_hash = hashlib.md5(parsed.query.encode()).hexdigest()[:8]
            base, ext = os.path.splitext(path)
            path = f"{base}_{query_hash}{ext}"
        
        # Clean the path
        path = path.lstrip('/')
        if not path:
            path = 'index.html'
            
        return self.output_dir / path

    def is_same_domain(self, url: str) -> bool:
        """Check if URL belongs to the same domain."""
        parsed = urlparse(url)
        return parsed.netloc == self.domain or parsed.netloc == ''

    def normalize_url(self, url: str, base: str) -> str:
        """Normalize and resolve relative URLs."""
        if url.startswith('data:') or url.startswith('javascript:') or url.startswith('#'):
            return None
        return urljoin(base, url)

    def download_file(self, url: str) -> bytes | None:
        """Download a file from URL."""
        try:
            response = self.session.get(url, timeout=30, allow_redirects=True)
            response.raise_for_status()
            return response.content
        except Exception as e:
            print(f"  ⚠ Failed to download {url}: {e}")
            return None

    def save_file(self, filepath: Path, content: bytes) -> bool:
        """Save content to file."""
        try:
            filepath.parent.mkdir(parents=True, exist_ok=True)
            filepath.write_bytes(content)
            return True
        except Exception as e:
            print(f"  ⚠ Failed to save {filepath}: {e}")
            return False

    def extract_css_urls(self, css_content: str, css_url: str) -> list:
        """Extract URLs from CSS content (url(), @import)."""
        urls = []
        # Match url() patterns
        url_pattern = r'url\([\'"]?([^\'"\)]+)[\'"]?\)'
        for match in re.finditer(url_pattern, css_content):
            url = self.normalize_url(match.group(1), css_url)
            if url:
                urls.append(url)
        # Match @import patterns
        import_pattern = r'@import\s+[\'"]([^\'"]+)[\'"]'
        for match in re.finditer(import_pattern, css_content):
            url = self.normalize_url(match.group(1), css_url)
            if url:
                urls.append(url)
        return urls

    def rewrite_css_urls(self, css_content: str, css_url: str, css_filepath: Path) -> str:
        """Rewrite URLs in CSS to point to local files."""
        def replace_url(match):
            original_url = match.group(1)
            full_url = self.normalize_url(original_url, css_url)
            if not full_url or full_url in self.downloaded_assets:
                if full_url and full_url in self.downloaded_assets:
                    local_path = self.downloaded_assets[full_url]
                    try:
                        rel_path = os.path.relpath(local_path, css_filepath.parent)
                        return f'url("{rel_path}")'
                    except ValueError:
                        pass
            return match.group(0)
        
        return re.sub(r'url\([\'"]?([^\'"\)]+)[\'"]?\)', replace_url, css_content)

    def download_asset(self, url: str, asset_type: str = 'asset') -> Path | None:
        """Download and save an asset, return local path."""
        if url in self.downloaded_assets:
            return self.downloaded_assets[url]
        
        content = self.download_file(url)
        if not content:
            return None
        
        filepath = self.url_to_filepath(url)
        if self.save_file(filepath, content):
            self.downloaded_assets[url] = filepath
            print(f"  ✓ {asset_type}: {filepath.name}")
            return filepath
        return None

    def process_html(self, html: str, page_url: str, page_filepath: Path) -> str:
        """Process HTML: download assets and rewrite URLs."""
        soup = BeautifulSoup(html, 'html.parser')
        
        # Process CSS links
        for link in soup.find_all('link', rel='stylesheet'):
            href = link.get('href')
            if href:
                full_url = self.normalize_url(href, page_url)
                if full_url:
                    local_path = self.download_asset(full_url, 'CSS')
                    if local_path:
                        # Also process CSS content for nested URLs
                        css_content = local_path.read_text(errors='ignore')
                        css_urls = self.extract_css_urls(css_content, full_url)
                        for css_url in css_urls:
                            self.download_asset(css_url, 'CSS asset')
                        # Rewrite CSS URLs
                        rewritten_css = self.rewrite_css_urls(css_content, full_url, local_path)
                        local_path.write_text(rewritten_css, errors='ignore')
                        # Update HTML link
                        try:
                            rel_path = os.path.relpath(local_path, page_filepath.parent)
                            link['href'] = rel_path
                        except ValueError:
                            pass

        # Process inline styles
        for style in soup.find_all('style'):
            if style.string:
                css_urls = self.extract_css_urls(style.string, page_url)
                for css_url in css_urls:
                    self.download_asset(css_url, 'Inline CSS asset')

        # Process scripts
        for script in soup.find_all('script', src=True):
            src = script.get('src')
            if src:
                full_url = self.normalize_url(src, page_url)
                if full_url:
                    local_path = self.download_asset(full_url, 'JS')
                    if local_path:
                        try:
                            rel_path = os.path.relpath(local_path, page_filepath.parent)
                            script['src'] = rel_path
                        except ValueError:
                            pass

        # Process images
        for img in soup.find_all('img'):
            src = img.get('src')
            if src:
                full_url = self.normalize_url(src, page_url)
                if full_url:
                    local_path = self.download_asset(full_url, 'Image')
                    if local_path:
                        try:
                            rel_path = os.path.relpath(local_path, page_filepath.parent)
                            img['src'] = rel_path
                        except ValueError:
                            pass
            # Handle srcset
            srcset = img.get('srcset')
            if srcset:
                new_srcset = []
                for part in srcset.split(','):
                    part = part.strip()
                    if ' ' in part:
                        url_part, size = part.rsplit(' ', 1)
                    else:
                        url_part, size = part, ''
                    full_url = self.normalize_url(url_part, page_url)
                    if full_url:
                        local_path = self.download_asset(full_url, 'Image')
                        if local_path:
                            try:
                                rel_path = os.path.relpath(local_path, page_filepath.parent)
                                new_srcset.append(f"{rel_path} {size}".strip())
                            except ValueError:
                                new_srcset.append(part)
                        else:
                            new_srcset.append(part)
                if new_srcset:
                    img['srcset'] = ', '.join(new_srcset)

        # Process background images in style attributes
        for elem in soup.find_all(style=True):
            style = elem['style']
            urls = re.findall(r'url\([\'"]?([^\'"\)]+)[\'"]?\)', style)
            for url in urls:
                full_url = self.normalize_url(url, page_url)
                if full_url:
                    local_path = self.download_asset(full_url, 'BG Image')
                    if local_path:
                        try:
                            rel_path = os.path.relpath(local_path, page_filepath.parent)
                            style = style.replace(url, rel_path)
                        except ValueError:
                            pass
            elem['style'] = style

        # Process favicons and other link tags
        for link in soup.find_all('link'):
            href = link.get('href')
            rel = link.get('rel', [])
            if href and any(r in ['icon', 'shortcut', 'apple-touch-icon'] for r in rel):
                full_url = self.normalize_url(href, page_url)
                if full_url:
                    local_path = self.download_asset(full_url, 'Favicon')
                    if local_path:
                        try:
                            rel_path = os.path.relpath(local_path, page_filepath.parent)
                            link['href'] = rel_path
                        except ValueError:
                            pass

        # Process video/audio sources
        for source in soup.find_all('source'):
            src = source.get('src')
            if src:
                full_url = self.normalize_url(src, page_url)
                if full_url:
                    local_path = self.download_asset(full_url, 'Media')
                    if local_path:
                        try:
                            rel_path = os.path.relpath(local_path, page_filepath.parent)
                            source['src'] = rel_path
                        except ValueError:
                            pass

        # Rewrite internal links to local pages
        for a in soup.find_all('a', href=True):
            href = a['href']
            full_url = self.normalize_url(href, page_url)
            if full_url and self.is_same_domain(full_url):
                local_path = self.url_to_filepath(full_url, is_page=True)
                try:
                    rel_path = os.path.relpath(local_path, page_filepath.parent)
                    a['href'] = rel_path
                except ValueError:
                    pass

        return str(soup)

    def extract_links(self, html: str, page_url: str) -> list:
        """Extract internal links from HTML."""
        soup = BeautifulSoup(html, 'html.parser')
        links = []
        for a in soup.find_all('a', href=True):
            href = a['href']
            full_url = self.normalize_url(href, page_url)
            if full_url and self.is_same_domain(full_url):
                # Remove fragment
                full_url = full_url.split('#')[0]
                if full_url and full_url not in self.visited_urls:
                    links.append(full_url)
        return list(set(links))

    def crawl_page(self, url: str, depth: int = 0) -> list:
        """Crawl a single page and return discovered links."""
        if url in self.visited_urls:
            return []
        if self.pages_downloaded >= self.max_pages:
            return []
        if depth > self.max_depth:
            return []
        
        self.visited_urls.add(url)
        
        print(f"\n📄 Page [{depth}]: {url}")
        content = self.download_file(url)
        if not content:
            return []
        
        try:
            html = content.decode('utf-8', errors='ignore')
        except:
            html = content.decode('latin-1', errors='ignore')
        
        filepath = self.url_to_filepath(url, is_page=True)
        
        # Extract links before processing (to get original hrefs)
        links = self.extract_links(html, url) if depth < self.max_depth else []
        
        # Process and save HTML
        processed_html = self.process_html(html, url, filepath)
        self.save_file(filepath, processed_html.encode('utf-8'))
        self.pages_downloaded += 1
        
        return links

    def replicate(self):
        """Main replication method."""
        print(f"\n{'='*60}")
        print(f"🌐 Website Replicator")
        print(f"{'='*60}")
        print(f"URL: {self.base_url}")
        print(f"Output: {self.output_dir}")
        print(f"Max depth: {self.max_depth}")
        print(f"Max pages: {self.max_pages}")
        print(f"{'='*60}")
        
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # BFS crawling
        to_crawl = [(self.base_url, 0)]
        
        while to_crawl and self.pages_downloaded < self.max_pages:
            url, depth = to_crawl.pop(0)
            new_links = self.crawl_page(url, depth)
            for link in new_links:
                if link not in self.visited_urls:
                    to_crawl.append((link, depth + 1))
        
        # Generate summary
        print(f"\n{'='*60}")
        print(f"✅ Replication Complete!")
        print(f"{'='*60}")
        print(f"Pages downloaded: {self.pages_downloaded}")
        print(f"Assets downloaded: {len(self.downloaded_assets)}")
        print(f"Output directory: {self.output_dir}")
        print(f"\nTo view the replicated site, open:")
        print(f"  {self.output_dir / 'index.html'}")
        
        # Create a manifest file
        manifest_path = self.output_dir / '_manifest.txt'
        with open(manifest_path, 'w') as f:
            f.write(f"Website Replication Manifest\n")
            f.write(f"{'='*60}\n")
            f.write(f"Source: {self.base_url}\n")
            f.write(f"Date: {__import__('datetime').datetime.now().isoformat()}\n")
            f.write(f"Pages: {self.pages_downloaded}\n")
            f.write(f"Assets: {len(self.downloaded_assets)}\n\n")
            f.write(f"Downloaded Pages:\n")
            for url in sorted(self.visited_urls):
                f.write(f"  - {url}\n")
            f.write(f"\nDownloaded Assets:\n")
            for url, path in sorted(self.downloaded_assets.items()):
                f.write(f"  - {path.name}: {url}\n")


def main():
    parser = argparse.ArgumentParser(
        description='Replicate a website locally for study purposes',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s https://example.com
  %(prog)s https://example.com -o ./my-clone
  %(prog)s https://example.com -d 3 -p 100
        """
    )
    parser.add_argument('url', help='URL of the website to replicate')
    parser.add_argument('-o', '--output', default='./replicated-site', 
                        help='Output directory (default: ./replicated-site)')
    parser.add_argument('-d', '--depth', type=int, default=2,
                        help='Maximum crawl depth (default: 2)')
    parser.add_argument('-p', '--pages', type=int, default=50,
                        help='Maximum number of pages to download (default: 50)')
    
    args = parser.parse_args()
    
    # Validate URL
    if not args.url.startswith(('http://', 'https://')):
        args.url = 'https://' + args.url
    
    replicator = WebsiteReplicator(
        url=args.url,
        output_dir=args.output,
        max_depth=args.depth,
        max_pages=args.pages
    )
    replicator.replicate()


if __name__ == '__main__':
    main()
