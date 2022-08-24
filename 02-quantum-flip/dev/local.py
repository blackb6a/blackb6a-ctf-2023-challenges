from math import acos, cos, pi
from qiskit import QuantumCircuit, QuantumRegister, Aer, ClassicalRegister, assemble
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import hashlib
import os

dump = lambda qobj: open('dump', 'w').write(
    str(qobj.to_dict()).replace("'", '"'))

n = 60000

qr = QuantumRegister(1)
cr = ClassicalRegister(n)
qc = QuantumCircuit(qr, cr)

zero_prob = 1 / 5
for i in range(n):
    qc.u(2 * acos(zero_prob**0.5), 0, 0, 0)
    qc.measure(0, i)

sv_sim = Aer.get_backend('qasm_simulator')

seed = 69
qobj = assemble(qc, seed_simulator=seed, shots=1)

dump(qobj)

job = sv_sim.run(qobj)

res = list(job.result().get_counts().keys())[0][::-1]
open('res', 'w').write(res)
# bstart = False
# for i, c in enumerate(res):
#     if not bstart:
#         if c == '0':
#             print(i, '00')
#     else:
#         if c == '1':
#             print(i, '11')
#     bstart = bool(int(c))