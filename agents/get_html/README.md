# Get HTML Agent

Fetch HTML elements matching a CSS selector from a URL.

## Usage

```bash
python dispatcher.py run get_html '{"url": "https://example.com", "selector": "title"}'
```

## Parameters
- `url` (str): page URL.
- `selector` (str): CSS selector to extract.

## Output
Returns matched HTML elements separated by newlines.
