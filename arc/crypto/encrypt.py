import os

from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding, rsa
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes


def generate_keypair(
    timestamp: str, email: str, key_path: str
) -> tuple[rsa.RSAPrivateKey, rsa.RSAPublicKey]:
    """Generate an RSA keypair for a recipient."""
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    public_key = private_key.public_key()

    # Ensure the directory exists
    os.makedirs(os.path.dirname(key_path), exist_ok=True)

    # Save the private key
    with open(key_path, "wb") as f:
        f.write(
            private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption(),
            )
        )
    return private_key, public_key


def encrypt_data(data: bytes, public_key: rsa.RSAPublicKey, timestamp: str, email: str) -> str:
    """Encrypt data using AES-256 with RSA key wrapping."""
    # Generate symmetric key for AES
    aes_key = os.urandom(32)  # 256-bit key
    iv = os.urandom(16)  # 128-bit IV

    # Encrypt data with AES
    cipher = Cipher(algorithms.AES(aes_key), modes.CBC(iv))
    encryptor = cipher.encryptor()
    padded_data = data + b"\0" * (16 - len(data) % 16)  # Pad to block size
    encrypted_data = encryptor.update(padded_data) + encryptor.finalize()

    # Encrypt AES key with RSA public key
    encrypted_aes_key = public_key.encrypt(
        aes_key,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None
        ),
    )

    # Create a temporary encrypted file
    temp_name = f"temp-{timestamp}-{email.replace('@', '_at_')}"
    with open(temp_name, "wb") as f:
        f.write(iv + encrypted_aes_key + encrypted_data)
    return temp_name
