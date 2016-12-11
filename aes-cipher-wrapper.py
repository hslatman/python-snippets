# using the improved cryptography library from https://cryptography.io/
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend


class AESCipher(object):
    """Provides abstraction for AES initialization, encryption and decryption."""

    def __init__(self, key, iv):
        self.cipher = Cipher(algorithms.AES(bytes(key)), modes.CBC(bytes(iv)), backend=default_backend())
        self.encryptor = self.cipher.encryptor()
        self.decryptor = self.cipher.decryptor()
        self.padder = padding.PKCS7(128).padder()
        self.unpadder = padding.PKCS7(128).unpadder()

    def encrypt(self, data):
        """Performs AES CBC encryption."""
        data = self.padder.update(bytes(data)) + self.padder.finalize()
        enc = self.encryptor.update(data) + self.encryptor.finalize()
        return bytearray(enc)

    def decrypt(self, data):
        """Performs AES CBC decryption."""
        dec = self.decryptor.update(bytes(data)) + self.decryptor.finalize()
        data = self.unpadder.update(dec)
        return data + self.unpadder.finalize()
        
        
key = "00000000000000000000000000000000"
iv = "0000000000000000"
aes = AESCipher(key, iv)
plain = "11111111111111110000000000000000"
print len(plain), plain
encrypted = aes.encrypt(plain)
print len(encrypted), encrypted
decrypted = aes.decrypt(encrypted)
print len(encrypted), decrypted