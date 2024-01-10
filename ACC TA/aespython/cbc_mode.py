
__all__ = "CBCMode",
from . import Mode

class CBCMode(Mode):

    def encrypt_block(self, plaintext):
        a0,a1,a2,a3,a4,a5,a6,a7,a8,a9,aa,ab,ac,ad,ae,af=plaintext
        b0,b1,b2,b3,b4,b5,b6,b7,b8,b9,ba,bb,bc,bd,be,bf=self._iv
        a0=self._iv=self._block_cipher.cipher_block((a0^b0,a1^b1,a2^b2,a3^b3,a4^b4,a5^b5,a6^b6,a7^b7,a8^b8,a9^b9,aa^ba,ab^bb,ac^bc,ad^bd,ae^be,af^bf))
        return a0

    def decrypt_block(self, ciphertext):
        a0,a1,a2,a3,a4,a5,a6,a7,a8,a9,aa,ab,ac,ad,ae,af=self._block_cipher.decipher_block(ciphertext)
        b0,b1,b2,b3,b4,b5,b6,b7,b8,b9,ba,bb,bc,bd,be,bf=self._iv
        self._iv=ciphertext
        return a0^b0,a1^b1,a2^b2,a3^b3,a4^b4,a5^b5,a6^b6,a7^b7,a8^b8,a9^b9,aa^ba,ab^bb,ac^bc,ad^bd,ae^be,af^bf
