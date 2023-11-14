# -*- coding: utf-8 -*-
"""
CS 182 Problem Set 3: Python Coding Questions - Fall 2023
Due November 15, 2023 at 11:59pm
"""

### Package Imports ###
import numpy as np
import matplotlib.pyplot as plt
import random
### Package Imports ###

#### Coding Problem Set General Instructions - PLEASE READ ####
# 1. Unlike previous psets, this code does not need to be submitted; there is no autograder
# 2. This code goes with Problem 2: Employment Status, on this pset
# 3. This starter code has been provided to you, feel free to use it (or not, if you want to code something different) however you
#    see fit. Change variables, solve the question in another way, however you need to best understand the question and your code.
#    This coding problem can be written in a variety of different ways, this code is only a rough sketch of what your code could
#    look like. We encourage you to change it if you need to.
# 4. Make sure you write the optimal policies your code determines and copy your code and graphs onto your written submission


n_states = 3 # 0 is Safely Employed (SE), 1 is PIP, 2 is Unemployed (UE)
n_actions = 2 # 0 is Code, 1 is Netflix

t_p = np.zeros((n_states, n_actions, n_states))
# Transition Probabilities: These are represented as a 3-dimensional array
# t_p[s_1, a, s_2] = p indicates that beginning from state s_1 and taking action a will result in state s_2 with probability p
t_p[0, 0, 0] = 1        # t_p[SE, Code, SE]      = 1
t_p[0, 1, 0] = 1 / 4    # t_p[SE, Netflix, SE]   = 1 / 4
t_p[0, 1, 1] = 3 / 4    # t_p[SE, Code, PIP]     = 3 / 4
t_p[1, 0, 0] = 1 / 4    # t_p[PIP, Code, SE]     = 1 / 4
t_p[1, 0, 1] = 3 / 4    # t_p[PIP, Code, PIP]    = 3 / 4
t_p[1, 1, 1] = 7 / 8    # t_p[PIP, Netflix, PIP] = 7 / 8
t_p[1, 1, 2] = 1 / 8    # t_p[PIP, Netflix, UE]  = 1 / 8
# all other transition probabilities are 0

r = np.zeros((n_states, n_actions))
# Reward values: These are represented as a 2-dimensional array
# r[s, a] = val indicates that taking at state s, taking action a will give a reward of val
r[0, 0] = 4     # r[SE, Code]       = 4
r[0, 1] = 10    # r[SE, Netflix]    = 10
r[1, 0] = 4     # r[PIP, Code]      = 4
r[1, 1] = 10    # r[PIP, Netflix]   = 10



def policy_iteration(gamma):
  """
  You should find the optimal policy for Liz under the constrants of discount factor gamma, which is given as a parameter.
  Relevant variables and the transition probabilities are defined above, feel free to use them and change them how you want.
  What this function returns is up to you and how you want to determine the sum of utilities at each iteration in the plots.
  """
  
  theta = 1e-5 # define a theta that determines if the change in utilities from iteration to iteration is "small enough"
  
  policy = np.zeros(n_states, dtype=int) # define your policy, which begins as Netflix regardless of state
  value = [0] * n_states # define your values, which is arbritrarily assigned at first

  def updated_value(s):
    total = 0
    a = policy[s]
    for s_p in range(n_states):
        total += t_p[s, a, s_p] * (r[s, a] + gamma * value[s_p])
    return total

  def best_action(s):
    actions = np.zeros(n_actions, dtype=int)
    for a in range(n_actions):
      for s_p in range(n_states):
        actions[a] += t_p[s, a, s_p] * (r[s, a] + gamma * value[s_p])
    best_a = np.argmax(actions)
    return best_a
  
  while True:
    # Policy Evaluation
    # TODO: Policy Evaluation code here
    while True:
      delta = 0
      for s in range(n_states):
        v = value[s]
        value[s] = updated_value(s)
        delta = max(delta, abs(v - value[s]))
      if delta < theta:
        break
    
    # Policy Change check
    policy_stable = True

    # Policy Iteration
    # TODO: Policy Iteration code here
    for s in range(n_states):
      a = policy[s]
      policy[s] = best_action(s)
      if a != policy[s]:
        policy_stable = False
    
    # TODO: Determine if policy has changed between iterations
    if policy_stable:
      break
  
  return policy
        

def value_plots():
    """
    Your plots should indicate the cumulative utility summed across all states across iterations. More specifically, your y-val
    should indicate the total amount of utility acumulated across the states and actions as the iterations progress. This means
    you likely will have to keep track of what policies you have at every iteration, or some other method that will allow you to
    determine the cumulative sum of utilities as iterations continue.
    """
    # policies
    p1 = policy_iteration(0.9)
    p2 = policy_iteration(0.8)

    n = 50
    iterations = range(0, n)

    def get_vals(p):
      # initialize array of values and initial state
      vals = np.zeros(n, dtype=int)
      state = 0

      for i in iterations:
        action = p[state]
        # calculate the cumulative utility
        if i == 0:
          vals[i] = r[state, action]
        else:
          vals[i] = vals[i-1] + r[state, action]

        # update the state
        weights = []
        next_states = []
        for s_p in range(n_states):
          if t_p[state, action, s_p] != 0:
            weights.append(t_p[state, action, s_p])
            next_states.append(s_p)
        if len(weights) > 0:
          state = random.choices(next_states, weights)

      return vals
    
    p1_vals = get_vals(p1)
    p2_vals = get_vals(p2)
    
    # you will need to find a way to calculate the cumulative utility values for policy 1 and policy 2
    plt.plot(iterations, p1_vals, label="Policies for gamma = 0.9")
    plt.plot(iterations, p2_vals, label="Policies for gamma = 0.8")
    plt.xlabel("Iterations")
    plt.ylabel("Cumulative Utility Value")
    plt.legend()
    plt.title("Cumulative Utility Values over Time")
    plt.show()

if __name__ == "__main__":
  # print("Gamma = 0.9:", policy_iteration(0.9)) # policy iteration to verify your answer from problem 2 part c, with gamma = 0.9
  # print("Gamma = 0.8:", policy_iteration(0.8)) # policy iteration for problem 2 part d, with gamma = 0.8
  
  value_plots()
  # You will need to find some way to get the total utility values to the value_plots function. For example, you could pass
  # in the policies or you could pass in the cumulative sum of utility values.