from node import Node
import numpy as np
import random
import time

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
print(np.min(normal))
print(np.max(normal))
# print(normal)

# Pareto Distribution
a, m = 3., 2.  # shape and mode
pareto = (np.random.pareto(a, 1000) + 1) * m
# pareto = np.add(paretoBefore, abs(np.min(paretoBefore)))
print(np.min(pareto))
print(np.max(pareto))
# print(pareto)

# Uniform/Constant Distribution
uniformBefore = np.random.uniform(-1,0,1000)
# Since normal Distribution goes from -inf to inf, shift by smallest value to get
# all positive numbers
# print(np.min(normal))
uniform = np.add(uniformBefore, abs(np.min(uniformBefore)))
print(np.min(uniform))
print(np.max(uniform))
# print(uniform)

# print(len(normal))
# print(len(pareto))
# print(len(uniform))

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



''' Information for algorithms '''

# Get the total number of packet flows in each of the nodes
# Be careful with the index here -- may want to change the above random node to 0 to max_nodes - 1
normal_count_flows_remaining = [None] * NUM_NODES
_, norm_nodes, _ = zip(*normal_data_arr)
pareto_count_flows_remaining = [None] * NUM_NODES
_, pareto_nodes, _ = zip(*pareto_data_arr)
uniform_count_flows_remaining = [None] * NUM_NODES
_, uniform_nodes, _ = zip(*uniform_data_arr)

# initialize values for count_flows_remaining
for i in range(NUM_NODES):
    # count the number of flows for each node
    normal_count_flows_remaining[i] = norm_nodes.count(i+1)
    pareto_count_flows_remaining[i] = pareto_nodes.count(i+1)
    uniform_count_flows_remaining[i] = uniform_nodes.count(i+1)


print(normal_count_flows_remaining, " Total flows: ", sum(normal_count_flows_remaining))
# print(pareto_count_flows_remaining, " Total flows: ", sum(pareto_count_flows_remaining))
# print(uniform_count_flows_remaining, " Total flows: ", sum(uniform_count_flows_remaining))

""" Potential problem:
        total time in defined should be proportionate to packet flow size
"""


""" returns a list with how many flows are left for each node """
# def get_flows_left(flow_arr):
#     count_flows_remaining = [None] * NUM_NODES
#     _, dist_nodes, _ = zip(*flow_arr)
#     # get values for count_flows_remaining
#     for i in range(NUM_NODES):
#         # count the number of flows for each node
#         count_flows_remaining[i] = dist_nodes.count(i+1)
#
#     return count_flows_remaining
#
# flows_remaining = get_flows_left(normal_count_flows_remaining)
# print(flows_remaining, " Total flows: ", sum(flows_remaining))


""" What is stored at the router """
# flow count remaining for each node
# total sent for each node
# List of the packet flows to be sent (this is used to detect collisions)


""" If I just sent the information without using the algorithms """


""" Normal wifi mean response time """
wifi_normal_response = 0
wifi_pareto_response = 0
wifi_uniform_response = 0
for i in range(len(normal_data_arr)):
    if(i==0):
        continue
    wifi_normal_response += normal_data_arr[i-1][0]
    wifi_pareto_response += pareto_data_arr[i-1][0]
    wifi_uniform_response += uniform_data_arr[i-1][0]

wifi_normal_response = wifi_normal_response/len(normal_data_arr)
wifi_pareto_response = wifi_pareto_response/len(pareto_data_arr)
wifi_uniform_response = wifi_uniform_response/len(uniform_data_arr)
print("Wifi normal without algos: ",wifi_normal_response)
print("Wifi pareto without algos: ",wifi_pareto_response)
print("Wifi uniform without algos: ",wifi_uniform_response)




""" Algorithm 1 -- smaller packet next, send it """
def algo1_check_swap(current, next):
    swap = False
    t0 = time.time()

    # Compare the burst time for the current flow and the next flow
    if(current[0] > next[0]):
        swap = True

    t1 = time.time()

    total = t1-t0
    return swap, total


""" run algo 1 -- smaller packet next """
algo1_time = 0
algo1_normal_response = 0
for i in range(len(normal_data_arr)-1):

    # Check if we need to swap
    swap, time_to_swap = algo1_check_swap(normal_data_arr[i], normal_data_arr[i+1])
    algo1_time += time_to_swap

    # swap if needed
    if(swap):
        normal_data_arr[i], normal_data_arr[i+1] = normal_data_arr[i+1], normal_data_arr[i]

    # if first iteration, continue (arrived at time = 0)
    if(i == 0):
        continue

    # After swap, calculate response time
    algo1_normal_response += normal_data_arr[i-1][0]


# Add response time with time to run the algo1
algo1_normal_response += algo1_time
algo1_normal_response = algo1_normal_response/len(normal_data_arr)


print("normal with algo 1: ",algo1_normal_response)
normal_speed_up = (wifi_normal_response - algo1_normal_response)/wifi_normal_response
print("Normal speed up: ", normal_speed_up)
