# Python SDK Status for Hosted Agents

## Current Status (November 26, 2025)

The Python SDK (`azure-ai-projects`) **does not yet have support** for programmatically deploying hosted agents with container images.

### What's Missing

The following models referenced in the Microsoft documentation are not available:
- `ImageBasedHostedAgentDefinition`
- `ProtocolVersionRecord` 
- `AgentProtocol`

### Versions Tested
- ❌ `azure-ai-projects==1.0.0b12` - No hosted agent support
- ❌ `azure-ai-projects==1.1.0b4` - No hosted agent support

### Documentation vs Reality

The official Microsoft documentation at:
https://learn.microsoft.com/en-us/azure/ai-foundry/agents/concepts/hosted-agents?view=foundry

Shows code examples using `ImageBasedHostedAgentDefinition`, but this is **not yet implemented** in the released SDK versions.

## Recommended Deployment Approaches

Until SDK support is added, use this method:

### 1. Azure Developer CLI (azd) - ONLY OPTION ✅

This is the **ONLY** currently supported method for deploying hosted agents:

```bash
# Install azd
curl -fsSL https://aka.ms/install-azd.sh | bash

# Initialize with existing project
azd ai agent init --project-id /subscriptions/<SUB_ID>/resourceGroups/<RG>/providers/Microsoft.CognitiveServices/accounts/<ACCOUNT>/projects/<PROJECT>

# Initialize agent configuration
azd ai agent init -m agent.yaml

# Deploy
azd up
```

**Pros:**
- Official Microsoft tool
- Handles infrastructure provisioning
- Manages ACR, RBAC, and deployments automatically
- Currently in preview but actively supported

**Cons:**
- Additional CLI tool to install
- More complex for simple deployments

### 2. Azure AI Foundry Portal - ❌ NOT AVAILABLE

**Important:** The Azure AI Foundry portal does **NOT** currently support creating hosted agents through the UI.

The portal only allows creating **declarative (prompt-based) agents**, not hosted (containerized) agents.

- ❌ No "Hosted Agent" option in the portal
- ❌ Cannot specify container images via UI
- ✅ Can VIEW and TEST hosted agents after they're deployed via azd
- ✅ Can manage existing hosted agents (start/stop/etc.)

**You cannot create hosted agents in the portal - you must use `azd`.**

### 3. Azure CLI (az) - LIMITED SUPPORT ⚠️

Some `az cognitiveservices agent` commands exist for management:
- `az cognitiveservices agent start`
- `az cognitiveservices agent stop`
- `az cognitiveservices agent update`
- `az cognitiveservices agent delete`

But **agent creation** commands for hosted/container agents are not fully documented or available yet.

## What Works in Python SDK Today

The Python SDK currently supports:
- ✅ Creating **prompt-based agents** (not hosted/container agents)
- ✅ Managing agent threads and conversations
- ✅ Invoking existing agents (including hosted agents once deployed)
- ✅ Agent evaluation and testing

Example of what DOES work:
```python
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import PromptAgentDefinition
from azure.identity import DefaultAzureCredential

client = AIProjectClient(
    endpoint="https://your-project.services.ai.azure.com/api/projects/your-project",
    credential=DefaultAzureCredential()
)

# This works - creating a prompt-based agent
agent = client.agents.create_version(
    agent_name="my-prompt-agent",
    definition=PromptAgentDefinition(
        model="gpt-4o",
        instructions="You are a helpful assistant."
    )
)

# This also works - invoking ANY agent (including hosted ones once deployed)
openai_client = client.get_openai_client()
response = openai_client.responses.create(
    input=[{"role": "user", "content": "Hello!"}],
    extra_body={"agent": {"name": "my-hosted-agent", "type": "agent_reference"}}
)
```

## When Will SDK Support Be Available?

Microsoft has not announced a timeline for when `ImageBasedHostedAgentDefinition` will be added to the Python SDK.

**Signs to watch for:**
- New preview releases of `azure-ai-projects` (check PyPI)
- Updates to the official documentation
- GitHub releases in the Azure SDK for Python repo

## Our Implementation

The files in this repository show the **intended** implementation once SDK support is available:

- `deploy_simple.py` - Now shows available deployment methods
- `check_deployment.py` - Works today (retrieves existing agents)
- `test_deployed_agent.py` - Works today (invokes existing agents)

Once `ImageBasedHostedAgentDefinition` is available, `deploy_simple.py` can be updated to use the SDK approach shown in the Microsoft docs.

## Summary

✅ **For Now:** Use Azure Developer CLI (`azd`) or the Azure Portal
📅 **Coming Soon:** Python SDK support with `ImageBasedHostedAgentDefinition`
🔄 **This Repository:** Ready to switch to SDK once available

See `DEPLOYMENT_GUIDE.md` for the complete `azd` workflow.
