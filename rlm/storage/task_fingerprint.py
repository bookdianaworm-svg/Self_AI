"""MinHash LSH fingerprinting for task descriptions."""

from typing import cast

from datasketch import MinHash

# MinHash parameters
K = 3  # k-shingle size
NUM_PERM = 128  # number of permutations (128-bit fingerprint)


def compute(description: str) -> str:
    """Compute a MinHash fingerprint for a task description.

    Args:
        description: The task description string.

    Returns:
        A 64-character hexadecimal string (128-bit fingerprint).
    """
    tokens = description.split()
    minhash = MinHash(num_perm=NUM_PERM)

    for i in range(len(tokens) - K + 1):
        shingle = " ".join(tokens[i : i + K])
        minhash.update(shingle.encode("utf-8"))

    return cast(bytes, minhash.byteshex()).hex()


def similarity(fingerprint_a: str, fingerprint_b: str) -> float:
    """Estimate Jaccard similarity between two MinHash fingerprints.

    Args:
        fingerprint_a: Hex string from compute().
        fingerprint_b: Hex string from compute().

    Returns:
        Jaccard similarity estimate between 0 and 1.
    """
    # Reconstruct MinHash objects from bytes
    bytes_a = bytes.fromhex(fingerprint_a)
    bytes_b = bytes.fromhex(fingerprint_b)

    minhash_a = MinHash(bytes=bytes_a)
    minhash_b = MinHash(bytes=bytes_b)

    return cast(float, minhash_a.jaccard(minhash_b))
