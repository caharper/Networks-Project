from node import Node
import numpy as np

# Create a node
n1 = Node(1, 5)


# Normal Distribution
mu, sigma = 0, 0.1 # mean and standard deviation
normal = np.random.normal(mu, sigma, 1000)
# print(normal)

# Pareto Distribution
a, m = 3., 2.  # shape and mode
pareto = (np.random.pareto(a, 1000) + 1) * m
# print(pareto)

# Uniform/Constant Distribution
uniform = np.random.uniform(-1,0,1000)
# print(uniform)
