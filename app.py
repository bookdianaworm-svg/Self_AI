#!/usr/bin/env python3
"""
Self_AI Application Entry Point

This is the main entry point for the Self-Improving Swarm System application.
It initializes the orchestrator, sets up logging, and runs the event loop.

Usage:
    python app.py                  # Start with defaults
    python app.py --debug          # Start with debug logging
    python app.py --log-file=app.log  # Log to file

Press Ctrl+C or send SIGTERM to gracefully shut down.
"""

import argparse
import asyncio
import signal
import sys
from pathlib import Path

APP_NAME = "Self_AI"
APP_VERSION = "1.0.0"


def print_banner() -> None:
    """Print the application banner."""
    banner = f"""
{"=" * 60}
  {APP_NAME} - Self-Improving Swarm System
  Version {APP_VERSION}
{"=" * 60}
  
  Application Runtime Starting...
  
  Press Ctrl+C to stop gracefully.
  
{"=" * 60}
"""
    print(banner)


def parse_args() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Self_AI Application Runtime",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable debug logging",
    )
    parser.add_argument(
        "--log-file",
        type=str,
        default=None,
        help="Path to log file (default: no file logging)",
    )
    parser.add_argument(
        "--log-level",
        type=str,
        default="INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        help="Log level (default: INFO)",
    )
    parser.add_argument(
        "--version",
        action="store_true",
        help="Print version and exit",
    )
    return parser.parse_args()


def setup_signal_handlers(orchestrator) -> None:
    """
    Set up signal handlers for graceful shutdown.

    Args:
        orchestrator: The orchestrator instance to stop on signal
    """

    def handle_signal(signum, frame):
        print(f"\n[Received signal {signum}, initiating graceful shutdown...]")
        orchestrator.stop()

    signal.signal(signal.SIGINT, handle_signal)
    signal.signal(signal.SIGTERM, handle_signal)


async def main_async(args: argparse.Namespace) -> None:
    """
    Main async entry point.

    Args:
        args: Parsed command line arguments
    """
    from rlm.app.logging_config import setup_logging
    from rlm.app.orchestrator import Orchestrator

    log_level = "DEBUG" if args.debug else args.log_level
    setup_logging(
        log_level=log_level,
        log_file=args.log_file,
        structured=True,
    )

    print_banner()

    orchestrator = Orchestrator()
    setup_signal_handlers(orchestrator)

    try:
        orchestrator.start()
        await orchestrator.run_async()
    except KeyboardInterrupt:
        print("\n[Keyboard interrupt received]")
    except Exception as e:
        print(f"\n[Fatal error: {e}]")
        sys.exit(1)
    finally:
        if orchestrator.status.value != "stopped":
            orchestrator.stop()
        print("\n[Application shutdown complete]")


def main() -> None:
    """Main synchronous entry point."""
    args = parse_args()

    if args.version:
        print(f"{APP_NAME} v{APP_VERSION}")
        sys.exit(0)

    try:
        asyncio.run(main_async(args))
    except KeyboardInterrupt:
        print("\n[Shutdown complete]")
        sys.exit(0)
    except Exception as e:
        print(f"\n[Fatal error: {e}]")
        sys.exit(1)


if __name__ == "__main__":
    main()
