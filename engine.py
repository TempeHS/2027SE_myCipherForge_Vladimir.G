"""
CipherForge — Encryption Engine
================================
Author: Vladimir G
Date: 2026

This file contains my custom 5-layer encryption algorithm.

PHASES:
  1. Substitution — Replace characters with different ones
  2. Transposition — Rearrange the order of characters
  3. Key-Dependent — Make output depend on a secret password
  4. Noise Injection — Add fake characters to confuse attackers
  5. Wild Card — My unique invention!

RULES:
  - encrypt() MUST be reversible
  - decrypt(encrypt(message)) MUST return the original message
"""

# Your encryption code will go below this line!


def phase1_encrypt(text, key):
    """
    Phase 1: Substitution — Shift every character by a fixed amount.

    This layer changes WHAT each character is (its identity).

    Args:
        text: The plaintext string to encrypt
        key: Dictionary containing encryption settings

    Returns:
        The encrypted string with all characters shifted
    """
    # Get the shift amount from the key (default to 5 if not specified)
    shift = key.get("shift", 5)

    result = ""
    for char in text:
        if 32 <= ord(char) <= 126:  # Printable ASCII range
            position = ord(char) - 32
            new_position = (position + shift) % 95
            result += chr(new_position + 32)
        else:
            result += char

    return result


def phase1_decrypt(text, key):
    """
    Phase 1: Reverse the substitution.

    Decryption shifts in the OPPOSITE direction (subtracts instead of adds).

    Args:
        text: The encrypted string
        key: Dictionary containing the same encryption settings

    Returns:
        The decrypted (original) string
    """
    shift = key.get("shift", 5)

    result = ""
    for char in text:
        if 32 <= ord(char) <= 126:
            position = ord(char) - 32
            new_position = (position - shift) % 95  # SUBTRACT to reverse!
            result += chr(new_position + 32)
        else:
            result += char

    return result


def phase2_encrypt(text, key):
    """
    Phase 2: Transposition — Rearrange character positions.

    Uses block reversal: split into blocks and reverse each one.
    This layer changes WHERE each character is (its position).

    Args:
        text: The string to transform (already Phase 1 encrypted)
        key: Dictionary containing encryption settings

    Returns:
        The transposed string with characters rearranged
    """
    # Get block size from key (default to 4 if not specified)
    block_size = key.get("block_size", 4)

    result = ""

    # Process text in chunks of block_size
    for i in range(0, len(text), block_size):
        # Extract this block (might be shorter at the end)
        block = text[i : i + block_size]
        # Reverse the block and add to result
        result += block[::-1]

    return result


def phase2_decrypt(text, key):
    """
    Phase 2: Reverse the transposition.

    For block reversal, decryption is the same as encryption!
    Reversing a reversed block returns the original.

    Args:
        text: The transposed string
        key: Dictionary containing the same encryption settings

    Returns:
        The un-transposed string
    """
    # Block reversal is self-inverting: encrypt == decrypt
    # Reverse twice = original!
    block_size = key.get("block_size", 4)

    result = ""
    for i in range(0, len(text), block_size):
        block = text[i : i + block_size]
        result += block[::-1]

    return result


def phase3_encrypt(text, key):
    """
    Phase 3: Password-Dependent — Variable shifts based on password.

    Each character is shifted by a different amount determined by
    the corresponding character in the repeating password.
    This destroys frequency patterns!

    Args:
        text: The string to transform (already Phase 1+2 encrypted)
        key: Dictionary containing encryption settings

    Returns:
        The password-encrypted string
    """
    # Get password from key (default to "SECRET" if not specified)
    password = key.get("password", "SECRET")

    result = ""

    for i, char in enumerate(text):
        if 32 <= ord(char) <= 126:
            # Get the password character for this position (cycling)
            password_char = password[i % len(password)]
            # Calculate shift from password character
            password_shift = ord(password_char) % 95

            # Apply the shift (same math as Phase 1)
            position = ord(char) - 32
            new_position = (position + password_shift) % 95
            result += chr(new_position + 32)
        else:
            result += char

    return result


def phase3_decrypt(text, key):
    """
    Phase 3: Reverse the password-dependent encryption.

    CRITICAL: Must use the SAME password that was used for encryption!
    Wrong password = garbage output.

    Args:
        text: The encrypted string
        key: Dictionary with the SAME password used for encryption

    Returns:
        The decrypted string (if password is correct)
    """
    password = key.get("password", "SECRET")

    result = ""

    for i, char in enumerate(text):
        if 32 <= ord(char) <= 126:
            # Get same password character for this position
            password_char = password[i % len(password)]
            password_shift = ord(password_char) % 95

            # SUBTRACT the shift to reverse encryption
            position = ord(char) - 32
            new_position = (position - password_shift) % 95
            result += chr(new_position + 32)
        else:
            result += char

    return result


###############################################
# PHASE 4: NOISE INJECTION
###############################################


def phase4_encrypt(text, key):
    """Insert noise character every N positions."""
    interval = key.get("noise_interval", 3)
    noise = key.get("noise_char", "~")

    result = ""
    count = 0

    for char in text:
        result += char
        count += 1
        # Insert noise after every N real characters
        if count % interval == 0:
            result += noise

    return result


def phase4_decrypt(text, key):
    """Remove noise characters at their known positions."""
    interval = key.get("noise_interval", 3)

    result = ""
    real_count = 0
    i = 0

    while i < len(text):
        result += text[i]
        real_count += 1
        i += 1

        # Skip the noise character after every N real characters
        if real_count % interval == 0 and i < len(text):
            i += 1  # Skip noise

    return result


###############################################
# PHASE 5: WILD CARD - [YOUR NAME HERE]
###############################################


def phase5_encrypt(text, key):
    """[Describe what your phase does]."""
    result = ""

    result = text[::-1]

    return result


def phase5_decrypt(text, key):
    """[Describe how you reverse it]."""
    result = ""

    result = text[::-1]

    return result


def encrypt(plaintext, key):
    """Apply all encryption phases in sequence."""
    result = plaintext

    # Phase 1: Substitution (shift all characters)
    result = phase1_encrypt(result, key)

    # Phase 2: Transposition (reverse blocks)
    result = phase2_encrypt(result, key)

    # Phase 3: Key-dependent (password-based variable shift)
    result = phase3_encrypt(result, key)

    # Phase 4: Noise injection (add decoy characters)
    result = phase4_encrypt(result, key)

    result = phase5_encrypt(result, key)

    return result


def decrypt(ciphertext, key):
    """Reverse all encryption phases."""
    result = ciphertext

    # Decrypt in REVERSE order!

    result = phase5_decrypt(result, key)

    # Phase 4: Remove noise characters
    result = phase4_decrypt(result, key)

    # Phase 3: Reverse password-based shift
    result = phase3_decrypt(result, key)

    # Phase 2: Reverse transposition (self-inverse)
    result = phase2_decrypt(result, key)

    # Phase 1: Reverse substitution (shift back)
    result = phase1_decrypt(result, key)

    return result
