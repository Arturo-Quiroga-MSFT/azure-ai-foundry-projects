"""Main entry point for AI Data Analyst Copilot"""

import asyncio
import logging
import sys
from pathlib import Path

from copilot import DataAnalystCopilot
from config import get_settings


def setup_logging(log_level: str = "INFO"):
    """Configure logging"""
    logging.basicConfig(
        level=getattr(logging, log_level.upper()),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler('copilot.log')
        ]
    )


async def main():
    """Main entry point"""
    settings = get_settings()
    setup_logging(settings.log_level)
    
    logger = logging.getLogger(__name__)
    logger.info("Starting AI Data Analyst Copilot")
    
    # Create copilot instance
    copilot = DataAnalystCopilot(
        enable_plan_review=settings.enable_plan_review,
        streaming_mode=settings.streaming_mode
    )
    
    # Check for query from command line
    if len(sys.argv) > 1:
        query = " ".join(sys.argv[1:])
    else:
        # Interactive mode
        print("\n" + "=" * 70)
        print("🤖 AI DATA ANALYST COPILOT - Interactive Mode")
        print("=" * 70)
        print("\nEnter your analysis query (or 'quit' to exit):")
        print("\nExample queries:")
        print("  - Analyze sales_data.csv and show monthly revenue trends")
        print("  - Load customer_data.json, segment by behavior, and visualize")
        print("  - Compare product performance and recommend top products to promote")
        print("\n" + "-" * 70)
        
        query = input("\n📝 Your query: ").strip()
        
        if query.lower() in ['quit', 'exit', 'q']:
            print("\n👋 Goodbye!")
            return
    
    if not query:
        print("❌ No query provided")
        return
    
    try:
        # Run analysis
        result = await copilot.analyze(query)
        
        # Save report
        report_path = copilot.save_report(result)
        
        print(f"\n✅ Analysis complete! Report saved to: {report_path}")
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Analysis interrupted by user")
        logger.warning("Analysis interrupted by user")
    except Exception as e:
        print(f"\n❌ Analysis failed: {e}")
        logger.exception("Analysis failed with error")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
