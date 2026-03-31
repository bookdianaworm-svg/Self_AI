#!/usr/bin/env python3
"""
Setup script for configuring encrypted MiniMax API key.

Usage:
    python -m rlm.utils.setup_minimax --set-key "your-api-key"
    python -m rlm.utils.setup_minimax --get-key
    python -m rlm.utils.setup_minimax --delete-key
"""

import argparse
import os
import sys

def main():
    parser = argparse.ArgumentParser(description="Manage encrypted MiniMax API key")
    parser.add_argument("--set-key", dest="api_key", help="Set the MiniMax API key")
    parser.add_argument("--master-key", dest="master_key", help="Master key for encryption (or set MINIMAX_MASTER_KEY env var)")
    parser.add_argument("--get-key", action="store_true", help="Get the stored API key (decrypted)")
    parser.add_argument("--delete-key", action="store_true", help="Delete the stored API key")
    parser.add_argument("--list-keys", action="store_true", help="List all stored key names")
    parser.add_argument("--store-path", dest="store_path", help="Path to encrypted keys file")
    
    args = parser.parse_args()
    
    if not any([args.api_key, args.get_key, args.delete_key, args.list_keys]):
        parser.print_help()
        return
    
    try:
        from rlm.utils.key_encryption import EncryptedKeyStore, KeyEncryption
    except ImportError as e:
        print(f"Error: Required package not installed: {e}")
        print("Install cryptography with: pip install cryptography")
        sys.exit(1)
    
    master_key = args.master_key or os.getenv("MINIMAX_MASTER_KEY")
    if not master_key:
        if args.api_key or args.get_key or args.delete_key or args.list_keys:
            print("Error: Master key required. Set MINIMAX_MASTER_KEY env var or use --master-key")
            sys.exit(1)
    
    store = EncryptedKeyStore(
        store_path=args.store_path,
        master_key=master_key
    )
    
    if args.list_keys:
        keys = store.list_keys()
        if keys:
            print("Stored keys:", ", ".join(keys))
        else:
            print("No keys stored")
    
    if args.set_key:
        store.set_key("minimax", args.api_key)
        print("MiniMax API key stored and encrypted successfully")
    
    if args.get_key:
        key = store.get_key("minimax")
        if key:
            print(f"MiniMax API key: {key}")
        else:
            print("No MiniMax API key stored")
    
    if args.delete_key:
        if store.delete_key("minimax"):
            print("MiniMax API key deleted")
        else:
            print("No MiniMax API key to delete")


if __name__ == "__main__":
    main()
