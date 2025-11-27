# Azure OpenAI vs Azure AI Foundry: When to Use Each

This guide helps you choose between `AzureOpenAIChatClient` and `AzureAIChatClient` for your Microsoft Agent Framework applications.

## Quick Comparison

| Feature | Azure OpenAI | Azure AI Foundry |
|---------|-------------|------------------|
| **Service** | Azure OpenAI Service | Azure AI Foundry (AI Studio) |
| **Primary Use Case** | OpenAI models (GPT-4, etc.) | Multi-provider model catalog |
| **Deployment** | Direct Azure OpenAI resource | AI Foundry project/deployment |
| **Model Selection** | OpenAI models only | Multiple providers (OpenAI, Meta, Mistral, etc.) |
| **Authentication** | Azure RBAC + API keys | Managed identity, API keys, tokens |
| **Endpoint Format** | `*.openai.azure.com` | `*.inference.ai.azure.com` |
| **Client Class** | `AzureOpenAIChatClient` | `AzureAIChatClient` |

## When to Use Azure OpenAI (`AzureOpenAIChatClient`)

### ✅ Best For:

1. **Dedicated OpenAI Models**
   - You're exclusively using OpenAI models (GPT-4o, GPT-4o-mini, etc.)
   - You need specific OpenAI features like function calling, JSON mode
   - You want the most direct integration with OpenAI capabilities

2. **Existing Azure OpenAI Resources**
   - You already have Azure OpenAI resources provisioned
   - Your infrastructure is built around Azure OpenAI Service
   - You're migrating from direct OpenAI API usage

3. **Enterprise Azure OpenAI Features**
   - Content filtering and moderation
   - Virtual network integration
   - Private endpoints
   - Specific compliance requirements for OpenAI models

4. **Simpler Deployment Model**
   - Direct resource → deployment → model path
   - No need for AI Foundry project overhead
   - Straightforward authentication with RBAC

### 📝 Example Use Cases:

```python
# Customer service chatbot using GPT-4o
chat_client = AzureOpenAIChatClient(
    credential=AzureCliCredential(),
    endpoint="https://my-openai.openai.azure.com/",
    deployment_name="gpt-4o",
)
```

- Production chatbots requiring GPT-4 quality
- Content generation systems
- Code assistance tools
- Document analysis with OpenAI embeddings

## When to Use Azure AI Foundry (`AzureAIChatClient`)

### ✅ Best For:

1. **Multi-Provider Model Strategy**
   - You want flexibility to use models from different providers
   - You need to compare models from OpenAI, Meta, Mistral, etc.
   - You're building a provider-agnostic AI platform

2. **Azure AI Model Catalog**
   - Using models from Azure AI model catalog
   - Accessing specialized models (Llama, Phi, Mistral)
   - Need for specific model capabilities not in OpenAI portfolio

3. **AI Foundry Project Integration**
   - You're building within Azure AI Foundry projects
   - Need integration with AI Foundry features:
     - Prompt flow
     - Model benchmarking
     - Evaluation tools
     - MLOps workflows

4. **Unified Inference API**
   - Want consistent API across different model types
   - Building infrastructure to support multiple providers
   - Need abstraction over provider-specific APIs

5. **Cost Optimization**
   - Mix and match models based on cost/performance
   - Use cheaper models for simple tasks, premium for complex
   - Easy A/B testing between model providers

### 📝 Example Use Cases:

```python
# Multi-model AI platform
chat_client = AzureAIChatClient(
    client=ChatCompletionsClient(
        endpoint="https://my-project.inference.ai.azure.com/",
        credential=DefaultAzureCredential()
    )
)
```

- Research comparing different LLMs
- Applications that dynamically select models
- Cost-sensitive deployments
- Platforms supporting multiple AI providers
- Prototype/experimentation environments

## Side-by-Side Code Comparison

### Azure OpenAI
```python
from agent_framework.azure import AzureOpenAIChatClient
from azure.identity import AzureCliCredential

chat_client = AzureOpenAIChatClient(
    credential=AzureCliCredential(),
    endpoint="https://my-resource.openai.azure.com/",
    deployment_name="gpt-4o-mini",
)
```

**Pros:**
- Direct, simple setup
- Full OpenAI feature support
- Established service with extensive documentation

**Cons:**
- Locked into OpenAI models
- Can't easily switch providers
- Requires separate resources for different model families

### Azure AI Foundry
```python
from agent_framework.azure import AzureAIChatClient
from azure.ai.inference import ChatCompletionsClient
from azure.identity import DefaultAzureCredential

inference_client = ChatCompletionsClient(
    endpoint="https://my-project.inference.ai.azure.com/",
    credential=DefaultAzureCredential()
)

chat_client = AzureAIChatClient(client=inference_client)
```

**Pros:**
- Provider flexibility
- Access to broader model catalog
- Unified API across providers
- Better for experimentation

**Cons:**
- Extra layer of abstraction
- Requires AI Foundry project setup
- May have different feature availability per model

## Migration Path

### From Azure OpenAI to Azure AI Foundry

1. Deploy your model in Azure AI Foundry
2. Get the inference endpoint
3. Change client initialization (agent code stays the same!)

```python
# Before: Azure OpenAI
# chat_client = AzureOpenAIChatClient(...)

# After: Azure AI Foundry
inference_client = ChatCompletionsClient(endpoint="...", credential=...)
chat_client = AzureAIChatClient(client=inference_client)

# Agent code unchanged!
agent = ChatAgent(
    name="MyAgent",
    instructions="...",
    chat_client=chat_client,  # Works with both!
)
```

## Recommendation Matrix

| Your Scenario | Recommended Choice |
|---------------|-------------------|
| Production app, OpenAI models only | Azure OpenAI |
| Need to test multiple model providers | Azure AI Foundry |
| Enterprise with strict compliance | Azure OpenAI |
| Research/experimentation | Azure AI Foundry |
| Existing Azure OpenAI setup | Azure OpenAI |
| New greenfield project | Azure AI Foundry (more future-proof) |
| Cost-sensitive, need flexibility | Azure AI Foundry |
| Mission-critical, proven service | Azure OpenAI |

## Authentication Differences

### Azure OpenAI
```python
# Supports:
- AzureCliCredential (development)
- DefaultAzureCredential (production)
- ManagedIdentityCredential (Azure resources)
- API keys (via Azure.Identity)
```

### Azure AI Foundry
```python
# Supports:
- DefaultAzureCredential (recommended)
- AzureKeyCredential (API keys)
- Token-based authentication
- Managed identity (preferred for production)
```

## Our Demo Setup

We provide three server implementations:

1. **`server.py`** - Azure OpenAI (original)
2. **`server_azure_ai.py`** - Azure AI Foundry
3. **`server_multi_provider.py`** - Configurable (both)

This lets you:
- Compare performance and behavior
- Understand the differences hands-on
- Choose the right option for your needs
- Easily switch between providers

## Further Reading

- [Azure OpenAI Service Documentation](https://learn.microsoft.com/azure/ai-services/openai/)
- [Azure AI Foundry Documentation](https://learn.microsoft.com/azure/ai-studio/)
- [Azure AI Inference SDK](https://learn.microsoft.com/azure/ai-studio/how-to/develop/sdk-overview)
- [Microsoft Agent Framework](https://learn.microsoft.com/agent-framework/)
