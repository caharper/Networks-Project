from node import Node
import numpy as np
import random
import time
import statistics


# Define the number of nodes in the network
NUM_NODES = 5

list_nodes = []

# Create nodes
for i in range(NUM_NODES):
    # Create distibution
    # Normal Distribution
    mu, sigma = 0, 0.1 # mean and standard deviation
    normalBefore = np.random.normal(mu, sigma, 500)
    # Since normal Distribution goes from -inf to inf, shift by smallest value to get
    # all positive numbers
    # print(np.min(normal))
    normal = np.add(normalBefore, abs(np.min(normalBefore)))
    # get the average value
    # this should not be computed every time, but for simplicity i am going to
    avg = statistics.mean(normal)

    # modify each flow entry to be relative to the .117 sec/average flow
    for entry in normal:
        entry = ((entry-avg)/avg)*.117 + .117

    # shuffle data
    random.shuffle(normal)

    # Create a node
    list_nodes.append(Node(i, normal))

# print(len(list_nodes[0].packetstream))
# list_nodes[0].remove_flow()
# print(len(list_nodes[0].packetstream))


# Function returns the nodes that still have flows left
def remove_empty_nodes(index):
    # if a node is empty, decrement NUM_NODES and remove the node from list_nodes
    NUM_NODES - 1
    del list_nodes[index]


# big_packet_flows = []
# for node in list_nodes:
#     for flow in node.packetstream:
#         big_packet_flows.append(flow)
#
#
# # reshuffle the




# print(np.max(list_nodes[0].packetstream))
# print(np.min(list_nodes[0].packetstream))
#
# print(avg)
# print(list_nodes[0].packetstream[0])
# print(((list_nodes[0].packetstream[0]-avg)/avg)*.117 + .117)
# Continue running the network until all nodes are done sending
big_packet_flows = []
while(len(list_nodes != 0)):
#     # Chose a random number of nodes to send data at this time
#         # right now just picking one random node to challenge it, should be random array of
#         # nodes probably, but for now just picking one at a time
#
    # Choose random node to get the attempt send flow
    attempt_send_node = list_nodes[random.randint(0,NUM_NODES-1)]
    attempt_send_flow = attempt_send_node.get_top_flow()

    # Choose another random node to try and collide with 
