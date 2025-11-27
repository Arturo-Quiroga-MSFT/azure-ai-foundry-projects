# Azure AI Foundry Agent Deployment - Permissions Fix

## Issue
When attempting to deploy an agent to Azure AI Foundry via VS Code extension, encountered the following error:

```
401: The principal `arturoqu@MngEnvMCAP094150.onmicrosoft.com` lacks the required data action `Microsoft.CognitiveServices/accounts/AIServices/agents/write` to perform `POST /api/projects/{projectName}/assistants` operation.
```

## Root Cause Analysis

### Current Role Assignments (Before Fix)
At the project level (`aq-ai-foundry-Sweden-Central/projects/firstProject`), the user had:

1. **Cognitive Services Contributor**
   - Control plane role only
   - Data actions: `[]` (none)
   - Cannot perform agent operations

2. **Azure AI Developer**
   - Data actions limited to:
     - `Microsoft.CognitiveServices/accounts/OpenAI/*`
     - `Microsoft.CognitiveServices/accounts/SpeechServices/*`
     - `Microsoft.CognitiveServices/accounts/ContentSafety/*`
     - `Microsoft.CognitiveServices/accounts/MaaS/*`
   - Does **NOT** include `AIServices/agents/*` operations

### Missing Permission
The **Azure AI User** role was missing, which provides:
- Data action: `Microsoft.CognitiveServices/*`
- This includes `Microsoft.CognitiveServices/accounts/AIServices/agents/write`
- Essential for creating and deploying agents in AI Foundry

## Solution Applied

### Command Executed
```bash
az role assignment create \
  --role "Azure AI User" \
  --assignee "arturoqu@MngEnvMCAP094150.onmicrosoft.com" \
  --scope "/subscriptions/7a28b21e-0d3e-4435-a686-d92889d4ee96/resourceGroups/AI-FOUNDRY-RG/providers/Microsoft.CognitiveServices/accounts/aq-ai-foundry-Sweden-Central/projects/firstProject"
```

### Result
- Exit Code: 0 (Success)
- The **Azure AI User** role was successfully assigned at the project level
- Agent deployment should now work from VS Code extension

## Current Role Assignments (After Fix)

| Role | Scope | Data Actions |
|------|-------|--------------|
| **Cognitive Services Contributor** | Project | None (control plane only) |
| **Azure AI Developer** | Project | OpenAI/*, SpeechServices/*, ContentSafety/*, MaaS/* |
| **Azure AI User** | Project | Microsoft.CognitiveServices/* (all data actions) |

## Key Takeaways

1. **Control Plane vs Data Plane**: 
   - Control plane roles (Contributor) manage resources but can't perform operations
   - Data plane roles (Azure AI User) enable actual interaction with services

2. **Role Specificity**:
   - Azure AI Developer is scoped to specific services (OpenAI, Speech, etc.)
   - Azure AI User provides broad data plane access including agents

3. **Minimum Required Role for Agent Deployment**:
   - **Azure AI User** at the project level
   - Provides all necessary data actions including agent creation/deployment

## Reference Documentation
- [Azure AI Foundry RBAC Documentation](https://learn.microsoft.com/en-us/azure/ai-foundry/concepts/rbac-azure-ai-foundry)
- [Error: Principal doesn't have access to operation](https://learn.microsoft.com/en-us/azure/ai-foundry/concepts/rbac-azure-ai-foundry#error-principal-doesnt-have-access-to-apioperation)

## Project Details
- **Subscription**: ARTURO-MngEnvMCAP094150 (7a28b21e-0d3e-4435-a686-d92889d4ee96)
- **Resource Group**: AI-FOUNDRY-RG
- **AI Foundry Resource**: aq-ai-foundry-Sweden-Central
- **Project**: firstProject
- **User**: arturoqu@MngEnvMCAP094150.onmicrosoft.com
- **Date Fixed**: November 26, 2025
