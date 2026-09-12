"""URL validation utility with regex and DNS checks."""
import re
import socket
from urllib.parse import urlparse

URL_PATTERN = re.compile(
    r'^https?://'  # http:// or https://
    r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+'  # domain...
    r'(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # host
    r'localhost|'  # localhost
    r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # or IP
    r'(?::\d+)?'  # optional port
    r'(?:/?|[/?]\S+)$', re.IGNORECASE)

def validate_url_format(url):
    return bool(URL_PATTERN.match(url))

def validate_url_dns(url):
    try:
        parsed = urlparse(url)
        socket.getaddrinfo(parsed.hostname, parsed.port or 80)
        return True
    except (socket.gaierror, OSError):
        return False

def validate_url(url, check_dns=False):
    if not validate_url_format(url):
        return False, 'Invalid URL format'
    if check_dns and not validate_url_dns(url):
        return False, 'DNS resolution failed'
    return True, 'Valid URL'

if __name__ == '__main__':
    test_urls = [
        'https://github.com',
        'http://localhost:8000',
        'not-a-url',
        'https://example.com/path?q=1'
    ]
    for url in test_urls:
        valid, msg = validate_url(url)
        print(f'{url}: {msg}')
