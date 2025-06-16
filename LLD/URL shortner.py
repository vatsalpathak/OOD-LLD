# Requirements:
# Implement a basic URL shortening service similar to bit.ly with the following features:

# Functional Requirements:
# shorten(long_url) -> short_url:
# Given a long URL, return a unique short URL.
# expand(short_url) -> long_url:
# Given a previously shortened URL, return the original long URL.
# Each short URL should be unique and deterministic (same long URL → same short URL).

# Constraints:
# Short URL can be a 6-character alphanumeric code.
# Avoid duplicate short codes.
# Support bidirectional mapping between short and long URLs.

# Optional Stretch Features (only if time permits or as an extension):
# Auto-increment or base62 encoded IDs.
# Collision handling if you allow custom short URLs.
# Validation of input URLs.
# Thread-safe access (with locks or concurrency controls).

import string

class Base62Encoder:
    characters = string.digits + string.ascii_letters  # 0-9 + a-z + A-Z
    base = len(characters)

    @classmethod
    def encode(cls, num):
        if num == 0:
            return cls.characters[0]
        result = []
        while num > 0:
            result.append(cls.characters[num % cls.base])
            num //= cls.base
        return ''.join(reversed(result))


class CodeGenerator:
    def __init__(self):
        self.counter = 1 

    def get_next_code(self,long_url):
        code = Base62Encoder.encode(long_url)
        self.counter += 1
        return code


class URLRepository:
    def __init__(self):
        self.short_to_long = {}
        self.long_to_short = {}

    def save(self, short_code, long_url):
        self.short_to_long[short_code] = long_url
        self.long_to_short[long_url] = short_code

    def get_long_url(self, short_code):
        return self.short_to_long.get(short_code)

    def get_short_code(self, long_url):
        return self.long_to_short.get(long_url)


class URLShortener:
    def __init__(self):
        self.generator = CodeGenerator()
        self.repo = URLRepository()
        self.domain = "http://short.ly/"

    def shorten_url(self, long_url):
        if self.repo.get_short_code(long_url):
            code = self.repo.get_short_code(long_url)
        else:
            code = self.generator.get_next_code(long_url)
            self.repo.save(code, long_url)
        return self.domain + code

    def expand_url(self, short_url):
        code = short_url.replace(self.domain, "")
        return self.repo.get_long_url(code)


if __name__ == "__main__":
    shortener = URLShortener()

    long1 = "https://www.example.com/page/123"
    long2 = "https://openai.com/research"

    short1 = shortener.shorten_url(long1)
    short2 = shortener.shorten_url(long2)
    short3 = shortener.shorten_url(long1)

    print(f"Short URL 1: {short1}")
    print(f"Short URL 2: {short2}")
    print(f"Short URL 3 (duplicate): {short3}")
    print(f"Expanded URL 1: {shortener.expand_url(short1)}")
    print(f"Expanded URL 2: {shortener.expand_url(short2)}")
