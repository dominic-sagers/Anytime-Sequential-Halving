import math
import time
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
from scipy.stats import norm
import SequentialHalvingMAB as sh
import csv
from tqdm import tqdm


class MAB_Experiment_runner:
    def __init__(self, num_arms, means_amt):
        self.means_amt = means_amt
        self.num_arms = num_arms
        self.arm_means = self.generate_means()
        np.random.seed(2079) 
            
    def generate_means(self):
        arm_means = np.random.normal(loc=0.0, scale=1.0, size=(self.means_amt, self.num_arms))
        return arm_means
        
    def run_sh_base_experiment(self, iterations, arm_means_idx):
        algo = sh.SequentialHalvingAlg(True, self.num_arms, iterations)
        
        start_time = int(round(time.time() * 1000))
        
        rewards = np.zeros(iterations)
        for t in range(iterations):
            arm = algo.choose_arm()

            reward = norm.rvs(loc=self.arm_means[arm_means_idx,:][arm], scale=1.0)

            algo.observe_reward(arm, reward)
            rewards[t] = reward  
        
        history = algo.hist
        
        total_time = int(round(time.time() * 1000)) - start_time
        
        
        
        print(f"Base SH Done, {iterations} iterations, Time Elapsed: {total_time}")
        
        return history
    
    
    def get_base_sh_times(self, times, iter_range):
        time_dict = {}
        
        # Initialize tqdm progress bar
        pbar = tqdm(iter_range, desc='Progress', unit='iteration')
        
        for iter in pbar:
            start_time = int(round(time.time() * 1000))

            self.run_sh_base_experiment(iter, 0)

            total_time = int(round(time.time() * 1000)) - start_time
            
            for timee in times:
                if total_time >= timee-200 and total_time <= timee+200:
                    time_dict.update({iter : total_time})
                    break
        
        return time_dict
                
        
    
    def plot_sh_experiment(self, history,mean_idx, iterations=None, time_budget=None, type="baseline"):
        frequencies = [history.count(i) for i in range(self.num_arms)]

        # Sort arms based on their means
        sorted_indices = sorted(range(self.num_arms), key=lambda x: self.arm_means[mean_idx, x])
        sorted_frequencies = [frequencies[i] for i in sorted_indices]

        # Plotting the distribution of counts per arm in ascending order
        plt.bar(range(self.num_arms), sorted_frequencies, tick_label=[f'{i}' for i in sorted_indices])
        plt.xlabel('Arms (Sorted by True Arm Means)')
        plt.ylabel('Pull Count')
        if type == "baseline": 
            plt.title(f'Pulls Per Arm - Baseline Sequential Halving | {iterations} Iterations')
        elif type =="anytime":
            plt.title(f'Pulls Per Arm - AnyTime Sequential Halving | {time_budget}ms Time Budget')
        else:
            plt.title(f'Pulls Per Arm - Time Budget Sequential Halving | {time_budget}ms Time Budget')
        plt.show()
    
    def run_sh_anytime_experiment(self, time_budget_ms, arm_means_idx):
        algo = sh.SequentialHalvingAlgAnyTime_v1(time_budget_ms, True, self.num_arms)
        arm_means_idx = int(arm_means_idx)
        rewards = []
        
        while int(round(time.time() * 1000)) < algo.stop_time:
            arm = algo.choose_arm()
            reward = norm.rvs(loc=self.arm_means[arm_means_idx,:][arm], scale=1.0)
            algo.observe_reward(arm, reward)
            rewards.append(reward)
            
        return algo.hist
    
    def run_sh_time_budget_experiment(self, time_budget_ms, arm_means_idx):
        algo = sh.SequentialHalvingAlgTime_v1(time_budget_ms, True, self.num_arms)
        
        rewards = []

        start_time = int(round(time.time() * 1000)) 
        while int(round(time.time() * 1000)) - start_time < time_budget_ms:
            arm = algo.choose_arm()
            arm_means_idx = int(arm_means_idx)
            #print("arm: ", arm)
            reward = norm.rvs(loc=self.arm_means[arm_means_idx,:][arm], scale=1.0)

            algo.observe_reward(arm, reward)
            rewards.append(reward)  
                
        history = algo.hist
        return history
    
    def run_sh_time_budget_experiment2(self, time_budget_ms, arm_means_idx):
        algo = sh.SequentialHalvingAlgTime_v1(time_budget_ms, True, self.num_arms)
        
        rewards = []

        start_time = int(round(time.time() * 1000)) 
        while int(round(time.time() * 1000)) - start_time < time_budget_ms:
            arm = algo.choose_arm()

            reward = norm.rvs(loc=self.arm_means[arm_means_idx,:][arm], scale=1.0)

            algo.observe_reward(arm, reward)
            rewards.append(reward)  
                
        history = algo.hist
        return history, self.arm_means[arm_means_idx,:], algo.total_means
    
    def run_time_budget_range_experiment(self, time_range, arm_means_idx):
        hists = []
        for range in time_range:
            hist = self.run_sh_time_budget_experiment(range, arm_means_idx)
            hists.append(hist)
        return hists
    
    def plot_time_range_experiment(self, histories, arm_means_idx, time_range):
        num_plots = len(histories)
        fig, axes = plt.subplots(num_plots, 1, figsize=(10, 5 * num_plots), gridspec_kw={'hspace': 0.5})
        
        for i, history in enumerate(histories):
            frequencies = [history.count(j) for j in range(self.num_arms)]

            # Sort arms based on their means
            sorted_indices = sorted(range(self.num_arms), key=lambda x: self.arm_means[arm_means_idx, x])
            sorted_frequencies = [frequencies[j] for j in sorted_indices]

            # Plotting the distribution of counts per arm in ascending order
            ax = axes[i] if num_plots > 1 else axes  # Handle single subplot case
            ax.bar(range(self.num_arms), sorted_frequencies, tick_label=[f'{j}' for j in sorted_indices])
            
            title_suffix = f'{iterations} Iterations' if type == "baseline" else f'{time_range[histories.index(history)]}ms'
            ax.set_title(f'{title_suffix}')
        
        fig.supxlabel('Arms (Sorted by True Arm Means)', ha='center', va='center')
        fig.supylabel('Pull Count', ha='center', va='center', rotation='vertical')
    
        plt.tight_layout()
        plt.show()

    #Given a list of means, returns a list of equal size denoting the ranking of the means/arms at that index.
    def rank_means(self, means):
        return [sorted(range(len(means)), key=lambda x: -means[x]).index(i) + 1 for i in range(len(means))]
    
    
    #Given a list which is a ranking of arms (0 indexed), return how far off the true ranking is.
    def get_edit_distance(self, true_means, predicted_means):
        #Make the rankings for each list
        arms_considered = 4 #Only consider the top 4 arms
        indexes_top_arms = []
        
        true_means_ranked = self.rank_means(true_means)
        predicted_means_ranked = self.rank_means(predicted_means)
        # print(true_means_ranked)
        # print(predicted_means_ranked)
        for i in range(len(true_means_ranked)):
            if true_means_ranked[i] < arms_considered:
                indexes_top_arms.append(i)
            if predicted_means_ranked[i] < arms_considered:
                indexes_top_arms.append(i)
        
        #Get the edit distance between these two lists
        return sum([1 for i in range(len(true_means_ranked)) if true_means_ranked[i] != predicted_means_ranked[i] and i in indexes_top_arms])
   
   #Given the true means and the mean of the predicted best arm, returns the regret relative to the true best arm.     
    def get_regret(self, true_means, best_predicted_arm_mean):
        return abs(max(true_means) - best_predicted_arm_mean)
    
 
        
    
    

    
    def run_regret_and_edit_distance_experiment(self, algo_type="iteration", iterations=None, time_budget_ms=None, print_results=True):
        match(algo_type):
            case "iteration":
                regrets = []
                edit_distances = []
                for t in range(self.arm_means.shape[0]):
                    algo = sh.SequentialHalvingAlg(True, self.num_arms, iterations)
                    true_means = self.arm_means[t,:]
                    #rewards = np.zeros(iterations)
                    for i in range(iterations):
                        arm = algo.choose_arm()
                        reward = norm.rvs(loc=self.arm_means[t,:][arm], scale=1.0)
                        algo.observe_reward(arm, reward)
                    # print(true_means)
                    # print(algo.total_means)
                    # assert len(true_means) == len(algo.total_means)
                    keys = algo.total_means.keys()
                    max_val = -1
                    for key in keys:
                        if algo.total_means.get(key) > max_val:
                            max_val = algo.total_means.get(key)
                    # algo.reset()
                    
                    regrets.append(self.get_regret(true_means, max_val))
                    
                    edit_distances.append(self.get_edit_distance(true_means, algo.total_rewards))
                
                avg_regret = sum(regrets) / len(regrets)
                std_regret = np.std(regrets)
                avg_edit_distance = sum(edit_distances) / len(edit_distances)
                std_edit_distance = np.std(edit_distances)
            
            case "time":
                regrets = []
                edit_distances = []
                for t in range(self.arm_means.shape[0]):
                    algo = sh.SequentialHalvingAlgTime_v1(time_budget_ms, True, self.num_arms)
                    start_time = int(round(time.time() * 1000))                     
                    true_means = self.arm_means[t,:]
                    
                    while int(round(time.time() * 1000)) - start_time < time_budget_ms:
                        arm = algo.choose_arm()
                        reward = norm.rvs(loc=self.arm_means[t,:][arm], scale=1.0)
                        algo.observe_reward(arm, reward)
                    
                    
                    keys = algo.total_means.keys()
                    max_val = -1
                    for key in keys:
                        if algo.total_means.get(key) > max_val:
                            max_val = algo.total_means.get(key)
                            
                    # print("\n******************")
                    # print(true_means)
                    # print("\n-----\n")
                    # print(algo.current_arms)
                    # print("\n-----\n")
                    # print(algo.total_means)
                    # print("******************\n")
                    regrets.append(self.get_regret(true_means, max_val))
                    
                    edit_distances.append(self.get_edit_distance(true_means, algo.total_rewards))

                    #print(t)
                
                avg_regret = sum(regrets) / len(regrets)
                std_regret = np.std(regrets)
                avg_edit_distance = sum(edit_distances) / len(edit_distances)
                std_edit_distance = np.std(edit_distances)
            case "anytime":
                regrets = []
                edit_distances = []
                for t in range(self.arm_means.shape[0]):
                    algo = sh.SequentialHalvingAlgAnyTime_v1(time_budget_ms, True, self.num_arms)
                    start_time = int(round(time.time() * 1000))                     
                    true_means = self.arm_means[t,:]
                    
                    while int(round(time.time() * 1000)) <algo.stop_time:
                        arm = algo.choose_arm()
                        reward = norm.rvs(loc=self.arm_means[t,:][arm], scale=1.0)
                        algo.observe_reward(arm, reward)
                    
                    
                    keys = algo.total_means.keys()
                    max_val = -1
                    for key in keys:
                        if algo.total_means.get(key) > max_val:
                            max_val = algo.total_means.get(key)
                            
                    # print("\n******************")
                    # print(true_means)
                    # print("\n-----\n")
                    # print(algo.current_arms)
                    # print("\n-----\n")
                    # print(algo.total_means)
                    # print("******************\n")
                    regrets.append(self.get_regret(true_means, max_val))
                    
                    edit_distances.append(self.get_edit_distance(true_means, algo.total_rewards))

                    #print(t)
                
                avg_regret = sum(regrets) / len(regrets)
                std_regret = np.std(regrets)
                avg_edit_distance = sum(edit_distances) / len(edit_distances)
                std_edit_distance = np.std(edit_distances)
                            
                    
  #  start_time = int(round(time.time() * 1000)) 
#         while int(round(time.time() * 1000)) - start_time < time_budget_ms:
#             arm = algo.choose_arm()

#             reward = norm.rvs(loc=self.arm_means[arm_means_idx,:][arm], scale=1.0)

#             algo.observe_reward(arm, reward)
#             rewards.append(reward)  
                
#         history = algo.hist                  
                    
        if print_results:
            print(f"Sequential Halving Algorithm - Version: {algo_type} Tested over {self.arm_means.shape[0]} different distributions with {num_arms} arms.")
            if algo_type == "iteration":
                print(f"Number of iterations: {iterations}")
            elif algo == "time" or algo == "anytime":
                print(f"Time budget: {time_budget_ms}ms")
            print(f"===============================")
            print(f"Average regret: {avg_regret}")
            print(f"Standard deviation of regret: {std_regret}")
            print(f"Average edit distance: {avg_edit_distance}")
            print(f"Standard deviation of edit distance: {std_edit_distance}")
            print(f"===============================")
            
            
            
        return regrets, avg_regret, std_regret, edit_distances, avg_edit_distance, std_edit_distance
                
                
        


    def make_csv_edit_regret_experiment(self, algo_type="iteration", iteration_range=None, time_range=None):
        avg_regret_list = []
        std_regret_list = []
        avg_edit_distance_list = []
        std_edit_distance_list = []
        
        if algo_type == "iteration":
            for r in iteration_range:
                regrets, avg_regret, std_regret, edit_distances, avg_edit_distance, std_edit_distance = self.run_regret_and_edit_distance_experiment(algo_type, iterations=r, print_results=False)
                avg_regret_list.append(avg_regret)
                std_regret_list.append(std_regret)
                avg_edit_distance_list.append(avg_edit_distance)
                std_edit_distance_list.append(std_edit_distance)
        elif algo_type == "time":  
            for r in time_range:
                regrets, avg_regret, std_regret, edit_distances, avg_edit_distance, std_edit_distance = self.run_regret_and_edit_distance_experiment(algo_type, time_budget_ms=r, print_results=False)
                avg_regret_list.append(avg_regret)
                std_regret_list.append(std_regret)
                avg_edit_distance_list.append(avg_edit_distance)
                std_edit_distance_list.append(std_edit_distance)
        elif algo_type == "anytime":
            for r in time_range:
                regrets, avg_regret, std_regret, edit_distances, avg_edit_distance, std_edit_distance = self.run_regret_and_edit_distance_experiment(algo_type, time_budget_ms=r, print_results=False)
                avg_regret_list.append(avg_regret)
                std_regret_list.append(std_regret)
                avg_edit_distance_list.append(avg_edit_distance)
                std_edit_distance_list.append(std_edit_distance)
        
        filename = f"{algo_type}_regret_edit_distance.csv"
        with open(filename, 'w', newline='') as f:
            writer = csv.writer(f)
            
            # Write header row
            writer.writerow(["Index", "Avg Regret", "Std Regret", "Avg Edit Distance", "Std Edit Distance"])
            
            # Write data rows
            if algo_type == "iteration":
                for i, r in enumerate(iteration_range):
                    writer.writerow([r, avg_regret_list[i], std_regret_list[i], avg_edit_distance_list[i], std_edit_distance_list[i]])
            elif algo_type == "time" or algo_type == "anytime":
                for i, r in enumerate(time_range):
                    writer.writerow([r, avg_regret_list[i], std_regret_list[i], avg_edit_distance_list[i], std_edit_distance_list[i]])
        
        print(f"CSV file created for {algo_type} experiment.")
        return filename



#Experiments to run (write implementation down in detail):
"""
1. Ranking accuracy (average edit distance(?)) over different iteration/time budgets ()
2. Chosen arm true mean reward over different iteration/time budgets (regret: true mean best arm - true mean chosen arm)
"""   
if __name__ == "__main__":
    
    
    csv1it = pd.read_csv("anytime_regret_edit_distance.csv")
    csv1time = pd.read_csv("iteration_regret_edit_distance_time_relative.csv")


    plt.figure(figsize=(8, 5))

    # Plotting Avg Regret vs Time for both datasets
    plt.plot(csv1time["Index"], csv1time["Avg Regret"], label="Base SH", marker='x')
    plt.plot(csv1time["Index"], csv1it["Avg Regret"], label="Iteration Budget", marker='x')
    plt.axhline(y=0, color='r', linestyle='--')  # Add horizontal line at y=0

    plt.xlabel("Time (milliseconds) : Iterations")
    plt.ylabel("Avg Regret")
    plt.title("AnyTime Sequential Halving vs Base Sequential Halving (Time-Relative Iteration Budgets)")
    plt.legend()

    # Adjust x-axis labels to show time and corresponding iterations
    time_iterations_labels = [f"{time}ms : {iterations}" for time, iterations in zip(csv1time["Index"], csv1it["Index"])]
    plt.xticks(csv1time["Index"], time_iterations_labels, rotation=45)

    plt.tight_layout()
    plt.savefig("avg_regret_vs_anytime_vs_relative_iter_csv_overlapped.png")
    plt.show()


    # plt.figure(figsize=(10, 10))

    # # Plotting Avg Regret vs Iteration/Time for CSV 1
    # plt.figure(figsize=(10, 10))

    # # # Plotting Avg Regret vs Iteration for CSV 1
    # plt.subplot(2, 1, 1)
    # plt.plot(csv1it["Index"], csv1it["Avg Regret"], label="Iteration Budget", marker='o')
    # plt.axhline(y=0, color='r', linestyle='--')  # Add horizontal line at y=0
    # plt.xlabel("Time Budget (milliseconds)")
    # plt.ylabel("Avg Regret")
    # plt.title("Avg Regret vs Time Budget (AnyTime Sequential Halving)")
    # plt.legend()
    # plt.xlim(csv1it["Index"].min(), csv1it["Index"].max())  # Set x-axis limits based on CSV 1 data

    # # Plotting Avg Regret vs Time for CSV 1
    # plt.subplot(2, 1, 2)
    # plt.plot(csv1time["Index"], csv1time["Avg Regret"], label="Iterations", marker='o')
    # plt.axhline(y=0, color='r', linestyle='--')  # Add horizontal line at y=0
    # plt.xlabel("Iteration Budget (milliseconds)")
    # plt.ylabel("Avg Regret")
    # plt.title("Avg Regret vs Time-Relative Iteration Budget (Base Sequential Halving - Version 1)")
    # plt.legend()
    # plt.xlim(csv1time["Index"].min(), csv1time["Index"].max())  # Set x-axis limits based on CSV 1 data

    # plt.tight_layout()
    # plt.savefig("avg_regret_vs_anytime_vs_relative_iter_csv.png")
    # # plt.clf()  # Clear the current figure

    # # Plotting Std Regret vs Iteration/Time for CSV 1
    # plt.figure(figsize=(10, 10))

    # # Plotting Std Regret vs Iteration for CSV 1
    # plt.subplot(2, 1, 1)
    # plt.plot(csv1it["Index"], csv1it["Std Regret"], label="Iteration Budget", marker='o')
    # plt.xlabel("Iteration")
    # plt.ylabel("Std Regret")
    # plt.title("Std Regret vs Iteration Budget (Baseline Sequential Halving)")
    # plt.legend()
    # plt.xlim(csv1it["Index"].min(), csv1it["Index"].max())  # Set x-axis limits based on CSV 1 data

    # # Plotting Std Regret vs Time for CSV 1
    # plt.subplot(2, 1, 2)
    # plt.plot(csv1time["Index"], csv1time["Std Regret"], label="Time Budget", marker='o')
    # plt.xlabel("Time Budget (milliseconds)")
    # plt.ylabel("Std Regret")
    # plt.title("Std Regret vs Time Budget (Time Based Sequential Halving - Version 1)")
    # plt.legend()
    # plt.xlim(csv1time["Index"].min(), csv1time["Index"].max())  # Set x-axis limits based on CSV 1 data

    # plt.tight_layout()
    # plt.savefig("std_regret_vs_iteration_time_csv1.png")
    # plt.clf()  # Clear the current figure

    # # Plotting Avg Edit Distance vs Iteration/Time for CSV 1
    # plt.figure(figsize=(10, 10))

    # # Plotting Avg Edit Distance vs Iteration for CSV 1
    # plt.subplot(2, 1, 1)
    # plt.plot(csv1it["Index"], csv1it["Avg Edit Distance"], label="Iteration Budget", marker='o')
    # plt.xlabel("Iteration")
    # plt.ylabel("Avg Edit Distance")
    # plt.title("Avg Edit Distance vs Iteration Budget (Baseline Sequential Halving)")
    # plt.legend()
    # plt.xlim(csv1it["Index"].min(), csv1it["Index"].max())  # Set x-axis limits based on CSV 1 data

    # # Plotting Avg Edit Distance vs Time for CSV 1
    # plt.subplot(2, 1, 2)
    # plt.plot(csv1time["Index"], csv1time["Avg Edit Distance"], label="Time Budget", marker='o')
    # plt.xlabel("Time Budget (milliseconds)")
    # plt.ylabel("Avg Edit Distance")
    # plt.title("Avg Edit Distance vs Time Budget (Time Based Sequential Halving - Version 1)")
    # plt.legend()
    # plt.xlim(csv1time["Index"].min(), csv1time["Index"].max())  # Set x-axis limits based on CSV 1 data

    # plt.tight_layout()
    # plt.savefig("avg_edit_distance_vs_iteration_time_csv1.png")
    # plt.clf()  # Clear the current figure

    # # Plotting Std Edit Distance vs Iteration/Time for CSV 1
    # plt.figure(figsize=(10, 10))

    # # Plotting Std Edit Distance vs Iteration for CSV 1
    # plt.subplot(2, 1, 1)
    # plt.plot(csv1it["Index"], csv1it["Std Edit Distance"], label="Iteration Budget", marker='o')
    # plt.xlabel("Iteration")
    # plt.ylabel("Std Edit Distance")
    # plt.title("Std Edit Distance vs Iteration Budget (Baseline Sequential Halving)")
    # plt.legend()
    # plt.xlim(csv1it["Index"].min(), csv1it["Index"].max())  # Set x-axis limits based on CSV 1 data

    # # Plotting Std Edit Distance vs Time for CSV 1
    # plt.subplot(2, 1, 2)
    # plt.plot(csv1time["Index"], csv1time["Std Edit Distance"], label="Time Budget", marker='o')
    # plt.xlabel("Time Budget (milliseconds)")
    # plt.ylabel("Std Edit Distance")
    # plt.title("Std Edit Distance vs Time Budget (Time Based Sequential Halving - Version 1)")
    # plt.legend()
    # plt.xlim(csv1time["Index"].min(), csv1time["Index"].max())  # Set x-axis limits based on CSV 1 data

    # plt.tight_layout()
    # plt.savefig("std_edit_distance_vs_iteration_time_csv1.png")
    # plt.clf()  # Clear the current figure
        
   
    """
    
    ms - iterations
    500ms - 18500
    1000ms - 37000
    1500ms - 55500
    2000ms - 73000
    2500ms - 93000
    3000ms - 112500
    3500ms - 131000
    4000ms - 150500
    4500ms - 167500
    5000ms - 186500
    

    
    """
    
    
    # num_arms = 10
    # means_amt = 100
    # iterations = 60000
    # arm_means_idx = 5
    # times = range(500,5500,500)
    # iters = [18500, 37000, 55500, 73000, 93000, 112500, 131000, 150500, 167500, 186500]
    # time_budget_ms = 1000

    # mab_exp_runner = MAB_Experiment_runner(num_arms, means_amt)
    # mab_exp_runner.make_csv_edit_regret_experiment(algo_type="iteration", iteration_range=iters)
    # mab_exp_runner.run_sh_base_experiment(190000, 5)
    # time_dict = mab_exp_runner.get_base_sh_times(times, range(16000, 190500, 500))

    # print(time_dict)
    # hist = mab_exp_runner.run_sh_anytime_experiment(time_budget_ms, arm_means_idx)
    # print(hist)
    # mab_exp_runner.plot_sh_experiment(hist,arm_means_idx,time_budget=time_budget_ms,type="anytime")
    # mab_exp_runner.run_regret_and_edit_distance_experiment("anytime",time_budget_ms=time_budget_ms,print_results=True)
    
    
    # # # # mab_exp_runner.run_regret_and_edit_distance_experiment(algo_type="iteration", iterations=iterations)
    # # # mab_exp_runner.run_regret_and_edit_distance_experiment(algo_type="time", time_budget_ms=1000)

    
    # # # mab_exp_runner.make_csv_edit_regret_experiment(algo_type="time", time_range=times)
    # mab_exp_runner.make_csv_edit_regret_experiment(algo_type="anytime", time_range=times)
    # # mab_exp_runner.make_csv_edit_regret_experiment(algo_type="iteration", iteration_range=[100,500,1000,5000,10000])
    # print(mab_exp_runner.arm_means[arm_means_idx, :])
    
    # histories = mab_exp_runner.run_time_budget_range_experiment(time_range, arm_means_idx)
    # print(mab_exp_runner.arm_means[arm_means_idx,:])
    # histories = mab_exp_runner.run_time_budget_range_experiment([500], arm_means_idx)
    # mab_exp_runner.plot_time_range_experiment(histories, arm_means_idx, time_range)
    
    # history = mab_exp_runner.run_sh_base_experiment(iterations, arm_means_idx)
    # mab_exp_runner.plot_sh_experiment(history,arm_means_idx, iterations=iterations,type="baseline")
    
    # print(mab_exp_runner.arm_means[arm_means_idx,:])
    # history = mab_exp_runner.run_sh_time_budget_experiment(time_budget_ms, arm_means_idx)
    # mab_exp_runner.plot_sh_experiment(history, time_budget=time_budget_ms, type="time_budget")
    # print(history)
    
    
    # frequencies = [history.count(i) for i in range(num_arms)]

    # # Sort arms based on their means
    # print(arm_means_idx)
    # sorted_indices = sorted(range(num_arms), key=lambda x: mab_exp_runner.arm_means[arm_means_idx, x])
    # sorted_frequencies = [frequencies[i] for i in sorted_indices]

    # # Plotting the distribution of counts per arm in ascending order
    # plt.bar(range(num_arms), sorted_frequencies, tick_label=[f'{i}' for i in sorted_indices])
    # plt.xlabel('Arms (Sorted by True Arm Means Means)')
    # plt.ylabel('Pull Count')
    # plt.title(f'Distribution of Counts per Arm Baseline Sequential Halving | {iterations} Iterations')
    # plt.show()
    
    # #print(history)