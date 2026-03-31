#!/usr/bin/env python3
"""
Real-time LLM Query Monitor for Self-Improving AI
Attaches to running RLM process and logs all llm_query calls
"""

import time
import json
import re
import os
from datetime import datetime
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.live import Live
from rich.layout import Layout
from rich.text import Text
import threading

class LLMCallMonitor:
    def __init__(self, log_file_pattern="logs/rlm_*.jsonl"):
        self.console = Console()
        self.log_file_pattern = log_file_pattern
        self.current_log_file = None
        self.llm_calls = []
        self.running = True
        
    def find_latest_log_file(self):
        """Find the most recent RLM log file"""
        log_files = []
        for file in os.listdir("logs"):
            if file.startswith("rlm_") and file.endswith(".jsonl"):
                log_files.append(os.path.join("logs", file))
        
        if log_files:
            # Sort by modification time, most recent first
            log_files.sort(key=os.path.getmtime, reverse=True)
            return log_files[0]
        return None
    
    def parse_llm_query_from_response(self, response_text):
        """Extract llm_query calls and their results from AI response"""
        # Pattern to match llm_query calls
        query_pattern = r'llm_query\s*\(\s*["\'](.*?)["\'].*?\)'
        
        # Pattern to match potential responses (this is tricky since we need to infer)
        # Look for sections that might be responses to llm_query
        response_sections = re.split(r'\n\n+', response_text)
        
        calls = []
        for i, section in enumerate(response_sections):
            query_match = re.search(query_pattern, section, re.IGNORECASE | re.DOTALL)
            if query_match:
                query = query_match.group(1)
                
                # Try to find the response (next section or within same section)
                response = ""
                if i + 1 < len(response_sections):
                    response = response_sections[i + 1].strip()
                else:
                    # Look for response within same section after the query
                    after_query = section[query_match.end():]
                    if len(after_query.strip()) > 50:  # Assume substantial text is response
                        response = after_query.strip()
                
                calls.append({
                    'query': query,
                    'response': response,
                    'timestamp': datetime.now().strftime("%H:%M:%S"),
                    'status': 'completed' if response else 'pending'
                })
        
        return calls
    
    def monitor_log_file(self):
        """Monitor the RLM log file for new entries"""
        while self.running:
            try:
                latest_log = self.find_latest_log_file()
                if latest_log and latest_log != self.current_log_file:
                    self.current_log_file = latest_log
                    self.console.print(f"[yellow]Monitoring new log file: {latest_log}[/yellow]")
                
                if self.current_log_file and os.path.exists(self.current_log_file):
                    # Tail the last few lines of the log file
                    try:
                        with open(self.current_log_file, 'r') as f:
                            # Go to end of file
                            f.seek(0, 2)
                            
                            # Read new lines as they appear
                            while self.running:
                                line = f.readline()
                                if not line:
                                    time.sleep(0.1)
                                    continue
                                
                                try:
                                    log_entry = json.loads(line.strip())
                                    self.process_log_entry(log_entry)
                                except json.JSONDecodeError:
                                    continue
                                    
                    except (IOError, OSError):
                        time.sleep(1)
                        
            except Exception as e:
                self.console.print(f"[red]Error monitoring log: {e}[/red]")
                time.sleep(5)
    
    def process_log_entry(self, entry):
        """Process a new log entry and extract llm_query information"""
        if 'response' in entry and entry['response']:
            response_text = entry['response']
            
            # Check if this contains llm_query calls
            if 'llm_query' in response_text.lower():
                calls = self.parse_llm_query_from_response(response_text)
                
                for call in calls:
                    self.llm_calls.append(call)
                    
                    # Display the call
                    self.display_llm_call(call)
    
    def display_llm_call(self, call):
        """Display a single LLM call in a nice format"""
        self.console.print(Panel(
            f"[bold cyan]llm_query()[/bold cyan] called at {call['timestamp']}\n"
            f"[yellow]Query:[/yellow] {call['query']}\n"
            f"[green]Response:[/green] {call['response'][:200]}{'...' if len(call['response']) > 200 else ''}",
            title="[bold magenta]Sub-LLM Call Detected[/bold magenta]",
            border_style="magenta"
        ))
    
    def create_dashboard(self):
        """Create a live dashboard showing recent LLM calls"""
        layout = Layout()
        
        table = Table(title="Recent LLM Query Calls")
        table.add_column("Time", style="cyan", width=8)
        table.add_column("Query", style="yellow", width=40)
        table.add_column("Response", style="green", width=50)
        table.add_column("Status", style="bold", width=10)
        
        # Show last 5 calls
        for call in self.llm_calls[-5:]:
            table.add_row(
                call['timestamp'],
                call['query'][:35] + ('...' if len(call['query']) > 35 else ''),
                call['response'][:45] + ('...' if len(call['response']) > 45 else ''),
                f"[green]✓[/green] {call['status']}" if call['status'] == 'completed' else f"[yellow]⏳[/yellow] {call['status']}"
            )
        
        return table
    
    def run(self):
        """Start the monitor"""
        self.console.print(Panel(
            "[bold green]LLM Query Monitor Started[/bold green]\n"
            "Monitoring for llm_query() calls in real-time...",
            title="[bold blue]AI Sub-LLM Monitor[/bold blue]",
            border_style="blue"
        ))
        
        # Start monitoring thread
        monitor_thread = threading.Thread(target=self.monitor_log_file, daemon=True)
        monitor_thread.start()
        
        try:
            while self.running:
                # Update dashboard every 5 seconds
                dashboard = self.create_dashboard()
                self.console.clear()
                self.console.print(dashboard)
                self.console.print(f"\n[dim]Monitoring: {self.current_log_file or 'No log file found'}[/dim]")
                self.console.print("[dim]Press Ctrl+C to stop monitoring[/dim]")
                time.sleep(5)
                
        except KeyboardInterrupt:
            self.running = False
            self.console.print("\n[red]Monitor stopped.[/red]")

if __name__ == "__main__":
    monitor = LLMCallMonitor()
    monitor.run()