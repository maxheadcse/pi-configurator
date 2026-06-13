"""
Terminal User Interface for Pi Configurator
Inspired by Linux kernel's make menuconfig
"""

import os
import sys
import curses
from typing import List, Dict, Any, Callable
from config.core import ConfigManager

class TUI:
    """Terminal User Interface for configuration."""
    
    def __init__(self, config_manager: ConfigManager):
        """Initialize the TUI."""
        self.config_manager = config_manager
        self.current_menu = "main"
        self.menus = self._build_menus()
        self.current_selection = 0
        self.running = True
    
    def _build_menus(self) -> Dict[str, Dict]:
        """Build the menu structure."""
        return {
            "main": {
                "title": "Pi Coding Agent Configuration",
                "items": [
                    ("Model & AI Settings", "model", "Configure AI models and providers"),
                    ("UI & Display", "ui", "Theme, layout and visual settings"),
                    ("System & Performance", "system", "Compaction, retry and delivery settings"),
                    ("Resources & Extensions", "resources", "Manage extensions, skills and packages"),
                    ("Bedrock Pricing", "bedrock", "AWS Bedrock tier configuration"),
                    ("Search Settings", "search", "Search for specific settings"),
                    ("View Configuration", "view", "View current settings"),
                    ("Save & Exit", "save", "Save configuration and exit"),
                    ("Exit Without Saving", "exit", "Exit without saving changes")
                ]
            },
            "model": {
                "title": "Model & AI Settings",
                "items": [
                    ("Default Provider", "provider", f"Current: {self.config_manager.get_provider()}"),
                    ("Default Model", "model", f"Current: {self.config_manager.settings.get('model', {}).get('defaultModel', 'Not set')}"),
                    ("Thinking Level", "thinking", f"Current: {self.config_manager.get_thinking_level()}"),
                    ("Hide Thinking Block", "thinking_block", f"Current: {self.config_manager.settings.get('model', {}).get('hideThinkingBlock', False)}"),
                    ("Back to Main Menu", "main", "Return to main menu")
                ]
            },
            # Add more menus as needed
        }
    
    def _draw_header(self, stdscr):
        """Draw the header with title and navigation info."""
        height, width = stdscr.getmaxyx()
        
        # Clear screen
        stdscr.clear()
        
        # Draw border
        stdscr.border()
        
        # Draw title
        menu_title = self.menus[self.current_menu]["title"]
        title = f" 🎛️  {menu_title} "
        stdscr.addstr(1, 2, title, curses.A_BOLD | curses.A_UNDERLINE)
        
        # Draw navigation help
        nav_help = "↑↓ Navigate  │  Enter Select  │  q Quit  │  ? Help"
        stdscr.addstr(1, width - len(nav_help) - 3, nav_help, curses.A_DIM)
        
        # Draw separator
        stdscr.hline(2, 1, curses.ACS_HLINE, width - 2)
    
    def _draw_menu(self, stdscr):
        """Draw the current menu."""
        height, width = stdscr.getmaxyx()
        menu_items = self.menus[self.current_menu]["items"]
        
        # Draw menu items
        for i, (text, action, description) in enumerate(menu_items):
            if i >= height - 5:  # Don't draw past screen bottom
                break
                
            row = 4 + i
            if i == self.current_selection:
                # Selected item
                stdscr.addstr(row, 4, f"▶ {text}", curses.A_REVERSE)
                stdscr.addstr(row, width // 2, description, curses.A_DIM)
            else:
                # Unselected item
                stdscr.addstr(row, 6, text)
                stdscr.addstr(row, width // 2, description, curses.A_DIM)
    
    def _draw_footer(self, stdscr):
        """Draw the footer with status information."""
        height, width = stdscr.getmaxyx()
        
        # Draw separator
        stdscr.hline(height - 3, 1, curses.ACS_HLINE, width - 2)
        
        # Draw status
        status = f"Selection: {self.current_selection + 1}/{len(self.menus[self.current_menu]['items'])}"
        stdscr.addstr(height - 2, 2, status, curses.A_DIM)
        
        # Draw key hints
        if self.current_menu == "main":
            hints = "F1 Help  │  F2 Search  │  F10 Save & Exit"
        else:
            hints = "F1 Help  │  ESC Back  │  F10 Save"
        stdscr.addstr(height - 2, width - len(hints) - 2, hints, curses.A_DIM)
    
    def _handle_input(self, stdscr):
        """Handle user input."""
        key = stdscr.getch()
        menu_items = self.menus[self.current_menu]["items"]
        
        if key == curses.KEY_UP or key == ord('k'):
            # Move up
            self.current_selection = max(0, self.current_selection - 1)
        elif key == curses.KEY_DOWN or key == ord('j'):
            # Move down
            self.current_selection = min(len(menu_items) - 1, self.current_selection + 1)
        elif key == ord('q') or key == 27:  # q or ESC
            # Quit or go back
            if self.current_menu == "main":
                self.running = False
            else:
                self.current_menu = "main"
                self.current_selection = 0
        elif key == ord('?') or key == curses.KEY_F1:
            # Help
            self._show_help(stdscr)
        elif key == ord('\n') or key == ord(' '):
            # Select item
            if self.current_selection < len(menu_items):
                text, action, description = menu_items[self.current_selection]
                self._handle_action(action)
        elif key == curses.KEY_F10:
            # Save and exit
            if self.current_menu == "main":
                self._handle_action("save")
            else:
                self._handle_action("main")
    
    def _handle_action(self, action: str):
        """Handle menu actions."""
        if action == "main":
            self.current_menu = "main"
            self.current_selection = 0
        elif action == "save":
            self.config_manager.save_settings()
            self.running = False
            print("\n✅ Configuration saved successfully!")
        elif action == "exit":
            self.running = False
            print("\n❌ Exited without saving.")
        elif action == "provider":
            self._edit_provider()
        # Add more action handlers as needed
    
    def _edit_provider(self):
        """Edit the AI provider."""
        providers = ["anthropic", "openai", "google", "aws-bedrock"]
        current = self.config_manager.get_provider()
        
        print(f"\nCurrent provider: {current}")
        print("Available providers:")
        for i, provider in enumerate(providers, 1):
            marker = "▶" if provider == current else " "
            print(f"  {marker} {i}. {provider}")
        
        choice = input("\nSelect provider (number or name): ").strip()
        
        if choice.isdigit() and 1 <= int(choice) <= len(providers):
            new_provider = providers[int(choice) - 1]
        elif choice in providers:
            new_provider = choice
        else:
            print("❌ Invalid provider")
            input("Press Enter to continue...")
            return
        
        self.config_manager.settings.setdefault('model', {})['defaultProvider'] = new_provider
        print(f"✅ Provider set to: {new_provider}")
        input("Press Enter to continue...")
        
        # Rebuild menus to update current values
        self.menus = self._build_menus()
    
    def _show_help(self, stdscr):
        """Show help screen."""
        height, width = stdscr.getmaxyx()
        
        # Save current screen
        help_screen = [stdscr.instr(y, 0, width) for y in range(height)]
        
        # Draw help overlay
        stdscr.clear()
        stdscr.border()
        stdscr.addstr(1, 2, " 📖 Help - Pi Configurator ", curses.A_BOLD)
        stdscr.hline(2, 1, curses.ACS_HLINE, width - 2)
        
        help_text = [
            "Navigation:",
            "  ↑↓ arrows or j/k - Move selection",
            "  Enter or Space   - Select item",
            "  q or ESC         - Quit/Go back",
            "  ? or F1          - Show help",
            "",
            "Main Menu:",
            "  F10              - Save & Exit",
            "  F2               - Search settings",
            "",
            "Editing:",
            "  Follow prompts to edit values",
            "  Changes are applied immediately",
            "  Save to persist changes",
            "",
            "Press any key to continue..."
        ]
        
        for i, line in enumerate(help_text):
            stdscr.addstr(4 + i, 4, line)
        
        stdscr.refresh()
        stdscr.getch()
        
        # Restore screen
        for y, line in enumerate(help_screen):
            stdscr.move(y, 0)
            stdscr.clrtoeol()
            stdscr.addstr(y, 0, line[0])
        stdscr.refresh()
    
    def run(self) -> None:
        """Run the TUI."""
        try:
            # Initialize curses
            stdscr = curses.initscr()
            curses.noecho()
            curses.cbreak()
            stdscr.keypad(True)
            curses.curs_set(0)  # Hide cursor
            
            # Check if terminal supports color
            if curses.has_colors():
                curses.start_color()
                curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)  # Selected item
                curses.init_pair(2, curses.COLOR_CYAN, curses.COLOR_BLACK)   # Titles
                curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)  # Success
                curses.init_pair(4, curses.COLOR_RED, curses.COLOR_BLACK)    # Errors
            
            # Main loop
            while self.running:
                self._draw_header(stdscr)
                self._draw_menu(stdscr)
                self._draw_footer(stdscr)
                stdscr.refresh()
                self._handle_input(stdscr)
            
        except KeyboardInterrupt:
            print("\n\n❌ Operation cancelled by user.")
        except Exception as e:
            print(f"\n\n❌ Error: {e}")
        finally:
            # Clean up curses
            curses.nocbreak()
            stdscr.keypad(False)
            curses.echo()
            curses.endwin()
            print("\n👋 Thank you for using Pi Configurator!")

class TUIHandler:
    """Handler for TUI operations."""
    
    def __init__(self, config_manager: ConfigManager):
        self.config_manager = config_manager
    
    def run(self) -> None:
        """Run the TUI."""
        tui = TUI(self.config_manager)
        tui.run()