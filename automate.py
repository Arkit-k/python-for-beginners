import requests
from urllib.parse import urljoin, urlparse, urlunparse
from bs4 import BeautifulSoup
import concurrent.futures
import openai
import os
import re
from collections import defaultdict
import argparse
import hashlib
import json
from pathlib import Path
from typing import List, Dict, Tuple, Optional
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class AILinkRepairAgent:
    def __init__(self, base_url: str, openai_api_key: str = None, max_workers: int = 10, 
                 timeout: int = 10, user_agent: str = None, cache_dir: str = ".ailinkcache"):
        """
        AI-powered dead link detection and repair agent
        
        Args:
            base_url: Root URL of the website to analyze
            openai_api_key: OpenAI API key for AI suggestions
            max_workers: Maximum concurrent workers
            timeout: Request timeout in seconds
            user_agent: Custom User-Agent string
            cache_dir: Directory to cache results
        """
        self.base_url = base_url.rstrip('/')
        self.domain = urlparse(base_url).netloc
        self.scheme = urlparse(base_url).scheme
        self.openai_api_key = openai_api_key or os.getenv('OPENAI_API_KEY')
        self.max_workers = max_workers
        self.timeout = timeout
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)
        
        # Initialize data structures
        self.visited_urls = set()
        self.broken_links = defaultdict(list)
        self.redirect_map = {}
        self.url_content_cache = {}
        self.url_structure = defaultdict(set)
        self.link_contexts = defaultdict(dict)
        
        # Configure session
        self.session = requests.Session()
        self.headers = {
            'User-Agent': user_agent or 'AILinkRepairAgent/1.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
        }
        
        # AI configuration
        self.ai_enabled = bool(self.openai_api_key)
        self.ai_model = "gpt-4-turbo"
        self.ai_temperature = 0.3
        
        logger.info(f"Initialized AI Link Repair Agent for {self.base_url}")

    def _get_cache_key(self, url: str) -> str:
        """Generate a cache key for a URL"""
        return hashlib.md5(url.encode('utf-8')).hexdigest()

    def _load_from_cache(self, key: str):
        """Load data from cache"""
        cache_file = self.cache_dir / f"{key}.json"
        if cache_file.exists():
            with open(cache_file, 'r') as f:
                return json.load(f)
        return None

    def _save_to_cache(self, key: str, data):
        """Save data to cache"""
        cache_file = self.cache_dir / f"{key}.json"
        with open(cache_file, 'w') as f:
            json.dump(data, f)

    def is_valid_url(self, url: str) -> bool:
        """Check if URL is valid"""
        parsed = urlparse(url)
        return bool(parsed.netloc) and bool(parsed.scheme)

    def is_same_domain(self, url: str) -> bool:
        """Check if URL belongs to the same domain"""
        return urlparse(url).netloc == self.domain

    def normalize_url(self, url: str) -> str:
        """Normalize URL by removing fragments and queries"""
        parsed = urlparse(url)
        return urlunparse(parsed._replace(fragment='', query='')).rstrip('/')

    def get_absolute_url(self, url: str) -> str:
        """Convert relative URL to absolute"""
        return urljoin(self.base_url + '/', url)

    def check_url(self, url: str) -> Tuple[str, int, Optional[str], Optional[str]]:
        """
        Check a URL's status with caching
        
        Returns:
            Tuple of (url, status_code, final_url, error_message)
        """
        cache_key = self._get_cache_key(f"check_{url}")
        cached = self._load_from_cache(cache_key)
        if cached:
            return tuple(cached)
        
        try:
            # Try HEAD first for efficiency
            response = self.session.head(
                url, 
                headers=self.headers, 
                timeout=self.timeout, 
                allow_redirects=True
            )
            
            # Fall back to GET if HEAD not allowed
            if response.status_code == 405:
                response = self.session.get(
                    url,
                    headers=self.headers,
                    timeout=self.timeout,
                    allow_redirects=True,
                    stream=True
                )
            
            final_url = response.url
            status = response.status_code
            
            result = (url, status, final_url, None)
            self._save_to_cache(cache_key, result)
            return result
            
        except requests.RequestException as e:
            result = (url, 'Error', None, str(e))
            self._save_to_cache(cache_key, result)
            return result

    def fetch_page_content(self, url: str) -> Optional[str]:
        """Fetch and cache page content"""
        cache_key = self._get_cache_key(f"content_{url}")
        cached = self._load_from_cache(cache_key)
        if cached:
            return cached
        
        try:
            response = self.session.get(
                url,
                headers=self.headers,
                timeout=self.timeout,
                allow_redirects=True
            )
            
            if response.status_code == 200:
                content = response.text
                self._save_to_cache(cache_key, content)
                return content
            return None
            
        except requests.RequestException:
            return None

    def analyze_page_structure(self, url: str, content: str):
        """Analyze page structure and extract semantic information"""
        soup = BeautifulSoup(content, 'html.parser')
        
        # Extract headings hierarchy
        headings = [tag.text.strip() for tag in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])]
        
        # Extract main content sections
        sections = {}
        for section in soup.find_all(['article', 'section', 'main', 'div']):
            if 'id' in section.attrs:
                sections[section['id']] = section.text.strip()[:200] + "..."  # Store preview
        
        # Store in structure cache
        self.url_structure[url] = {
            'headings': headings,
            'sections': sections,
            'title': soup.title.text if soup.title else None
        }

    def find_links(self, url: str) -> set:
        """Find all links on a page with context"""
        content = self.fetch_page_content(url)
        if not content:
            return set()
            
        self.analyze_page_structure(url, content)
        soup = BeautifulSoup(content, 'html.parser')
        links = set()
        
        for tag in soup.find_all(['a', 'img', 'link', 'script', 'iframe', 'source']):
            href = tag.get('href') or tag.get('src') or tag.get('data-src')
            if href:
                # Skip special URLs
                if href.startswith(('mailto:', 'tel:', 'javascript:', '#', 'data:')):
                    continue
                
                absolute_url = self.get_absolute_url(href)
                normalized_url = self.normalize_url(absolute_url)
                
                if self.is_valid_url(normalized_url):
                    links.add(normalized_url)
                    # Store link context for AI analysis
                    self.link_contexts[normalized_url][url] = {
                        'anchor_text': tag.text.strip() if hasattr(tag, 'text') else None,
                        'tag_name': tag.name,
                        'surrounding_text': ' '.join(tag.find_parent().get_text().strip().split()[:20]),
                        'position': len(self.link_contexts[normalized_url])  # Order on page
                    }
        
        return links

    def crawl_site(self, start_url: str = None):
        """Crawl the website and analyze links"""
        start_url = start_url or self.base_url
        queue = {self.normalize_url(start_url)}
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            while queue:
                current_url = queue.pop()
                
                if current_url in self.visited_urls:
                    continue
                    
                self.visited_urls.add(current_url)
                
                if not self.is_same_domain(current_url):
                    continue
                
                logger.info(f"Crawling: {current_url}")
                
                # Find all links on the page
                page_links = self.find_links(current_url)
                new_links = page_links - set(self.link_contexts.keys())
                
                # Add new links to queue
                queue.update(new_links)
                
                # Check all links on the page
                futures = []
                for link in page_links:
                    futures.append(executor.submit(self.check_url, link))
                
                for future in concurrent.futures.as_completed(futures):
                    url, status, final_url, error = future.result()
                    if status == 404 or isinstance(status, str):
                        self.broken_links[url].append({
                            'referrer': current_url,
                            'status': status,
                            'final_url': final_url,
                            'error': error
                        })

    def get_ai_suggestion(self, broken_url: str, context: dict) -> Optional[dict]:
        """Get AI-powered suggestion for fixing a broken link"""
        if not self.ai_enabled:
            return None
            
        cache_key = self._get_cache_key(f"ai_suggestion_{broken_url}")
        cached = self._load_from_cache(cache_key)
        if cached:
            return cached
            
        try:
            # Prepare context information
            referring_pages = []
            for ref_url, ctx in context['occurrences'].items():
                content = self.fetch_page_content(ref_url)
                soup = BeautifulSoup(content, 'html.parser') if content else None
                referring_pages.append({
                    'url': ref_url,
                    'title': soup.title.text if soup and soup.title else None,
                    'context': ctx
                })
            
            # Prepare prompt
            prompt = f"""
            Website Link Repair Analysis Request:
            
            Broken URL: {broken_url}
            Domain: {self.domain}
            
            Link Context:
            {json.dumps(referring_pages, indent=2)}
            
            Website Structure Knowledge:
            {json.dumps(self.url_structure, indent=2)}
            
            Please analyze this broken link and provide:
            1. The most likely cause of the 404 error
            2. Three possible correct URLs this might have been pointing to
            3. Recommended fix approach
            4. Confidence level (0-100) in your suggestions
            
            Respond in JSON format with these keys:
            - "likely_cause"
            - "possible_correct_urls"
            - "recommended_fix"
            - "confidence"
            """
            
            response = openai.ChatCompletion.create(
                model=self.ai_model,
                messages=[
                    {"role": "system", "content": "You are an expert web developer and SEO specialist."},
                    {"role": "user", "content": prompt}
                ],
                temperature=self.ai_temperature,
                max_tokens=1000
            )
            
            try:
                suggestion = json.loads(response.choices[0].message.content)
                self._save_to_cache(cache_key, suggestion)
                return suggestion
            except json.JSONDecodeError:
                logger.warning("Failed to parse AI response")
                return None
                
        except Exception as e:
            logger.error(f"AI suggestion failed: {str(e)}")
            return None

    def suggest_fixes(self):
        """Generate intelligent fixes for broken links"""
        logger.info("Generating fixes for broken links...")
        
        # First pass: Standard technical fixes
        for broken_url, occurrences in self.broken_links.items():
            context = {
                'occurrences': {occ['referrer']: self.link_contexts[broken_url].get(occ['referrer'], {}) 
                for occ in occurrences
            }
            
            # Check if this is a redirected URL
            if broken_url in self.redirect_map:
                target = self.redirect_map[broken_url]
                if target not in self.broken_links:
                    yield {
                        'broken_url': broken_url,
                        'type': 'redirect_chain',
                        'suggestion': f"Update to point directly to: {target}",
                        'confidence': 90,
                        'source': 'automatic'
                    }
            else:
                    # Handle cases where the target is in broken_links
                    logger.warning(f"Target {target} is also a broken link.")
            else:
                # Add an appropriate else block or handle the case where the condition is not met
                logger.info(f"No redirect mapping found for {broken_url}.")
            
            # Try common technical fixes
            parsed = urlparse(broken_url)
            path_parts = parsed.path.split('/')
            filename = path_parts[-1] if path_parts else ''
            
            # Case sensitivity fixes
            lowercase_path = parsed.path.lower()
            if lowercase_path != parsed.path:
                test_url = urlunparse(parsed._replace(path=lowercase_path))
                if self.check_url(test_url)[1] == 200:
                    yield {
                        'broken_url': broken_url,
                        'type': 'case_sensitivity',
                        'suggestion': f"Update case to: {test_url}",
                        'confidence': 85,
                        'source': 'automatic'
                    }
                    continue
            
            # Missing extension fixes
            common_extensions = ['.html', '.htm', '.php', '.aspx', '']
            for ext in common_extensions:
                if not filename.endswith(ext):
                    test_url = urlunparse(parsed._replace(path=parsed.path + ext))
                    if self.check_url(test_url)[1] == 200:
                        yield {
                            'broken_url': broken_url,
                            'type': 'missing_extension',
                            'suggestion': f"Add extension: {test_url}",
                            'confidence': 80,
                            'source': 'automatic'
                        }
                        break
            
            # AI-powered suggestions
            if self.ai_enabled:
                ai_suggestion = self.get_ai_suggestion(broken_url, context)
                if ai_suggestion and ai_suggestion.get('confidence', 0) > 70:
                    yield {
                        'broken_url': broken_url,
                        'type': 'ai_suggestion',
                        'suggestion': ai_suggestion['recommended_fix'],
                        'confidence': ai_suggestion['confidence'],
                        'possible_correct_urls': ai_suggestion.get('possible_correct_urls', []),
                        'source': 'ai'
                    }

    def generate_report(self, output_file: str = 'link_repair_report.html'):
        """Generate an interactive HTML report"""
        logger.info(f"Generating report: {output_file}")
        
        fixes = list(self.suggest_fixes())
        
        # Prepare report data
        report_data = {
            'base_url': self.base_url,
            'stats': {
                'total_pages': len(self.visited_urls),
                'total_links': len(self.link_contexts),
                'broken_links': len(self.broken_links),
                'auto_fixes': len([f for f in fixes if f['source'] == 'automatic']),
                'ai_fixes': len([f for f in fixes if f['source'] == 'ai'])
            },
            'broken_links': self.broken_links,
            'fixes': fixes,
            'redirect_map': self.redirect_map
        }
        
        # Generate HTML report
        html_template = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Link Repair Report for {self.base_url}</title>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; margin: 0; padding: 20px; }}
                h1, h2 {{ color: #2c3e50; }}
                .summary {{ background: #f8f9fa; padding: 15px; border-radius: 5px; }}
                .fix-card {{ border: 1px solid #ddd; padding: 15px; margin-bottom: 15px; border-radius: 5px; }}
                .automatic {{ border-left: 4px solid #2ecc71; }}
                .ai {{ border-left: 4px solid #3498db; }}
                .confidence {{ display: inline-block; padding: 2px 5px; background: #eee; border-radius: 3px; }}
                .high-confidence {{ background: #d4edda; }}
                .medium-confidence {{ background: #fff3cd; }}
                table {{ width: 100%; border-collapse: collapse; }}
                th, td {{ padding: 8px; text-align: left; border-bottom: 1px solid #ddd; }}
                tr:hover {{ background-color: #f5f5f5; }}
            </style>
        </head>
        <body>
            <h1>Link Repair Report for {self.base_url}</h1>
            
            <div class="summary">
                <h2>Summary</h2>
                <ul>
                    <li>Pages crawled: {report_data['stats']['total_pages']}</li>
                    <li>Total links found: {report_data['stats']['total_links']}</li>
                    <li>Broken links found: {report_data['stats']['broken_links']}</li>
                    <li>Automatic fixes suggested: {report_data['stats']['auto_fixes']}</li>
                    <li>AI-powered fixes suggested: {report_data['stats']['ai_fixes']}</li>
                </ul>
            </div>
            
            <h2>Suggested Fixes</h2>
            {"".join([
                f"""
                <div class="fix-card {'automatic' if fix['source'] == 'automatic' else 'ai'}">
                    <h3>{fix['broken_url']}</h3>
                    <p><strong>Type:</strong> {fix['type'].replace('_', ' ').title()}</p>
                    <p><strong>Suggestion:</strong> {fix['suggestion']}</p>
                    <p><strong>Confidence:</strong> <span class="confidence {'high-confidence' if fix['confidence'] > 80 else 'medium-confidence'}">{fix['confidence']}%</span></p>
                    {'' if not fix.get('possible_correct_urls') else f"<p><strong>Possible URLs:</strong><br>" + "<br>".join(fix['possible_correct_urls']) + "</p>"}
                    <p><strong>Found on pages:</strong></p>
                    <ul>
                        {"".join([f"<li><a href='{occ['referrer']}' target='_blank'>{occ['referrer']}</a></li>" for occ in report_data['broken_links'][fix['broken_url']])}
                    </ul>
                </div>
                """ for fix in report_data['fixes']
            ])}
            
            <h2>All Broken Links</h2>
            <table>
                <tr>
                    <th>Broken URL</th>
                    <th>Referrer</th>
                    <th>Status</th>
                </tr>
                {"".join([
                    f"""
                    <tr>
                        <td><a href="{url}" target="_blank">{url}</a></td>
                        <td><a href="{occ['referrer']}" target="_blank">{occ['referrer']}</a></td>
                        <td>{occ['status']}</td>
                    </tr>
                    """ for url, occurrences in report_data['broken_links'].items() for occ in occurrences
                ])}
            </table>
            
            <h2>Redirect Mapping</h2>
            <table>
                <tr>
                    <th>Original URL</th>
                    <th>Redirects To</th>
                </tr>
                {"".join([
                    f"<tr><td><a href='{src}' target='_blank'>{src}</a></td><td><a href='{dest}' target='_blank'>{dest}</a></td></tr>"
                    for src, dest in report_data['redirect_map'].items()
                ])}
            </table>
        </body>
        </html>
        """
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_template)
        
        logger.info(f"Report generated successfully: {output_file}")

def main():
    parser = argparse.ArgumentParser(description='AI-powered website link repair tool')
    parser.add_argument('url', help='Base URL of the website to scan')
    parser.add_argument('--openai-key', help='OpenAI API key (or set OPENAI_API_KEY environment variable)')
    parser.add_argument('--workers', type=int, default=10, help='Number of concurrent workers')
    parser.add_argument('--timeout', type=int, default=10, help='Request timeout in seconds')
    parser.add_argument('--output', default='link_repair_report.html', help='Output report file')
    parser.add_argument('--user-agent', help='Custom User-Agent string')
    
    args = parser.parse_args()
    
    logger.info(f"Starting AI Link Repair Agent for {args.url}")
    agent = AILinkRepairAgent(
        args.url,
        openai_api_key=args.openai_key,
        max_workers=args.workers,
        timeout=args.timeout,
        user_agent=args.user_agent
    )
    
    # Crawl the website
    agent.crawl_site()
    
    # Generate report
    agent.generate_report(args.output)
    
    logger.info("\nScan complete!")
    logger.info(f"Found {len(agent.broken_links)} broken links.")
    logger.info(f"Report generated: {args.output}")

if __name__ == '__main__':
    if __name__ == '__main__':
        main()