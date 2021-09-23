import cirq
import cirq_google
import numpy as np
import math

# Convert a number into its binary representation
def binary(num, l):
    s = bin(num).split('0b')[1]
    while len(s) < l:
        s = '0' + s
    return s

# Check if all tupples of adjacent bits are different
def check(num, l):
    binary_val = binary(num, l)
    for i in range(1, len(binary_val)):
        if binary_val[i] == binary_val[i - 1]:
            return False
    return True

# Binary length of an integer
def bin_len(num):
    return int(math.ceil(math.log2(num)))

# Maximum binary length of a list of integers
def max_bin_len(nums):
    return int(max([bin_len(i) for i in nums]))

# List of indices of integers whose binary representation is such 
# that two adjacent bits are different
def get_list(nums):
    l = max_bin_len(nums)
    return [i for i in range(len(nums)) if check(nums[i], l)]

# Generating transition probabilities across the leaves
def generating_leaves(tree, leaves, n):
    # Generating leaves
    index = 2 ** n
    for i in range(len(leaves)):
        tree[index + i] = leaves[i]
    return tree

# Generating transition probabilities across the tree
def generation(tree, leaves, n):
    tree = generating_leaves(tree, leaves, n)
    for i in range(2 ** n - 1, 0, -1):
        l = tree[2 * i]
        r = tree[2 * i + 1]
        tree[i] = (l ** 2 + r ** 2) ** 0.5
        if tree[i] == 0:
            tree[2 * i] = 0
            tree[2 * i  + 1] = 0
        else:
            tree[2 * i] = l / tree[i]
            tree[2 * i + 1] = r / tree[i]
    return tree

# Clean binary representation
def cleaned_binary(ind):
    s = bin(ind).split('0b')[1]
    return [int(x) for x in list(s[1:])]

# Rotation angle theta
def theta(l):
    return np.angle(complex(np.absolute(l), np.absolute((1 - l ** 2) ** 0.5)))

# Applying controlled operations as required]
# to create the state
def construct(tree, number_of_qubits, qubits):
    # assuming that qubits are set to \ket{0}
    circ = cirq.Circuit()
    for x in qubits:
        cirq.reset(x)

    for index in range(1, 2 ** number_of_qubits):
        l = tree[2*index]
        angle = 2 *theta(l)/np.pi
        bits = cleaned_binary(index)

        # applying rotation
        height = int(np.floor(np.log2(index)))
        if height == 0:
            circ.append(cirq.YPowGate(exponent=angle).on(qubits[0]))
        else:
            circ.append(
                cirq.YPowGate(exponent=angle).on(qubits[height]).controlled_by(
                    *qubits[:height], control_values=bits
                )
            )
    return circ

# Creating the required state
def oracle(n, arr):
    """
    Given the array 'arr', we now have to make a list of indices 
    '{i, j, ...}' such that all elements of the array at those 
    indices have a binary representation where any of its two
    adjacent bits are different. 
    """
    # Required list of indices are as follows:
    indices = get_list(arr)
    number_of_qubits = bin_len(n)

    """
    Now, given that we have the required indices,
    we need to create a array ('params') first which represents 
    the required superposed state we want.
    """
    q = cirq.LineQubit.range(number_of_qubits)
    k = 1 / math.sqrt(len(indices))

    params = []
    for i in range(2 ** number_of_qubits):
        if i in indices:
            params.append(k)
        else:
            params.append(0)
    
    """
    Given that we have the array representation of the required 
    state, all that we need is an efficient algorithm/oracle to 
    convert a quantum state |000...0> to one that resembles our
    array.
    In my case, I try to model the state as a probability 
    distribution across a binary tree (similar to the bifurcation 
    graph for QRAM) and apply controlled rotations based on the
    probabilities at any node.
    """
    # Creating a binary tree
    tree = [0] * (2 ** (number_of_qubits + 1))
    tree = generation(tree, params, number_of_qubits)

    """
    This circuit below constructed based on the algorithm
    mentioned above, yields the quantum state (the required 
    superposition) we wanted.
    """
    circ = construct(tree, number_of_qubits, q)
    return circ

if __name__ == "__main__":
    # Taking the vector of integers as input
    arr = []
    n = int(input("Enter number of elements : "))
    print("Enter elements: ")
    for i in range(0, n):
        arr.append(int(input()))
    
    # Obtaining the circuit that represents 
    # the required superposition
    circ = oracle(n, arr)
    print("\nRequired circuit: ")
    print(circ)

    # Simulation to show that the state is 
    # indeed what was needed
    simulator = cirq.Simulator()
    val = simulator.simulate(circ)
    state = val.final_state_vector
    print("\nSuperposition required: ")
    print(state.tolist())