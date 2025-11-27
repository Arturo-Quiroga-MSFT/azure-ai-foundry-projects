"""
AG-UI FastAPI Server for Financial Analysis Agent

This server demonstrates:
- AG-UI protocol endpoint using Microsoft Agent Framework
- CORS configuration for web clients
- Health check endpoint
- Environment-based configuration
- Proper error handling and logging
"""

import os
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from agent_framework_ag_ui import add_agent_framework_fastapi_endpoint

from agents import get_agent
from config import get_settings

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Load configuration
settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager."""
    logger.info("Starting AG-UI Financial Analysis Server")
    logger.info(f"Environment: {settings.ENVIRONMENT}")
    logger.info(f"Host: {settings.HOST}:{settings.PORT}")
    
    # Validate Azure configuration
    if not settings.AZURE_OPENAI_ENDPOINT:
        logger.error("AZURE_OPENAI_ENDPOINT not configured!")
    if not settings.AZURE_OPENAI_DEPLOYMENT_NAME:
        logger.error("AZURE_OPENAI_DEPLOYMENT_NAME not configured!")
    
    yield
    
    logger.info("Shutting down AG-UI Financial Analysis Server")


# Create FastAPI application
app = FastAPI(
    title="AG-UI Financial Analysis Server",
    description="AG-UI protocol server for financial analysis agent with CopilotKit support",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)


# Configure CORS for web clients
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring."""
    return {
        "status": "healthy",
        "service": "ag-ui-financial-analysis",
        "version": "1.0.0",
        "agent": "FinancialAnalyst"
    }


# Root endpoint
@app.get("/")
async def root():
    """Root endpoint with server information."""
    return {
        "message": "AG-UI Financial Analysis Server",
        "description": "FastAPI server with AG-UI protocol support for financial analysis agents",
        "endpoints": {
            "agent": "/agent",
            "health": "/health",
            "docs": "/docs",
            "redoc": "/redoc"
        },
        "protocols": ["AG-UI"],
        "compatible_clients": ["CopilotKit", "AG-UI Terminal", "Custom Clients"],
        "documentation": "https://docs.ag-ui.com"
    }


# Create and register the financial analysis agent
try:
    logger.info("Creating Financial Analysis Agent...")
    
    # Set environment variables from settings for agent to use
    os.environ["AZURE_OPENAI_ENDPOINT"] = settings.AZURE_OPENAI_ENDPOINT
    os.environ["AZURE_OPENAI_DEPLOYMENT_NAME"] = settings.AZURE_OPENAI_DEPLOYMENT_NAME
    os.environ["AZURE_OPENAI_API_VERSION"] = settings.AZURE_OPENAI_API_VERSION
    
    financial_agent = get_agent()
    
    # Register AG-UI endpoint
    add_agent_framework_fastapi_endpoint(
        app=app,
        agent=financial_agent,
        path="/agent"
    )
    
    logger.info("✅ Financial Analysis Agent registered at /agent")
    logger.info("✅ AG-UI protocol endpoint ready for connections")
    
except Exception as e:
    logger.error(f"❌ Failed to create agent: {e}")
    raise


# Error handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Handle HTTP exceptions."""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.detail,
            "status_code": exc.status_code
        }
    )


@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """Handle general exceptions."""
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "message": str(exc) if settings.ENVIRONMENT == "development" else "An error occurred"
        }
    )


# Run server
if __name__ == "__main__":
    import uvicorn
    
    logger.info(f"Starting server on {settings.HOST}:{settings.PORT}")
    logger.info(f"Access the API at: http://{settings.HOST}:{settings.PORT}")
    logger.info(f"View docs at: http://{settings.HOST}:{settings.PORT}/docs")
    logger.info(f"AG-UI endpoint: http://{settings.HOST}:{settings.PORT}/agent")
    
    uvicorn.run(
        "server:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.ENVIRONMENT == "development",
        log_level=settings.LOG_LEVEL.lower()
    )
