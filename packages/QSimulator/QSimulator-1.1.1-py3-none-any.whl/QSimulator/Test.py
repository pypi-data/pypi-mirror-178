from matplotlib.pyplot import polar
from numpy import percentile
from Functions import *

'''

def checkPassword(password, polarizers):
    pass_length = len(password)
    pass_copy = copy(password)
    expected_results = measureQubits(pass_copy)
    result = {}
    for i in range(pass_length):
        result[i] = polarizers[i].polarize(password[i]).measure() == expected_results[i]
    return result

def checkResults(Alice, Bob):
    result = {}
    total = 0
    trues = 0
    for i in range(len(Alice)):
        total += 1
        if Alice[i] == Bob[i]:
            result[i] = True
            trues += 1
        else:
            result[i] = False
    return result
    
print("Test 1:\n------------------\n")
Q1 = Qubit()
Q1.generateRandomQubit()

Pol1 = Polarizer(90)

print(Pol1)
print(Q1.strOriginalState())
Pol1.polarize(Q1)
print(Q1.strOriginalState())
print(Q1.measure())






print("\n\n\nTest 2:\n------------------\n")
for i in range(10):
    q = Qubit().generateRandomQubit()
    print(q.strOriginalState())
    p = Polarizer(random.choice([0, 1])*90)
    print(p)
    p.polarize(q)
    print(q.strOriginalState())
    print(str(q.measure()) + "\n")






print("\n\n\nTest 3:\n------------------\n")
Q1 = Qubit().generateRandomQubit()
print(Q1.strOriginalState())
print(Q1)






print("\n\n\nTest 4:\n------------------\n")
Q1 = Qubit(0.8, 0.6)
print(Q1.strOriginalState())
print(Q1)






print("\n\n\nTest 5:\n------------------\n")
qubits = createQubits(10)
for i in qubits:
    print(i.strOriginalState())






print("\n\n\nTest 6:\n------------------\n")
Qb = Qubit(1, 1)
print(Qb.strOriginalState())






print("\n\n\nTest 7:\n------------------\n")
password = createRandomPassword([Polarizer(0), Polarizer(0), Polarizer(90), Polarizer(90), Polarizer(0), Polarizer(0), Polarizer(90), Polarizer(0)])
for i in password:
    print(i.strOriginalState())
    print(i.measure())






print("\n\n\nTest 8:\n------------------\n")
PolarizedQubit = Qubit(1, 0)
Polarizer1 = Polarizer(0)
Polarizer1.polarize(PolarizedQubit)
print(PolarizedQubit.strOriginalState())

PolarizedQubit = Qubit(1, 0)
Polarizer1 = Polarizer(90)
Polarizer1.polarize(PolarizedQubit)
print(PolarizedQubit.strOriginalState())
PolarizedQubit = Qubit(0, 1)
Polarizer1 = Polarizer(0)
Polarizer1.polarize(PolarizedQubit)
print(PolarizedQubit.strOriginalState())

PolarizedQubit = Qubit(0, 1)
Polarizer1 = Polarizer(90)
Polarizer1.polarize(PolarizedQubit)
print(PolarizedQubit.strOriginalState())






print("\n\n\nTest 9:\n------------------\n")
qubits = [Qubit(1, 0), Qubit(0, 1), Qubit(1, 0), Qubit(1, 0), Qubit(0, 1), Qubit(0, 1), Qubit(1, 0), Qubit(1, 0)]
polarizers = [Polarizer(0), Polarizer(0), Polarizer(90), Polarizer(90), Polarizer(0), Polarizer(0), Polarizer(90), Polarizer(0)]
result = checkPassword(qubits, polarizers)
print(result)






print("\n\n\nTest 10:\n------------------\n")
AlicesQubits = createQubits(10)
AlicesPolarizers = createPolarizers(10)
AlicesPolarized = polarizeQubits(AlicesQubits, AlicesPolarizers)
AlicesResult = measureQubits(AlicesPolarized)
print(AlicesResult)

BobsPolarizers = createPolarizers(10)
BobsPolarized = polarizeQubits(AlicesQubits, BobsPolarizers)
BobsResult = measureQubits(BobsPolarized)
print(BobsResult)


print(checkResults(AlicesResult, BobsResult))






print("\n\n\nTest 11:\n------------------\n")
n = 20
qkd_simulation_list = qkd_simulation(n)
alice_bits = qkd_simulation_list[0]
alice_polarizers = qkd_simulation_list[1]
alice_qubits = qkd_simulation_list[2]
bobs_polarizers = qkd_simulation_list[3]
bobs_bits = qkd_simulation_list[4]

result_comparison = compare_qkd_simulation_results(n, alice_bits, bobs_bits, alice_polarizers, bobs_polarizers)
print(result_comparison)
'''

'''
alphas = 0

for i in range(100):
    qubit = Qubit(0.4160247979575664, 0.9093532688039154)
    #print(qubit.strOriginalState())
    polarizer = Polarizer(90)

    new_qubit = polarizer.polarize(qubit)
    #print(new_qubit.strOriginalState())

    if new_qubit.alpha == 0:
        alphas += 1
    
    #measure = new_qubit.measure()
    #print(measure)
    
print(alphas)
'''




'''
print("\n\n\nTest QKD (BB84 Protocol):\n------------------\n")
n = 10000
qkd_simulation_list = qkd_simulation(n, False)
alice_bits = qkd_simulation_list[0]
alice_polarizers = qkd_simulation_list[1]
alice_qubits = qkd_simulation_list[2]
bobs_polarizers = qkd_simulation_list[3]
bobs_bits = qkd_simulation_list[4]

result_comparison = compare_qkd_simulation_results(n, alice_bits, bobs_bits, alice_polarizers, bobs_polarizers)
print(f"{result_comparison['text']}")
print(f"{round(result_comparison['result'], 2)}% of the bits were the same.")



print("\n\n\nTest QKD (BB84 Protocol) 2:\n------------------\n")
percentage = 0
lowest = 100
highest = 0
for i in range(100):
    n = 10000
    qkd_simulation_list = qkd_simulation(n, False)
    alice_bits = qkd_simulation_list[0]
    alice_polarizers = qkd_simulation_list[1]
    alice_qubits = qkd_simulation_list[2]
    bobs_polarizers = qkd_simulation_list[3]
    bobs_bits = qkd_simulation_list[4]

    result_comparison = compare_qkd_simulation_results(n, alice_bits, bobs_bits, alice_polarizers, bobs_polarizers)
    percentage += result_comparison['result']
    if result_comparison['result'] > highest:
        highest = result_comparison['result']
    if result_comparison['result'] < lowest:
        lowest = result_comparison['result']
        
print(f"{round(percentage/100, 2)}% of the bits were the same.")
print(f"The highest percentage was {round(highest, 2)}%")
print(f"The lowest percentage was {round(lowest, 2)}%")
'''


print("\n\n\nTest QKD (BB84 Protocol) 3:\n------------------\n")
percentage = 0
lowest = 100
highest = 0
for i in range(100):
    n = 10000
    qkd_simulation_list = qkd_simulation(n, False, True)
    alice_bits = qkd_simulation_list[0]
    alice_polarizers = qkd_simulation_list[1]
    alice_qubits = qkd_simulation_list[2]
    bobs_polarizers = qkd_simulation_list[3]
    bobs_bits = qkd_simulation_list[4]

    result_comparison = compare_qkd_simulation_results(n, alice_bits, bobs_bits, alice_polarizers, bobs_polarizers)
    percentage += result_comparison['result']
    if result_comparison['result'] > highest:
        highest = result_comparison['result']
    if result_comparison['result'] < lowest:
        lowest = result_comparison['result']
        
print(f"{round(percentage/100, 2)}% of the bits were the same.")
print(f"The highest percentage was {round(highest, 2)}%")
print(f"The lowest percentage was {round(lowest, 2)}%")



print("\n\n\nTest QKD (BB84 Protocol) 4:\n------------------\n")
alice_bits = [0, 0, 1, 1]
alice_polarizers = [Polarizer(0), Polarizer(90), Polarizer(0), Polarizer(90)]
alice_qubits = [Qubit().createFromBit(alice_bits[i]) for i in range(4)]

mitm_polarizers = [Polarizer(90), Polarizer(90), Polarizer(90), Polarizer(90)]
mitm_bits = measureQubits(polarizeQubits(alice_qubits, mitm_polarizers))
mitm_qubits = [Qubit().createFromBit(mitm_bits[i]) for i in range(4)]

bobs_polarizers = [Polarizer(0), Polarizer(90), Polarizer(0), Polarizer(90)]
bobs_bits = measureQubits(polarizeQubits(mitm_qubits, bobs_polarizers))


print(f"Alice bits: {alice_bits}\n")
print(f"Alice polarizer's angles: {[i.polarizerAngle for i in alice_polarizers]}\n")
print(f"Alice qbits' states: {[i.strOriginalState() for i in alice_qubits]}\n")

print(f"MitM polarizer's angles: {[i.polarizerAngle for i in mitm_polarizers]}\n")
print(f"MitM bits: {mitm_bits}\n")
print(f"MitM qbits' states: {[i.strOriginalState() for i in mitm_qubits]}\n")

print(f"Bob polarizer's angles: {[i.polarizerAngle for i in bobs_polarizers]}\n")
print(f"Bob's results: {bobs_bits}\n")