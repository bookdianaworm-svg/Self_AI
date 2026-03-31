import json
import sys
import os
from rich.console import Console
from rich.syntax import Syntax
from rich.panel import Panel

def view_log(log_file):
    """
    Parses and displays an RLM log file in a readable, colorized format.
    """
    if not os.path.exists(log_file):
        print(f"Error: Log file not found at {log_file}")
        return

    console = Console()

    with open(log_file, 'r') as f:
        for line in f:
            try:
                data = json.loads(line)
                if 'metadata' in data:
                    console.print(Panel(json.dumps(data['metadata'], indent=2), title="Run Metadata", style="yellow"))
                elif 'iteration' in data:
                    iteration = data['iteration']
                    title = f"Iteration {iteration['iteration_number']} ({iteration['iteration_time']:.2f}s)"
                    
                    content = f"[bold]Prompt:[/bold] {iteration['prompt']}\n\n[bold]Response:[/bold] {iteration['response']}"

                    if iteration['code_blocks']:
                        content += "\n\n[bold]Code Blocks:[/bold]"
                        for block in iteration['code_blocks']:
                            code = block['code']
                            result = block['result']
                            content += f"\n  [bold]Code:[/bold]\n{code}\n  [bold]Result:[/bold] {result}"

                    console.print(Panel(content, title=title, style="green"))

            except json.JSONDecodeError:
                console.print(f"[red]Error decoding JSON from line: {line}[/red]")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        view_log(sys.argv[1])
    else:
        print("Usage: python view_log.py <path_to_log_file>")
