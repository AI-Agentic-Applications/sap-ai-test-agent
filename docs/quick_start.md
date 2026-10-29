# 🚀 Quick Start

1. Prerequisites

> Ensure you have Python 3.10+ installed and a running instance of [sap-mcp-server](https://github.com/AI-Agentic-Applications/sap-mcp-server) configured to point to your SAP Sandbox or BTP Environment.

2. Installation

```bash
git clone https://github.com
cd sap-agentic-test
pip install -r requirements.txt
```

3. Configuration

Create a .env file in the root directory:

```env
OPENAI_API_KEY=your_openai_api_key_here
SAP_MCP_SERVER_URL=http://localhost:3000
TARGET_ODATA_SERVICE=/sap/opu/odata/sap/Z_INVENTORY_STATUS_SRV
```


4. Execute Your First Agentic Test Run

```bash
python -m src.agent.run --service Z_INVENTORY_STATUS_SRV --generate-mocks
```
