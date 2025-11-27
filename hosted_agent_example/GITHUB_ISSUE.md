# GitHub Issue: Request for ImageBasedHostedAgentDefinition Support in azure-ai-projects

**Post this at**: https://github.com/Azure/azure-sdk-for-python/issues/new

---

## Title
[Feature Request] ImageBasedHostedAgentDefinition support for deploying hosted agents in azure-ai-projects

## Labels
- `Client` - azure-ai-projects
- `feature-request`
- `needs-team-attention`

---

## Issue Description

### Summary
The Microsoft Learn documentation for [Azure AI Foundry Hosted Agents](https://learn.microsoft.com/en-us/azure/ai-foundry/agents/concepts/hosted-agents) shows Python SDK code examples using `ImageBasedHostedAgentDefinition` to deploy containerized agents programmatically. However, this class does not exist in any current version of the `azure-ai-projects` package, forcing developers to use Azure Developer CLI (azd) as the only deployment method.

### Current Situation
- **Documentation shows**: Code examples with `ImageBasedHostedAgentDefinition` for programmatic deployment
- **SDK reality**: Class not available in any released version (tested up to `1.1.0b4`)
- **Current workaround**: Must use `azd ai agent` commands instead of Python SDK
- **Changelog**: No mention of hosted agent support in any version history

### Versions Tested
```bash
# Tested both versions - neither contains ImageBasedHostedAgentDefinition
azure-ai-projects==1.0.0b12
azure-ai-projects==1.1.0b4
```

### Expected Behavior
Based on the official Microsoft documentation, developers should be able to deploy hosted agents programmatically using Python SDK:

```python
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import ImageBasedHostedAgentDefinition
from azure.identity import DefaultAzureCredential

project_client = AIProjectClient(
    credential=DefaultAzureCredential(),
    endpoint="https://<account>.services.ai.azure.com/api/projects/<project>"
)

# Expected to work but currently fails with ImportError
agent_definition = ImageBasedHostedAgentDefinition(
    name="my-hosted-agent",
    image="myregistry.azurecr.io/my-agent:v1",
    version="1"
)

agent = project_client.agents.create_hosted_agent(agent_definition)
```

### Actual Behavior
```python
# This import fails
from azure.ai.projects.models import ImageBasedHostedAgentDefinition
# ImportError: cannot import name 'ImageBasedHostedAgentDefinition' from 'azure.ai.projects.models'
```

### Current Workaround
Developers must use Azure Developer CLI instead:

```bash
# Only working deployment method
azd ai agent init --project-id <PROJECT_RESOURCE_ID>
azd ai agent init -m agent.yaml
azd up
```

While `azd` works, it:
- Breaks programmatic deployment workflows
- Prevents CI/CD automation with pure Python
- Creates inconsistency with declarative agent workflows (which have full SDK support)
- Doesn't align with the documented SDK approach

### Impact
This affects developers who:
- Need programmatic deployment in Python scripts
- Want to automate hosted agent deployment in CI/CD pipelines
- Prefer infrastructure-as-code approaches using Python
- Are following the official Microsoft documentation examples

### Questions
1. **When will `ImageBasedHostedAgentDefinition` be added to `azure-ai-projects`?**
2. **Which version will include hosted agent support?**
3. **Is there a preview/alpha version available for testing?**
4. **Why does the documentation show SDK examples if the SDK doesn't support it yet?**
5. **Are there any temporary alternatives besides `azd`?**

### Documentation References
- **Main documentation**: https://learn.microsoft.com/en-us/azure/ai-foundry/agents/concepts/hosted-agents
- **Shows SDK examples that don't work**: The page contains Python code snippets using `ImageBasedHostedAgentDefinition`
- **Package CHANGELOG**: https://github.com/Azure/azure-sdk-for-python/blob/release/azure-ai-projects/1.1.0b4/sdk/ai/azure-ai-projects/CHANGELOG.md
  - No mention of hosted agent support in any version

### Environment
```
OS: macOS
Python: 3.13
azure-ai-projects: 1.1.0b4 (latest beta)
azure-identity: latest
```

### Additional Context
- **Declarative agents** (prompt-based) have full SDK support via `client.agents.create_agent()`
- **Hosted agents** (containerized) currently have NO SDK support
- The Azure AI Foundry portal also doesn't support creating hosted agents (only viewing/testing them after `azd` deployment)
- This creates a significant gap between documented capabilities and actual SDK functionality

### Proposed Solution
Add hosted agent management to `azure-ai-projects` with classes like:
- `ImageBasedHostedAgentDefinition` (for container-based agents)
- `HostedAgent` (response model)
- Methods: `client.agents.create_hosted_agent()`, `client.agents.list_hosted_agents()`, etc.

### Related Issues
- [ ] Check if this relates to any existing issues about hosted agents
- [ ] Cross-reference with Azure AI Foundry service announcements

---

## Thank you!
Would greatly appreciate any timeline or roadmap information about hosted agent SDK support. This would help us plan our development approach and choose between waiting for SDK support vs. building around `azd` CLI.

---

### Maintainers to notify (from CODEOWNERS)
@dargilco @trangevi @glharper @nick863 @howieleung
