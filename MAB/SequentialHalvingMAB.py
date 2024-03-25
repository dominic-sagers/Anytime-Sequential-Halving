import math
import time
import numpy as np

np.random.seed(2079)    # fix seed to make everything below reproducible
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
      self.current_arms = range(k) #A list of all arms that the algorithm cares about. Will be sequentially halved ;)
      self.current_arm = self.current_arms[0] #Keeping track of the current arm to pull
      self.current_rewards = [0] * k #The rewards that the algorithm has observed for each arm
      self.visits = [0] * k #The amount of times that the algorithm has pulled each arm
      self.total_rewards = [0] * k #The total rewards that the algorithm has observed for each arm
      self.total_means = [0] * k #The total rewards that the algorithm has observed for each arm
      self.considered_arms_amt = k #The amount of arms that the algorithm is currently considering
      self.time_steps_per_problem = time_steps_per_problem 
      self.sample_count_per_arm = self.get_dist_per_arm(k) #Amount of times by which each arm should be sampled (as per Karnin et al algorithm).
      self.current_iteration = 0 
      self.budget_left = time_steps_per_problem
      self.current_round = 1
      self.return_hist = return_hist
      self.hist = [] #Stores history of arms pulled
      self.k = k
      


  """
  Retruns the amount of budget to be allocated to each arm.
  """
  def get_dist_per_arm(self, num_arms):
      return math.floor(self.time_steps_per_problem/(num_arms*math.ceil(math.log2(num_arms))))
    
  
  def reset(self) -> None:
    self.current_arms = range(self.k)
    self.current_arm = self.current_arms[0]
    self.current_rewards = [0] * self.k
    self.visits = [0] * self.k 
    self.total_rewards = [0] * self.k 
    self.considered_arms_amt = self.k
    self.sample_count_per_arm = self.get_dist_per_arm(self.k)
    self.budget_left = self.time_steps_per_problem
    self.current_round = 1
    self.hist = [] #Stores history of arms pulled
    self.budget_left = self.time_steps_per_problem
  

  def choose_arm(self) -> int:
    #print(f"current_arm: {self.current_arm} current index: {self.current_arms.index(self.current_arm)} current_iteration: {self.current_iteration} considered_arms_amt: {self.considered_arms_amt} current_round: {self.current_round} budget_left: {self.budget_left} sample_count_per_arm: {self.sample_count_per_arm} arms left: {len(self.current_arms)}")
    if(self.considered_arms_amt < 1): return self.current_arm
    
    
    if self.current_iteration == self.sample_count_per_arm:
      self.current_iteration = 0
      
      
      #Check to see if we have used every arm the amount of times we should have
      if self.current_arms.index(self.current_arm) + 1 == self.considered_arms_amt:
        #If we have, we halve the amount of considered arms based on rewards and reset the current arm to the first arm in the list
        
        # Pair each arm with its corresponding reward, sort the pairs, and extract the arms
        self.current_arms, self.current_rewards = zip(*sorted(zip(self.current_arms, self.current_rewards), key=lambda x: x[1], reverse=True))
        self.current_arms = list(self.current_arms)
        self.current_rewards = list(self.current_rewards)
        
        
        self.current_arms = self.current_arms[:math.ceil(self.considered_arms_amt/2)] #Take top half of the list
        self.current_rewards = self.current_rewards[:math.ceil(self.considered_arms_amt/2)]
        self.considered_arms_amt = len(self.current_arms)
        # self.considered_arms_amt = math.ceil(self.considered_arms_amt/2)
        self.current_round = self.current_round + 1
        
        self.budget_left = self.budget_left/2 #FIXME: Is this correct or should it be rounded up before use in the halving method?
        
        # budget_left = self.budget_left
        if self.considered_arms_amt == 1:
          self.sample_count_per_arm = self.budget_left
        else:
          self.sample_count_per_arm = self.get_dist_per_arm(self.considered_arms_amt)
          
        self.current_arm = self.current_arms[0]
        
        if self.return_hist: self.hist.append(self.current_arm)
        
        return self.current_arm
      
     
      self.current_arm = self.current_arms[self.current_arms.index(self.current_arm)+1]
      
      if self.return_hist: self.hist.append(self.current_arm)
      return self.current_arm
    else:
      self.current_iteration = self.current_iteration + 1
      if self.return_hist: self.hist.append(self.current_arm)
      return self.current_arm

  def observe_reward(self, arm: int, reward: float) -> None:
    """
    This function lets us observe rewards from arms we have selected.

    :param arm: Index (starting at 0) of the arm we played.
    :param reward: The reward we received.
    
    """
    self.visits[self.current_arms.index(arm)] = self.visits[self.current_arms.index(arm)] + 1
    self.total_rewards[self.current_arms.index(arm)] = self.total_rewards[self.current_arms.index(arm)] + reward
    self.total_means[self.current_arms.index(arm)] = self.total_rewards[self.current_arms.index(arm)]/self.visits[self.current_arms.index(arm)]
    self.current_rewards[self.current_arms.index(arm)] = self.total_rewards[self.current_arms.index(arm)]/self.visits[self.current_arms.index(arm)]
    
    

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
      self.current_arms = range(k) #A list of all arms that the algorithm cares about. Will be sequentially halved ;)
      self.current_arm = self.current_arms[0] #Keeping track of the current arm to pull
      self.current_rewards = [0] * k #The rewards that the algorithm has observed for each arm
      self.visits = [0] * k #The amount of times that the algorithm has pulled each arm
      self.total_rewards = [0] * k #The total rewards that the algorithm has observed for each arm
      self.considered_arms_amt = k #The amount of arms that the algorithm is currently considering
      self.total_means = [0] * k #The total rewards that the algorithm has observed for each arm
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
    
  

  def choose_arm(self) -> int:
    #print(f"current_arm: {self.current_arm} current index: {self.current_arms.index(self.current_arm)} considered_arms_amt: {self.considered_arms_amt} current_round: {self.current_round} budget_left: {self.budget_left} sample_count_per_arm: {self.sample_count_per_arm} arms left: {len(self.current_arms)}")
    
    self.current_time = int(round(time.time() * 1000))
    #print(f"Current round: {self.current_round} round time: {self.round_time}")
    
      #print(f"current_arms.index(self.current_arm): {self.current_arms.index(self.current_arm)}, considered_arms_amt: {self.considered_arms_amt}")
    # print(f"time elapsed: {self.current_time - self.prev_switch_time} round time: {self.round_time}")
    
    if self.current_time - self.prev_switch_time >= self.round_time:
      
      # Pair each arm with its corresponding reward, sort the pairs, and extract the arms
      self.current_arms, self.current_rewards = zip(*sorted(zip(self.current_arms, self.current_rewards), key=lambda x: x[1], reverse=True))
      self.current_arms = list(self.current_arms)
      self.current_rewards = list(self.current_rewards)
      
      # self.round_time = math.ceil(self.round_time/self.phases)
      
      self.current_arms = self.current_arms[:math.ceil(self.considered_arms_amt/2)] #Take top half of the list
      self.current_rewards = self.current_rewards[:math.ceil(self.considered_arms_amt/2)]
      self.considered_arms_amt = len(self.current_arms)
      self.current_round = self.current_round + 1
      
      self.current_arm_idx = 0
      self.current_arm = self.current_arms[self.current_arm_idx]
      if len(self.current_arms) > 1: self.current_arm_idx = self.current_arm_idx + 1
      
      # print("here")
      if self.return_hist:
        self.hist.append("#") 
        self.hist.append(self.current_arm)
      self.prev_switch_time = int(round(time.time() * 1000))
      return self.current_arm
    
    
    self.current_arm = self.current_arms[self.current_arm_idx]
    
    
    
    if self.current_arm_idx == len(self.current_arms) - 1:
      self.current_arm_idx = 0
    else:
      self.current_arm_idx = self.current_arm_idx + 1
    
    
    if self.return_hist: self.hist.append(self.current_arm)
    
    self.current_time = int(round(time.time() * 1000))
    
    return self.current_arm

      

  def observe_reward(self, arm: int, reward: float) -> None:
    """
    This function lets us observe rewards from arms we have selected.

    :param arm: Index (starting at 0) of the arm we played.
    :param reward: The reward we received.
    
    """
    self.visits[self.current_arms.index(arm)] = self.visits[self.current_arms.index(arm)] + 1
    self.total_rewards[self.current_arms.index(arm)] = self.total_rewards[self.current_arms.index(arm)] + reward
    self.total_means[self.current_arms.index(arm)] = self.total_rewards[self.current_arms.index(arm)]/self.visits[self.current_arms.index(arm)]
    self.current_rewards[self.current_arms.index(arm)] = self.total_rewards[self.current_arms.index(arm)]/self.visits[self.current_arms.index(arm)]
    
    

  def __str__(self):
    return print(f"Sequential_halving:\nArm history: {self.hist}\n")