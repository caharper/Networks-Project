from node import Node
import numpy as np
import random
import time
import statistics


# Define the number of nodes in the network
NUM_NODES = 100

list_nodes = []

# Create nodes
for i in range(NUM_NODES):
    # Create distibution

    """ Normal Distribution """
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

    max = np.max(normal)
    min = np.min(normal)

    # shuffle data
    random.shuffle(normal)

    # Create a node
    list_nodes.append(Node(i, normal))



    """ Pareto Distribution """
    # a, m = 3., 2.  # shape and mode
    # pareto = (np.random.pareto(a, 500) + 1) * m
    #
    # # get the average value
    # # this should not be computed every time, but for simplicity i am going to
    # avg = statistics.mean(pareto)
    #
    # # modify each flow entry to be relative to the .117 sec/average flow
    # for entry in pareto:
    #     entry = ((entry-avg)/avg)*.117 + .117
    #
    # max = np.max(pareto)
    # min = np.min(pareto)
    #
    # # shuffle data
    # random.shuffle(pareto)
    #
    # # Create a node
    # list_nodes.append(Node(i, pareto))


    """ Uniform Distribution """
    # uniformBefore = np.random.uniform(-1,0,500)
    # # Since normal Distribution goes from -inf to inf, shift by smallest value to get
    # # all positive numbers
    # # print(np.min(normal))
    # uniform = np.add(uniformBefore, abs(np.min(uniformBefore)))
    # # get the average value
    # # this should not be computed every time, but for simplicity i am going to
    # avg = statistics.mean(uniform)
    #
    # # modify each flow entry to be relative to the .117 sec/average flow
    # for entry in uniform:
    #     entry = ((entry-avg)/avg)*.117 + .117
    #
    # max = np.max(uniform)
    # min = np.min(uniform)
    #
    # # shuffle data
    # random.shuffle(uniform)
    #
    # # Create a node
    # list_nodes.append(Node(i, uniform))

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

# Right now this is the optimal case where nothing waits in the queue
# Now adding in randomness overlap in queue
overlap = 0
for node in list_nodes:
    for flow in node.packetstream:
        overlap += avg * (random.randint(0,NUM_NODES-1))
avg_add_overlap_time = random.uniform(0, avg) * (500*NUM_NODES)


print("Wifi response baseline: ",  overlap)


# # reshuffle the



def find_algo1_winner(algo1_nodes):
    algo1_nodes.sort(key=lambda x: x.get_num_remaining())
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
rand_transmission_time = 0

was_sender = False

# Choose random node to get the attempt send flow --- to start with
attempt_send_num = random.randint(0,NUM_NODES-1)
attempt_send_node = list_nodes[attempt_send_num]
attempt_send_flow = attempt_send_node.get_top_flow()



# Continue running the network until all nodes are done sending
big_packet_flows = []
rand_colliders_nodes = []
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

    # Update a new sender if it was the sender on the previous step
    # Choose new random sending node
    if(was_sender):
        try:
            attempt_send_num = random.randint(0,NUM_NODES-1)
            attempt_send_node = list_nodes[attempt_send_num]
            attempt_send_flow = attempt_send_node.get_top_flow()
        except:
            print("Here is the error: ", len(list_nodes))

    # same = True
    #
    # # make sure collision is from a different node
    # while(same):
    #     # Choose another random node to try and collide with
    #     attempt_collide_num = random.randint(0,NUM_NODES-1)
    #
    #     if(attempt_collide_num != attempt_send_num):   # what if only one node left ????
    #         same = False
    #
    # attempt_collide_node = list_nodes[attempt_collide_num]
    # attempt_collide_flow = attempt_collide_node.get_top_flow()


    rand_colliders_nums = random.sample(range(0, NUM_NODES-1), random.randint(1,NUM_NODES-1))

    for rand in rand_colliders_nums:
        rand_colliders_nodes.append(list_nodes[rand])

    """ Algorithm 1 --- packet flow size comparison """
    # Set the timer for the algorithm
    t0 = time.time()
    winner_node = find_algo1_winner(rand_colliders_nodes)
    t1 = time.time()
    algo1_time += t1-t0

    # Check if the winner node is the same as the attempted sender, otherwise,
    # add in random transmission time
    # print("winner: " , winner_node.id)
    # print("maybe: " ,attempt_send_node.id)
    if(winner_node.id != attempt_send_node.id):
        # Random transmission time
        rand_transmission_time += random.uniform(0, attempt_send_node.get_top_flow())

        # Update the sender to the winner
        attempt_send_node = winner_node

        # Set was sender
        was_sender = False

        # Update the sender info with number
        # Have to search for match
        for rand in rand_colliders_nums:
            # Get the list nodes with this random number, and compare with id
            if(list_nodes[rand].id == winner_node.id):
                # Set values
                attempt_send_num = rand
                attempt_send_flow = winner_node.get_top_flow()

                # break loop
                break



        # Repeat the process

    # Winner was the already sending node
    else:
        # Add in the previous sender's time
        response_time += previous_time_to_send

        # Update the previous_time_to_send to this flow
        previous_time_to_send = attempt_send_flow

        # Delete this flow
        attempt_send_node.remove_flow()

        # Update values
        # Remove node if all streams have been sent
        if(attempt_send_node.is_empty()):
            remove_empty_nodes(attempt_send_num)
            NUM_NODES = NUM_NODES - 1

        # Set was sender
        was_sender = True



    # Clear the random colliding nodes
    rand_colliders_nodes = []

response_time += algo1_time
response_time += rand_transmission_time
print(" Algorithm 1 resp time: ",response_time)
percent_increase = ((response_time-overlap)/overlap)*100
print("Percent increase: ", percent_increase)
