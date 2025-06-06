import argparse
import importlib
import importlib.util
import json
from datetime import datetime
from pathlib import Path

import yaml


class Dispatcher:
    def __init__(self, project_dir: Path):
        self.project_dir = project_dir
        self.agents_dir = self.project_dir / "agents"
        self.agents = self.discover_agents()

    def log(self, level: str, actor: str, message: str):
        ts = datetime.utcnow().isoformat()
        print(f"{ts} | {level} | {actor} | {message}")

    def discover_agents(self):
        agents = {}
        if not self.agents_dir.is_dir():
            return agents
        for item in self.agents_dir.iterdir():
            if item.is_dir() and (item / "agent.py").is_file():
                agents[item.name] = item
        return agents

    def list_agents(self):
        for name in sorted(self.agents):
            print(name)

    def load_agent(self, name: str):
        path = self.agents.get(name)
        if not path:
            raise ValueError(f"Agent '{name}' not found")
        module = importlib.import_module(f"agents.{name}.agent")
        agent_cls = getattr(module, "Agent")
        config_path = path / "config.yaml"
        config = {}
        if config_path.is_file():
            with open(config_path, "r", encoding="utf-8") as f:
                config = yaml.safe_load(f)
        return agent_cls(config, self)

    def run_agent(self, name: str, input_data: dict):
        agent = self.load_agent(name)
        self.log("INFO", name, "starting agent")
        result = None
        try:
            result = agent.process(input_data)
            if result is not None:
                print(result)
        except Exception as e:
            self.log("ERROR", name, str(e))
        finally:
            self.log("INFO", name, "finished")
        return result

    def help_agent(self, name: str):
        path = self.agents.get(name)
        if not path:
            raise ValueError(f"Agent '{name}' not found")
        readme = path / "README.md"
        if readme.is_file():
            print(readme.read_text())
        else:
            print(f"No documentation for {name}")

    def generate_docs(self, out_path: Path):
        with open(out_path, "w", encoding="utf-8") as outf:
            for name in sorted(self.agents):
                path = self.agents[name]
                readme = path / "README.md"
                if readme.is_file():
                    outf.write(f"# {name}\n\n")
                    outf.write(readme.read_text())
                    outf.write("\n\n")

    def run_pipeline(self, pipeline_file: Path):
        with open(pipeline_file, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
        steps = data.get("steps", [])
        prev_output = None
        for step in steps:
            name = step["agent"]
            input_data = step.get("input", {})
            for k, v in list(input_data.items()):
                if isinstance(v, str) and v == "$prev":
                    input_data[k] = prev_output
            prev_output = self.run_agent(name, input_data)


def main():
    parser = argparse.ArgumentParser(description="Agent dispatcher")
    parser.add_argument("--project", default=".")
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("list", help="List available agents")

    run_parser = subparsers.add_parser("run", help="Run an agent")
    run_parser.add_argument("name", help="Agent name")
    run_parser.add_argument("input", help="JSON string with input data")

    help_parser = subparsers.add_parser("help", help="Show agent help")
    help_parser.add_argument("name", help="Agent name")

    pipeline_parser = subparsers.add_parser("pipeline", help="Run a pipeline")
    pipeline_parser.add_argument("file", help="Path to pipeline YAML")

    docgen_parser = subparsers.add_parser("docgen", help="Generate AGENTS.md")
    docgen_parser.add_argument("file", help="Output markdown file")

    args = parser.parse_args()
    dispatcher = Dispatcher(Path(args.project))

    if args.command == "list":
        dispatcher.list_agents()
    elif args.command == "run":
        input_data = json.loads(args.input)
        dispatcher.run_agent(args.name, input_data)
    elif args.command == "help":
        dispatcher.help_agent(args.name)
    elif args.command == "pipeline":
        dispatcher.run_pipeline(Path(args.file))
    elif args.command == "docgen":
        dispatcher.generate_docs(Path(args.file))


if __name__ == "__main__":
    main()
