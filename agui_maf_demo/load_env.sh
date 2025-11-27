#!/bin/bash
# Load environment variables from .env file

set -a
source .env
set +a

echo "✅ Environment variables loaded from .env"
echo "📡 AZURE_OPENAI_ENDPOINT: $AZURE_OPENAI_ENDPOINT"
echo "🤖 AZURE_OPENAI_DEPLOYMENT_NAME: $AZURE_OPENAI_DEPLOYMENT_NAME"
echo "🔧 AZURE_PROVIDER: $AZURE_PROVIDER"
