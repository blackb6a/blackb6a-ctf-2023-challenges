from qiskit import QuantumCircuit, QuantumRegister, Aer, ClassicalRegister, assemble
import os


# Quantum is truly random
def generateTrulyRandomSeq(n: int) -> list:
    qr = QuantumRegister(1)
    cr = ClassicalRegister(n)
    qc = QuantumCircuit(qr, cr)

    for i in range(n):
        # Apply H-gate
        # path: qiskit.circuit.library.HGate
        # https://qiskit.org/documentation/stubs/qiskit.circuit.library.HGate.html?highlight=hgate#qiskit.circuit.library.HGate
        qc.h(0)

        # Measure the qubit
        # path: qiskit.circuit.quantumcircuit.QuantumCircuit.measure
        # https://qiskit.org/documentation/stubs/qiskit.circuit.QuantumCircuit.measure.html?highlight=measure#qiskit.circuit.QuantumCircuit.measure
        qc.measure(0, i)

    # https://qiskit.org/documentation/stubs/qiskit.providers.aer.QasmSimulator.html?highlight=qasmsimulator#qiskit.providers.aer.QasmSimulator
    sv_sim = Aer.get_backend('qasm_simulator')

    # seed = int.from_bytes(os.urandom(8), 'big') & 0x7FFFFFFFFFFFFFFF
    seed = 69

    qobj = assemble(qc, seed_simulator=seed, shots=1)
    job = sv_sim.run(qobj)
    result = job.result()

    res = list(result.get_counts().keys())[0]

    return res


def main():
    n = 100

    fq = []
    for _ in range(1):
        seq = generateTrulyRandomSeq(n)[::-1]
        print(seq)


if __name__ == '__main__':
    main()
