# Micro AI Agent Platform

This project provides a minimal framework for running small CLI agents that can be chained together via a dispatcher.  Agents live in the `agents/` directory, each in its own folder with a config and documentation.

## Usage

Install dependencies:

```bash
pip install -r requirements.txt
```

List available agents:

```bash
python dispatcher.py list
```

Run an agent with JSON input:

```bash
python dispatcher.py run get_html '{"url": "https://example.com", "selector": "title"}'
```

Show help for an agent:

```bash
python dispatcher.py help parse_html_selectors
```

Run a pipeline defined in YAML:

```bash
python dispatcher.py pipeline configs/pipelines/example.yaml
```

Generate combined documentation for all agents:

```bash
python dispatcher.py docgen docs/AGENTS.md
```

`OPENAI_API_KEY` must be set in the environment for agents that call the OpenAI API.
