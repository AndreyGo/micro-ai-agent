import bs4
from ..base_agent import BaseAgent


class Agent(BaseAgent):
    """Fetch HTML content by CSS selector from a URL."""

    def process(self, input_data: dict):
        url = input_data.get("url")
        selector = input_data.get("selector")
        if not url or not selector:
            raise ValueError("'url' and 'selector' fields are required")
        response = self.http_request(url)
        soup = bs4.BeautifulSoup(response.text, "html.parser")
        elements = soup.select(selector)
        if not elements:
            return ""
        return "\n".join(str(el) for el in elements)
