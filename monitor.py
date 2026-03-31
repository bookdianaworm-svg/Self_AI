#!/usr/bin/env python3
"""
AI Monitor - Color-coded visualization of AI thoughts vs script logs
"""
import json
import re
from pathlib import Path
from datetime import datetime

class AIMonitor:
    def __init__(self):
        self.log_file = Path("/mnt/c/Users/drave/Documents/trae_projects/Self_AI/logs/ai_log_20260218.log")
        self.colors = {
            'script_action': '\033[94m',    # Blue - what the script is doing
            'ai_thought': '\033[92m',      # Green - AI's actual thoughts
            'ai_action': '\033[93m',      # Yellow - AI's planned actions
            'error': '\033[91m',           # Red - errors
            'success': '\033[92m',          # Green - successes
            'reset': '\033[0m'              # Reset
        }
        
    def colorize(self, text, color_type):
        return f"{self.colors[color_type]}{text}{self.colors['reset']}"
    
    def parse_log_line(self, line):
        """Parse a log line and categorize it"""
        if "INFO:" in line:
            timestamp = line.split("]")[0] + "]"
            message = line.split("INFO:")[1].strip()
            
            # Categorize the message
            if "🤔 Self-reflection prompt:" in message:
                return {
                    'type': 'ai_thinking',
                    'timestamp': timestamp,
                    'prompt': message.split("🤔 Self-reflection prompt:")[1].strip()
                }
            elif "Self-reflection error:" in message:
                return {
                    'type': 'error',
                    'timestamp': timestamp,
                    'error': message.split("Self-reflection error:")[1].strip()
                }
            elif "📖 Reading own source code" in message:
                return {
                    'type': 'script_action',
                    'timestamp': timestamp,
                    'action': "Analyzing its own code structure"
                }
            elif "💾 Memory added:" in message:
                return {
                    'type': 'memory',
                    'timestamp': timestamp,
                    'memory_id': message.split("💾 Memory added:")[1].strip()
                }
            else:
                return {
                    'type': 'script_info',
                    'timestamp': timestamp,
                    'message': message
                }
        elif "ERROR:" in line:
            timestamp = line.split("]")[0] + "]"
            error = line.split("ERROR:")[1].strip()
            return {
                'type': 'error',
                'timestamp': timestamp,
                'error': error
            }
        
        return None
    
    def display_real_time(self):
        """Display color-coded output in real-time"""
        print(self.colorize("🤖 AI MONITOR - Color-Coded Output", 'ai_thought'))
        print(self.colorize("=" * 50, 'ai_thought'))
        print()
        
        print(self.colorize("🔵 BLUE = Script Actions (what the code is doing)", 'script_action'))
        print(self.colorize("🟢 GREEN = AI Thoughts (when we get them)", 'ai_thought'))
        print(self.colorize("🟡 YELLOW = AI Planned Actions", 'ai_action'))
        print(self.colorize("🔴 RED = Errors", 'error'))
        print(self.colorize("🟢 GREEN = Success/Memory", 'success'))
        print()
        
        # Read current log file
        try:
            with open(self.log_file, 'r') as f:
                lines = f.readlines()
                
            for line in lines[-20:]:  # Show last 20 lines
                parsed = self.parse_log_line(line.strip())
                if parsed:
                    self.display_parsed_line(parsed)
                    
        except FileNotFoundError:
            print(self.colorize("Log file not found. Make sure the AI is running.", 'error'))
    
    def display_parsed_line(self, parsed):
        """Display a parsed line with appropriate coloring"""
        if parsed['type'] == 'ai_thinking':
            print(self.colorize(f"🤔 AI THINKING:", 'ai_thought'))
            print(self.colorize(f"   Prompt: {parsed['prompt']}", 'ai_thought'))
            
        elif parsed['type'] == 'error':
            print(self.colorize(f"❌ ERROR: {parsed['error']}", 'error'))
            
        elif parsed['type'] == 'script_action':
            print(self.colorize(f"🔧 SCRIPT: {parsed['action']}", 'script_action'))
            
        elif parsed['type'] == 'memory':
            print(self.colorize(f"💾 MEMORY: Added memory with ID {parsed['memory_id']}", 'success'))
            
        elif parsed['type'] == 'script_info':
            print(self.colorize(f"ℹ️  SCRIPT: {parsed['message']}", 'script_action'))
    
    def watch_for_ai_thoughts(self):
        """Watch for actual AI thoughts (when they appear)"""
        print(self.colorize("\n👁️  WATCHING FOR AI THOUGHTS...", 'ai_thought'))
        print(self.colorize("When the AI successfully reflects, you'll see:", 'ai_thought'))
        print(self.colorize("🟢 AI THOUGHTS:", 'ai_thought'))
        print(self.colorize("   thoughts: 'I need to improve my Ollama command syntax...'", 'ai_thought'))
        print(self.colorize("   actions: ['fix_ollama_command', 'test_new_syntax']", 'ai_action'))
        print(self.colorize("   risks: ['breaking existing functionality']", 'ai_action'))
        print(self.colorize("   success_metrics: ['successful self-reflection calls']", 'ai_action'))

if __name__ == "__main__":
    monitor = AIMonitor()
    monitor.display_real_time()
    monitor.watch_for_ai_thoughts()