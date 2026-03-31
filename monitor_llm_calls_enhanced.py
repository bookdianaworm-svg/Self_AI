#!/usr/bin/env python3
"""
Enhanced Real-time LLM Query Monitor for Self-Improving AI
Now monitors both main responses AND REPL execution logs
"""

import time
import json
import re
import os
from datetime import datetime
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
import threading

class EnhancedLLMCallMonitor:
    def __init__(self):
        self.console = Console()
        self.llm_calls = []
        self.running = True
        self.repl_logs = []
        
    def find_latest_files(self):
        """Find the most recent RLM and REPL log files"""
        rlm_files = []
        repl_files = []
        
        for file in os.listdir("logs"):
            if file.startswith("rlm_") and file.endswith(".jsonl"):
                rlm_files.append(os.path.join("logs", file))
            elif file.startswith("repl_") and file.endswith(".log"):
                repl_files.append(os.path.join("logs", file))
        
        # Sort by modification time, most recent first
        rlm_files.sort(key=os.path.getmtime, reverse=True)
        repl_files.sort(key=os.path.getmtime, reverse=True)
        
        return rlm_files[0] if rlm_files else None, repl_files[0] if repl_files else None
    
    def parse_llm_query_from_text(self, text):
        """Extract llm_query calls and their results from any text"""
        calls = []
        
        # Pattern to match llm_query calls
        query_pattern = r'llm_query\s*\(\s*["\'](.*?)["\'].*?\)'
        
        # Find all query calls
        for match in re.finditer(query_pattern, text, re.IGNORECASE | re.DOTALL):
            query = match.group(1)
            
            # Look for response after the query (within the same text block)
            start_pos = match.end()
            # Look for next 500 characters or until next code block
            end_pos = start_pos + 500
            next_code = text.find('```', start_pos)
            if next_code != -1 and next_code < end_pos:
                end_pos = next_code
            
            response = text[start_pos:end_pos].strip()
            
            calls.append({
                'query': query,
                'response': response,
                'timestamp': datetime.now().strftime("%H:%M:%S"),
                'status': 'completed' if response else 'pending',
                'source': 'response'
            })
        
        return calls
    
    def monitor_rlm_log(self, rlm_file):
        """Monitor RLM log file for llm_query mentions"""
        if not rlm_file:
            return
            
        try:
            with open(rlm_file, 'r') as f:
                # Go to end of file
                f.seek(0, 2)
                
                while self.running:
                    line = f.readline()
                    if not line:
                        time.sleep(0.1)
                        continue
                    
                    try:
                        log_entry = json.loads(line.strip())
                        
                        # Check response for llm_query calls
                        if 'response' in log_entry and log_entry['response']:
                            response_text = log_entry['response']
                            
                            # Check if this contains llm_query calls
                            if 'llm_query' in response_text.lower():
                                calls = self.parse_llm_query_from_text(response_text)
                                
                                for call in calls:
                                    self.llm_calls.append(call)
                                    self.display_llm_call(call)
                        
                        # Also check any REPL execution results
                        if 'repl_execution' in log_entry:
                            repl_result = log_entry['repl_execution']
                            if 'llm_query' in str(repl_result).lower():
                                calls = self.parse_llm_query_from_text(str(repl_result))
                                
                                for call in calls:
                                    call['source'] = 'repl'
                                    self.llm_calls.append(call)
                                    self.display_llm_call(call)
                                    
                    except json.JSONDecodeError:
                        continue
                        
        except Exception as e:
            self.console.print(f"[red]Error monitoring RLM log: {e}[/red]")
    
    def display_llm_call(self, call):
        """Display a single LLM call in a nice format"""
        source_icon = "🔍" if call['source'] == 'response' else "⚙️"
        
        self.console.print(Panel(
            f"{source_icon} [bold cyan]llm_query()[/bold cyan] called at {call['timestamp']} [{call['source']}]\n"
            f"[yellow]Query:[/yellow] {call['query']}\n"
            f"[green]Response:[/green] {call['response'][:300]}{'...' if len(call['response']) > 300 else ''}",
            title="[bold magenta]Sub-LLM Call Detected[/bold magenta]",
            border_style="magenta"
        ))
    
    def create_dashboard(self):
        """Create a live dashboard showing recent LLM calls"""
        table = Table(title="Recent LLM Query Calls")
        table.add_column("Time", style="cyan", width=8)
        table.add_column("Query", style="yellow", width=35)
        table.add_column("Response", style="green", width=40)
        table.add_column("Source", style="blue", width=8)
        table.add_column("Status", style="bold", width=8)
        
        # Show last 5 calls
        for call in self.llm_calls[-5:]:
            source_icon = "🔍" if call['source'] == 'response' else "⚙️"
            status_icon = "✅" if call['status'] == 'completed' else "⏳"
            
            table.add_row(
                call['timestamp'],
                call['query'][:30] + ('...' if len(call['query']) > 30 else ''),
                call['response'][:35] + ('...' if len(call['response']) > 35 else ''),
                source_icon,
                status_icon
            )
        
        return table
    
    def run(self):
        """Start the monitor"""
        self.console.print(Panel(
            "[bold green]Enhanced LLM Query Monitor Started[/bold green]\n"
            "Monitoring for llm_query() calls in real-time...",
            title="[bold blue]AI Sub-LLM Monitor[/bold blue]",
            border_style="blue"
        ))
        
        # Find latest log files
        rlm_file, repl_file = self.find_latest_files()
        
        self.console.print(f"[dim]Monitoring RLM log: {rlm_file or 'None found'}[/dim]")
        self.console.print(f"[dim]Monitoring REPL log: {repl_file or 'None found'}[/dim]")
        
        # Start monitoring thread
        monitor_thread = threading.Thread(target=self.monitor_rlm_log, args=(rlm_file,), daemon=True)
        monitor_thread.start()
        
        try:
            while self.running:
                # Update dashboard every 3 seconds
                dashboard = self.create_dashboard()
                self.console.clear()
                self.console.print(dashboard)
                self.console.print(f"\n[dim]Total calls detected: {len(self.llm_calls)}[/dim]")
                self.console.print("[dim]Press Ctrl+C to stop monitoring[/dim]")
                time.sleep(3)
                
        except KeyboardInterrupt:
            self.running = False
            self.console.print("\n[red]Monitor stopped.[/red]")

if __name__ == "__main__":
    monitor = EnhancedLLMCallMonitor()
    monitor.run()