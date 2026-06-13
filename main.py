"""
Pi Coding Agent Configuration Tool - Main Entry Point

This is the main entry point that orchestrates the modular components.
"""

import sys
import os
import argparse

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import modular components
from config.core import ConfigManager
from config.cli import CLIHandler
from config.interactive import InteractiveHandler

def main():
    """Main entry point for the application."""
    parser = argparse.ArgumentParser(
        description="Pi Coding Agent Configuration Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    # Add arguments
    parser.add_argument("-i", "--interactive", action="store_true",
                       help="Run interactive menu-driven configuration")
    parser.add_argument("-c", "--config-dir", type=str,
                       help="Override config directory (default: ~/.pi/agent)")
    parser.add_argument("--list", action="store_true",
                       help="List all available settings and their values")
    parser.add_argument("--default-bedrock-tier", type=str,
                       help="AWS Bedrock pricing tier: flex, standard, spot")
    parser.add_argument("--list-models", action="store_true",
                       help="List all available models for the current provider")

    
    args = parser.parse_args()
    
    # Initialize config manager
    config_manager = ConfigManager(args.config_dir)
    
    # Handle --list option
    if args.list:
        config_manager.list_settings()
        return
    
    # Handle --list-models option
    if args.list_models:
        config_manager.list_available_models()
        return
    
    # Handle --default-bedrock-tier option
    if args.default_bedrock_tier:
        config_manager.set_bedrock_tier(args.default_bedrock_tier)
        return
    
    # Handle interactive mode
    if args.interactive:
        interactive_handler = InteractiveHandler(config_manager)
        interactive_handler.run()
        return
    
    # Print help if no arguments provided
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

if __name__ == "__main__":
    main()
