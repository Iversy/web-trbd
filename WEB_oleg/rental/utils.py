from django.urls import get_resolver, URLPattern, URLResolver

def get_all_urls():
    url_patterns = get_resolver().url_patterns
    urls = []

    def extract_urls(patterns):
        for pattern in patterns:
            if isinstance(pattern, URLPattern):
                if pattern.name:  # Check if the pattern has a name
                    urls.append(pattern.name)
            elif isinstance(pattern, URLResolver):
                extract_urls(pattern.url_patterns)

    extract_urls(url_patterns)
    print(urls)  # Debugging line to see collected URLs
    return urls