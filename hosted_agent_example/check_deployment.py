"""Check the status of a deployed hosted agent"""
import os
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential

# Configuration
PROJECT_ENDPOINT = "https://aq-ai-foundry-sweden-central.services.ai.azure.com/api/projects/firstProject"
AGENT_NAME = "my-hosted-agent"

print(f"Checking hosted agent deployment status")
print(f"Project: {PROJECT_ENDPOINT}")
print(f"Agent: {AGENT_NAME}\n")

# Initialize client
client = AIProjectClient(
    endpoint=PROJECT_ENDPOINT,
    credential=DefaultAzureCredential()
)

try:
    # Try to retrieve the agent
    print("Retrieving agent information...")
    agent = client.agents.retrieve(agent_name=AGENT_NAME)
    
    print(f"\n✅ Agent found!")
    print(f"   Agent ID: {agent.id}")
    print(f"   Agent Name: {agent.name}")
    
    if hasattr(agent, 'version'):
        print(f"   Version: {agent.version}")
    
    if hasattr(agent, 'description'):
        print(f"   Description: {agent.description}")
    
    print("\n📊 Agent Details:")
    print(f"   {agent}")
    
except Exception as e:
    print(f"\n❌ Error retrieving agent: {e}")
    print("\nPossible reasons:")
    print("1. Agent hasn't been deployed yet")
    print("2. Agent name is incorrect")
    print("3. Authentication issue - try: az login")
