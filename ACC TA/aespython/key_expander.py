
__all__ = "expandKey",
from .aes_tables import sbox,rcon
_expanded_key_length={16:176,24:208,32:240}
def expandKey(new_key):
    _n=len(new_key)
    if _n not in (16,24,32):
        raise RuntimeError('expand(): key size is invalid')
    rcon_iter=1
    _nn16=_n!=16
    _n32=_n==32
    n0=new_key[-4]
    n1=new_key[-3]
    n2=new_key[-2]
    n3=new_key[-1]
    _n0=-_n
    _n1=1-_n
    _n2=2-_n
    _n3=3-_n
    _n=_expanded_key_length[_n]-_n
    nex=new_key.extend
    while 1:
        nx=n0,n1,n2,n3=(sbox[n1]^rcon[rcon_iter]^new_key[_n0],
            sbox[n2]^new_key[_n1],
            sbox[n3]^new_key[_n2],
            sbox[n0]^new_key[_n3])
        nex(nx)
        rcon_iter += 1

        nx=n0,n1,n2,n3=(n0^new_key[_n0],
            n1^new_key[_n1],
            n2^new_key[_n2],
            n3^new_key[_n3])
        nex(nx)
        nx=n0,n1,n2,n3=(n0^new_key[_n0],
            n1^new_key[_n1],
            n2^new_key[_n2],
            n3^new_key[_n3])
        nex(nx)
        nx=n0,n1,n2,n3=(n0^new_key[_n0],
            n1^new_key[_n1],
            n2^new_key[_n2],
            n3^new_key[_n3])
        nex(nx)
        _n -= 16
        if _n <= 0:return new_key
        elif _nn16:
            if _n32:
                nx=n0,n1,n2,n3=(sbox[n0]^new_key[_n0],
                    sbox[n1]^new_key[_n1],
                    sbox[n2]^new_key[_n2],
                    sbox[n3]^new_key[_n3])
                nex(nx)
                _n -= 4
                if _n <= 0:return new_key

            nx=n0,n1,n2,n3=(n0^new_key[_n0],
                n1^new_key[_n1],
                n2^new_key[_n2],
                n3^new_key[_n3])
            nex(nx)
            nx=n0,n1,n2,n3=(n0^new_key[_n0],
                n1^new_key[_n1],
                n2^new_key[_n2],
                n3^new_key[_n3])
            nex(nx)
            if _n32:
                nx=n0,n1,n2,n3=(n0^new_key[_n0],
                    n1^new_key[_n1],
                    n2^new_key[_n2],
                    n3^new_key[_n3])
                nex(nx)
                _n -= 12
            else:_n -= 8
            if _n <= 0:return new_key