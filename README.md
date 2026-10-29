# sap-ai-test-agent
AI-driven autonomous testing framework for SAP landscapes. 


## ✨ Core Features

• 🔮 Automated Supplier Virtualization: Uses an LLM agent to parse SAP OData metadata/ABAP data structures and dynamically generate hundreds of realistic, complex test payloads.

• 🛠️ Self-Healing Pipelines: When an Integration Flow mapping breaks due to schema updates, the AI analyzes the error logs and proposes an instant code diff or schema patch.

• 🚀 Seamless CI/CD: A plug-and-play GitHub Actions workflow that executes AI-driven testing on every repository commit.

• 🔌 Universal Connectivity: Fully decoupled architecture powered natively by the companion sap-mcp-server.


## 🏗️ Technical Architecture

The framework operates as an intelligent agentic orchestration layer interacting directly with your SAP backend through standard endpoints.


```bash
                  ┌───────────────────────────────────────────────┐
                  │            GitHub Actions CI/CD Pipeline      │
                  │             (deploy-backend.yml)              │
                  └───────────────────────┬───────────────────────┘
                                          │ Trigger Tests
                                          ▼
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                              AI-AGENT CORE LAYER (Python)                              │
│                                                                                        │
│ ┌──────────────────────────────┐              ┌──────────────────────────────────────┐ │
│ │   LLM Payload Generator      │              │         Self-Healing Engine          │ │
│ │  (Simulates Supplier XML)    │              │    (Fixes inbound_stock-update.json) │ │
│ └──────────────┬───────────────┘              └──────────────────▲───────────────────┘ │
└────────────────│─────────────────────────────────────────────────│─────────────────────┘
                 │ Generates Test Payload                          │ Detects Mismatch / Proposes Fix
                 ▼                                                 │
┌──────────────────────────────────────────────────────────────────┴─────────────────────┐
│                          INTEGRATION & CORE LOGIC LAYER (SAP)                          │
│                                                                                        │
│   ┌────────────────────────┐      OData V4      ┌──────────────────────────────────┐   │
│   │   Fiori Elements App   │───────────────────►│       S/4HANA Cloud Backend      │   │
│   │  (Mobile Responsive UI)│                    │  (Z_INVENTORY_STATUS CDS Views)  │   │
│   └────────────────────────┘                    └──────────────────▲───────────────┘   │
└────────────────────────────────────────────────────────────────────┼───────────────────┘
                                                                     │ Reads System Context
                                                   ┌─────────────────┴──────────────────┐
                                                   │          sap-mcp-server            │
                                                   │    (Universal Protocol Proxy)      │
                                                   └────────────────────────────────────┘
```


## 🚀 Quick Start


1. Prerequisites

Ensure you have Python 3.10+ installed and a running instance of [sap-mcp-server](https://github.com/AI-Agentic-Applications/sap-mcp-server) configured to point to your SAP Sandbox or BTP Environment.

READ THE DOCS: [quick_start.md](https://github.com/AI-Agentic-Applications/sap-ai-test-agent/blob/main/docs/quick_start.md)


## 🤝 Contributing

We love open-source contributions! Whether you want to add a new self-healing rule, support SAP IDocs, or improve the payload generation prompts, feel free to dive in.
Development Setup Instructions
1. Fork this repository.
2. Create your feature branch (git checkout -b feature/AmazingFeature).
3. Install development dependencies (pip install -r requirements-dev.txt).
4. Run code linters (flake8 src/) and ensure all tests pass (pytest).
5. Open a Pull Request.


📄 License

Distributed under the MIT License. See [LICENSE](https://github.com/AI-Agentic-Applications/sap-ai-test-agent/blob/main/LICENSE) for more information.


