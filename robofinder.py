import sys
import argparse
import urllib.request
import urllib.parse
from urllib.error import URLError, HTTPError


def normalize_url(url):
    url = url.strip()

    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    parsed = urllib.parse.urlparse(url)

    if not parsed.netloc:
        raise ValueError("Invalid URL")

    return f"{parsed.scheme}://{parsed.netloc}"


def fetch_robots_txt(base_url):
    # Create "robots.txt" path
    parsed = urllib.parse.urlparse(base_url)
    robots_url = f"{parsed.scheme}://{parsed.netloc}/robots.txt"
    
    try:
        request = urllib.request.Request(
            robots_url,
            headers={"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:147.0) Gecko/20100101 Firefox/147.0"}
        )

        with urllib.request.urlopen(request, timeout=10) as response:
            return response.read().decode("utf-8", errors="replace")
    except (HTTPError, URLError) as e:
        raise RuntimeError(f"Failed to fetch robots.txt: {e}") from e

def parse_disallow_paths(robots_content):
    disallow_paths = []
    for line in robots_content.splitlines():
        line = line.strip()
        # Ignore empty lines and comments
        if not line or line.startswith('#'):
            continue
        
        # Extract Disallow paths
        if line.lower().startswith('disallow:') or line.lower().startswith('disallow :'):
            path = line.split(':', 1)[1].strip()
            if path:
                if not path.startswith('/'):
                    path = '/' + path
                disallow_paths.append(path)
    return disallow_paths

def build_full_urls(base_url, paths):
    
    full_urls = []
    for path in paths:
        full_url = urllib.parse.urljoin(base_url, path)
        full_urls.append(full_url)
    return full_urls

def main():
    parser = argparse.ArgumentParser(
        description="Robots.txt Disallow Scanner",
        usage="%(prog)s -d DOMAIN [options]"
        )
    parser.add_argument(
        "-d", "--domain",
        required=True,
        help="Enter the Domain Name (e.g., example.com or https://example.com)"
        )
    parser.add_argument(
        "-s", "--silent",
        action="store_true",
        help="Run scanner silently (no console output except errors)"
        )
    parser.add_argument(
        "-o", "--output",
        metavar="OUTPUT",
        help="Write results to specified file"
        )
    
    args = parser.parse_args()
    
    try:
        target_url = normalize_url(args.domain) # Validate URL
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    
    if not args.silent:
        print(f"[*] Fetch Robots txt {target_url} ...")
    try:
        robots_content = fetch_robots_txt(target_url)
    except RuntimeError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    
    #  Disallow
    if not args.silent:
        print("[*] Disallow Path ...")
    disallow_paths = parse_disallow_paths(robots_content)
    
    if not disallow_paths:
        if not args.silent:
            print("[!] Not Found Disallow URLs")
        return
    
    # Build full URLs
    if not args.silent:
        print("[*] Build Full URLs ...")
    full_urls = build_full_urls(target_url, disallow_paths)
    
    # Export as txt file
    if args.output:
        try:
            with open(args.output, 'w', encoding='utf-8') as f:
                for url in full_urls:
                    f.write(url + '\n')
            if not args.silent:
                print(f"[*] Results written to {args.output}")
        except IOError as e:
            print(f"Error writing to file: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        if not args.silent:
            print("\n--- Disallow URLs ---")
            for url in full_urls:
                print(url)

if __name__ == "__main__":
    main()