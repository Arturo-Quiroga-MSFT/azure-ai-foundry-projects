"""
Test script for the deployed hosted agent
"""
import os
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from azure.ai.projects.models import AgentReference


def test_hosted_agent():
    """Test the deployed hosted agent"""
    
    # Configuration
    PROJECT_ENDPOINT = os.getenv(
        "AZURE_AI_PROJECT_ENDPOINT",
        "https://aq-ai-foundry-sweden-central.services.ai.azure.com/api/projects/firstProject"
    )
    AGENT_NAME = os.getenv("AGENT_NAME", "my-hosted-agent")
    AGENT_VERSION = os.getenv("AGENT_VERSION", "1")
    
    print("Testing hosted agent...")
    print(f"  Project: {PROJECT_ENDPOINT}")
    print(f"  Agent: {AGENT_NAME}")
    print(f"  Version: {AGENT_VERSION}")
    print()
    
    # Initialize client
    client = AIProjectClient(
        endpoint=PROJECT_ENDPOINT,
        credential=DefaultAzureCredential()
    )
    
    # Retrieve the agent
    print("Retrieving agent...")
    agent = client.agents.retrieve(agent_name=AGENT_NAME)
    print(f"✅ Agent found: {agent.name} (ID: {agent.id})")
    print()
    
    # Get OpenAI client for conversation
    openai_client = client.get_openai_client()
    
    # Test cases
    test_messages = [
        "What is the weather in Seattle?",
        "Calculate 25 * 4 + 10",
        "What's the weather in New York?",
        "Can you calculate (100 - 25) / 5?"
    ]
    
    print("=" * 60)
    print("Running Test Cases")
    print("=" * 60)
    
    for i, message in enumerate(test_messages, 1):
        print(f"\n📝 Test {i}/{len(test_messages)}")
        print(f"User: {message}")
        
        try:
            # Send message to agent
            response = openai_client.responses.create(
                input=[{"role": "user", "content": message}],
                extra_body={
                    "agent": AgentReference(
                        name=agent.name,
                        version=AGENT_VERSION
                    ).as_dict()
                }
            )
            
            # Print response
            print(f"Agent: {response.output_text}")
            print("✅ Success")
            
        except Exception as e:
            print(f"❌ Error: {str(e)}")
    
    print("\n" + "=" * 60)
    print("Testing Complete!")
    print("=" * 60)


if __name__ == "__main__":
    try:
        test_hosted_agent()
    except Exception as e:
        print(f"\n❌ Test failed: {str(e)}")
        print("\nTroubleshooting:")
        print("1. Ensure the agent is started:")
        print("   az cognitiveservices agent show \\")
        print("     --account-name aq-ai-foundry-Sweden-Central \\")
        print("     --project-name firstProject \\")
        print("     --name my-hosted-agent")
        print()
        print("2. Check agent logs in Azure Portal")
        print("3. Verify Azure AI User role is assigned")
        exit(1)
