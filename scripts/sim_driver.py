from node import Node
import numpy as np
import random

# Create a node
n1 = Node(1, 5)

''' Distributions '''

# Normal Distribution
mu, sigma = 0, 0.1 # mean and standard deviation
normalBefore = np.random.normal(mu, sigma, 1000)
# Since normal Distribution goes from -inf to inf, shift by smallest value to get
# all positive numbers
# print(np.min(normal))
normal = np.add(normalBefore, abs(np.min(normalBefore)))
# print(np.min(normal))
# print(np.max(normal))
# print(normal)

# Pareto Distribution
a, m = 3., 2.  # shape and mode
pareto = (np.random.pareto(a, 1000) + 1) * m
# pareto = np.add(paretoBefore, abs(np.min(paretoBefore)))
# print(np.min(pareto))
# print(np.max(pareto))
# print(pareto)

# Uniform/Constant Distribution
uniformBefore = np.random.uniform(-1,0,1000)
# Since normal Distribution goes from -inf to inf, shift by smallest value to get
# all positive numbers
# print(np.min(normal))
uniform = np.add(uniformBefore, abs(np.min(uniformBefore)))
# print(np.min(uniform))
# print(np.max(uniform))
# print(uniform)

print(len(normal))
print(len(pareto))
print(len(uniform))

''' Create network architecture '''

# Define the number of nodes in the network
NUM_NODES = 5

# Create a list of tuples that stores the individual packet flow with a node and
# random arrival time
normal_data_arr = []
pareto_data_arr = []
uniform_data_arr = []

# Defining the time interval between 1 and 50 since only 1000 flows for testing
MAX_TIME = 50

# Iterate over each element in each distibution (aka each packet flow) and assign
# it to a random node
for flow in normal:
    # Packet flow, node assignment, arrival time
    normal_data_arr.append((flow, random.randint(1,NUM_NODES), random.uniform(0,MAX_TIME)))

# Could do all of this in the same for loop, but for clarity's sake
for flow in pareto:
    # Packet flow, node assignment, arrival time
    pareto_data_arr.append((flow, random.randint(1,NUM_NODES), random.uniform(0,MAX_TIME)))

for flow in uniform:
    # Packet flow, node assignment, arrival time
    uniform_data_arr.append((flow, random.randint(1,NUM_NODES), random.uniform(0,MAX_TIME)))

# print('----------Before-------------')
# print(normal_data_arr[0])
# print(pareto_data_arr[0])
# print(uniform_data_arr[0])


''' Sort flow data by arrival time '''

# Sorts in place
# Sort normal
normal_data_arr.sort(key=lambda tup: tup[2])
# Sort pareto
pareto_data_arr.sort(key=lambda tup: tup[2])
# Sort uniform
uniform_data_arr.sort(key=lambda tup: tup[2])
