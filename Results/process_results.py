import csv
from tqdm import tqdm
import math
import numpy as np
import pandas as pd
import statistics
import re
import matplotlib.pyplot as plt
import os


def process_raw_results(csv_path):
    data = pd.read_csv(csv_path)
    
    n = data.shape[0]
    
    pattern = r"\('([^']*)' / '([^']*)'\)"
    input_str = data.iloc[0]['agents']
    match = re.match(pattern, input_str)
    if match:
        agent1 = match.group(1)
        agent2 = match.group(2)
        
    agents = sorted([agent1, agent2])
    agent1, agent2 = agents
        
    agent1_scores = []
    agent2_scores = []
    
    for index, row in data.iterrows():
        agents = row['agents']
        utilities = row['utilities']
        
        if agents == f"('{agent1}' / '{agent2}')":
            score1, score2 = convert_utilities(utilities)
            agent1_scores.append(score1)
            agent2_scores.append(score2)
        else:
            score1, score2 = convert_utilities(utilities)
            agent1_scores.append(score2)
            agent2_scores.append(score1)
    
    mean1 = statistics.mean(agent1_scores)
    mean2 = statistics.mean(agent2_scores)
    
    std1 = statistics.stdev(agent1_scores)
    std2 = statistics.stdev(agent2_scores)
    
    conf1 = 1.96*(std1/math.sqrt(n))
    conf2 = 1.96*(std2/math.sqrt(n))
    
    return mean1, mean2, std1, std2, conf1, conf2, agent1, agent2


def make_results_dataframe_csv(csv_paths, game_name, time_or_iterations):
    # Create an empty list to store the results
    results = []
    
    # Process each CSV file
    for csv_path, value in zip(csv_paths, time_or_iterations):
        # Process the raw results
        mean1, mean2, std1, std2, conf1, conf2, agent1, agent2 = process_raw_results(csv_path)
        data = pd.read_csv(csv_path)
        
        # Create a dictionary to store the results for this CSV file
        result = {
            'Iterations/Time': value,
            'Agent1': agent1,
            'Agent2': agent2,
            f'{agent1}_Mean': mean1,
            f'{agent2}_Mean': mean2,
            f'{agent1}_Confidence': conf1,
            f'{agent2}_Confidence': conf2,
        }
        results.append(result)
    
    # Create a DataFrame from the list of results
    results_df = pd.DataFrame(results)
    
    # Save the DataFrame to a CSV file
    results_df.to_csv(f"{game_name}_{agent1}_{agent2}_results_dataframe.csv", index=False)

def convert_utilities(utility_str):
    # Split the string by the semicolon
    utility_values = utility_str.split(';')
    # Convert the split values to integers
    util1, util2 = [int(float(value)) for value in utility_values]
    util1 = (util1 + 1)/2
    util2 = (util2 + 1)/2
    return util1, util2

def make_plot(csv_path, agent, file_name):
    df = pd.read_csv(csv_path)
    # Convert means and confidence intervals to percentages
    df['Agent1_Mean'] *= 100
    df['Agent1_Confidence'] *= 100
    df['Agent2_Mean'] *= 100
    df['Agent2_Confidence'] *= 100

    # Plotting
    plt.figure(figsize=(10, 6))

    if agent == 1:
        # Plot Agent 1's mean with shaded region for confidence interval
        plt.plot(df['Iterations/Time'], df['Agent1_Mean'], label="Anytime SH", marker='o')
        plt.fill_between(df['Iterations/Time'], df['Agent1_Mean'] - df['Agent1_Confidence'], df['Agent1_Mean'] + df['Agent1_Confidence'], alpha=0.3)
    elif agent == 2:
        # # Plot Agent 2's mean with shaded region for confidence interval
        plt.plot(df['Iterations/Time'], df['Agent2_Mean'], label=df['Agent2'].iloc[0], marker='o')
        plt.fill_between(df['Iterations/Time'], df['Agent2_Mean'] - df['Agent2_Confidence'], df['Agent2_Mean'] + df['Agent2_Confidence'], alpha=0.3)

    # Set labels and title
    plt.xlabel('Iterations')
    plt.ylabel('Win Rate (%)')
    # plt.title('Anytime Sequential Halving Win Rate vs UCT - Pentalath')
    plt.legend()

    # Set y-axis limits to 0-100%
    plt.ylim(0, 100)

    # Increase the resolution of the y-axis tick marks
    plt.yticks(range(0, 101, 5))  # Tick marks every 5%

    # Show plot
    plt.savefig(file_name)
    plt.show()

def make_doubleplot_plot(csv_path1, csv_path2, df1_agent_to_plot, df2_agent_to_plot, opponent, game):
    df1 = pd.read_csv(csv_path1)
    df2 = pd.read_csv(csv_path2)
    # Convert means and confidence intervals to percentages
    df1[f'{df1_agent_to_plot}_Mean'] *= 100
    df1[f'{df1_agent_to_plot}_Confidence'] *= 100
    df1[f'{opponent}_Mean'] *= 100
    df1[f'{opponent}_Confidence'] *= 100

    # Convert means and confidence intervals to percentages
    df2[f'{opponent}_Mean'] *= 100
    df2[f'{opponent}_Confidence'] *= 100
    df2[f'{df2_agent_to_plot}_Mean'] *= 100
    df2[f'{df2_agent_to_plot}_Confidence'] *= 100
    # Plotting
    plt.figure(figsize=(10, 6))

    plt.plot(df1['Iterations/Time'], df1[f'{df1_agent_to_plot}_Mean'], label=df1_agent_to_plot, marker='o')
    plt.fill_between(df1['Iterations/Time'], df1[f'{df1_agent_to_plot}_Mean'] - df1[f'{df1_agent_to_plot}_Confidence'], df1[f'{df1_agent_to_plot}_Mean'] + df1[f'{df1_agent_to_plot}_Confidence'], alpha=0.3)

    plt.plot(df2['Iterations/Time'], df2[f'{df2_agent_to_plot}_Mean'], label=df2_agent_to_plot, marker='o')
    plt.fill_between(df2['Iterations/Time'], df2[f'{df2_agent_to_plot}_Mean'] - df2[f'{df2_agent_to_plot}_Confidence'], df2[f'{df2_agent_to_plot}_Mean'] + df2[f'{df2_agent_to_plot}_Confidence'], alpha=0.3)

    # Set labels and title
    plt.xlabel('Iterations')
    plt.ylabel('Win Rate (%)')

    plt.title(f'{game} - vs. {opponent}')
    plt.legend()

    # Set y-axis limits to 0-100%
    plt.ylim(0, 100)

    # Increase the resolution of the y-axis tick marks
    plt.yticks(range(0, 101, 5))  # Tick marks every 5%

    # Show plot
    plt.savefig(f"{df1_agent_to_plot} and {df2_agent_to_plot} vs {opponent} - {game}.png")


if __name__ == "__main__":
    #data = pd.read_csv('C://Users//domin\Documents//UM//Thesis//Code//Sequential-Halving-With-Time-Constraints-In-Ludii//Ludii_Experiment_Data//anytime_vs_baseSH//clobber//150000//raw_results.csv')

    # paths = {f'C://Users//domin//Documents//UM//Thesis//Code//Sequential-Halving-With-Time-Constraints-In-Ludii//Ludii_Experiment_Data//base_SH_UCT//{game}//150000//raw_results.csv',
    #          f'C://Users//domin//Documents//UM//Thesis//Code//Sequential-Halving-With-Time-Constraints-In-Ludii//Ludii_Experiment_Data//base_SH_UCT//{game}//100000//raw_results.csv',
             
    #          f'C://Users//domin//Documents//UM//Thesis//Code//Sequential-Halving-With-Time-Constraints-In-Ludii//Ludii_Experiment_Data//base_SH_UCT//{game}//1000//raw_results.csv'}
    # # # # 

    
    
    # paths = {f'C://Users//domin//Documents//UM//Thesis//Code//Sequential-Halving-With-Time-Constraints-In-Ludii//Ludii_Experiment_Data//base_SH_UCT//{game}//50000//raw_results.csv',
    #         f'C://Users//domin//Documents//UM//Thesis//Code//Sequential-Halving-With-Time-Constraints-In-Ludii//Ludii_Experiment_Data//base_SH_UCT//{game}//10000//raw_results.csv',
    #         f'C://Users//domin//Documents//UM//Thesis//Code//Sequential-Halving-With-Time-Constraints-In-Ludii//Ludii_Experiment_Data//base_SH_UCT//{game}//5000//raw_results.csv',
    #         f'C://Users//domin//Documents//UM//Thesis//Code//Sequential-Halving-With-Time-Constraints-In-Ludii//Ludii_Experiment_Data//base_SH_UCT//{game}//1000//raw_results.csv'}
    
   
    # # make_results_dataframe_csv(paths, game, [10000, 5000,1000])
    # make_results_dataframe_csv(paths, game, [50000, 10000, 5000, 1000])
    # csv_path = f'Ludii_Experiment_Data//{game}_SHUCT_UCT_results_dataframe.csv'
    # agent = 1
    

    # file_name = f"SHUCT vs UCT - {game}.png"
    # make_plot(csv_path, agent, file_name)

    # for game in games:
        
    #     csv_path = f'Ludii_Experiment_Data//{game}_SHUCT_UCT_results_dataframe.csv'
    #     agent = 2

    #     file_name = f"UCT vs HMCTS (Opponent-Plot) - {game}.png"
    #     make_plot(csv_path, agent, file_name)

    # for game in games:
    #         #pentalath_SHUCTAnyTime_SHUCT_results_dataframe
    #         csv_path = f'Ludii_Experiment_Data//{game}_SHUCTAnyTime_SHUCT_results_dataframe.csv'
    #         agent = 1


    #         file_name = f"Anytime SH vs HMCTS (Opponent-Plot) - {game}.png"
    #         make_plot(csv_path, agent, file_name)
    
    games = ["Amazons", "Breakthrough", "Clobber", "Pentalath"]
    budgets = [1000, 5000, 10000, 20000, 30000, 40000, 50000]
    
    for game in games:
        paths = [f'anytimeSH_baseSH/{game}/{budget}/raw_results.csv' for budget in budgets]
        make_results_dataframe_csv(paths, game, budgets)
        
        paths = [f'anytimeSH_UCT/{game}/{budget}/raw_results.csv' for budget in budgets]
        make_results_dataframe_csv(paths, game, budgets)
        
        paths = [f'base_SH_UCT/{game}/{budget}/raw_results.csv' for budget in budgets]
        make_results_dataframe_csv(paths, game, budgets)
    
    for game in games:
        csv_path1 =  os.path.join(os.getcwd(), f'{game}_SHUCT_SHUCTAnyTime_results_dataframe.csv')
        agent1_name = "SHUCTAnyTime"
                
        csv_path2 = os.path.join(os.getcwd(), f'{game}_Example UCT_SHUCT_results_dataframe.csv')
        agent2_name = "Example UCT"

        opp = "SHUCT"
        make_doubleplot_plot(csv_path1, csv_path2, agent1_name, agent2_name, opp, game)
        
    for game in games:
        csv_path1 =  os.path.join(os.getcwd(), f'{game}_Example UCT_SHUCTAnyTime_results_dataframe.csv')
        agent1_name = "SHUCTAnyTime"
                
        csv_path2 = os.path.join(os.getcwd(), f'{game}_Example UCT_SHUCT_results_dataframe.csv')
        agent2_name = "SHUCT"

        opp = "Example UCT"
        make_doubleplot_plot(csv_path1, csv_path2, agent1_name, agent2_name, opp, game)
        
    plt.show()

    
    
    
    
   



 

    
    
 