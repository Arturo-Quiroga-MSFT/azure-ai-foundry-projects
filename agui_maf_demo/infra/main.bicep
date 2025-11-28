// Main Bicep file for AG-UI Demo deployment to Azure Container Apps
// Deploys: Container Apps Environment, Backend (FastAPI), Frontend (Next.js), Container Registry, Key Vault, Monitoring

targetScope = 'resourceGroup'

// Required parameters for azd
@minLength(1)
@maxLength(64)
@description('Name of the environment that can be used as part of naming resource convention')
param environmentName string

@minLength(1)
@description('Primary location for all resources')
param location string

// Service-specific parameters
@description('Azure OpenAI endpoint URL')
param azureOpenAIEndpoint string

@description('Azure OpenAI deployment name')
param azureOpenAIDeploymentName string

@secure()
@description('OpenWeatherMap API key')
param openWeatherAPIKey string

@secure()
@description('Tavily API key')
param tavilyAPIKey string

// Generate unique resource token for naming
var resourceToken = uniqueString(subscription().id, resourceGroup().id, location, environmentName)

// Tags for azd
var tags = {
  'azd-env-name': environmentName
}

// ============================================================================
// User-Assigned Managed Identity (Required by azd)
// ============================================================================

resource managedIdentity 'Microsoft.ManagedIdentity/userAssignedIdentities@2023-01-31' = {
  name: 'azid${resourceToken}'
  location: location
  tags: tags
}

// ============================================================================
// Log Analytics Workspace for monitoring
// ============================================================================

resource logAnalytics 'Microsoft.OperationalInsights/workspaces@2022-10-01' = {
  name: 'azlog${resourceToken}'
  location: location
  tags: tags
  properties: {
    sku: {
      name: 'PerGB2018'
    }
    retentionInDays: 30
  }
}

// ============================================================================
// Application Insights for telemetry
// ============================================================================

resource appInsights 'Microsoft.Insights/components@2020-02-02' = {
  name: 'azai${resourceToken}'
  location: location
  tags: tags
  kind: 'web'
  properties: {
    Application_Type: 'web'
    WorkspaceResourceId: logAnalytics.id
  }
}

// ============================================================================
// Azure Container Registry
// ============================================================================

resource containerRegistry 'Microsoft.ContainerRegistry/registries@2023-07-01' = {
  name: 'azacr${resourceToken}'
  location: location
  tags: tags
  sku: {
    name: 'Basic'
  }
  properties: {
    adminUserEnabled: false  // Required: admin user disabled for security
    publicNetworkAccess: 'Enabled'
  }
}

// AcrPull role assignment (Required before any Container Apps)
// GUID 7f951dda-4ed3-4680-a7ca-43fe172d538d = AcrPull role
resource acrPullRole 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  name: guid(containerRegistry.id, managedIdentity.id, 'acrPull')
  scope: containerRegistry
  properties: {
    roleDefinitionId: subscriptionResourceId('Microsoft.Authorization/roleDefinitions', '7f951dda-4ed3-4680-a7ca-43fe172d538d')
    principalId: managedIdentity.properties.principalId
    principalType: 'ServicePrincipal'
  }
}

// ============================================================================
// Key Vault for secrets
// ============================================================================

resource keyVault 'Microsoft.KeyVault/vaults@2023-07-01' = {
  name: 'azkv${resourceToken}'
  location: location
  tags: tags
  properties: {
    sku: {
      family: 'A'
      name: 'standard'
    }
    tenantId: subscription().tenantId
    enableRbacAuthorization: true
    enabledForDeployment: false
    enabledForTemplateDeployment: false
    enabledForDiskEncryption: false
    enablePurgeProtection: true  // Required: purge protection enabled
  }
}

// Store secrets in Key Vault
resource secretAzureOpenAIEndpoint 'Microsoft.KeyVault/vaults/secrets@2023-07-01' = {
  parent: keyVault
  name: 'azure-openai-endpoint'
  properties: {
    value: azureOpenAIEndpoint
  }
}

resource secretAzureOpenAIDeployment 'Microsoft.KeyVault/vaults/secrets@2023-07-01' = {
  parent: keyVault
  name: 'azure-openai-deployment-name'
  properties: {
    value: azureOpenAIDeploymentName
  }
}

resource secretOpenWeather 'Microsoft.KeyVault/vaults/secrets@2023-07-01' = {
  parent: keyVault
  name: 'openweather-api-key'
  properties: {
    value: openWeatherAPIKey
  }
}

resource secretTavily 'Microsoft.KeyVault/vaults/secrets@2023-07-01' = {
  parent: keyVault
  name: 'tavily-api-key'
  properties: {
    value: tavilyAPIKey
  }
}

// Key Vault Secrets User role for managed identity
// GUID 4633458b-17de-408a-b874-0445c86b69e6 = Key Vault Secrets User
resource keyVaultSecretsUserRole 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  name: guid(keyVault.id, managedIdentity.id, 'secretsUser')
  scope: keyVault
  properties: {
    roleDefinitionId: subscriptionResourceId('Microsoft.Authorization/roleDefinitions', '4633458b-17de-408a-b874-0445c86b69e6')
    principalId: managedIdentity.properties.principalId
    principalType: 'ServicePrincipal'
  }
}

// ============================================================================
// Container Apps Environment
// ============================================================================

resource containerAppsEnvironment 'Microsoft.App/managedEnvironments@2024-03-01' = {
  name: 'azcae${resourceToken}'
  location: location
  tags: tags
  properties: {
    appLogsConfiguration: {
      destination: 'log-analytics'
      logAnalyticsConfiguration: {
        customerId: logAnalytics.properties.customerId
        sharedKey: logAnalytics.listKeys().primarySharedKey
      }
    }
  }
}

// ============================================================================
// Backend Container App (FastAPI + Agent Framework)
// ============================================================================

resource backendContainerApp 'Microsoft.App/containerApps@2024-03-01' = {
  name: 'azca-backend-${resourceToken}'
  location: location
  tags: union(tags, {
    'azd-service-name': 'backend'  // Required: matches azure.yaml service name
  })
  identity: {
    type: 'UserAssigned'
    userAssignedIdentities: {
      '${managedIdentity.id}': {}
    }
  }
  properties: {
    managedEnvironmentId: containerAppsEnvironment.id
    configuration: {
      ingress: {
        external: false  // Internal only - accessed by frontend
        targetPort: 8888
        transport: 'http'
        corsPolicy: {
          allowedOrigins: ['*']
          allowedMethods: ['GET', 'POST', 'OPTIONS']
          allowedHeaders: ['*']
          allowCredentials: true
        }
      }
      registries: [
        {
          server: containerRegistry.properties.loginServer
          identity: managedIdentity.id
        }
      ]
      secrets: [
        {
          name: 'azure-openai-endpoint'
          keyVaultUrl: secretAzureOpenAIEndpoint.properties.secretUri
          identity: managedIdentity.id
        }
        {
          name: 'azure-openai-deployment-name'
          keyVaultUrl: secretAzureOpenAIDeployment.properties.secretUri
          identity: managedIdentity.id
        }
        {
          name: 'openweather-api-key'
          keyVaultUrl: secretOpenWeather.properties.secretUri
          identity: managedIdentity.id
        }
        {
          name: 'tavily-api-key'
          keyVaultUrl: secretTavily.properties.secretUri
          identity: managedIdentity.id
        }
      ]
    }
    template: {
      containers: [
        {
          name: 'backend'
          image: 'mcr.microsoft.com/azuredocs/containerapps-helloworld:latest'  // Required: base image, will be updated by azd
          resources: {
            cpu: json('1.0')
            memory: '2.0Gi'
          }
          env: [
            {
              name: 'AZURE_OPENAI_ENDPOINT'
              secretRef: 'azure-openai-endpoint'
            }
            {
              name: 'AZURE_OPENAI_DEPLOYMENT_NAME'
              secretRef: 'azure-openai-deployment-name'
            }
            {
              name: 'OPENWEATHER_API_KEY'
              secretRef: 'openweather-api-key'
            }
            {
              name: 'TAVILY_API_KEY'
              secretRef: 'tavily-api-key'
            }
            {
              name: 'APPLICATIONINSIGHTS_CONNECTION_STRING'
              value: appInsights.properties.ConnectionString
            }
          ]
        }
      ]
      scale: {
        minReplicas: 0
        maxReplicas: 10
        rules: [
          {
            name: 'http-scaling'
            http: {
              metadata: {
                concurrentRequests: '10'
              }
            }
          }
        ]
      }
    }
  }
  dependsOn: [
    acrPullRole  // Ensure ACR role assignment is done first
    keyVaultSecretsUserRole
  ]
}

// ============================================================================
// Frontend Container App (Next.js)
// ============================================================================

resource frontendContainerApp 'Microsoft.App/containerApps@2024-03-01' = {
  name: 'azca-frontend-${resourceToken}'
  location: location
  tags: union(tags, {
    'azd-service-name': 'frontend'  // Required: matches azure.yaml service name
  })
  identity: {
    type: 'UserAssigned'
    userAssignedIdentities: {
      '${managedIdentity.id}': {}
    }
  }
  properties: {
    managedEnvironmentId: containerAppsEnvironment.id
    configuration: {
      ingress: {
        external: true  // External access
        targetPort: 3000
        transport: 'http'
        corsPolicy: {
          allowedOrigins: ['*']
          allowedMethods: ['GET', 'POST', 'OPTIONS']
          allowedHeaders: ['*']
        }
      }
      registries: [
        {
          server: containerRegistry.properties.loginServer
          identity: managedIdentity.id
        }
      ]
    }
    template: {
      containers: [
        {
          name: 'frontend'
          image: 'mcr.microsoft.com/azuredocs/containerapps-helloworld:latest'  // Required: base image, will be updated by azd
          resources: {
            cpu: json('0.5')
            memory: '1.0Gi'
          }
          env: [
            {
              name: 'NEXT_TELEMETRY_DISABLED'
              value: '1'
            }
            {
              name: 'BACKEND_URL'
              value: 'https://${backendContainerApp.properties.configuration.ingress.fqdn}'
            }
            {
              name: 'APPLICATIONINSIGHTS_CONNECTION_STRING'
              value: appInsights.properties.ConnectionString
            }
          ]
        }
      ]
      scale: {
        minReplicas: 0
        maxReplicas: 10
        rules: [
          {
            name: 'http-scaling'
            http: {
              metadata: {
                concurrentRequests: '20'
              }
            }
          }
        ]
      }
    }
  }
  dependsOn: [
    acrPullRole  // Ensure ACR role assignment is done first
  ]
}

// ============================================================================
// Outputs (Required by azd)
// ============================================================================

@description('The ID of the resource group')
output RESOURCE_GROUP_ID string = resourceGroup().id

@description('The endpoint of the container registry')
output AZURE_CONTAINER_REGISTRY_ENDPOINT string = containerRegistry.properties.loginServer

@description('The name of the container registry')
output AZURE_CONTAINER_REGISTRY_NAME string = containerRegistry.name

@description('Frontend URL')
output FRONTEND_URL string = 'https://${frontendContainerApp.properties.configuration.ingress.fqdn}'

@description('Backend internal URL')
output BACKEND_URL string = 'https://${backendContainerApp.properties.configuration.ingress.fqdn}'

@description('Application Insights connection string')
output APPLICATIONINSIGHTS_CONNECTION_STRING string = appInsights.properties.ConnectionString

@description('Key Vault name')
output KEY_VAULT_NAME string = keyVault.name
