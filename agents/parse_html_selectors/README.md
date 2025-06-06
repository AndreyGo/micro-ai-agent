# Parse HTML Selectors Agent

Use OpenAI to determine a CSS selector based on an instruction and HTML snippet.

## Usage

```bash
python dispatcher.py run parse_html_selectors '{"html": "<div>...</div>", "instruction": "price"}'
```

## Parameters
- `html` (str): source HTML snippet.
- `instruction` (str): description of the desired element.

## Output
Returns the CSS selector proposed by the language model.
