#!/usr/bin/env python3
"""
CLI entry point for the Interactive Operations Console.
"""

import sys
import argparse


def main():
    parser = argparse.ArgumentParser(
        description="Interactive Operations Console for Self-Improving Swarm System"
    )
    parser.add_argument(
        "--resume",
        type=str,
        metavar="SESSION_ID",
        help="Resume a previous session"
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8765,
        help="WebSocket server port (default: 8765)"
    )
    parser.add_argument(
        "--host",
        type=str,
        default="localhost",
        help="WebSocket server host (default: localhost)"
    )
    parser.add_argument(
        "--websocket",
        action="store_true",
        help="Start WebSocket server for remote connections"
    )
    parser.add_argument(
        "--no-ui",
        action="store_true",
        help="Run without interactive UI (headless mode)"
    )

    args = parser.parse_args()

    if args.resume:
        from rlm.redux import SessionPersistence, create_store
        persistence = SessionPersistence()
        session = persistence.load_session(args.resume)
        if session:
            print(f"Resumed session: {args.resume}")
            store = create_store(session)
        else:
            print(f"Session not found: {args.resume}")
            sys.exit(1)
    else:
        from rlm.redux import create_store
        store = create_store()

    if args.websocket:
        from rlm.console import create_websocket_server
        import asyncio
        server = create_websocket_server(host=args.host, port=args.port, redux_store=store)
        print(f"Starting WebSocket server on {args.host}:{args.port}")
        asyncio.run(server.start())
    else:
        from rlm.console import create_console
        console = create_console(store)
        console.run()


if __name__ == "__main__":
    main()
