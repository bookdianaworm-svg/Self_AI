import os
import base64
import hashlib
from typing import Optional

try:
    from cryptography.fernet import Fernet
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
except ImportError:
    Fernet = None

from rlm.utils.exceptions import ConfigurationError


class KeyEncryption:
    """
    Handles encryption and decryption of API keys using Fernet symmetric encryption.
    Keys are derived from a master password using PBKDF2.
    """

    def __init__(self, master_key: Optional[str] = None):
        """
        Initialize with an optional master key.
        
        Args:
            master_key: Master password for deriving encryption key. If None,
                       reads from MINIMAX_MASTER_KEY environment variable.
        """
        if Fernet is None:
            raise ConfigurationError(
                "cryptography package required for key encryption. "
                "Install with: pip install cryptography"
            )
        
        self._master_key = master_key or os.getenv("MINIMAX_MASTER_KEY")
        if not self._master_key:
            raise ConfigurationError(
                "Master key required for encryption. "
                "Set MINIMAX_MASTER_KEY environment variable or pass master_key parameter."
            )
        self._fernet = self._init_fernet(self._master_key)

    def _init_fernet(self, master_key: str) -> Fernet:
        """Derive a Fernet key from the master password using PBKDF2."""
        salt = b"self_ai_rlm_salt_v1"
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=480000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(master_key.encode()))
        return Fernet(key)

    def encrypt(self, plaintext: str) -> str:
        """
        Encrypt a plaintext string.
        
        Args:
            plaintext: The string to encrypt
            
        Returns:
            Base64-encoded encrypted string
        """
        if not plaintext:
            return ""
        encrypted = self._fernet.encrypt(plaintext.encode())
        return base64.urlsafe_b64encode(encrypted).decode()

    def decrypt(self, ciphertext: str) -> str:
        """
        Decrypt an encrypted string.
        
        Args:
            ciphertext: Base64-encoded encrypted string
            
        Returns:
            Decrypted plaintext string
        """
        if not ciphertext:
            return ""
        encrypted = base64.urlsafe_b64decode(ciphertext.encode())
        decrypted = self._fernet.decrypt(encrypted)
        return decrypted.decode()


class EncryptedKeyStore:
    """
    Manages encrypted API keys stored in a local file.
    """

    def __init__(self, store_path: Optional[str] = None, master_key: Optional[str] = None):
        """
        Initialize the encrypted key store.
        
        Args:
            store_path: Path to the encrypted keys file. Defaults to .rlm_keys.encrypted in user dir.
            master_key: Master key for encryption. If None, reads from environment.
        """
        self._store_path = store_path or os.path.join(
            os.path.expanduser("~"), ".self_ai", "rlm_keys.encrypted"
        )
        self._encryption = KeyEncryption(master_key)
        self._keys: dict[str, str] = {}
        self._load_keys()

    def _load_keys(self) -> None:
        """Load encrypted keys from file."""
        if os.path.exists(self._store_path):
            try:
                with open(self._store_path, "r") as f:
                    for line in f:
                        line = line.strip()
                        if ":" in line:
                            key_name, encrypted_value = line.split(":", 1)
                            self._keys[key_name.strip()] = encrypted_value.strip()
            except Exception:
                self._keys = {}

    def _save_keys(self) -> None:
        """Save encrypted keys to file."""
        os.makedirs(os.path.dirname(self._store_path), exist_ok=True)
        with open(self._store_path, "w") as f:
            for key_name, encrypted_value in self._keys.items():
                f.write(f"{key_name}:{encrypted_value}\n")

    def set_key(self, name: str, value: str) -> None:
        """
        Store an encrypted API key.
        
        Args:
            name: Name for the key (e.g., 'minimax', 'openai')
            value: The API key value
        """
        self._keys[name] = self._encryption.encrypt(value)
        self._save_keys()

    def get_key(self, name: str) -> Optional[str]:
        """
        Retrieve and decrypt an API key.
        
        Args:
            name: Name of the key to retrieve
            
        Returns:
            Decrypted API key or None if not found
        """
        encrypted = self._keys.get(name)
        if encrypted:
            return self._encryption.decrypt(encrypted)
        return None

    def delete_key(self, name: str) -> bool:
        """
        Delete an API key.
        
        Args:
            name: Name of the key to delete
            
        Returns:
            True if deleted, False if not found
        """
        if name in self._keys:
            del self._keys[name]
            self._save_keys()
            return True
        return False

    def list_keys(self) -> list[str]:
        """List all key names (not values)."""
        return list(self._keys.keys())


def get_encrypted_api_key(
    key_name: str,
    env_var: Optional[str] = None,
    encrypted_store: Optional[EncryptedKeyStore] = None
) -> Optional[str]:
    """
    Get an API key, checking environment variable first, then encrypted store.
    
    Priority:
    1. If key_name is 'minimax' and MINIMAX_API_KEY is set, use it
    2. If encrypted store has the key, use decrypted value
    3. Return None
    
    Args:
        key_name: Name of the key (e.g., 'minimax', 'openai')
        env_var: Environment variable name to check first (e.g., 'MINIMAX_API_KEY')
        encrypted_store: Optional EncryptedKeyStore instance
        
    Returns:
        API key value or None
    """
    env_key_map = {
        "minimax": "MINIMAX_API_KEY",
        "openai": "OPENAI_API_KEY",
        "anthropic": "ANTHROPIC_API_KEY",
    }
    
    env_var = env_var or env_key_map.get(key_name)
    if env_var:
        env_value = os.getenv(env_var)
        if env_value:
            return env_value
    
    if encrypted_store:
        return encrypted_store.get_key(key_name)
    
    return None
