#!/usr/bin/env python3
"""
Authenticated Website Replicator
================================
Clone websites that require login authentication.

Uses Playwright for browser automation to handle:
- Login forms with username/password
- Multi-factor authentication (manual intervention)
- SSO/OAuth flows
- JavaScript-rendered content

Then downloads all pages and assets while preserving authenticated session.

Usage:
    python3 authenticated_website_replicator.py <login_url> <target_url> [options]

Examples:
    # Basic login and replicate
    python3 authenticated_website_replicator.py https://example.com/login https://example.com/dashboard

    # With credentials
    python3 authenticated_website_replicator.py https://example.com/login https://example.com/dashboard \\
        --username myuser --password mypass

    # Interactive mode (for MFA or complex logins)
    python3 authenticated_website_replicator.py https://example.com/login https://example.com/dashboard \\
        --interactive

    # Custom selectors
    python3 authenticated_website_replicator.py https://example.com/login https://example.com/dashboard \\
        --username-selector "#email" --password-selector "#pass" --submit-selector "button[type=submit]"
"""

import os
import re
import sys
import json
import time
import hashlib
import argparse
from pathlib import Path
from urllib.parse import urljoin, urlparse, unquote
from typing import Optional, Dict, List, Set

# Install dependencies
def install_dependencies():
    """Install required packages."""
    import subprocess
    packages = [
        "requests",
        "beautifulsoup4", 
        "playwright"
    ]
    print("📦 Installing dependencies...")
    subprocess.check_call([
        sys.executable, "-m", "pip", "install", 
        *packages, "--break-system-packages", "-q"
    ])
    # Install Playwright browsers
    print("🌐 Installing Playwright browsers...")
    subprocess.check_call([sys.executable, "-m", "playwright", "install", "chromium"])

try:
    import requests
    from bs4 import BeautifulSoup
    from playwright.sync_api import sync_playwright, Page, Browser, BrowserContext
except ImportError:
    install_dependencies()
    import requests
    from bs4 import BeautifulSoup
    from playwright.sync_api import sync_playwright, Page, Browser, BrowserContext


class AuthenticatedWebsiteReplicator:
    """
    Replicates websites that require authentication.
    
    Workflow:
    1. Launch browser and navigate to login page
    2. Perform authentication (auto or manual)
    3. Capture session cookies
    4. Crawl and download authenticated pages
    5. Download all assets (CSS, JS, images, etc.)
    6. Rewrite URLs to local paths
    """
    
    def __init__(
        self,
        login_url: str,
        target_url: str,
        output_dir: str = "./replicated-site",
        max_depth: int = 2,
        max_pages: int = 50,
        username: Optional[str] = None,
        password: Optional[str] = None,
        username_selector: str = "input[type='email'], input[type='text'][name*='user'], input[name*='email'], #username, #email",
        password_selector: str = "input[type='password'], #password",
        submit_selector: str = "button[type='submit'], input[type='submit'], button:has-text('Sign in'), button:has-text('Log in')",
        interactive: bool = False,
        headless: bool = True,
        wait_after_login: int = 3,
        use_playwright_for_pages: bool = False
    ):
        self.login_url = login_url
        self.target_url = target_url.rstrip('/')
        self.parsed_target = urlparse(self.target_url)
        self.domain = self.parsed_target.netloc
        self.output_dir = Path(output_dir)
        self.max_depth = max_depth
        self.max_pages = max_pages
        
        # Auth settings
        self.username = username
        self.password = password
        self.username_selector = username_selector
        self.password_selector = password_selector
        self.submit_selector = submit_selector
        self.interactive = interactive
        self.headless = headless and not interactive
        self.wait_after_login = wait_after_login
        self.use_playwright_for_pages = use_playwright_for_pages
        
        # State tracking
        self.visited_urls: Set[str] = set()
        self.downloaded_assets: Dict[str, Path] = {}
        self.pages_downloaded = 0
        self.cookies: List[Dict] = []
        
        # Session for HTTP requests (faster than Playwright for assets)
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
        })
        
        # Playwright instances
        self.playwright = None
        self.browser: Optional[Browser] = None
        self.context: Optional[BrowserContext] = None
        self.page: Optional[Page] = None

    def start_browser(self):
        """Start Playwright browser."""
        print("\n🚀 Starting browser...")
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(
            headless=self.headless,
            args=['--disable-blink-features=AutomationControlled']
        )
        self.context = self.browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        )
        self.page = self.context.new_page()
        
    def stop_browser(self):
        """Stop Playwright browser."""
        if self.context:
            self.context.close()
        if self.browser:
            self.browser.close()
        if self.playwright:
            self.playwright.stop()

    def perform_login(self) -> bool:
        """
        Perform login using Playwright.
        
        Returns True if login appears successful.
        """
        print(f"\n🔐 Navigating to login page: {self.login_url}")
        self.page.goto(self.login_url, wait_until='networkidle')
        time.sleep(1)
        
        if self.interactive:
            return self._interactive_login()
        else:
            return self._automated_login()
    
    def _automated_login(self) -> bool:
        """Attempt automated login with provided credentials."""
        if not self.username or not self.password:
            print("⚠️  No credentials provided. Switching to interactive mode...")
            return self._interactive_login()
        
        print("🤖 Attempting automated login...")
        
        try:
            # Find and fill username
            username_field = self.page.locator(self.username_selector).first
            username_field.wait_for(state='visible', timeout=10000)
            username_field.fill(self.username)
            print(f"  ✓ Entered username")
            
            # Find and fill password
            password_field = self.page.locator(self.password_selector).first
            password_field.wait_for(state='visible', timeout=5000)
            password_field.fill(self.password)
            print(f"  ✓ Entered password")
            
            # Submit the form
            time.sleep(0.5)  # Brief pause before submit
            submit_button = self.page.locator(self.submit_selector).first
            submit_button.click()
            print(f"  ✓ Clicked submit")
            
            # Wait for navigation
            print(f"  ⏳ Waiting for login to complete...")
            self.page.wait_for_load_state('networkidle', timeout=30000)
            time.sleep(self.wait_after_login)
            
            # Check if we're still on login page (login might have failed)
            current_url = self.page.url
            if 'login' in current_url.lower() or 'signin' in current_url.lower():
                # Check for error messages
                error_selectors = [
                    ".error", ".alert-danger", ".error-message", 
                    "[role='alert']", ".invalid-feedback"
                ]
                for selector in error_selectors:
                    error = self.page.locator(selector).first
                    if error.is_visible():
                        error_text = error.text_content()
                        print(f"  ⚠️  Login error detected: {error_text}")
                        print("  Switching to interactive mode...")
                        return self._interactive_login()
            
            print("  ✅ Login appears successful!")
            return True
            
        except Exception as e:
            print(f"  ⚠️  Automated login failed: {e}")
            print("  Switching to interactive mode...")
            return self._interactive_login()
    
    def _interactive_login(self) -> bool:
        """Allow user to manually complete login."""
        print("\n" + "="*60)
        print("🖐️  INTERACTIVE LOGIN MODE")
        print("="*60)
        print("A browser window should be open (or will open shortly).")
        print("Please complete the login process manually, including:")
        print("  - Entering your credentials")
        print("  - Completing any MFA/2FA verification")
        print("  - Accepting any terms or prompts")
        print("\nOnce logged in and you see the authenticated page,")
        print("press ENTER here to continue...")
        print("="*60)
        
        # Make browser visible for interactive login
        if self.headless:
            print("\n⚠️  Restarting browser in visible mode...")
            self.stop_browser()
            self.headless = False
            self.start_browser()
            self.page.goto(self.login_url, wait_until='networkidle')
        
        input("\n>>> Press ENTER when login is complete...")
        
        # Give a moment for any final redirects
        time.sleep(2)
        self.page.wait_for_load_state('networkidle')
        
        print("\n✅ Continuing with authenticated session...")
        return True

    def capture_cookies(self):
        """Capture cookies from browser and transfer to requests session."""
        print("\n🍪 Capturing session cookies...")
        self.cookies = self.context.cookies()
        
        # Transfer cookies to requests session
        for cookie in self.cookies:
            self.session.cookies.set(
                cookie['name'],
                cookie['value'],
                domain=cookie.get('domain', ''),
                path=cookie.get('path', '/')
            )
        
        print(f"  ✓ Captured {len(self.cookies)} cookies")
        
        # Save cookies for potential reuse
        cookies_path = self.output_dir / '_cookies.json'
        self.output_dir.mkdir(parents=True, exist_ok=True)
        with open(cookies_path, 'w') as f:
            json.dump(self.cookies, f, indent=2)
        print(f"  ✓ Saved cookies to {cookies_path}")

    def url_to_filepath(self, url: str, is_page: bool = False) -> Path:
        """Convert URL to local file path."""
        parsed = urlparse(url)
        path = unquote(parsed.path) or '/index.html'
        
        if is_page and not path.endswith(('.html', '.htm', '.php', '.asp', '.aspx')):
            if path.endswith('/'):
                path += 'index.html'
            else:
                path += '/index.html'
        
        # Handle query strings
        if parsed.query:
            query_hash = hashlib.md5(parsed.query.encode()).hexdigest()[:8]
            base, ext = os.path.splitext(path)
            path = f"{base}_{query_hash}{ext}"
        
        path = path.lstrip('/')
        if not path:
            path = 'index.html'
            
        return self.output_dir / path

    def is_same_domain(self, url: str) -> bool:
        """Check if URL belongs to the same domain."""
        parsed = urlparse(url)
        return parsed.netloc == self.domain or parsed.netloc == ''

    def normalize_url(self, url: str, base: str) -> Optional[str]:
        """Normalize and resolve relative URLs."""
        if url.startswith('data:') or url.startswith('javascript:') or url.startswith('#'):
            return None
        return urljoin(base, url)

    def download_file(self, url: str) -> Optional[bytes]:
        """Download a file from URL using authenticated session."""
        try:
            response = self.session.get(url, timeout=30, allow_redirects=True)
            response.raise_for_status()
            return response.content
        except Exception as e:
            print(f"  ⚠️  Failed to download {url}: {e}")
            return None

    def download_with_playwright(self, url: str) -> Optional[str]:
        """Download page content using Playwright (for JS-rendered content)."""
        try:
            self.page.goto(url, wait_until='networkidle')
            time.sleep(1)  # Extra time for dynamic content
            return self.page.content()
        except Exception as e:
            print(f"  ⚠️  Playwright failed for {url}: {e}")
            return None

    def save_file(self, filepath: Path, content: bytes) -> bool:
        """Save content to file."""
        try:
            filepath.parent.mkdir(parents=True, exist_ok=True)
            filepath.write_bytes(content)
            return True
        except Exception as e:
            print(f"  ⚠️  Failed to save {filepath}: {e}")
            return False

    def extract_css_urls(self, css_content: str, css_url: str) -> List[str]:
        """Extract URLs from CSS content."""
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
            if full_url and full_url in self.downloaded_assets:
                local_path = self.downloaded_assets[full_url]
                try:
                    rel_path = os.path.relpath(local_path, css_filepath.parent)
                    return f'url("{rel_path}")'
                except ValueError:
                    pass
            return match.group(0)
        
        return re.sub(r'url\([\'"]?([^\'"\)]+)[\'"]?\)', replace_url, css_content)

    def download_asset(self, url: str, asset_type: str = 'asset') -> Optional[Path]:
        """Download and save an asset."""
        if url in self.downloaded_assets:
            return self.downloaded_assets[url]
        
        content = self.download_file(url)
        if not content:
            return None
        
        filepath = self.url_to_filepath(url)
        if self.save_file(filepath, content):
            self.downloaded_assets[url] = filepath
            print(f"    ✓ {asset_type}: {filepath.name}")
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
                        css_content = local_path.read_text(errors='ignore')
                        css_urls = self.extract_css_urls(css_content, full_url)
                        for css_url in css_urls:
                            self.download_asset(css_url, 'CSS asset')
                        rewritten_css = self.rewrite_css_urls(css_content, full_url, local_path)
                        local_path.write_text(rewritten_css, errors='ignore')
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
                        src_url, size = part.rsplit(' ', 1)
                    else:
                        src_url, size = part, ''
                    
                    full_url = self.normalize_url(src_url.strip(), page_url)
                    if full_url:
                        local_path = self.download_asset(full_url, 'Image (srcset)')
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

        # Process favicons and icons
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

        # Rewrite internal links
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

    def extract_links(self, html: str, page_url: str) -> List[str]:
        """Extract internal links from HTML."""
        soup = BeautifulSoup(html, 'html.parser')
        links = []
        for a in soup.find_all('a', href=True):
            href = a['href']
            full_url = self.normalize_url(href, page_url)
            if full_url and self.is_same_domain(full_url):
                full_url = full_url.split('#')[0]
                if full_url and full_url not in self.visited_urls:
                    links.append(full_url)
        return list(set(links))

    def crawl_page(self, url: str, depth: int = 0) -> List[str]:
        """Crawl a single page and return discovered links."""
        if url in self.visited_urls:
            return []
        if self.pages_downloaded >= self.max_pages:
            return []
        if depth > self.max_depth:
            return []
        
        self.visited_urls.add(url)
        
        print(f"\n📄 Page [{depth}]: {url}")
        
        # Get page content
        if self.use_playwright_for_pages:
            html = self.download_with_playwright(url)
            if not html:
                return []
        else:
            content = self.download_file(url)
            if not content:
                return []
            try:
                html = content.decode('utf-8', errors='ignore')
            except:
                html = content.decode('latin-1', errors='ignore')
        
        filepath = self.url_to_filepath(url, is_page=True)
        
        # Extract links before processing
        links = self.extract_links(html, url) if depth < self.max_depth else []
        
        # Process and save HTML
        processed_html = self.process_html(html, url, filepath)
        self.save_file(filepath, processed_html.encode('utf-8'))
        self.pages_downloaded += 1
        
        return links

    def replicate(self):
        """Main replication method."""
        print("\n" + "="*60)
        print("🔐 Authenticated Website Replicator")
        print("="*60)
        print(f"Login URL: {self.login_url}")
        print(f"Target URL: {self.target_url}")
        print(f"Output: {self.output_dir}")
        print(f"Max depth: {self.max_depth}")
        print(f"Max pages: {self.max_pages}")
        print(f"Mode: {'Interactive' if self.interactive else 'Automated'}")
        print("="*60)
        
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        try:
            # Start browser and login
            self.start_browser()
            
            if not self.perform_login():
                print("\n❌ Login failed. Aborting.")
                return
            
            # Capture session
            self.capture_cookies()
            
            # Navigate to target and start crawling
            print(f"\n🌐 Starting replication from: {self.target_url}")
            
            # BFS crawling
            to_crawl = [(self.target_url, 0)]
            
            while to_crawl and self.pages_downloaded < self.max_pages:
                url, depth = to_crawl.pop(0)
                new_links = self.crawl_page(url, depth)
                for link in new_links:
                    if link not in self.visited_urls:
                        to_crawl.append((link, depth + 1))
            
            # Generate summary
            self._generate_summary()
            
        finally:
            self.stop_browser()
    
    def _generate_summary(self):
        """Generate completion summary and manifest."""
        print(f"\n{'='*60}")
        print(f"✅ Replication Complete!")
        print(f"{'='*60}")
        print(f"Pages downloaded: {self.pages_downloaded}")
        print(f"Assets downloaded: {len(self.downloaded_assets)}")
        print(f"Output directory: {self.output_dir}")
        print(f"\nTo view the replicated site, open:")
        
        # Find the entry point
        entry_point = self.url_to_filepath(self.target_url, is_page=True)
        print(f"  {entry_point}")
        
        # Create manifest
        manifest_path = self.output_dir / '_manifest.txt'
        with open(manifest_path, 'w') as f:
            f.write("Authenticated Website Replication Manifest\n")
            f.write("="*60 + "\n")
            f.write(f"Login URL: {self.login_url}\n")
            f.write(f"Target URL: {self.target_url}\n")
            f.write(f"Date: {__import__('datetime').datetime.now().isoformat()}\n")
            f.write(f"Pages: {self.pages_downloaded}\n")
            f.write(f"Assets: {len(self.downloaded_assets)}\n\n")
            f.write("Downloaded Pages:\n")
            for url in sorted(self.visited_urls):
                f.write(f"  - {url}\n")
            f.write("\nDownloaded Assets:\n")
            for url, path in sorted(self.downloaded_assets.items()):
                f.write(f"  - {path.name}: {url}\n")


def main():
    parser = argparse.ArgumentParser(
        description='Replicate websites that require authentication',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Interactive login (recommended for first use)
  %(prog)s https://app.example.com/login https://app.example.com/dashboard --interactive
  
  # Automated login with credentials
  %(prog)s https://app.example.com/login https://app.example.com/dashboard \\
      --username user@email.com --password mypassword
  
  # Custom selectors for non-standard login forms
  %(prog)s https://app.example.com/login https://app.example.com/dashboard \\
      --username-selector "#login-email" --password-selector "#login-pass" \\
      --submit-selector "#login-btn"
  
  # For heavy JavaScript sites, use Playwright for all pages
  %(prog)s https://app.example.com/login https://app.example.com/dashboard \\
      --interactive --use-playwright
        """
    )
    
    parser.add_argument('login_url', help='URL of the login page')
    parser.add_argument('target_url', help='URL to start replicating from after login')
    
    parser.add_argument('-o', '--output', default='./replicated-site',
                        help='Output directory (default: ./replicated-site)')
    parser.add_argument('-d', '--depth', type=int, default=2,
                        help='Maximum crawl depth (default: 2)')
    parser.add_argument('-p', '--pages', type=int, default=50,
                        help='Maximum pages to download (default: 50)')
    
    # Authentication options
    auth_group = parser.add_argument_group('Authentication')
    auth_group.add_argument('-u', '--username', help='Username/email for login')
    auth_group.add_argument('--password', help='Password for login')
    auth_group.add_argument('-i', '--interactive', action='store_true',
                            help='Interactive mode - manually complete login in browser')
    
    # Selector options
    sel_group = parser.add_argument_group('Custom Selectors')
    sel_group.add_argument('--username-selector', 
                           default="input[type='email'], input[type='text'][name*='user'], input[name*='email'], #username, #email",
                           help='CSS selector for username field')
    sel_group.add_argument('--password-selector',
                           default="input[type='password'], #password",
                           help='CSS selector for password field')
    sel_group.add_argument('--submit-selector',
                           default="button[type='submit'], input[type='submit'], button:has-text('Sign in'), button:has-text('Log in')",
                           help='CSS selector for submit button')
    
    # Advanced options
    adv_group = parser.add_argument_group('Advanced')
    adv_group.add_argument('--wait', type=int, default=3,
                           help='Seconds to wait after login (default: 3)')
    adv_group.add_argument('--use-playwright', action='store_true',
                           help='Use Playwright for all page downloads (slower but handles JS)')
    adv_group.add_argument('--visible', action='store_true',
                           help='Show browser window during automated login')
    
    args = parser.parse_args()
    
    # Validate URLs
    for url_name, url in [('login_url', args.login_url), ('target_url', args.target_url)]:
        if not url.startswith(('http://', 'https://')):
            setattr(args, url_name, 'https://' + url)
    
    replicator = AuthenticatedWebsiteReplicator(
        login_url=args.login_url,
        target_url=args.target_url,
        output_dir=args.output,
        max_depth=args.depth,
        max_pages=args.pages,
        username=args.username,
        password=args.password,
        username_selector=args.username_selector,
        password_selector=args.password_selector,
        submit_selector=args.submit_selector,
        interactive=args.interactive,
        headless=not args.visible,
        wait_after_login=args.wait,
        use_playwright_for_pages=args.use_playwright
    )
    
    replicator.replicate()


if __name__ == '__main__':
    main()
