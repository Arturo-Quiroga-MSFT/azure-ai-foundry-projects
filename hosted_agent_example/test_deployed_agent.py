"""Test the deployed hosted agent by sending sample queries"""
import os
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import AgentReference
from azure.identity import DefaultAzureCredential

# Configuration
PROJECT_ENDPOINT = "https://aq-ai-foundry-sweden-central.services.ai.azure.com/api/projects/firstProject"
AGENT_NAME = "my-hosted-agent"

print(f"Testing hosted agent")
print(f"Project: {PROJECT_ENDPOINT}")
print(f"Agent: {AGENT_NAME}\n")

# Initialize client
client = AIProjectClient(
    endpoint=PROJECT_ENDPOINT,
    credential=DefaultAzureCredential()
)

try:
    # Retrieve the agent
    print("Retrieving agent...")
    agent = client.agents.retrieve(agent_name=AGENT_NAME)
    print(f"✅ Found agent: {agent.name}")
    
    if hasattr(agent, 'version'):
        print(f"   Version: {agent.version}")
    
    # Get OpenAI client
    openai_client = client.get_openai_client()
    
    # Test queries
    test_queries = [
        "What's the weather in Seattle?",
        "Calculate 25 * 48",
        "What's the weather in Tokyo and what is 100 divided by 4?"
    ]
    
    print(f"\n{'='*60}")
    for i, query in enumerate(test_queries, 1):
        print(f"\n🤔 Query {i}: {query}")
        print("-" * 60)
        
        try:
            response = openai_client.responses.create(
                input=[{"role": "user", "content": query}],
                extra_body={
                    "agent": {
                        "name": agent.name, 
                        "type": "agent_reference"
                    }
                }
            )
            
            print(f"🤖 Response: {response.output_text}")
            
        except Exception as e:
            print(f"❌ Error: {e}")
        
        print("-" * 60)
    
    print(f"\n{'='*60}")
    print("\n✅ Testing complete!")
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    print("\nMake sure:")
    print("1. The agent is deployed and running")
    print("2. You're authenticated with: az login")
    print("3. The agent name is correct")
