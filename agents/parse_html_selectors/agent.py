from ..base_agent import BaseAgent


PROMPT_TEMPLATE = (
    "Given the following HTML snippet, return the CSS selector that matches the "
    "element described in the instruction.\n"
    "Instruction: {instruction}\n"
    "HTML:\n{html}\n"
    "Selector:" 
)


class Agent(BaseAgent):
    """Return CSS selector for a given instruction and HTML."""

    def process(self, input_data: dict):
        html = input_data.get("html")
        instruction = input_data.get("instruction")
        if not html or not instruction:
            raise ValueError("'html' and 'instruction' fields are required")
        prompt = PROMPT_TEMPLATE.format(instruction=instruction, html=html)
        selector = self.openai_request(prompt)
        return selector
