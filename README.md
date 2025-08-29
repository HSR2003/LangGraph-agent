# Lang Graph Agent

This project implements a simplified **Lang Graph Agent** that processes customer support requests in structured **stages**.  
It demonstrates stage modeling, state persistence, and sample query execution flows.

---

## Features
- **Stage Modeling**: Each stage (INTAKE, UNDERSTAND, PREPARE, ASK, WAIT, RETRIEVE, DECIDE, UPDATE, CREATE, DO, COMPLETE) is modeled clearly.  
- **Deterministic & Non-deterministic Execution**:
  - Deterministic: sequential steps (e.g., parsing, enrichment).  
  - Non-deterministic: decision-making (`DECIDE` stage chooses auto-resolve vs escalation).  
- **State Persistence**: Payload is updated and passed across all stages, ensuring context is preserved.  
- **MCP Client Integration**: Calls abilities on `COMMON` and `ATLAS` servers using Google Gemini (`gemini-2.5-flash`).  
- **Sample Inputs**:
  - **Alice (Auto-resolve)**: Order not arrived → system checks status → resolved automatically.  
  - **Bob (Escalated)**: Duplicate billing/refund → escalated to human agent.  

---

##  Project Structure
.
├── config/
│ ├── agent_config.yaml # Defines stages & abilities
│ ├── sample_input_1.json # Alice (auto-resolve)
│ ├── sample_input_2.json # Bob (escalated)
├── src/
│ ├── agent.py # Main entrypoint
│ ├── stages.py # Stage factory
│ ├── mcp_clients.py # MCPClient for ability execution



##  Requirements
Install dependencies:
```bash
pip install -r requirements.txt
Dependencies include:

pyyaml

google-genai

dataclasses (built-in for Python 3.7+)

##  Running the Agent

To run with Alice (auto-resolve):

    python -m src.agent config/agent_config.yaml config/sample_input_1.json

To run with Bob (escalation):


    python -m src.agent config/agent_config.yaml config/sample_input_2.json
Example Output
    Alice (Auto-resolve)
    Decision: Auto-resolved

    Decision Score: 95

    Response: "I understand that your order has not arrived yet. I'll check the status of your order right away."

    Bob (Escalation)
    Decision: Escalated

    Decision Score: 40

    Response: "I understand you've been charged twice. Could you provide transaction IDs so we can resolve this?"

Interview Criteria Mapping
    Stage Modeling → Modeled via agent_config.yaml + stages.py.
    
    State Persistence → state["payload"] is carried and updated across all stages.
    
    Sample Query Execution → sample_input_1.json (Alice, auto-resolve) and sample_input_2.json (Bob, escalation).