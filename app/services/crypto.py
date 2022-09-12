from cryptography.fernet import Fernet

CIPHER_KEY = Fernet.generate_key()
_cipher = Fernet(CIPHER_KEY)


def encrypt(data: str, cipher=_cipher) -> str:
    """
    Encrypts a set of bytes using the service cipher key
    Args:
        data: bytes to encrypt
        cipher: Cipher to use

    Returns:
        str: Encrypted data
    """

    return cipher.encrypt(data.encode()).decode()


def decrypt(token: str, ttl: int = None, cipher=_cipher) -> str:
    """
    Decrypts a token using the service cipher key

    Args:
        token: Token to decrypt
        ttl: Seconds to check for expiration
        cipher: Cipher to use

    Returns:
        str: Decrypted data

    """
    return cipher.decrypt(token.encode(), ttl=ttl).decode()
