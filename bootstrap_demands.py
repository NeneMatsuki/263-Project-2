from math import ceil
from scipy import stats
import numpy as np
import csv
import pandas as pd
import random 
from utilities import *
import matplotlib.pyplot as plt
import seaborn as sns
import statistics
import statsmodels.stats.weightstats as sms

def get_random_demand_mt():
    with open("mon_thurs_pool.csv", mode = 'r') as f:
        f.readline()
        reader = csv.reader(f)
        dict = {rows[0]:int(rows[random.randint(1,15)]) for rows in reader}
    return dict

def mt_get_rand_cost():
    with open("m_t.optimal.routes.txt") as f:
        routes = [tuple(line.strip().split(",")) for line in f.readlines()]
    demands_mt = get_random_demand_mt()
    return(sum(get_cost_of_route(route,demands_mt) for route in routes))

def get_cost_of_route(route, demand):
     
    number_of_pallets = sum(demand.get(store,0) for store in route)  
    travel_duration = sum(travel_durations[store1][store2] for store1, store2 in zip(route, route[1:]))
    minutes = ceil((travel_duration + number_of_pallets * TIME_PER_PALLET)/60)
    extrahrs = 0
    if (minutes) > 240:
        extrahrs = minutes-240
    return ( minutes * (COST_PER_HOUR/60) + extrahrs * (275/60))


    
def main():
    costs = np.zeros(1000)
    for i in range (1000):
        costs[i] = mt_get_rand_cost()
    # print(costs)
    
    print("////////////////////////////////////////////////////////////////////////////")
    print('The mean cost for Monday to Thurday is', statistics.mean(costs))
    print('The 95%"" confidence interval is', sms.DescrStatsW(costs).tconfint_mean(alpha = 0.05))
    print("///////////////////////////////////////////////////////////////////////////")

    sns.displot(data = costs, binwidth = 200)
    plt.ylabel("frequency")
    plt.xlabel("cost of route (NZD)")
    plt.title("Bootstrap distribution for cost of optimal route for Monday to Thurday(demands)")
    plt.show()




    


if __name__ == "__main__":
    main()
