"""
Deployment script for hosted agent to Azure AI Foundry
Run this after building and pushing your Docker image to ACR
"""
import os
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import (
    ImageBasedHostedAgentDefinition,
    ProtocolVersionRecord,
    AgentProtocol
)
from azure.identity import DefaultAzureCredential


def deploy_hosted_agent():
    """Deploy the hosted agent to Azure AI Foundry"""
    
    # Configuration
    PROJECT_ENDPOINT = os.getenv(
        "AZURE_AI_PROJECT_ENDPOINT",
        "https://aq-ai-foundry-sweden-central.services.ai.azure.com/api/projects/firstProject"
    )
    AGENT_NAME = os.getenv("AGENT_NAME", "my-hosted-agent")
    CONTAINER_IMAGE = os.getenv("CONTAINER_IMAGE")  # e.g., myregistry.azurecr.io/my-hosted-agent:v1
    
    if not CONTAINER_IMAGE:
        raise ValueError(
            "CONTAINER_IMAGE environment variable is required. "
            "Example: myregistry.azurecr.io/my-hosted-agent:v1"
        )
    
    print(f"Deploying hosted agent...")
    print(f"  Project: {PROJECT_ENDPOINT}")
    print(f"  Agent Name: {AGENT_NAME}")
    print(f"  Container Image: {CONTAINER_IMAGE}")
    
    # Initialize client
    client = AIProjectClient(
        endpoint=PROJECT_ENDPOINT,
        credential=DefaultAzureCredential()
    )
    
    # Create hosted agent version
    print("\nCreating agent version...")
    agent = client.agents.create_version(
        agent_name=AGENT_NAME,
        definition=ImageBasedHostedAgentDefinition(
            container_protocol_versions=[
                ProtocolVersionRecord(
                    protocol=AgentProtocol.RESPONSES,
                    version="v1"
                )
            ],
            cpu="1",  # 1 CPU core
            memory="2Gi",  # 2GB RAM
            image=CONTAINER_IMAGE,
            environment_variables={
                "AZURE_AI_PROJECT_ENDPOINT": PROJECT_ENDPOINT,
                "AZURE_OPENAI_CHAT_DEPLOYMENT_NAME": os.getenv("AZURE_OPENAI_CHAT_DEPLOYMENT_NAME", "gpt-4o"),
                "AZURE_OPENAI_ENDPOINT": os.getenv("AZURE_OPENAI_ENDPOINT", ""),
            },
            min_replicas=1,  # Minimum number of instances
            max_replicas=3   # Maximum number of instances for auto-scaling
        )
    )
    
    print(f"\n✅ Agent created successfully!")
    print(f"   Agent ID: {agent.id}")
    print(f"   Agent Name: {agent.name}")
    print(f"   Version: {agent.version}")
    
    print("\n📋 Next Steps:")
    print(f"1. Start the agent:")
    print(f"   az cognitiveservices agent start \\")
    print(f"     --account-name aq-ai-foundry-Sweden-Central \\")
    print(f"     --project-name firstProject \\")
    print(f"     --name {AGENT_NAME} \\")
    print(f"     --agent-version {agent.version}")
    print()
    print(f"2. Test the agent:")
    print(f"   python test_agent.py")
    print()
    print(f"3. View in Azure Portal:")
    print(f"   {PROJECT_ENDPOINT.replace('/api/projects/', '/project/')}")
    
    return agent


def check_prerequisites():
    """Check if all prerequisites are met"""
    
    print("Checking prerequisites...\n")
    
    # Check environment variables
    required_vars = {
        "CONTAINER_IMAGE": "Container image URL (e.g., myregistry.azurecr.io/my-hosted-agent:v1)",
        "AZURE_OPENAI_CHAT_DEPLOYMENT_NAME": "Azure OpenAI deployment name (e.g., gpt-4o)",
    }
    
    missing = []
    for var, description in required_vars.items():
        value = os.getenv(var)
        if value:
            print(f"✅ {var}: {value}")
        else:
            print(f"❌ {var}: Not set ({description})")
            missing.append(var)
    
    if missing:
        print(f"\n⚠️  Missing required environment variables: {', '.join(missing)}")
        print("\nSet them with:")
        for var in missing:
            print(f"  export {var}=<value>")
        return False
    
    print("\n✅ All prerequisites met!")
    return True


if __name__ == "__main__":
    print("=" * 60)
    print("Azure AI Foundry Hosted Agent Deployment")
    print("=" * 60)
    print()
    
    if check_prerequisites():
        print()
        try:
            agent = deploy_hosted_agent()
        except Exception as e:
            print(f"\n❌ Deployment failed: {str(e)}")
            print("\nCommon issues:")
            print("1. ACR permissions not configured")
            print("2. Azure AI User role not assigned")
            print("3. Container image doesn't exist")
            print("4. Invalid project endpoint")
            exit(1)
    else:
        exit(1)
