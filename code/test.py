from main import oracle
import cirq, math
import numpy as np

def simulation(circ):
    print("Required circuit: ")
    print(circ)
    simulator = cirq.Simulator()
    val = simulator.simulate(circ)
    state = val.final_state_vector
    print("State obtained: ")
    print(state.tolist())
    return state.tolist()

def checker(state, expected):
    print("Expected state: ", expected)
    flag = True
    for i in range(len(expected)):
        flag = int(np.abs(state[i]) * 1000) == int(1000 * np.abs(expected[i]))
        if not flag:
            break
    print("Correct (global phase is irrelevant)?", (flag and len(state) == len(expected)))


"""
This is a tester for the main program. Here,
I run a few examples and compare the expected and
obtained outputs.
"""

# Example 1
print("\nEXAMPLE 1")
print("---------")

# Given vector: [1, 5, 4, 2]
n = 4
arr = [1, 5, 4, 2]

# It will have a corresponding binary representation
# [001, 101, 100, 010], where 1 and 3 are the satisfying 
# indices.

# Indices converted to binary states: [1, 3] -> [01, 11]
# and hence the required superposition will be 
# 1/sqrt(2) * (|01> + |11>)
expected = [0, math.sqrt(1/2), 0, math.sqrt(1/2)]
checker(simulation(oracle(n, arr)), expected)

# Example 2
print("\nEXAMPLE 2")
print("---------")

# Given vector: [1, 5, 7, 10]
n = 4
arr = [1, 5, 7, 10]

# It will have a corresponding binary representation
# [0001, 0101, 0111, 1010], where 1 and 3 are the satisfying 
# indices.

# Indices converted to binary states: [1, 3] -> [01, 11]
# and hence the required superposition will be 
# 1/sqrt(2) * (|01> + |11>)
expected = [0, math.sqrt(1/2), 0, math.sqrt(1/2)]
checker(simulation(oracle(n, arr)), expected)

# Example 3
print("\nEXAMPLE 3")
print("---------")

# Given vector: [1, 5, 7, 10]
n = 10
arr = [5, 0, 5, 10, 8, 7, 4, 2, 10, 5]

# It will have a corresponding binary representation
# [0101, 0000, 0101, 1010, 1000, 0111, 0100, 0010, 1010, 0101], 
# where 0, 2, 3, 8 and 9 are the satisfying indices.

# Indices converted to binary states: 
# [0, 2, 3, 8, 9] -> [0000, 0010, 0011, 1000, 1001]
# and hence the required superposition will be 
# 1/sqrt(5) * (|0000> + |0010> + |0011> +  |1000> + |1001>)
expected = np.array([1, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0]) * math.sqrt(1/5)
checker(simulation(oracle(n, arr)), expected.tolist())