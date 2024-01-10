
import os
import hashlib
import struct
import getopt
import sys
import time

from aespython import expandKey, AESCipher, CBCMode

if bytes is str:
    def fix_bytes(byte_list):
        return ''.join(map(chr, byte_list))
else:
    fix_bytes = bytes

class AESalgo:
    def __init__(self):
        self._salt = None
        self._iv = None
        self._key = None

    def new_salt(self):
        self._salt = os.urandom(32)

    def set_iv(self, iv):
        self._iv = iv

    def set_key(self, key):
        self._key = key

    def hex_string_to_int_array(self, hex_string):
        return [int(hex_string[i:i+2], 16) for i in range(0, len(hex_string), 2)]

    def create_key_from_password(self, password):
        if self._salt is None:
            return
        sha512 = hashlib.sha512(password.encode('utf-8') + self._salt[:16]).digest()
        self._key = bytearray(sha512[:32])
        self._iv = [i ^ j for i, j in zip(bytearray(self._salt[16:]), bytearray(sha512[32:48]))]

    def decrypt_file(self, in_file_path, out_file_path, password = None):
        with open(in_file_path, 'rb') as in_file:

            if password is not None:
                self._salt = in_file.read(32)
                self.create_key_from_password(password)

            if self._key is None or self._iv is None:
                return False

            expanded_key = expandKey(self._key)
            aes_cipher_256 = AESCipher(expanded_key)
            aes_cbc_256 = CBCMode(aes_cipher_256)
            aes_cbc_256.set_iv(self._iv)

            filesize = struct.unpack('!L',in_file.read(4))[0]

            with open(out_file_path, 'wb') as out_file:
                while 1:
                    in_data = in_file.read(16)
                    if not in_data:
                        self._salt = None
                        return True
                    else:
                        out_data = aes_cbc_256.decrypt_block(bytearray(in_data))
                        out_file.write(fix_bytes(
                            out_data[:filesize - out_file.tell()] if filesize - out_file.tell() < 16
                            else fix_bytes(out_data)))

    def encrypt_file(self, in_file_path, out_file_path, password = None):
        if password is not None:
            self.new_salt()
            self.create_key_from_password(password)
        else:
            self._salt = None

        if self._key is None or self._iv is None:
            return False

        expanded_key = expandKey(self._key)
        aes_cipher_256 = AESCipher(expanded_key)
        aes_cbc_256 = CBCMode(aes_cipher_256)
        aes_cbc_256.set_iv(self._iv)

        try:
            filesize = os.stat(in_file_path)[6]
        except:
            return False

        with open(in_file_path, 'rb') as in_file:
            with open(out_file_path, 'wb') as out_file:
                if self._salt is not None:
                    out_file.write(self._salt)

                out_file.write(struct.pack('!L',filesize))

                while 1:
                    in_data = bytearray(in_file.read(16))
                    if not in_data:
                        self._salt = None
                        return True
                    else:
                        while len(in_data) < 16:in_data.append(0)
                        out_data = aes_cbc_256.encrypt_block(in_data)
                        out_file.write(fix_bytes(out_data))
