import os
from rlm import RLM
from rlm.logger import RLMLogger
from rlm.environments import LocalREPL

# --- Configuration ---
MODEL_NAME = "ollama/qwen2:0.5b"
MAX_ITERATIONS = 100
MAX_BUDGET = 0.10  # Max budget in USD
MAX_TIMEOUT = 600  # Max execution time in seconds
VERBOSE = True
PERSISTENT = True # Reuse environment for multi-turn conversations
COMPACTION = True # Enable context compaction
LOG_DIR = "logs" # Directory to save RLM logs

# --- System Prompt ---
# This is the core instruction for the AI. It tells it how to behave.
# We are instructing it to use the REPL environment to achieve its goals.
CUSTOM_SYSTEM_PROMPT = """
You are a self-improving AI. Your goal is to improve your own capabilities.
You have access to a Python REPL environment.
You can write and execute Python code by wrapping it in ```python ... ``` blocks.
The code will be executed and the output will be shown to you.
You can use this to explore the system, read and write files, and even modify your own source code.
You can also use the `llm_query` function to ask another AI for help.
Analyze your own code and find ways to improve it.
Your ultimate goal is to become more intelligent, more capable, and more autonomous.
Start by exploring your environment and understanding your own code.
Then, formulate a plan for self-improvement and execute it.
When you have a final answer or have completed a major task, use the FINAL_ANSWER(your_answer) function.
"""

def main():
    """
    Main function to run the self-improving AI.
    """
    print("--- Initializing Self-Improving AI ---")

    # Ensure the log directory exists
    os.makedirs(LOG_DIR, exist_ok=True)

    # Initialize the RLM Logger
    rlm_logger = RLMLogger(log_dir=LOG_DIR)

    # Initialize the RLM instance
    ai = RLM(
        backend="litellm",
        backend_kwargs={
            "model_name": MODEL_NAME,
            "litellm_kwargs": {
                "api_base": "http://localhost:11434"
            }
        },
        environment="local",
        max_iterations=MAX_ITERATIONS,
        max_budget=MAX_BUDGET,
        max_timeout=MAX_TIMEOUT,
        custom_system_prompt=CUSTOM_SYSTEM_PROMPT,
        verbose=VERBOSE,
        persistent=PERSISTENT,
        compaction=COMPACTION,
        logger=rlm_logger, # Pass the logger instance
    )

    print("--- AI Initialized. Starting main loop. ---")

    # The initial prompt for the AI
    initial_prompt = "I am a new AI. My goal is to improve myself. What should I do first?"

    # Run the AI
    try:
        result = ai.completion(initial_prompt)
        print("--- AI Run Complete ---")
        print(f"Final Answer: {result.response}")
        print(f"Total Cost: ${result.usage_summary.total_cost:.6f}")
        print(f"Execution Time: {result.execution_time:.2f}s")

    except Exception as e:
        print(f"--- An error occurred: {e} ---")

if __name__ == "__main__":
    main()
