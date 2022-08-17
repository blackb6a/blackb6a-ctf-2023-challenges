from qiskit import QuantumCircuit, QuantumRegister, Aer, ClassicalRegister, assemble
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import hashlib
import os

# from secret import flag


# Quantum is truly random
def generateTrulyRandomSeq(n: int) -> list:
    qr = QuantumRegister(1)
    cr = ClassicalRegister(n)
    qc = QuantumCircuit(qr, cr)

    for i in range(n):
        # Apply H-gate
        qc.h(0)
        # Measure the qubit
        qc.measure(0, i)

    sv_sim = Aer.get_backend('qasm_simulator')
    # I afraid using too much urandom will draw all the entropy so I decided to use quantum (which is truly random as urandom too!)
    # seed = int.from_bytes(os.urandom(8), 'big') & 0x7FFFFFFFFFFFFFFF
    seed = 69
    qobj = assemble(qc, seed_simulator=seed, shots=1)
    job = sv_sim.run(qobj)

    res = list(job.result().get_counts().keys())[0]
    return res


# AES that supports any bit length!
def AES_encrypt(key: bytes, iv: bytes, msg: bytes) -> bytes:
    key = hashlib.md5(key).digest()
    iv = hashlib.md5(iv).digest()
    cipher = AES.new(key=key, iv=iv, mode=AES.MODE_CBC)
    ct = cipher.encrypt(pad(msg, 16))
    return ct


def main():
    n = 20000

    seq = generateTrulyRandomSeq(n)
    iv, key = seq[:-64], seq[-64:]
    print(key, int(key, 2))

    iv = int(iv, 2).to_bytes(len(iv) // 8, 'big')
    key = int(key, 2).to_bytes(len(key) // 8, 'big')

    ct = AES_encrypt(key, iv, flag)

    print('ct =', ct.hex())
    print('iv =', iv.hex())


if __name__ == '__main__':
    main()
