

from typing import Dict, Any
from .mcp_clients import MCPClient, MCPResponse


def make_stage(stage_conf: Dict[str, Any], clients: Dict[str, MCPClient], persona: str = ""):

    def stage_fn(state):
        stage_name = stage_conf["name"]
        mode = stage_conf.get("mode", "deterministic")

        state["logs"].append(f"[{stage_name}] Stage started (mode={mode})")

        # Handle deterministic stages
        if mode == "deterministic":
            for ability in stage_conf["abilities"]:
                ability_name = ability["name"]
                server = ability["server"]
                response = clients[server].execute_ability(server, ability_name, state["payload"])

                if response.success and response.data:
                    
                    if isinstance(response.data, dict):
                        state["payload"].update(response.data)

                state["logs"].append(
                    f"[{stage_name}] {ability_name} → [{server}] → {response.message}"
                )

        # Handling non-deterministic stage 
        elif mode == "non-deterministic" and stage_name.upper() == "DECIDE":
            
            eval_resp: MCPResponse = clients["COMMON"].execute_ability("COMMON", "solution_evaluation", state["payload"])
            score = eval_resp.data.get("confidence_score", 0) if eval_resp.success else 0
            state["payload"]["decision_score"] = score
            state["logs"].append(f"[{stage_name}] solution_evaluation → Score={score}")

           
            if score < 90:
                esc_resp = clients["ATLAS"].execute_ability("ATLAS", "escalation_decision", state["payload"])
                if esc_resp.success and esc_resp.data:
                    state["payload"].update(esc_resp.data)
                state["payload"]["decision"] = "Escalated"
                state["logs"].append(f"[{stage_name}] Escalation triggered via ATLAS")
            else:
                state["payload"]["decision"] = "Auto-resolved"
                state["logs"].append(f"[{stage_name}] Auto-resolved by COMMON")

            # Step 3: updating payload
            upd_resp = clients["COMMON"].execute_ability("COMMON", "update_payload", state["payload"])
            if upd_resp.success and upd_resp.data:
                state["payload"].update(upd_resp.data)
            state["logs"].append(f"[{stage_name}] update_payload → [{upd_resp.message}]")

        else:
            state["logs"].append(f"[{stage_name}] Mode={mode} not implemented yet")

        state["logs"].append(f"[{stage_name}] Stage completed")
        return state

    return stage_fn
