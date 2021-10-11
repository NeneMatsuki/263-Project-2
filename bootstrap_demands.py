import csv
import random 
from utilities import *
import matplotlib.pyplot as plt
import seaborn as sns
import statistics
import statsmodels.stats.weightstats as sms
import os
import numpy as np

global EXCEEDED 
EXCEEDED = np.zeros(23)



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
    #print(sum(checkPallet(route, demands) for route in routes))

    totalCost = 0
    newRoute = []
    extraBus = 0
    for route in routes:
        totalCost += get_cost_of_bootroute(route,demands,routes)[0]

        removedStores = get_cost_of_bootroute(route,demands,routes)[1]

        if(len(removedStores)> 0):
            for i in range(len(removedStores)):
                newRoute.append(removedStores[i])
            nPallets = sum(demands.get(store,0) for store in newRoute)
            travel_duration = sum(travel_durations[store1][store2] for store1, store2 in zip(newRoute, newRoute[1:])) 
            travel_duration += travel_durations["Distribution Centre Auckland"][newRoute[0]] + travel_durations[newRoute[-1]]["Distribution Centre Auckland"]

            if((nPallets > 26) or (travel_duration > 2400)):
                tempRoute = []


                while (((nPallets > 26) or (travel_duration > 2400)) and (len(newRoute) > 1)):
                    tempRoute.append(newRoute[-1])
                    newRoute = newRoute[:-1]
                    nPallets = sum(demands.get(store,0) for store in newRoute)
                    travel_duration = travel_duration - travel_durations[tempRoute[-1]][DISTRIBUTION_CENTER]
                    travel_duration = travel_duration + travel_durations[newRoute[-1]]["Distribution Centre Auckland"]

                minutes = ceil((travel_duration + nPallets * TIME_PER_PALLET)/60)                             # find the minutes it takes
                extrahrs = 0

                # if minutes over than four hours, apply the extra cost
                if (minutes) > 240:
                    extrahrs = minutes-240
                totalCost += ((minutes * (COST_PER_HOUR/60) + extrahrs * (275/60)))
                extraBus += 1
                newRoute = tempRoute
    
    if (len(newRoute)> 0):
        nPallets = sum(demands.get(store,0) for store in newRoute)
        travel_duration = sum(travel_durations[store1][store2] for store1, store2 in zip(newRoute, newRoute[1:])) 
        travel_duration += travel_durations["Distribution Centre Auckland"][newRoute[0]] + travel_durations[newRoute[-1]]["Distribution Centre Auckland"]
        minutes = ceil((travel_duration + nPallets * TIME_PER_PALLET)/60)                             # find the minutes it takes
        extrahrs = 0

        # if minutes over than four hours, apply the extra cost
        if (minutes) > 240:
            extrahrs = minutes-240
        totalCost += ((minutes * (COST_PER_HOUR/60) + extrahrs * (275/60)))
        extraBus += 1

    if((extraBus + len(routes))>60):
        totalCost += ((extraBus + len(routes))-60) * 20000

                
            

    return(totalCost)


def get_cost_of_bootroute(routeO, demand, routes):
    # this function returns the cost of a single route subject to the specified demand

    route = []
    for i in range(len(routeO)):
        route.append(routeO[i])

    newRoute = []
    # if greater than 26, record the route
    if sum(demand.get(store,0) for store in route) > 26:
        i = 0
        while (routes[i] != routeO):
            i = i+1
        EXCEEDED[i] += 1


    while ((sum(demand.get(store,0) for store in route)>24) or ((sum(travel_durations[store1][store2] for store1, store2 in zip(route, route[1:]))) > MAXIMUM_SECONDS_PER_DELIVERY)):
        newRoute.append( route[-2])
        route[-2] = route[-1]
        route = route[:-1]


    number_of_pallets = sum(demand.get(store,0) for store in route)   # get the number of pallets                         
    travel_duration = sum(travel_durations[store1][store2] for store1, store2 in zip(route, route[1:]))    # get the travel duration
    minutes = ceil((travel_duration + number_of_pallets * TIME_PER_PALLET)/60)                             # find the minutes it takes
    extrahrs = 0
    # if minutes over than four hours, apply the extra cost
    if (minutes) > 240:
        extrahrs = minutes-240
    return ((minutes * (COST_PER_HOUR/60) + extrahrs * (275/60)), newRoute)

def plot_boot(day):
    # this plots the bootstrap distribution of the plots and prints the mean and 95% bootstrap interval
    # get 1000 random costs
    costs = [None] * 1000
    for i in range (1000):
        costs[i] = get_rand_cost(day)
    costs.sort()    # sort the cost

    global EXCEEDED

    print("\n////////////////////////////////////////////////////////////////////////////")
    print('The mean cost for '+ day +' is', statistics.mean(costs))
    print('The 95%" bootstrap confidence interval is', costs[25], ",", costs[975])
    print('\nthese are the times each route exceeds the pallet limit:')
    print(EXCEEDED)
    print("///////////////////////////////////////////////////////////////////////////")

    # plot the data
    sns.displot(data = costs, binwidth = 200)

    plt.ylabel("frequency")
    plt.xlabel("cost of route (NZD)")
    plt.title("Bootstrap distribution for cost of optimal "+ day + " route for "+day+" (demands)")
    plt.show()

    EXCEEDED = np.zeros(23)

def main():
    #plot bootstraps
    plot_boot("m_t")
    plot_boot("fri")
    plot_boot("sat")


if __name__ == "__main__":
    main()
