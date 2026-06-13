"""
CLI Handler

Handles command-line interface operations for the Pi Coding Agent Configuration Tool.
"""

import sys
import argparse
from typing import List, Dict, Any
from config.core import ConfigManager

class CLIHandler:
    """Handles command-line interface operations."""
    
    def __init__(self, config_manager: ConfigManager):
        """Initialize the CLI handler.
        
        Args:
            config_manager: ConfigManager instance
        """
        self.config_manager = config_manager
    
    def handle_command(self, args: argparse.Namespace) -> None:
        """Handle a command-line command.
        
        Args:
            args: Parsed command-line arguments
        """
        if args.list:
            self.config_manager.list_settings()
        elif args.list_models:
            self.config_manager.list_available_models()
        elif args.default_bedrock_tier:
            self.config_manager.set_bedrock_tier(args.default_bedrock_tier)
        else:
            # Print help if no arguments provided
            parser = self.create_parser()
            parser.print_help()
    
    def create_parser(self) -> argparse.ArgumentParser:
        """Create and configure the argument parser."""
        parser = argparse.ArgumentParser(
            description="Pi Coding Agent Configuration Tool",
            formatter_class=argparse.RawDescriptionHelpFormatter
        )
        
        # Add arguments
        parser.add_argument("--list", action="store_true",
                           help="List all available settings and their values")
        parser.add_argument("--default-bedrock-tier", type=str,
                           help="AWS Bedrock pricing tier: flex, standard, spot")
        parser.add_argument("--list-models", action="store_true",
                           help="List all available models for the current provider")
        parser.add_argument("--help", action="help",
                           help="Show this help message and exit")
        
        return parser
