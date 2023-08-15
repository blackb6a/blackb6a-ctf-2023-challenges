from qiskit import QuantumCircuit, QuantumRegister, Aer, ClassicalRegister, assemble
from bitarray import bitarray
import os

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
    qobj = assemble(qc, seed_simulator=int.from_bytes(os.urandom(8), 'big') & 0x7FFFFFFFFFFFFFFF, shots=1)
    job = sv_sim.run(qobj)

    res = list(job.result().get_counts().keys())[0]
    return res

def main():
    seq_per_file = 2
    enc_filenames = ['quantum.jpg', 'flag']
    read_files = []

    for fn in enc_filenames:
        arr = bitarray()
        arr.fromfile(fn)
        read_files.append(arr)

    len_seq = sum(map(len, read_files)) * seq_per_file
    seq = generateTrulyRandomSeq(len_seq)

    head = 0
    for i in range(len(enc_filenames)):
        pt = read_files[i]
        len_pt = len(pt)
        for _ in range(seq_per_file):
            assert head + len(pt) <= len_seq
            stream = seq[head:head+len_pt]
            stream = bitarray(stream)
            pt ^= stream
            
            head += len_pt

        pt.tofile(enc_filenames[i] + '.enc')

if __name__ == '__main__':
    main()
