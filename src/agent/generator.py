"""
src/agent/generator.py
AI Payload Generator for SAP Agentic Testing Framework.
Fetches EDMX/OData metadata via sap-mcp-server and uses an LLM to generate robust test payloads.
"""

import os
import json
import requests
from typing import Dict, Any, List
from pydantic import BaseModel, Field
from openai import OpenAI
from dotenv import load_load_env

# Load environment variables
load_env()

# Initialize OpenAI client (can be substituted with local models like Ollama/Llama3)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
SAP_MCP_SERVER_URL = os.getenv("SAP_MCP_SERVER_URL", "http://localhost:3000")


class TestCasePayload(BaseModel):
    test_case_name: str = Field(description="A descriptive name of the test scenario (e.g., 'Negative Stock Edge Case')")
    scenario_type: str = Field(description="Category: 'HAPPY_PATH', 'EDGE_CASE', or 'MALFORMED'")
    payload: Dict[str, Any] = Field(description="The actual JSON payload matching the SAP OData Entity Type structure")
    developer_notes: str = Field(description="Explanation of what business rules or boundaries this specific payload is testing")


class GeneratedTestSuite(BaseModel):
    entity_set: str = Field(description="The target SAP OData Entity Set name")
    test_cases: List[TestCasePayload] = Field(description="List of AI-generated test case payloads")


def fetch_sap_metadata(service_name: str) -> str:
    """
    Invokes the sap-mcp-server to fetch the OData metadata (EDMX) schema.
    """
    print(f"🔌 Connecting to MCP Server at {SAP_MCP_SERVER_URL}...")
    try:
        # Simulating an MCP Tool call proxying to sap_read_metadata
        response = requests.post(
            f"{SAP_MCP_SERVER_URL}/tools/sap_read_metadata",
            json={"service_name": service_name},
            timeout=10
        )
        if response.status_code == 200:
            return response.json().get("metadata_content", "")
        else:
            raise RuntimeError(f"MCP Server returned status code {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"⚠️ Warning: Could not connect to sap-mcp-server ({e}). Falling back to local mock metadata.")
        # Fallback minimal mock metadata for Z_INVENTORY_STATUS_SRV if MCP server is offline
        return """
        <EntityType Name="InventoryStatus">
            <Key><PropertyRef Name="MaterialID"/></Key>
            <Property Name="MaterialID" Type="Edm.String" MaxLength="18" Nullable="false"/>
            <Property Name="Plant" Type="Edm.String" MaxLength="4" Nullable="false"/>
            <Property Name="StorageLocation" Type="Edm.String" MaxLength="4"/>
            <Property Name="StockQuantity" Type="Edm.Decimal" Precision="13" Scale="3"/>
            <Property Name="LastCheckedDate" Type="Edm.DateTime"/>
        </EntityType>
        """

def generate_test_suite(service_name: str, entity_set: str, count: int = 3) -> GeneratedTestSuite:
    """
    Analyzes the SAP structural schemas and uses Structured Outputs to return a verified test suite.
    """
    metadata_schema = fetch_sap_metadata(service_name)
    
    print(f"🧠 Synthesizing {count} distinct test scenarios via LLM...")
    
    system_prompt = (
        "You are an expert SAP Enterprise QA Automation Architect. Your task is to analyze the provided "
        "SAP OData Metadata schema and generate highly precise JSON payloads to comprehensively stress-test the system."
    )
    
    user_prompt = f"""
    Target OData Service: {service_name}
    Target Entity Set: {entity_set}
    
    --- SAP METADATA SCHEMA ---
    {metadata_schema}
    ---------------------------
    
    Generate a suite of exactly {count} test cases. 
    Ensure you include:
    1. A 'HAPPY_PATH' payload with optimal, realistic standard enterprise values.
    2. An 'EDGE_CASE' payload exploring bounds (e.g., zero quantities, maximum string lengths, decimal precisions).
    3. A 'MALFORMED' or critical boundary payload simulating complex invalid states (e.g., negative stock fields if the type allows it, or unexpected datetime format mismatches) to test SAP backend validations.
    
    Strictly adhere to the property data types, lengths, and constraints defined in the metadata schema.
    """

    # Using OpenAI's structured outputs feature (response_format) to guarantee reliable compilation
    completion = client.beta.chat.completions.parse(
        model="gpt-4o-2024-08-06", # Or any model supporting structured parsing
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        response_format=GeneratedTestSuite,
        temperature=0.2 # Low temperature for programmatic precision
    )
    
    return completion.choices[0].message.parsed


if __name__ == "__main__":
    # Example execution configuration
    TARGET_SERVICE = "Z_INVENTORY_STATUS_SRV"
    TARGET_ENTITY = "InventoryStatusSet"
    
    print(f"🚀 Starting AI Test Generator for Entity Set: {TARGET_ENTITY}...")
    suite = generate_test_suite(service_name=TARGET_SERVICE, entity_set=TARGET_ENTITY, count=3)
    
    # Output the result as cleanly formatted JSON
    print("\n✅ Successfully Generated Test Suite Structure:")
    print(json.dumps(suite.model_dump(), indent=2))
    
    # Save the output file to disk for the CI/CD execution pipeline to pick up
    output_path = "tests/generated_payloads.json"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w") as f:
        json.dump(suite.model_dump(), f, indent=2)
    print(f"\n💾 Saved payloads to disk at: {output_path}")
