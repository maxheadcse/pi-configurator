# Pi Coding Agent Configurator Makefile
# Provides convenient shortcuts for common configuration tasks

.PHONY: help interactive cli list clean backup restore

CONFIGURATOR = configurator.sh

help:
	@echo "=== Pi Coding Agent Configurator ==="
	@echo ""
	@echo "Available targets:"
	@echo "  help              - Show this help message"
	@echo "  interactive       - Run interactive configuration"
	@echo "  cli               - Run CLI mode with defaults"
	@echo "  list              - List all available settings"
	@echo "  clean             - Remove generated settings files"
	@echo "  backup            - Backup current settings to backup.json"
	@echo "  restore           - Restore settings from backup.json"
	@echo "  default-theme     - Set default theme to dark"
	@echo "  default-light     - Set default theme to light"
	@echo "  high-thinking     - Set high thinking level"
	@echo "  medium-thinking   - Set medium thinking level"
	@echo "  low-thinking      - Set low thinking level"
	@echo "  no-telemetry      - Disable install telemetry"
	@echo "  trust-always      - Set project trust to always"
	@echo "  trust-ask         - Set project trust to ask (default)"
	@echo "  trust-never       - Set project trust to never"
	@echo "  show-config       - Display current configuration"
	@echo ""

interactive:
	@./$(CONFIGURATOR) --interactive

cli:
	@./$(CONFIGURATOR)

list:
	@./$(CONFIGURATOR) --list

clean:
	@echo "Removing generated settings files..."
	@rm -f ~/.pi/agent/settings.json
	@echo "Clean complete."

backup:
	@echo "Backing up current settings to backup.json..."
	@cp ~/.pi/agent/settings.json ~/.pi/agent/settings.json.backup.$(shell date +%Y%m%d_%H%M%S)
	@echo "Backup created: ~/.pi/agent/settings.json.backup.$(shell date +%Y%m%d_%H%M%S)"

restore:
	@echo "Restoring settings from backup.json..."
	@if [ ! -f ~/.pi/agent/settings.json.backup.$(shell date +%Y%m%d_%H%M%S) ]; then \
		echo "No backup found for today. Use specific backup date:"; \
		echo "  make restore DATE=20240115_120000"; \
		exit 1; \
	fi
	@cp ~/.pi/agent/settings.json.backup.$(shell date +%Y%m%d_%H%M%S) ~/.pi/agent/settings.json
	@echo "Settings restored from backup."

default-theme:
	@./$(CONFIGURATOR) --default-theme dark

default-light:
	@./$(CONFIGURATOR) --default-theme light

high-thinking:
	@./$(CONFIGURATOR) --default-thinking-level high

medium-thinking:
	@./$(CONFIGURATOR) --default-thinking-level medium

low-thinking:
	@./$(CONFIGURATOR) --default-thinking-level low

no-telemetry:
	@./$(CONFIGURATOR) --no-enable-install-telemetry

trust-always:
	@./$(CONFIGURATOR) --default-project-trust always

trust-ask:
	@./$(CONFIGURATOR) --default-project-trust ask

trust-never:
	@./$(CONFIGURATOR) --default-project-trust never

show-config:
	@echo "=== Current Configuration ==="
	@cat ~/.pi/agent/settings.json | jq .

# Predefined configurations

minimal-config:
	@echo "Applying minimal configuration..."
	@./$(CONFIGURATOR) --default-theme dark --default-thinking-level low --no-enable-install-telemetry --quiet-startup true

developer-config:
	@echo "Applying developer configuration..."
	@./$(CONFIGURATOR) --default-theme dark --default-thinking-level high --default-project-trust always --enable-install-telemetry true

conservative-config:
	@echo "Applying conservative configuration..."
	@./$(CONFIGURATOR) --default-theme dark --default-thinking-level medium --compaction-enabled true --compaction-reserve-tokens 8192 --retry-enabled false

lightweight-config:
	@echo "Applying lightweight configuration..."
	@./$(CONFIGURATOR) --default-theme light --default-thinking-level low --quiet-startup true --no-enable-install-telemetry --no-show-images --no-images-auto-resize --no-images-block-images

# Examples
example-1:
	@echo "Example 1: Light theme with high thinking"
	@./$(CONFIGURATOR) --default-theme light --default-thinking-level high

example-2:
	@echo "Example 2: Disable telemetry and thinking blocks"
	@./$(CONFIGURATOR) --no-enable-install-telemetry --no-hide-thinking-block

example-3:
	@echo "Example 3: Set project trust"
	@./$(CONFIGURATOR) --default-project-trust always

example-4:
	@echo "Example 4: Configure compaction"
	@./$(CONFIGURATOR) --compaction-enabled true --compaction-reserve-tokens 16384 --compaction-keep-recent-tokens 20000

example-5:
	@echo "Example 5: Configure retry settings"
	@./$(CONFIGURATOR) --retry-enabled true --retry-max-retries 3 --retry-base-delay-ms 2000

# Custom settings file
custom-settings:
	@echo "Using custom settings file..."
	@./$(CONFIGURATOR) --settings ~/.pi/agent/custom-settings.json

# Pass-through to configurator with all arguments
$(CONFIGURATOR):
	@./$(CONFIGURATOR) $(filter-out $@,$(MAKECMDGOALS))

%:
	@:
