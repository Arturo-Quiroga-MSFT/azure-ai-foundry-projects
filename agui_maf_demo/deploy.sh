#!/bin/bash
set -e

# Configuration
RESOURCE_GROUP="rg-agui-maf-demo"
LOCATION="swedencentral"
ACR_NAME="acraguidemo$(openssl rand -hex 4)"
ENVIRONMENT_NAME="env-agui-maf-demo"
BACKEND_APP_NAME="agui-backend"
FRONTEND_APP_NAME="agui-frontend"

# Load environment variables from .env
if [ -f .env ]; then
    export $(grep -v '^#' .env | xargs)
fi

echo "🚀 Starting deployment to Azure Container Apps..."
echo "=================================================="

# Check if logged in to Azure
echo "Checking Azure login status..."
if ! az account show &> /dev/null; then
    echo "❌ Not logged in to Azure. Please run 'az login' first."
    exit 1
fi

SUBSCRIPTION_ID=$(az account show --query id -o tsv)
echo "✅ Using subscription: $SUBSCRIPTION_ID"

# Create or reuse Resource Group
echo ""
echo "📦 Setting up Resource Group..."
if az group show --name $RESOURCE_GROUP &> /dev/null; then
    echo "✅ Resource Group '$RESOURCE_GROUP' already exists, reusing it"
else
    echo "Creating Resource Group '$RESOURCE_GROUP'..."
    az group create --name $RESOURCE_GROUP --location $LOCATION
    echo "✅ Resource Group created"
fi

# Create or reuse Container Registry
echo ""
echo "🐳 Setting up Azure Container Registry..."
# Check if any ACR exists in the resource group
EXISTING_ACR=$(az acr list --resource-group $RESOURCE_GROUP --query "[0].name" -o tsv)

if [ -n "$EXISTING_ACR" ]; then
    ACR_NAME=$EXISTING_ACR
    echo "✅ Container Registry '$ACR_NAME' already exists, reusing it"
else
    echo "Creating Container Registry '$ACR_NAME'..."
    az acr create \
        --resource-group $RESOURCE_GROUP \
        --name $ACR_NAME \
        --sku Basic \
        --admin-enabled false
    echo "✅ Container Registry created"
fi

ACR_LOGIN_SERVER=$(az acr show --name $ACR_NAME --resource-group $RESOURCE_GROUP --query loginServer -o tsv)
echo "Registry: $ACR_LOGIN_SERVER"

# Build backend image in Azure
echo ""
echo "🔨 Building backend image in Azure..."
BACKEND_IMAGE="$ACR_LOGIN_SERVER/agui-backend:latest"
az acr build \
    --registry $ACR_NAME \
    --image agui-backend:latest \
    --file ./Dockerfile \
    .
echo "✅ Backend image built and pushed: $BACKEND_IMAGE"

# Build frontend image in Azure
echo ""
echo "🔨 Building frontend image in Azure..."
FRONTEND_IMAGE="$ACR_LOGIN_SERVER/agui-frontend:latest"
az acr build \
    --registry $ACR_NAME \
    --image agui-frontend:latest \
    --file ./agui_web_ui/Dockerfile \
    ./agui_web_ui
echo "✅ Frontend image built and pushed: $FRONTEND_IMAGE"

# Create or reuse Container Apps Environment
echo ""
echo "🌍 Setting up Container Apps Environment..."
if az containerapp env show --name $ENVIRONMENT_NAME --resource-group $RESOURCE_GROUP &> /dev/null; then
    echo "✅ Container Apps Environment '$ENVIRONMENT_NAME' already exists, reusing it"
else
    echo "Creating Container Apps Environment '$ENVIRONMENT_NAME'..."
    az containerapp env create \
        --name $ENVIRONMENT_NAME \
        --resource-group $RESOURCE_GROUP \
        --location $LOCATION
    echo "✅ Container Apps Environment created"
fi

# Get or create system-assigned identity for ACR access
echo ""
echo "🔐 Setting up authentication..."

# Deploy or update backend Container App
echo ""
echo "🚀 Deploying backend Container App..."
if az containerapp show --name $BACKEND_APP_NAME --resource-group $RESOURCE_GROUP &> /dev/null; then
    echo "Updating existing backend Container App..."
    az containerapp update \
        --name $BACKEND_APP_NAME \
        --resource-group $RESOURCE_GROUP \
        --image $BACKEND_IMAGE \
        --set-env-vars \
            AZURE_OPENAI_ENDPOINT="$AZURE_OPENAI_ENDPOINT" \
            AZURE_OPENAI_DEPLOYMENT_NAME="$AZURE_OPENAI_DEPLOYMENT_NAME" \
            OPENWEATHER_API_KEY="$OPENWEATHER_API_KEY" \
            TAVILY_API_KEY="$TAVILY_API_KEY"
    echo "✅ Backend Container App updated"
else
    echo "Creating backend Container App..."
    az containerapp create \
        --name $BACKEND_APP_NAME \
        --resource-group $RESOURCE_GROUP \
        --environment $ENVIRONMENT_NAME \
        --image $BACKEND_IMAGE \
        --target-port 8888 \
        --ingress internal \
        --registry-server $ACR_LOGIN_SERVER \
        --registry-identity system \
        --cpu 1.0 \
        --memory 2.0Gi \
        --min-replicas 0 \
        --max-replicas 10 \
        --env-vars \
            AZURE_OPENAI_ENDPOINT="$AZURE_OPENAI_ENDPOINT" \
            AZURE_OPENAI_DEPLOYMENT_NAME="$AZURE_OPENAI_DEPLOYMENT_NAME" \
            OPENWEATHER_API_KEY="$OPENWEATHER_API_KEY" \
            TAVILY_API_KEY="$TAVILY_API_KEY" \
        --system-assigned
    echo "✅ Backend Container App created"
fi

# Get backend internal URL
BACKEND_URL="https://$(az containerapp show --name $BACKEND_APP_NAME --resource-group $RESOURCE_GROUP --query properties.configuration.ingress.fqdn -o tsv)"
echo "Backend URL: $BACKEND_URL"

# Deploy or update frontend Container App
echo ""
echo "🚀 Deploying frontend Container App..."
if az containerapp show --name $FRONTEND_APP_NAME --resource-group $RESOURCE_GROUP &> /dev/null; then
    echo "Updating existing frontend Container App..."
    az containerapp update \
        --name $FRONTEND_APP_NAME \
        --resource-group $RESOURCE_GROUP \
        --image $FRONTEND_IMAGE \
        --set-env-vars \
            BACKEND_URL="$BACKEND_URL" \
            NEXT_TELEMETRY_DISABLED="1"
    echo "✅ Frontend Container App updated"
else
    echo "Creating frontend Container App..."
    az containerapp create \
        --name $FRONTEND_APP_NAME \
        --resource-group $RESOURCE_GROUP \
        --environment $ENVIRONMENT_NAME \
        --image $FRONTEND_IMAGE \
        --target-port 3000 \
        --ingress external \
        --registry-server $ACR_LOGIN_SERVER \
        --registry-identity system \
        --cpu 0.5 \
        --memory 1.0Gi \
        --min-replicas 0 \
        --max-replicas 10 \
        --env-vars \
            BACKEND_URL="$BACKEND_URL" \
            NEXT_TELEMETRY_DISABLED="1" \
        --system-assigned
    echo "✅ Frontend Container App created"
fi

# Grant backend app access to Azure OpenAI (if needed)
echo ""
echo "🔐 Configuring Azure OpenAI access..."
BACKEND_IDENTITY=$(az containerapp show --name $BACKEND_APP_NAME --resource-group $RESOURCE_GROUP --query identity.principalId -o tsv)

if [ -n "$BACKEND_IDENTITY" ]; then
    # Extract OpenAI resource info from endpoint
    # Format: https://resource-name.openai.azure.com/
    OPENAI_RESOURCE_NAME=$(echo $AZURE_OPENAI_ENDPOINT | sed -E 's|https://([^.]+)\..*|\1|')
    
    echo "Granting 'Cognitive Services OpenAI User' role to backend identity..."
    echo "  Backend Principal ID: $BACKEND_IDENTITY"
    echo "  OpenAI Resource: $OPENAI_RESOURCE_NAME"
    
    # Try to find the OpenAI resource ID
    OPENAI_RESOURCE_ID=$(az cognitiveservices account show \
        --name $OPENAI_RESOURCE_NAME \
        --query id -o tsv 2>/dev/null || echo "")
    
    if [ -n "$OPENAI_RESOURCE_ID" ]; then
        echo "  OpenAI Resource ID: $OPENAI_RESOURCE_ID"
        az role assignment create \
            --assignee $BACKEND_IDENTITY \
            --role "Cognitive Services OpenAI User" \
            --scope "$OPENAI_RESOURCE_ID" \
            2>/dev/null && echo "✅ Role assigned successfully" || echo "⚠️  Role assignment failed (may already exist)"
    else
        echo "⚠️  Could not find OpenAI resource. Please manually assign 'Cognitive Services OpenAI User' role:"
        echo "    az role assignment create \\"
        echo "      --assignee $BACKEND_IDENTITY \\"
        echo "      --role 'Cognitive Services OpenAI User' \\"
        echo "      --scope /subscriptions/$SUBSCRIPTION_ID/resourceGroups/YOUR_OPENAI_RG/providers/Microsoft.CognitiveServices/accounts/$OPENAI_RESOURCE_NAME"
    fi
else
    echo "⚠️  Could not get backend identity"
fi

# Get frontend URL
FRONTEND_URL="https://$(az containerapp show --name $FRONTEND_APP_NAME --resource-group $RESOURCE_GROUP --query properties.configuration.ingress.fqdn -o tsv)"

echo ""
echo "=================================================="
echo "✅ Deployment complete!"
echo "=================================================="
echo ""
echo "📋 Deployment Summary:"
echo "  Resource Group: $RESOURCE_GROUP"
echo "  Location: $LOCATION"
echo "  Container Registry: $ACR_NAME"
echo "  Environment: $ENVIRONMENT_NAME"
echo ""
echo "🌐 Application URLs:"
echo "  Frontend: $FRONTEND_URL"
echo "  Backend:  $BACKEND_URL (internal)"
echo ""
echo "🔗 Azure Portal:"
echo "  https://portal.azure.com/#@/resource/subscriptions/$SUBSCRIPTION_ID/resourceGroups/$RESOURCE_GROUP"
echo ""
echo "💡 To view logs:"
echo "  Backend:  az containerapp logs show --name $BACKEND_APP_NAME --resource-group $RESOURCE_GROUP --follow"
echo "  Frontend: az containerapp logs show --name $FRONTEND_APP_NAME --resource-group $RESOURCE_GROUP --follow"
echo ""
echo "🧹 To delete everything:"
echo "  az group delete --name $RESOURCE_GROUP --yes --no-wait"
echo ""
