from sympy import sqrt
from sympy.physics.quantum.applyops import apply_operators
from sympy.physics.quantum.qubit import Qubit, IntQubit
from sympy.physics.quantum.grover import *

def return_one_on_two(qubits):
    return True if qubits == IntQubit(2, qubits.nqubits) else False

def return_one_on_one(qubits):
    return True if qubits == IntQubit(1, qubits.nqubits) else False

def test_superposition_basis():
    nbits = 2
    first_half_state = IntQubit(0, nbits)/2 + IntQubit(1, nbits)/2
    second_half_state = IntQubit(2, nbits)/2 + IntQubit(3, nbits)/2
    assert first_half_state + second_half_state == superposition_basis(nbits)

    nbits = 3
    firstq = (1/sqrt(8))*IntQubit(0, nbits) + (1/sqrt(8))*IntQubit(1, nbits)
    secondq = (1/sqrt(8))*IntQubit(2, nbits) + (1/sqrt(8))*IntQubit(3, nbits)
    thirdq = (1/sqrt(8))*IntQubit(4, nbits) + (1/sqrt(8))*IntQubit(5, nbits)
    fourthq = (1/sqrt(8))*IntQubit(6, nbits) + (1/sqrt(8))*IntQubit(7, nbits)
    assert firstq + secondq + thirdq + fourthq == superposition_basis(nbits)

def test_OracleGate():
    v = OracleGate(1, lambda qubits: True if qubits == IntQubit(0) else False)
    assert apply_operators(v*IntQubit(0)) == -IntQubit(0)
    assert apply_operators(v*IntQubit(1)) == IntQubit(1)

    nbits = 2
    v = OracleGate(2, return_one_on_two)
    assert apply_operators(v*IntQubit(0, nbits)) == IntQubit(0, nbits)
    assert apply_operators(v*IntQubit(1, nbits)) == IntQubit(1, nbits)
    assert apply_operators(v*IntQubit(2, nbits)) == -IntQubit(2, nbits)
    assert apply_operators(v*IntQubit(3, nbits)) == IntQubit(3, nbits)

def test_WGate():
    nqubits = 2
    basis_states = superposition_basis(nqubits)
    assert apply_operators(WGate(nqubits)*basis_states) == basis_states

    expected = ((2/sqrt(pow(2, nqubits)))*basis_states) - IntQubit(1, nqubits)
    assert apply_operators(WGate(nqubits)*IntQubit(1, nqubits)) == expected

def test_grover_iteration_1():
    numqubits = 2
    basis_states = superposition_basis(numqubits)
    v = OracleGate(numqubits, return_one_on_one)
    expected = IntQubit(1, numqubits)
    assert apply_operators(grover_iteration(basis_states, v)) == expected

def test_grover_iteration_2():
    numqubits = 4
    basis_states = superposition_basis(numqubits)
    v = OracleGate(numqubits, return_one_on_two)
    # After (pi/4)sqrt(pow(2, n)), IntQubit(2) should have highest prob
    # In this case, after around pi times (3 or 4)
    # print ''
    # print basis_states
    iterated = grover_iteration(basis_states, v)
    iterated = apply_operators(iterated)
    # print iterated
    iterated = grover_iteration(iterated, v)
    iterated = apply_operators(iterated)
    # print iterated
    iterated = grover_iteration(iterated, v)
    iterated = apply_operators(iterated)
    # print iterated
    # In this case, probability was highest after 3 iterations
    # Probability of Qubit('0010') was 251/256 (3) vs 781/1024 (4)
    # Ask about measurement
    expected = (-13*basis_states)/64 + 264*IntQubit(2, numqubits)/256
    assert apply_operators(expected) == iterated

def test_grover():
    nqubits = 2
    assert apply_grover(return_one_on_one, nqubits) == IntQubit(1, nqubits)

    nqubits = 4
    basis_states = superposition_basis(nqubits)
    expected = (-13*basis_states)/64 + 264*IntQubit(2, nqubits)/256
    assert apply_grover(return_one_on_two, 4) == apply_operators(expected)

