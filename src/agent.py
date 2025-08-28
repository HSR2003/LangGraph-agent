# src/agent.py
import yaml, json
from .mcp_clients import MCPClient
from .stages import make_stage

def run_agent(yaml_config_path: str, input_json_path: str):
    # Load config
    with open(yaml_config_path) as f:
        config = yaml.safe_load(f)

    with open(input_json_path) as f:
        sample_input = json.load(f)

    # Create clients
    clients = {
        "COMMON": MCPClient("COMMON"),
        "ATLAS": MCPClient("ATLAS"),
    }

    # Initial state
    state = {"payload": sample_input, "logs": []}

    print(f"🤖 Agent {config['agent_name']} starting...")
    print(f"Personality:\n{config['personality']}")

    # Run stages
    for stage_conf in config["stages"]:
        stage_fn = make_stage(stage_conf, clients, config["personality"])
        state = stage_fn(state)

    print("\n FINAL PAYLOAD:")
    print(json.dumps(state["payload"], indent=2))

    print("\nLOGS:")
    for log in state["logs"]:
        print(log)


if __name__ == "__main__":
    run_agent("config/agent_config.yaml", "config/sample_input.json")
