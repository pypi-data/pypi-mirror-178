from copy import copy
from unittest import result
from .Qubit import *
from .Polarizer import *

def createPolarizers(n):
    return [Polarizer().generateRandomPolarizer() for i in range(n)]

def createQubits(n):
    return [Qubit().generateRandomQubit() for i in range(n)]

def createRandomPassword(polarizers):
    return polarizeQubits(createQubits(len(polarizers)), polarizers)

def polarizeQubits(password, polarizers):
    return [polarizers[i].polarize(password[i]) for i in range(len(password))]

def measureQubits(password):
    return [password[i].measure() for i in range(len(password))]

def qkd_simulation(n, print_results=True, mitm_Attack_simulation=False):
    alice_bits = [random.randint(0, 1) for i in range(n)]
    alice_polarizers = createPolarizers(n)
    alice_qubits = [Qubit().createFromBit(alice_bits[i]) for i in range(n)]
    bobs_polarizers = createPolarizers(n)
    
    if mitm_Attack_simulation:
        mitm_polarizers = createPolarizers(n)
        mitm_bits = measureQubits(polarizeQubits(alice_qubits, mitm_polarizers))
        mitm_qubits = [Qubit().createFromBit(mitm_bits[i]) for i in range(n)]
        bobs_bits = measureQubits(polarizeQubits(mitm_qubits, bobs_polarizers))
    else:
        bobs_bits = measureQubits(polarizeQubits(alice_qubits, bobs_polarizers))
    

    if print_results:
        print(f"Alice bits: {alice_bits}\n")
        print(f"Alice polarizer's angles: {[i.polarizerAngle for i in alice_polarizers]}\n")
        print(f"Alice qbits' states: {[i.strOriginalState() for i in alice_qubits]}\n")
        
        if mitm_Attack_simulation:
            print(f"MitM polarizer's angles: {[i.polarizerAngle for i in mitm_polarizers]}\n")
            print(f"MitM bits: {mitm_bits}\n")
            print(f"MitM qbits' states: {[i.strOriginalState() for i in mitm_qubits]}\n")
        
        print(f"Bob polarizer's angles: {[i.polarizerAngle for i in bobs_polarizers]}\n")
        print(f"Bob's results: {bobs_bits}\n")
    
    return [alice_bits, alice_polarizers, alice_qubits, bobs_polarizers, bobs_bits]

def compare_qkd_simulation_results(n, alice_bits, bobs_bits, alice_polarizers, bobs_polarizers):
    result = ""
    trues = 0
    for i in range(n):
        if alice_bits[i]==bobs_bits[i]:
            trues += 1
        result += f"{i}: Bits (A->{alice_bits[i]}, B->{bobs_bits[i]}) EQUAL {alice_bits[i]==bobs_bits[i]} Polarizers (A->{alice_polarizers[i]}, B->{bobs_polarizers[i]}) EQUAL {alice_polarizers[i].polarizerAngle==bobs_polarizers[i].polarizerAngle}\n"
    result += f"Trues: {trues} / {n}"
    return {"text": result, "result": (trues/n)*100}