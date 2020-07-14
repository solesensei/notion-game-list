import requests


def is_valid_link(url):
    try:
        r = requests.get(url, timeout=3)
    except requests.Timeout:
        return False
    return r.ok
