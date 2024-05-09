import math
import time
import numpy as np

#np.random.seed(2079)    # fix seed to make everything below reproducible
arms = 10      # number of arms per MAB problem
num_mab_problems = 200
#iteration_budget = 1000

# Matrix of means, where the i'th row contains the means of all arms for the
# i'th MAB problem
arm_means = np.random.normal(loc=0.0, scale=1.0, size=(num_mab_problems, arms))


class SequentialHalvingAlg:
  """
  Baseline sequential halving algorithm using a discrete iteration budget (as per Karnin et al., 2013).
  """
  
  def __init__(self,return_hist=False, k=10, time_steps_per_problem=1000):
      self.original_indices = {index: 0 for index, arm in enumerate(range(k))}  # Map arm to its original index
      self.current_arms = {index: 0 for index, arm in enumerate(range(k))}
      self.current_arm = self.current_arms.get(0) #Keeping track of the current arm to pull
      self.current_rewards = {index: 0 for index, arm in enumerate(range(k))}  # Map arm to its original index
      self.visits = {index: 0 for index, arm in enumerate(range(k))}  #The amount of times that the algorithm has pulled each arm
      self.total_rewards =  {index: 0 for index, arm in enumerate(range(k))}  #The total rewards that the algorithm has observed for each arm

      self.considered_arms_amt = k #The amount of arms that the algorithm is currently considering
      self.total_means = {index: 0 for index, arm in enumerate(range(k))} #The total rewards that the algorithm has observed for each arm
      self.considered_arms_amt = k #The amount of arms that the algorithm is currently considering
      self.time_steps_per_problem = time_steps_per_problem 
      self.sample_count_per_arm = self.get_dist_per_arm(k) #Amount of times by which each arm should be sampled (as per Karnin et al algorithm).
      self.current_iteration = 0 
      
      self.budget_left = time_steps_per_problem
      self.current_round = 1
      self.return_hist = return_hist
      self.hist = [] #Stores history of arms pulled
      self.k = k
      self.current_arm_idx = 0
      
      self.phases = math.ceil(math.log2(k))
      self.round_time = time_steps_per_problem/self.phases
      


  """
  Retruns the amount of budget to be allocated to each arm.
  """
  def get_dist_per_arm(self, num_arms):
      return math.floor(self.time_steps_per_problem/(num_arms*math.ceil(math.log2(num_arms))))
    
  
  def reset(self) -> None:
    self.current_arms = range(self.k)
    self.current_arm = self.current_arms.get(0) #Keeping track of the current arm to pull
    self.current_rewards = [0] * self.k
    self.visits = [0] * self.k 
    self.total_rewards = [0] * self.k 
    self.considered_arms_amt = self.k
    self.sample_count_per_arm = self.get_dist_per_arm(self.k)
    self.budget_left = self.time_steps_per_problem
    self.current_round = 1
    self.hist = [] #Stores history of arms pulled
    self.budget_left = self.time_steps_per_problem
  
  def sort_arms(self, arms):
      # Pair each arm with its corresponding reward, sort the pairs, and extract the arms
        # self.current_arms, self.current_rewards = zip(*sorted(zip(self.current_arms, self.current_rewards), key=lambda x: x[1], reverse=True))
        # self.current_arms = list(self.current_arms)
        # self.current_rewards = list(self.current_rewards)
      sorted_dict = dict(sorted(arms.items(), key=lambda item: item[1], reverse=True))
      return sorted_dict
    
  def halve_arms(self, arms):
      #print('here')
      new_dict = {}
      keys = list(arms.keys())
      #print('len keys: ', len(keys))
      #print('considered arms amount: ', self.considered_arms_amt)
      # print('Amount after halving: ', (math.ceil(len(keys) / (self.considered_arms_amt/2))))
      #ran = math.ceil(len(keys) / (self.considered_arms_amt/2))
      ran = math.ceil(len(keys)/2)
      #print('Amount after halving: ', ran)
      for i in range(ran):
          new_dict[keys[i]] = arms[keys[i]]
      return new_dict
  
    
  
  def choose_arm(self) -> int:
    #print(f"current_arm: {self.current_arm} current index: {self.current_arms.index(self.current_arm)} current_iteration: {self.current_iteration} considered_arms_amt: {self.considered_arms_amt} current_round: {self.current_round} budget_left: {self.budget_left} sample_count_per_arm: {self.sample_count_per_arm} arms left: {len(self.current_arms)}")
    if(self.considered_arms_amt < 1): return self.current_arm
    
    
    if self.current_iteration == self.round_time:
      self.current_iteration = 0
      
      
      #Check to see if we have used every arm the amount of times we should have

      #If we have, we halve the amount of considered arms based on rewards and reset the current arm to the first arm in the list
      
      # # Pair each arm with its corresponding reward, sort the pairs, and extract the arms
      
      self.budget_left = self.budget_left/2 
        # Pair each arm with its corresponding reward, sort the pairs, and extract the arms
      # print("*************************")
      # print("before sorting: ", self.current_arms)
      self.current_arms = self.sort_arms(self.current_arms)
      # print("after sorting: ", self.current_arms)
      self.current_arms = self.halve_arms(self.current_arms)
      # print("after halving: ", self.current_arms)
      # print("*************************\n\n")
      self.considered_arms_amt = len(self.current_arms)
        
        # budget_left = self.budget_left
      if self.considered_arms_amt == 1:
        self.sample_count_per_arm = self.budget_left
      else:
        self.sample_count_per_arm = self.get_dist_per_arm(self.considered_arms_amt)
        
      self.current_arm_idx = 0
      
      if len(self.current_arms) > 1: self.current_arm_idx = self.current_arm_idx + 1
        
      self.current_arm = list(self.current_arms.keys())[0]
      self.current_arm_idx = 0
      
      if self.return_hist: self.hist.append(self.current_arm)
      
      return self.current_arm
    
    
    
    if self.current_arm_idx == len(self.current_arms) - 1:
      self.current_arm_idx = 0
    else:
      self.current_arm_idx = self.current_arm_idx + 1
    
    self.current_arm =  list(self.current_arms.keys())[self.current_arm_idx] 
      
      
    if self.return_hist: self.hist.append(self.current_arm)
    self.current_iteration = self.current_iteration + 1
    return self.current_arm
  
  
  def observe_reward(self, arm: int, reward: float) -> None:
    """
    This function lets us observe rewards from arms we have selected.

    :param arm: Index (starting at 0) of the arm we played.
    :param reward: The reward we received.
    
    """
    
    vis = self.visits.get(arm)+1
    self.visits.update({arm: vis})
    rew = self.total_rewards.get(arm) + reward
    self.total_rewards.update({arm: self.total_rewards.get(arm) + reward})
    cur_rew = self.total_rewards.get(arm)/self.visits.get(arm)
    self.current_rewards.update({arm: cur_rew})
    self.current_arms.update({arm: self.total_rewards.get(arm)/self.visits.get(arm)})
    self.total_means.update({arm: self.total_rewards.get(arm)/self.visits.get(arm)})
    
    
    
    # self.visits[self.current_arms.index(arm)] = self.visits[self.current_arms.index(arm)] + 1
    # self.total_rewards[self.current_arms.index(arm)] = self.total_rewards[self.current_arms.index(arm)] + reward
    # self.total_means[self.current_arms.index(arm)] = self.total_rewards[self.current_arms.index(arm)]/self.visits[self.current_arms.index(arm)]
    # self.current_rewards[self.current_arms.index(arm)] = self.total_rewards[self.current_arms.index(arm)]/self.visits[self.current_arms.index(arm)]
    
    

  def __str__(self):
    return print(f"Sequential_halving:\nArm history: {self.hist}\n")

class SequentialHalvingAlgAnyTime_v1:
  def __init__(self, time_budget, return_hist=False, k=10):
    self.time_budget = time_budget
    self.stop_time = int(round(time.time() * 1000)) + time_budget
    self.original_indices = {index: 0 for index, arm in enumerate(range(k))}  # Map arm to its original index
    self.current_arms = {index: 0 for index, arm in enumerate(range(k))}
    self.current_arms_keys = list(self.current_arms.keys())
    self.keys_idx = 0
    self.current_arm = self.current_arms_keys[self.keys_idx] #Keeping track of the current arm to pull
    self.current_rewards = {index: 0 for index, arm in enumerate(range(k))}  # Map arm to its original index
    self.visits = {index: 0 for index, arm in enumerate(range(k))}  #The amount of times that the algorithm has pulled each arm
    self.total_rewards =  {index: 0 for index, arm in enumerate(range(k))}  #The total rewards that the algorithm has observed for each arm
    self.total_means = {index: 0 for index, arm in enumerate(range(k))} #The total rewards that the algorithm has observed for each arm
    self.hist = []
    self.return_hist = return_hist
    self.round_iter = 0

   
     
  def sort_arms(self, arms):
    # Pair each arm with its corresponding reward, sort the pairs, and extract the arms
      # self.current_arms, self.current_rewards = zip(*sorted(zip(self.current_arms, self.current_rewards), key=lambda x: x[1], reverse=True))
      # self.current_arms = list(self.current_arms)
      # self.current_rewards = list(self.current_rewards)
     sorted_dict = dict(sorted(arms.items(), key=lambda item: item[1], reverse=True))
     return sorted_dict
   
   
  def choose_arm(self) -> int:
    #print(f"current_arm: {self.current_arm} current index: {self.current_arms.index(self.current_arm)} considered_arms_amt: {self.considered_arms_amt} current_round: {self.current_round} budget_left: {self.budget_left} sample_count_per_arm: {self.sample_count_per_arm} arms left: {len(self.current_arms)}")
    
    if self.round_iter >= len(self.current_arms):#If this is true, we are ready to halve the search or we are ready to start over
      self.round_iter = 0
      if len(self.current_arms_keys) <= 2:#if true we reset the nodes we search
        self.keys_idx = 0
        self.current_arms_keys = list(self.current_arms.keys())
        
      else:#Otherwise we halve and continue with best arms
        
        half_size = math.ceil(len(self.current_arms_keys)/2)
        if(half_size<2): half_size = 2
        # print("halfsize: " + str(half_size))
        # print("current_arms: " + str(self.current_arms))
        
        temp_dict = {}
        for key in self.current_arms_keys:
          temp_dict.update({key : self.current_arms.get(key)})
          
        # print("temp dict: " + str(temp_dict))
        current_arms_sorted = self.sort_arms(temp_dict)
        # print("sorted: " + str(current_arms_sorted))
        sorted_keys = list(current_arms_sorted.keys())
        # print("sorted keys: " + str(sorted_keys))
        
        self.current_arms_keys = []
        for i in range(0,half_size):
          self.current_arms_keys.append(sorted_keys[i])
        
        # print("new current_arm_keys list: " + str(self.current_arms_keys))
        self.keys_idx = 0
        
    else:
      self.round_iter = self.round_iter + 1
      self.keys_idx = self.keys_idx + 1
      if self.keys_idx >= len(self.current_arms_keys): self.keys_idx = 0
      
    self.current_arm = self.current_arms_keys[self.keys_idx]
      # print("Current_arms: " + str(self.current_arms))
      # print("Current_arms_keys: " + str(self.current_arms_keys))
      # print(self.keys_idx)
      # print("curarm: " + str(self.current_arm))
    if self.return_hist: self.hist.append(self.current_arm)

    return self.current_arm

      

  def observe_reward(self, arm: int, reward: float) -> None:
    """
    This function lets us observe rewards from arms we have selected.

    :param arm: Index (starting at 0) of the arm we played.
    :param reward: The reward we received.
    
    """
    # self.visits[self.current_arms.index(arm)] = self.visits[self.current_arms.index(arm)] + 1
    vis = self.visits.get(arm)+1
    self.visits.update({arm: vis})
    # self.total_rewards[self.current_arms.index(arm)] = self.total_rewards[self.current_arms.index(arm)] + reward
    rew = self.total_rewards.get(arm) + reward
    self.total_rewards.update({arm: self.total_rewards.get(arm) + reward})
    
    #self.total_means[self.current_arms.index(arm)] = self.total_rewards[self.current_arms.index(arm)]/self.visits[self.current_arms.index(arm)]

    
    
    # self.current_rewards[self.current_arms.index(arm)] = self.total_rewards[self.current_arms.index(arm)]/self.visits[self.current_arms.index(arm)]
    cur_rew = self.total_rewards.get(arm)/self.visits.get(arm)
    
    
    self.current_rewards.update({arm: cur_rew})
    self.current_arms.update({arm: self.total_rewards.get(arm)/self.visits.get(arm)})
    self.total_means.update({arm: self.total_rewards.get(arm)/self.visits.get(arm)})
    
    #print(self.current_rewards)
#     self.visits[self.current_arms.index(arm)] = self.visits[self.current_arms.index(arm)] + 1
#     self.total_rewards[self.current_arms.index(arm)] = self.total_rewards[self.current_arms.index(arm)] + reward
#     self.total_means[self.current_arms.index(arm)] = self.total_rewards[self.current_arms.index(arm)]/self.visits[self.current_arms.index(arm)]
#     self.current_rewards[self.current_arms.index(arm)] = self.total_rewards[self.current_arms.index(arm)]/self.visits[self.current_arms.index(arm)]


  def __str__(self):
    return print(f"Sequential_halving:\nArm history: {self.hist}\n")
  
  
class SequentialHalvingAlgTime_v1:
  """
  Baseline sequential halving algorithm using a time based budget (inspired by Karnin et al., 2013).
  Rotates through arms sequentially (pun intended) until a round is over, then halves.
  TODO: Find out why regret is so high: 
  1. Is the indexing of pruned arms incorrect?
  2. Is the measure of regret incorrect?
    - measure iterations 
  """
  
  def __init__(self, time_budget, return_hist=False, k=10):
      #self.current_arms = range(k) #A list of all arms that the algorithm cares about. Will be sequentially halved ;)
      self.original_indices = {index: 0 for index, arm in enumerate(range(k))}  # Map arm to its original index
      self.current_arms = {index: 0 for index, arm in enumerate(range(k))}
      self.current_arm = self.current_arms.get(0) #Keeping track of the current arm to pull
      self.current_rewards = {index: 0 for index, arm in enumerate(range(k))}  # Map arm to its original index
      self.visits = {index: 0 for index, arm in enumerate(range(k))}  #The amount of times that the algorithm has pulled each arm
      self.total_rewards =  {index: 0 for index, arm in enumerate(range(k))}  #The total rewards that the algorithm has observed for each arm
      self.considered_arms_amt = k #The amount of arms that the algorithm is currently considering
      self.total_means = {index: 0 for index, arm in enumerate(range(k))} #The total rewards that the algorithm has observed for each arm
      self.k = k
      
      self.time_budget = time_budget
      self.sample_count_per_arm = self.get_dist_per_arm(k) #Amount of times by which each arm should be sampled (as per Karnin et al algorithm).
      self.current_iteration = 0 
      
      self.budget_left = time_budget
      
      self.phases = math.ceil(math.log2(k))
      self.round_time = time_budget/self.phases
      self.current_arm_idx = 0
      
      self.current_round = 1
      self.return_hist = return_hist
      self.hist = [] #Stores history of arms pulled
      self.current_time = int(round(time.time() * 1000))
      self.prev_switch_time = self.current_time
      self.start_time = self.current_time
      
      

  
  
  """
  Retruns the amount of time to be allocated to each arm.
  """
  def get_dist_per_arm(self, num_arms):
      return math.floor(self.time_budget/(num_arms*math.ceil(math.log2(num_arms))))
    
  
  def reset(self) -> None:
    self.current_arms = range(self.k)
    self.current_arm = self.current_arms[0]
    self.current_rewards = [0] * self.k
    self.visits = [0] * self.k 
    self.total_rewards = [0] * self.k 
    self.considered_arms_amt = self.k
    self.sample_count_per_arm = self.get_dist_per_arm(self.k)
    self.budget_left = self.time_budget
    self.current_round = 1
    self.hist = [] #Stores history of arms pulled
    #self.budget_left = self.time_steps_per_problem
    self.current_time = int(round(time.time() * 1000))
    self.prev_switch_time = self.current_time
    self.start_time = self.current_time
    
  def sort_arms(self, arms):
    # Pair each arm with its corresponding reward, sort the pairs, and extract the arms
      # self.current_arms, self.current_rewards = zip(*sorted(zip(self.current_arms, self.current_rewards), key=lambda x: x[1], reverse=True))
      # self.current_arms = list(self.current_arms)
      # self.current_rewards = list(self.current_rewards)
     sorted_dict = dict(sorted(arms.items(), key=lambda item: item[1], reverse=True))
     return sorted_dict
   
  def halve_arms(self, arms):
      #print('here')
      new_dict = {}
      keys = list(arms.keys())
      #print('len keys: ', len(keys))
      #print('considered arms amount: ', self.considered_arms_amt)
      # print('Amount after halving: ', (math.ceil(len(keys) / (self.considered_arms_amt/2))))
      #ran = math.ceil(len(keys) / (self.considered_arms_amt/2))
      ran = math.ceil(len(keys)/2)
      #print('Amount after halving: ', ran)
      for i in range(ran):
          new_dict[keys[i]] = arms[keys[i]]
      return new_dict
      

  def choose_arm(self) -> int:
    #print(f"current_arm: {self.current_arm} current index: {self.current_arms.index(self.current_arm)} considered_arms_amt: {self.considered_arms_amt} current_round: {self.current_round} budget_left: {self.budget_left} sample_count_per_arm: {self.sample_count_per_arm} arms left: {len(self.current_arms)}")
    
    self.current_time = int(round(time.time() * 1000))
    #print(f"Current round: {self.current_round} round time: {self.round_time}")
    
      #print(f"current_arms.index(self.current_arm): {self.current_arms.index(self.current_arm)}, considered_arms_amt: {self.considered_arms_amt}")
    # print(f"time elapsed: {self.current_time - self.prev_switch_time} round time: {self.round_time}")
    
    if self.current_time - self.prev_switch_time >= self.round_time:
      
      # Pair each arm with its corresponding reward, sort the pairs, and extract the arms
      # print("*************************")
      # print("before sorting: ", self.current_arms)
      self.current_arms = self.sort_arms(self.current_arms)
      # print("after sorting: ", self.current_arms)
      self.current_arms = self.halve_arms(self.current_arms)
      # print("after halving: ", self.current_arms)
      # print("*************************\n\n")
      self.considered_arms_amt = len(self.current_arms)
      # self.round_time = math.ceil(self.round_time/self.phases)
      
      # self.current_arms = self.current_arms[:math.ceil(self.considered_arms_amt/2)] #Take top half of the list
      # self.current_rewards = self.current_rewards[:math.ceil(self.considered_arms_amt/2)]
      # self.considered_arms_amt = len(self.current_arms)
      # self.current_round = self.current_round + 1
      

      

      self.current_arm = list(self.current_arms.keys())[0]
      self.current_arm_idx = 0
      if len(self.current_arms) > 1: self.current_arm_idx = self.current_arm_idx + 1
      
      # print("here")
      if self.return_hist:
        self.hist.append("#") 
        self.hist.append(self.current_arm)
      self.prev_switch_time = int(round(time.time() * 1000))
      return self.current_arm
    
    
    
    
    
    
    if self.current_arm_idx == len(self.current_arms) - 1:
      self.current_arm_idx = 0
    else:
      self.current_arm_idx = self.current_arm_idx + 1
    
    #print("list size: ", len(self.current_arms))
    #
    #print((self.current_arms))
    #print((self.current_arm))
    
    self.current_arm = list(self.current_arms.keys())[self.current_arm_idx]
    #print("idx: ", self.current_arm_idx) 
    #print((self.current_arm))
    #print(list(self.current_arms.keys()))
    
    if self.return_hist: self.hist.append(self.current_arm)
    
    self.current_time = int(round(time.time() * 1000))
    
    return self.current_arm

      

  def observe_reward(self, arm: int, reward: float) -> None:
    """
    This function lets us observe rewards from arms we have selected.

    :param arm: Index (starting at 0) of the arm we played.
    :param reward: The reward we received.
    
    """
    # self.visits[self.current_arms.index(arm)] = self.visits[self.current_arms.index(arm)] + 1
    vis = self.visits.get(arm)+1
    self.visits.update({arm: vis})
    # self.total_rewards[self.current_arms.index(arm)] = self.total_rewards[self.current_arms.index(arm)] + reward
    rew = self.total_rewards.get(arm) + reward
    self.total_rewards.update({arm: self.total_rewards.get(arm) + reward})
    
    #self.total_means[self.current_arms.index(arm)] = self.total_rewards[self.current_arms.index(arm)]/self.visits[self.current_arms.index(arm)]

    
    
    # self.current_rewards[self.current_arms.index(arm)] = self.total_rewards[self.current_arms.index(arm)]/self.visits[self.current_arms.index(arm)]
    cur_rew = self.total_rewards.get(arm)/self.visits.get(arm)
    
    
    self.current_rewards.update({arm: cur_rew})
    self.current_arms.update({arm: self.total_rewards.get(arm)/self.visits.get(arm)})
    self.total_means.update({arm: self.total_rewards.get(arm)/self.visits.get(arm)})
    
    #print(self.current_rewards)
#     self.visits[self.current_arms.index(arm)] = self.visits[self.current_arms.index(arm)] + 1
#     self.total_rewards[self.current_arms.index(arm)] = self.total_rewards[self.current_arms.index(arm)] + reward
#     self.total_means[self.current_arms.index(arm)] = self.total_rewards[self.current_arms.index(arm)]/self.visits[self.current_arms.index(arm)]
#     self.current_rewards[self.current_arms.index(arm)] = self.total_rewards[self.current_arms.index(arm)]/self.visits[self.current_arms.index(arm)]

class UCB1:
  """
  The UCB1 algorithm.
  """

  def __init__(self, C: float):
    """
    :param C: The exploration parameter C.
    """
    self.C = C
    self.t = 0
    self.num_pulls = [0 for _ in range(k)]
    self.avg_rewards = np.zeros(k)

  def reset(self) -> None:
    """
    Reset all memory.
    """
    self.t = 0
    self.num_pulls = [0 for _ in range(k)]
    self.avg_rewards = np.zeros(k)

  def choose_arm(self) -> int:
    """
    :return: Arm, in [0, k).
    """
    self.t = self.t + 1
    ucbs = np.copy(self.avg_rewards)
    log_t = log(self.t)

    for i in range(k):
      if self.num_pulls[i] == 0:
        ucbs[i] = np.inf
      else:
        ucbs[i] = ucbs[i] + self.C * sqrt(log_t / self.num_pulls[i])

    return np.argmax(ucbs)

  def observe_reward(self, arm: int, reward: float) -> None:
    """
    This function lets us observe rewards from arms we have selected.

    :param arm: Index (starting at 0) of the arm we played.
    :param reward: The reward we received.
    """
    self.num_pulls[arm] = self.num_pulls[arm] + 1
    self.avg_rewards[arm] = self.avg_rewards[arm] + ((reward - self.avg_rewards[arm]) / self.num_pulls[arm])

  def __str__(self):
    return f"UCB1({self.C:.3f})"
  def __str__(self):
    return print(f"Sequential_halving:\nArm history: {self.hist}\n")
  
  