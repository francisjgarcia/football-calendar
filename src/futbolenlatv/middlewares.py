import random


class CustomUserAgentMiddleware:
    # User-Agent list for different devices and browsers
    USER_AGENTS = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/91.0.4472.124 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/605.1.15 (KHTML, like Gecko) "
        "Version/14.1.1 Safari/605.1.15",
        "Mozilla/5.0 (Linux; Android 11; Pixel 5) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/91.0.4472.77 Mobile Safari/537.36",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) "
        "AppleWebKit/605.1.15 (KHTML, like Gecko) "
        "Version/14.6 Mobile/15E148 Safari/604.1",
    ]

    def process_request(self, request, spider):
        # Set a random User-Agent for each request
        user_agent = random.choice(self.USER_AGENTS)
        request.headers['User-Agent'] = user_agent


class HandleHTTPErrorMiddleware:
    def process_response(self, request, response, spider):
        # Handle HTTP errors (404, 500, etc.)
        if response.status == 404:
            spider.logger.warning(f"Page not found: {response.url}")
            return None  # If there is an error, return None
        return response  # If not, return the response
