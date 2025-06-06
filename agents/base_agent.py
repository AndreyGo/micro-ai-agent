import os
import json
import requests
from abc import ABC, abstractmethod
from datetime import datetime

try:
    import openai
except ImportError:  # If openai isn't installed, agents that use it will fail at runtime
    openai = None


class BaseAgent(ABC):
    """Base class for all agents."""

    def __init__(self, config: dict, dispatcher):
        self.config = config or {}
        self.dispatcher = dispatcher

    @abstractmethod
    def process(self, input_data: dict):
        """Process input data and return result."""
        pass

    def log(self, message: str, level: str = "INFO"):
        """Log a message via dispatcher."""
        if self.dispatcher:
            self.dispatcher.log(level, self.__class__.__name__, message)

    def openai_request(self, prompt: str, **kwargs) -> str:
        """Send a prompt to OpenAI and return the response text."""
        if openai is None:
            raise RuntimeError("openai package is not installed")

        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise RuntimeError("OPENAI_API_KEY environment variable is not set")
        openai.api_key = api_key

        params = {
            "model": self.config.get("model", "gpt-3.5-turbo"),
            "temperature": self.config.get("temperature", 0.2),
            "max_tokens": self.config.get("max_tokens", 500),
        }
        params.update(kwargs)
        messages = [{"role": "user", "content": prompt}]
        self.log(f"Calling OpenAI with model {params['model']}")
        resp = openai.ChatCompletion.create(messages=messages, **params)
        content = resp.choices[0].message.content.strip()
        self.log("Received response from OpenAI")
        return content

    def http_request(self, url: str, method: str = "GET", **kwargs) -> requests.Response:
        """Perform an HTTP request."""
        self.log(f"HTTP {method} request to {url}")
        if method.upper() == "GET":
            resp = requests.get(url, **kwargs)
        else:
            resp = requests.post(url, **kwargs)
        resp.raise_for_status()
        return resp
