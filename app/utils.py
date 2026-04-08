import string
import random
import validators
from urllib.parse import urlparse

def generate_short_id() -> str:
    # 5 alpha-numeric characters, mixed capital and lowercase
    chars = string.ascii_letters + string.digits
    return ''.join(random.choices(chars, k=5))

def is_valid_url(url: str) -> bool:
    if not isinstance(url, str):
        return False
    # Validate the semantic URL
    if not validators.url(url):
        return False
    # Extra sanitization: enforce http or https
    parsed = urlparse(url)
    if parsed.scheme not in ('http', 'https'):
        return False
    return True
