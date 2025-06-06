import argparse
import importlib
import json
from datetime import datetime
from pathlib import Path

import yaml


class Dispatcher:
    def __init__(self, registry_path: Path):
        self.registry_path = registry_path
        self.agents = self.load_registry()

    def log(self, level: str, actor: str, message: str):
        ts = datetime.utcnow().isoformat()
        print(f"{ts} | {level} | {actor} | {message}")

    def load_registry(self):
        with open(self.registry_path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
        return data.get("agents", [])

    def list_agents(self):
        for agent in self.agents:
            print(agent["name"])

    def load_agent(self, name: str):
        entry = next((a for a in self.agents if a["name"] == name), None)
        if not entry:
            raise ValueError(f"Agent '{name}' not found")
        module = importlib.import_module(entry["module"])
        agent_cls = getattr(module, entry.get("class", name))
        config_path = Path(entry.get("config", ""))
        config = {}
        if config_path.is_file():
            with open(config_path, "r", encoding="utf-8") as f:
                if config_path.suffix in {".yaml", ".yml"}:
                    config = yaml.safe_load(f)
                else:
                    config = json.load(f)
        return agent_cls(config, self)

    def run_agent(self, name: str, input_json: str):
        agent = self.load_agent(name)
        input_data = json.loads(input_json)
        self.log("INFO", name, "starting agent")
        try:
            result = agent.process(input_data)
            if result is not None:
                print(result)
        except Exception as e:
            self.log("ERROR", name, str(e))
        finally:
            self.log("INFO", name, "finished")


def main():
    parser = argparse.ArgumentParser(description="Agent dispatcher")
    parser.add_argument("--registry", default="configs/agents.yaml")
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("list", help="List available agents")

    run_parser = subparsers.add_parser("run", help="Run an agent")
    run_parser.add_argument("name", help="Agent name")
    run_parser.add_argument("input", help="JSON string with input data")

    args = parser.parse_args()
    dispatcher = Dispatcher(Path(args.registry))

    if args.command == "list":
        dispatcher.list_agents()
    elif args.command == "run":
        dispatcher.run_agent(args.name, args.input)


if __name__ == "__main__":
    main()
