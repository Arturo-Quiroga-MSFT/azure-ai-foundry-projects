# Declarative vs Hosted Agents in Microsoft AI Foundry

## Overview

Microsoft AI Foundry supports two main agent development approaches, each designed for different use cases and skill levels.

## Agent Types

### Declarative Agents
1. **Prompt-based Agents**: Single agents defined through YAML configuration combining model settings, instructions, tools, and natural language prompts
2. **Workflows**: Orchestrated sequences of actions or multiple agents working together

### Hosted Agents
Containerized, code-first agents developed using supported frameworks (LangGraph, Microsoft Agent Framework) or custom code, deployed on the Microsoft Foundry Agent Service.

---

## Detailed Comparison

| Feature | Declarative Agents | Hosted Agents |
|---------|-------------------|---------------|
| **Development Method** | No-code/low-code via portal UI | Code-first (Python, C#) |
| **Configuration** | YAML-based with visual editor | Dockerfile + container image |
| **Editing** | Can be edited directly in portal | Must modify code and redeploy |
| **Deployment** | Automatic, managed by platform | Requires Docker + Azure Container Registry |
| **Complexity Level** | Simple to moderate workflows | Advanced, complex custom logic |
| **Framework Support** | Foundry built-in tools only | LangGraph, MS Agent Framework, custom |
| **Testing Location** | Agent playground in portal | Local testing + REST API |
| **Version Control** | Built-in portal versioning | Code-based + container tags |
| **Infrastructure** | Fully managed, no setup | Requires ACR, managed identity setup |
| **Language Support** | Configuration only | Python, C# |
| **Custom Dependencies** | Limited to built-in tools | Any packages/libraries supported |
| **State Management** | Automatic conversation management | Full control + automatic management |
| **Deployment Time** | Seconds to minutes | Minutes (build + containerize + deploy) |

---

## Pros and Cons Analysis

### Declarative Agents

#### ✅ Pros
- **Rapid Development**: Create functional agents in minutes without writing code
- **Low Barrier to Entry**: No programming, Docker, or DevOps knowledge required
- **Visual Editing**: Intuitive portal interface for configuration and testing
- **Built-in Versioning**: Easy version management through UI
- **Simple Deployment**: No infrastructure or container management needed
- **Quick Iteration**: Make changes and test immediately in playground
- **Natural Language Instructions**: Define behavior through prompts
- **Ideal for Prototyping**: Fast experimentation and proof-of-concepts
- **No Container Management**: Platform handles all infrastructure

#### ❌ Cons
- **Limited Customization**: Restricted to platform's built-in capabilities
- **Less Control**: Cannot implement complex custom algorithms
- **Framework Constraints**: Must use Foundry's provided tools
- **Simpler Use Cases Only**: Not suitable for advanced workflows
- **No Custom Code**: Cannot add proprietary business logic
- **Dependency Limitations**: Can't use external libraries or packages

---

### Hosted Agents

#### ✅ Pros
- **Complete Code Control**: Implement any custom logic, algorithms, or business rules
- **Framework Flexibility**: Use LangGraph, Microsoft Agent Framework, or build from scratch
- **Advanced Capabilities**: Support for complex multi-agent orchestration
- **Portability**: Code runs anywhere (local dev, Azure, other clouds)
- **Professional Tools**: Leverage mature, production-grade frameworks
- **Custom Dependencies**: Include any Python/C# packages or libraries
- **Full State Control**: Manage agent memory and context exactly as needed
- **Managed Infrastructure**: Auto-scaling, monitoring, security handled by platform
- **OpenTelemetry Support**: Built-in observability and tracing
- **Conversation Management**: Automatic stateful multi-turn conversations
- **One-Line Deployment**: Simple adapter integration (`from_langgraph(agent).run()`)
- **Local Testing**: Test with REST API before deployment

#### ❌ Cons
- **Higher Complexity**: Requires understanding of Docker, containers, and ACR
- **DevOps Knowledge**: Need CI/CD, image builds, and registry management skills
- **Longer Development Cycle**: Build → Test → Containerize → Push → Deploy
- **No Portal Editing**: Must modify source code and redeploy for changes
- **Setup Overhead**: Configure Azure Container Registry, managed identities, RBAC
- **Preview Limitations**: Currently North Central US only (as of Nov 2025)
- **Scaling Limits**: Max 2 min replicas, 5 max replicas during preview
- **Learning Curve**: Requires programming proficiency

---

## When to Use Each Approach

### Choose Declarative Agents When:

✓ Building quick prototypes or proof-of-concepts  
✓ Creating simple conversational assistants  
✓ Team lacks deep coding or DevOps expertise  
✓ Need rapid iteration and experimentation  
✓ Using only standard patterns (RAG, Q&A, search)  
✓ Built-in tools meet all requirements:
  - Bing search/grounding
  - File search with vector stores
  - Code interpreter
  - OpenAPI integrations
✓ Want to go from idea to working agent in minutes  
✓ Focus is on prompt engineering and tool configuration  

### Choose Hosted Agents When:

✓ Implementing complex custom business logic  
✓ Integrating with existing Python/C# codebases  
✓ Building advanced multi-agent orchestration systems  
✓ Need specific frameworks (LangGraph, etc.)  
✓ Require custom external dependencies or libraries  
✓ Building production-grade enterprise applications  
✓ Team has strong software engineering and DevOps capabilities  
✓ Need complete control over agent behavior and state  
✓ Want to use established agent development patterns  
✓ Require custom authentication or data processing logic  

---

## Shared Capabilities

Both agent types support:

✅ **Evaluation & Testing**: Azure AI Evaluation SDK with built-in evaluators (Intent Resolution, Task Adherence, Tool Call Accuracy)  
✅ **Observability**: Application Insights integration with OpenTelemetry tracing  
✅ **Publishing Channels**: 
  - Microsoft 365 Copilot
  - Microsoft Teams
  - Web application preview
  - Stable API endpoints
✅ **Identity Management**: Agent Identity with Microsoft Entra ID  
✅ **RBAC**: Role-based access control and permissions  
✅ **Conversation Management**: Automatic state persistence across sessions  
✅ **Model Integration**: Access to all deployed Foundry models  
✅ **Monitoring**: Performance tracking and diagnostics  
✅ **Security**: Enterprise-grade compliance and governance  

---

## Development Workflow Comparison

### Declarative Agent Workflow
```
1. Open Foundry Portal → Agent Playground
2. Configure model, instructions, tools via UI
3. Test in playground immediately
4. Iterate on prompts and settings
5. Publish to channels
Total time: Minutes
```

### Hosted Agent Workflow
```
1. Write agent code (Python/C#)
2. Test locally with REST API (localhost:8088)
3. Create Dockerfile
4. Build container image
5. Push to Azure Container Registry
6. Configure managed identity + RBAC
7. Deploy to Foundry Agent Service
8. Test in playground
9. Publish to channels
Total time: Hours to days (first time)
```

---

## Framework Support

### Declarative Agents
- Foundry built-in tools only
- YAML-based workflow definitions
- OpenAPI tool integrations

### Hosted Agents

| Framework | Python | C# |
|-----------|--------|-----|
| Microsoft Agent Framework | ✅ | ✅ |
| LangGraph | ✅ | ❌ |
| Custom Code | ✅ | ✅ |

**Adapter Packages:**
- Python: `azure-ai-agentserver-core`, `azure-ai-agentserver-agentframework`, `azure-ai-agentserver-langgraph`
- .NET: `Azure.AI.AgentServer.Core`, `Azure.AI.AgentServer.AgentFramework`

---

## Cost Considerations

### Declarative Agents
**Pay for:**
- Model token usage only
- Storage for vector stores (if used)

**Typical monthly cost:** $10-$500 depending on usage

### Hosted Agents
**Pay for:**
- Model token usage
- Container hosting runtime (billing starts Feb 1, 2026+)
- Azure Container Registry storage (~$5/month)
- Application Insights telemetry (~$2-$50/month)
- Compute resources for replicas

**Typical monthly cost:** $50-$1000+ depending on scale

---

## Migration Path

Many teams follow this progression:

```
1. Start: Declarative Agent (Prototype)
   └─ Validate concept, test with users
   
2. Evolve: Enhanced Declarative Agent
   └─ Add more tools, refine prompts
   
3. Transition: Hybrid Approach
   └─ Declarative for simple tasks
   └─ Hosted for complex workflows
   
4. Scale: Full Hosted Agent
   └─ Custom code, advanced features
   └─ Production deployment
```

**When to Migrate:**
- Custom logic becomes too complex for prompts
- Need for external dependencies or libraries
- Performance or scaling requirements increase
- Team develops DevOps/containerization capabilities

---

## Technical Requirements

### Declarative Agents
**Prerequisites:**
- ✅ Microsoft Foundry project
- ✅ Model deployment
- ✅ Azure AI User role

**Skills Needed:**
- Prompt engineering
- Basic understanding of AI tools
- YAML configuration (optional)

### Hosted Agents
**Prerequisites:**
- ✅ Microsoft Foundry project
- ✅ Azure Container Registry
- ✅ Docker installed locally
- ✅ Model deployments
- ✅ Managed identity + RBAC configuration
- ✅ Azure AI User role

**Skills Needed:**
- Python or C# programming
- Docker and containerization
- Azure DevOps or GitHub Actions
- REST API design
- Identity and access management

---

## Best Practices

### For Declarative Agents
1. **Start Simple**: Begin with basic instructions, add complexity gradually
2. **Use Built-in Tools**: Leverage file search, code interpreter, Bing grounding
3. **Test Thoroughly**: Use playground to validate behavior
4. **Version Frequently**: Create versions at stable points
5. **Clear Instructions**: Write specific, unambiguous agent instructions
6. **Monitor Usage**: Track token consumption and costs

### For Hosted Agents
1. **Test Locally First**: Use hosting adapter for local development
2. **Use Azure Developer CLI**: Leverage `azd ai agent` for simplified deployment
3. **Enable Tracing**: Configure OpenTelemetry from the start
4. **Implement Error Handling**: Add robust exception handling
5. **Version Control**: Use Git for code + semantic versioning for containers
6. **Security First**: Configure least-privilege identities
7. **Monitor Performance**: Set up Application Insights dashboards
8. **Automate Deployment**: Use CI/CD pipelines

---

## Current Limitations (Preview - Nov 2025)

### Hosted Agents Specific:
- 🚧 Region availability: North Central US only
- 🚧 Max agents per Foundry resource: 200
- 🚧 Min replicas: 2 maximum
- 🚧 Max replicas: 5 maximum
- 🚧 Cannot edit in portal (view/invoke only)

### Both Types:
- Standard Azure resource limits apply
- Subject to model availability and quotas

---

## Recommendation Strategy

### **Start with Declarative** if:
- 🎯 New to AI agents
- 🎯 Building standard conversational use cases
- 🎯 Need fast time-to-value
- 🎯 Limited technical resources
- 🎯 Prototyping and experimentation phase

### **Go Directly to Hosted** if:
- 🎯 Have existing agent code
- 🎯 Need specific frameworks (LangGraph)
- 🎯 Require custom business logic
- 🎯 Strong DevOps team available
- 🎯 Production deployment from day one

### **Use Both** for:
- 🎯 Different agents with varying complexity levels
- 🎯 Gradual migration from simple to complex
- 🎯 Cost optimization (declarative for simple, hosted for complex)

---

## Resources

### Documentation
- [Understanding Agent Development Lifecycle](https://learn.microsoft.com/azure/ai-foundry/agents/concepts/development-lifecycle)
- [What are Hosted Agents?](https://learn.microsoft.com/azure/ai-foundry/agents/concepts/hosted-agents)
- [Agent Identity Concepts](https://learn.microsoft.com/azure/ai-foundry/agents/concepts/agent-identity)

### Tools
- Azure Developer CLI: `azd ai agent` extension
- Azure AI Projects SDK: `azure-ai-projects`
- Hosting adapters: `azure-ai-agentserver-*` packages

### Pricing
- [Azure AI Foundry Pricing](https://azure.microsoft.com/pricing/details/ai-foundry/)

---

## Summary

| Criteria | Declarative | Hosted |
|----------|-------------|---------|
| **Best For** | Rapid prototyping, simple agents | Complex workflows, custom logic |
| **Skill Level** | Beginner to Intermediate | Intermediate to Advanced |
| **Time to Deploy** | Minutes | Hours to Days |
| **Flexibility** | Limited | Unlimited |
| **Maintenance** | Low | Medium to High |
| **Cost** | Lower | Higher |
| **Scalability** | Managed automatically | Configurable |
| **Recommendation** | Start here | Graduate to this |

**Bottom Line**: Both approaches are powerful and complementary. Start with declarative agents for speed and simplicity, then migrate to hosted agents when you need advanced customization and control. Many production systems use both types for different use cases.
