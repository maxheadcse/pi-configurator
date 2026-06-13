# Changelog

## v1.0.0 - June 13, 2026

### Added
- Complete modular rewrite of Pi Coding Agent Configuration Tool
- Python-based CLI interface with interactive menu
- Support for listing available AI models from various providers
- Configuration of AWS Bedrock pricing tiers (flex, standard, spot)
- JSON-based configuration storage with schema validation
- Comprehensive error handling and user feedback

### Changed
- Replaced broken JavaScript implementation with robust Python implementation
- Modular architecture with separation of concerns
- Moved from monolithic script to well-structured components

### Removed
- All obsolete JavaScript files and modules
- Legacy configuration formats
- Unnecessary dependencies

### Fixed
- All syntax errors and corrupted code
- Inconsistent configuration handling
- Poor user experience in previous versions

### Security
- No hardcoded secrets or API keys in code
- Configuration stored in user's home directory
- No sensitive information exposed

### Documentation
- Comprehensive README.md with usage instructions
- Modular code with clear documentation
- Clear separation of concerns and responsibilities

### Testing
- Full CLI and interactive mode tested
- All features work as expected
- Proper error handling for all edge cases

## Migration Notes

The previous JavaScript implementation has been completely replaced with a Python-based solution. Users should:

1. Run `python main.py --help` to see all available commands
2. Use `--interactive` to enter the menu-driven interface
3. Use `--list` to view current configuration
4. Use `--list-models` to see available AI models
5. Use `--default-bedrock-tier flex` to set Bedrock pricing tier

The configuration directory is now located at `~/.pi/agent/` by default.
