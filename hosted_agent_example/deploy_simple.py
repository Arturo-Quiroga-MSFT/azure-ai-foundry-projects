"""Simple deployment script for hosted agent to Azure AI Foundry

Note: The Python SDK for hosted agents (ImageBasedHostedAgentDefinition) is not yet
available in the current azure-ai-projects package. For now, use Azure Developer CLI (azd)
or wait for SDK support.

This script provides the Azure CLI commands to deploy manually.
"""
import subprocess
import sys

# Configuration
ACCOUNT_NAME = "aq-ai-foundry-Sweden-Central"  # Your AI Foundry account name
PROJECT_NAME = "firstProject"  # Your project name
CONTAINER_IMAGE = "aqmlacr001.azurecr.io/my-hosted-agent:v1"
AGENT_NAME = "my-hosted-agent"
AGENT_VERSION = "1"

print("="*70)
print("Hosted Agent Deployment for Azure AI Foundry")
print("="*70)
print(f"\nConfiguration:")
print(f"  Account: {ACCOUNT_NAME}")
print(f"  Project: {PROJECT_NAME}")
print(f"  Agent: {AGENT_NAME}")
print(f"  Image: {CONTAINER_IMAGE}")
print(f"  Version: {AGENT_VERSION}")

print("\n" + "="*70)
print("⚠️  IMPORTANT: Python SDK Support Not Yet Available")
print("="*70)
print("\nThe ImageBasedHostedAgentDefinition is not yet available in")
print("azure-ai-projects (tested up to 1.1.0b4).")
print("\n📋 ONLY Available Deployment Method:")
print("\n🔧 Azure Developer CLI (azd) - REQUIRED")
print("   See: DEPLOYMENT_GUIDE.md for full instructions")
print()
print("❌ Portal UI: NOT available for hosted agents")
print("❌ Python SDK: NOT yet available")
print("❌ Azure CLI (az): NOT yet available for creation")

print("\n" + "="*70)
print("Azure CLI Deployment Commands")
print("="*70)

# Note: The actual az cognitiveservices agent create command isn't fully documented yet
# for hosted/container agents. The recommended path is using azd.

print("\n⚠️  Note: Azure CLI commands for hosted agents are still being finalized.")
print("The recommended approach is to use Azure Developer CLI (azd):\n")

print("# Install azd if not already installed")
print("curl -fsSL https://aka.ms/install-azd.sh | bash")
print()
print("# Initialize with your existing project")
print(f"azd ai agent init --project-id /subscriptions/<SUBSCRIPTION_ID>/resourceGroups/<RG_NAME>/providers/Microsoft.CognitiveServices/accounts/{ACCOUNT_NAME}/projects/{PROJECT_NAME}")
print()
print("# Initialize agent configuration")
print("azd ai agent init -m agent.yaml")
print()
print("# Deploy")
print("azd up")

print("\n" + "="*70)
print("⚠️  Portal Deployment NOT Available")
print("="*70)
print("\nNote: The Azure AI Foundry portal does NOT currently support")
print("creating hosted agents through the UI. The portal only supports")
print("declarative (prompt-based) agents.")
print()
print("Hosted agents MUST be deployed using Azure Developer CLI (azd).")
print()
print("Steps to deploy with azd:")
print("\n1. Build and push your container image:")
print(f"   docker build -t {AGENT_NAME}:v{AGENT_VERSION} .")
print(f"   az acr login --name aqmlacr001")
print(f"   docker tag {AGENT_NAME}:v{AGENT_VERSION} {CONTAINER_IMAGE}")
print(f"   docker push {CONTAINER_IMAGE}")
print()
print("2. Configure ACR permissions:")
print("   - Go to Azure Portal → Your AI Foundry Project")
print("   - Navigate to Identity → System assigned")
print("   - Copy the Object (principal) ID")
print("   - Run:")
print("     az role assignment create \\")
print("       --assignee <OBJECT_ID> \\")
print("       --role AcrPull \\")
print("       --scope /subscriptions/<SUB_ID>/resourceGroups/<RG>/providers/Microsoft.ContainerRegistry/registries/aqmlacr001")
print()
print("3. Deploy using azd (see commands above)")
print()
print("📌 Once deployed via azd, you CAN view and test the hosted agent")
print("   in the Azure AI Foundry portal, but creation must be via azd.")

print("\n" + "="*70)
print("📚 For More Information")
print("="*70)
print("\nSee DEPLOYMENT_GUIDE.md for comprehensive deployment instructions")
print("See QUICK_START.md for the recommended azd workflow")
print("\n✅ Once SDK support is added, this script will be updated automatically")
print("="*70 + "\n")
