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
    del list_nodes[index]

wifi_resonse_time = 0

big_packet_flows = []
for node in list_nodes:
    for flow in node.packetstream:
        big_packet_flows.append(flow)

for i in range(len(big_packet_flows)):
    if(i == 0):
        continue
    wifi_resonse_time += big_packet_flows[i-1]

print("Wifi response baseline: ", wifi_resonse_time)


# # reshuffle the



def find_algo1_winner(algo1_nodes):
    algo1_nodes.sort(key=lambda x: x.get_top_flow())
    return algo1_nodes[0]


# print(np.max(list_nodes[0].packetstream))
# print(np.min(list_nodes[0].packetstream))
#
# print(avg)
# print(list_nodes[0].packetstream[0])
# print(((list_nodes[0].packetstream[0]-avg)/avg)*.117 + .117)



# Initialize the response time
response_time = 0
previous_time_to_send = 0

# Initialize times to run algorithms
algo1_time = 0

# Choose random node to get the attempt send flow --- to start with
attempt_send_num = random.randint(0,NUM_NODES-1)
attempt_send_node = list_nodes[attempt_send_num]
attempt_send_flow = attempt_send_node.get_top_flow()



# Continue running the network until all nodes are done sending
big_packet_flows = []
while(len(list_nodes) != 0):
#     # Chose a random number of nodes to send data at this time
#         # right now just picking one random node to challenge it, should be random array of
#         # nodes probably, but for now just picking one at a time
#
    # Choose random node to get the attempt send flow
    # attempt_send_num = random.randint(0,NUM_NODES-1)
    # attempt_send_node = list_nodes[attempt_send_num]
    # attempt_send_flow = attempt_send_node.get_top_flow()

    # If only one node left, send all of its info
    if(len(list_nodes) == 1):
        # Iterate over its remaining flows
        for flow in list_nodes[0].packetstream:
            response_time += flow
        # Last flow doesn't need to wait
        response_time = response_time - list_nodes[0].packetstream[-1]
        # Clear list to end while loop
        list_nodes = []
        continue

    same = True

    # make sure collision is from a different node
    while(same):
        # Choose another random node to try and collide with
        attempt_collide_num = random.randint(0,NUM_NODES-1)

        if(attempt_collide_num != attempt_send_num):   # what if only one node left ????
            same = False

    attempt_collide_node = list_nodes[attempt_collide_num]
    attempt_collide_flow = attempt_collide_node.get_top_flow()

    """ Algorithm 1 --- packet flow size comparison """
    # Set the timer for the algorithm
    t0 = time.time()
    # if the attempt colliding flow is smaller than the sending flow, collide
    if(attempt_collide_flow < attempt_send_flow):
        t1 = time.time()
        algo1_time += t1-t0

        # Add in random amount of time transmitting


        # Send collision flow
        attempt_collide_node.remove_flow()

        # Remove node if all streams have been sent
        if(attempt_collide_node.is_empty()):
            remove_empty_nodes(attempt_collide_num)
            NUM_NODES = NUM_NODES - 1

        # keep same attempt send flow
        # add to response time
        response_time += previous_time_to_send
        # update previous_time_to_send to the current packet flow being sent
        previous_time_to_send = attempt_collide_flow

    # Send the intended one and make the attempt collide node be the attempt send node
    else:
        t1 = time.time()
        algo1_time += t1-t0
        # add to response time
        response_time += previous_time_to_send
        # update previous_time_to_send to the current packet flow being sent
        previous_time_to_send = attempt_send_flow

        # send send flow
        attempt_send_node.remove_flow()

        # Remove node if all streams have been sent
        if(attempt_send_node.is_empty()):
            remove_empty_nodes(attempt_send_num)
            NUM_NODES = NUM_NODES - 1


        # Update attempt sending to this collision flow
        attempt_send_num = attempt_collide_num
        attempt_send_node = attempt_collide_node
        attempt_send_flow = attempt_collide_flow


response_time += algo1_time
print(" Algorithm 1 resp time: ",response_time)
