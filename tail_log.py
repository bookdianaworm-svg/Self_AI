import json
import sys
import os
import time
from rich.console import Console
from rich.syntax import Syntax
from rich.panel import Panel

def tail_log(log_file):
    """
    Continuously reads new lines from a log file and displays them in a readable, colorized format.
    """
    if not os.path.exists(log_file):
        print(f"Error: Log file not found at {log_file}")
        return

    console = Console()
    console.print(Panel("[bold cyan]Starting real-time AI log monitor...[/bold cyan]", title="AI Monitor"))

    with open(log_file, 'r') as f:
        # Go to the end of the file
        f.seek(0, 2)

        while True:
            line = f.readline()
            if not line:
                time.sleep(0.1) # Wait for new data
                continue

            try:
                data = json.loads(line)
                if 'metadata' in data:
                    console.print(Panel(json.dumps(data['metadata'], indent=2), title="Run Metadata", style="yellow"))
                elif 'iteration' in data:
                    iteration = data['iteration']
                    title = f"Iteration {iteration['iteration_number']} ({iteration['iteration_time']:.2f}s)"
                    
                    # AI's thoughts/response
                    response_content = iteration['response']
                    console.print(Panel(response_content, title=f"{title} - AI Thoughts", style="blue"))

                    # Code blocks
                    if iteration['code_blocks']:
                        for block in iteration['code_blocks']:
                            code = block['code']
                            result = block['result']
                            console.print(Panel(Syntax(code, "python", theme="monokai", line_numbers=True), title="Code Block", style="green"))
                            console.print(Panel(result, title="Code Result", style="magenta"))

            except json.JSONDecodeError:
                console.print(f"[red]Error decoding JSON from line: {line}[/red]")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        tail_log(sys.argv[1])
    else:
        print("Usage: python tail_log.py <path_to_log_file>")
