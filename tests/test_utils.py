from app.utils import generate_short_id, is_valid_url
import string

def test_generate_short_id():
    sh_id = generate_short_id()
    assert len(sh_id) == 5
    assert sh_id.isalnum()
    
def test_generate_short_id_uniqueness():
    ids = set(generate_short_id() for _ in range(100))
    assert len(ids) == 100

def test_is_valid_url():
    assert is_valid_url("https://www.example.com") is True
    assert is_valid_url("http://test.com/path?key=val") is True
    assert is_valid_url("not a url") is False
    assert is_valid_url("javascript:alert(1)") is False
