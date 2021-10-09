import csv
import random 
from utilities import *
import matplotlib.pyplot as plt
import seaborn as sns
import statistics
import statsmodels.stats.weightstats as sms
import os

def get_random_demand(day):
    # this function creates a dictionary of each store with a randomly sampled demand from the pool

    # open and read the specific demand pool file
    with open("demand_pool" + os.sep + f"{day}_pool.csv", mode = 'r') as f:
        f.readline()
        reader = csv.reader(f)
        if (day == "sat"):
            dict = {rows[0]:int(rows[random.randint(1,3)]) for rows in reader}   
        else:
            dict = {rows[0]:int(rows[random.randint(1,15)]) for rows in reader}
    # return the dictionary  
    return dict

def get_rand_cost(day):
    # this function gets the total cost of the optimal routes

    # open the optimal route file and get the cost
    with open(f"{day}.optimal.routes.txt") as f:
        routes = [tuple(line.strip().split(",")) for line in f.readlines()]
    demands = get_random_demand(day)
    return(sum(get_cost_of_bootroute(route,demands) for route in routes))

def get_cost_of_bootroute(route, demand):
    # this function returns the cost of a single route subject to the specified demand
    number_of_pallets = sum(demand.get(store,0) for store in route)                                        # get the number of pallets
    travel_duration = sum(travel_durations[store1][store2] for store1, store2 in zip(route, route[1:]))    # get the travel duration
    minutes = ceil((travel_duration + number_of_pallets * TIME_PER_PALLET)/60)                             # find the minutes it takes
    extrahrs = 0
    # if minutes over than four hours, apply the extra cost
    if (minutes) > 240:
        extrahrs = minutes-240
    return (minutes * (COST_PER_HOUR/60) + extrahrs * (275/60))

def plot_boot(day):
    # this plots the bootstrap distribution of the plots and prints the mean and 95% bootstrap interval
    # get 1000 random costs
    costs = [None] * 1000
    for i in range (1000):
        costs[i] = get_rand_cost(day)
    costs.sort()    # sort the cost

    print("////////////////////////////////////////////////////////////////////////////")
    print('The mean cost for '+ day +' is', statistics.mean(costs))
    print('The 95%" bootstrap confidence interval is', costs[25], ",", costs[975])
    print("///////////////////////////////////////////////////////////////////////////")

    # plot the data
    sns.displot(data = costs, binwidth = 200)

    plt.ylabel("frequency")
    plt.xlabel("cost of route (NZD)")
    plt.title("Bootstrap distribution for cost of optimal "+ day + " route for "+day+" (demands)")
    plt.show()

def main():
    #plot bootstraps
    plot_boot("m_t")
    plot_boot("fri")
    plot_boot("sat")


if __name__ == "__main__":
    main()
