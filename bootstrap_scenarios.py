import csv
import random 
from utilities import *
import matplotlib.pyplot as plt
import seaborn as sns
import statistics
import statsmodels.stats.weightstats as sms
import os
import numpy as np
from scipy import stats

# stores whcih routes exceeded demand
global EXCEEDED 
EXCEEDED = np.zeros(25)

global ORIGINALTOTAL
ORIGINALTOTAL = 132946

def get_random_demand(day):
    """ returns a dictinoary with demands for each day randomly pulled from a pool
        
        Parameters:
        -----------
        string      day: the day of the pool that we must select from

        Returns:
        --------
        dictionary  dict: demands for each day randomly pulled from a pool

        Notes:
        ------
        This function is called within get_rand_cost()

    """

    # open and read the specific demand pool file
    with open("demand_pool" + os.sep + f"{day}_pool.csv", mode = 'r') as f:
        f.readline()
        reader = csv.reader(f)
        if (day != "m_t_manukau"):
            dict = {rows[0]:int(rows[random.randint(1,3)]) for rows in reader}   
        else:
            dict = {rows[0]:int(rows[random.randint(1,15)]) for rows in reader}
    # return the dictionary  
    return dict

def get_total_cost(pool, day):
    """ returns the total cost of the optimal routes for a day
        
        Parameters:
        -----------
        string  day:    the day of the pool that we must select from

        Returns:
        --------
        int totalCost:  the total cost of the optimal routes

        Notes:
        ------
        This function is called within plot_boot()

    """
    # open the optimal route file and get the cost
    with open("optimal routes" + os.sep  + f"{pool}.optimal.routes.txt") as f:
        routes = [tuple(line.strip().split(",")) for line in f.readlines()]
    demands = get_random_demand(pool)
    #print(sum(checkPallet(route, demands) for route in routes))

    totalCost = 0 # this stores the total cost of the route
    newRoute = [] # this stores any new route made
    extraBus = 0  # stores any extra busses needed

    # loop through all the routes
    for route in routes:

        # get the total cost of the route and the removed stores from the route in order to keep routes under constraint. Add the cost to the total cost
        totalCost += get_cost_of_bootroute(route,demands,routes,day)[0]
        removedStores = get_cost_of_bootroute(route,demands,routes, day)[1]

        # if there are some stores removed
        if(len(removedStores)> 0):

            # append stores removed to newRoute
            for i in range(len(removedStores)):
                newRoute.append(removedStores[i])

            # get the details of the newRoute
            nPallets, travel_duration = get_newRoute_details(newRoute, demands, day)

            # if the newRoute exceeds the constraints
            if((nPallets > MAXIMUM_PALLETS_PER_DELIVERY) or (travel_duration > MAXIMUM_SECONDS_PER_DELIVERY)):
                
                tempRoute = [] # this stores the stores removed from newRoute

                # while newRoute does not meet the constraints
                while (((nPallets > 26) or (travel_duration > 2400)) and (len(newRoute) > 1)):
                    # remove last store and record
                    tempRoute.append(newRoute[-1])
                    newRoute = newRoute[:-1]
                    # re-calculate details of newRoute
                    nPallets, travel_duration = get_newRoute_details(newRoute, demands, day)
                
                if((extraBus + len(routes))>MAXIMUM_NUMBER_OF_TRUCKS_PER_DAY):
                    totalCost += 2000
                else:
                    totalCost += calculate_cost(nPallets, travel_duration) # add the cost of the newRoute to the total cost
                extraBus += 1                                          # add an Extra bus used
                newRoute = tempRoute                                   # replaced newRoute with stores removed from the previous one
    
    # if there are still stores in newRoute after all the optimal routes has been checked
    if (len(newRoute)> 0):

        # add the cost of the new route to the total cost and increase the number of trucks used
        nPallets, travel_duration = get_newRoute_details(newRoute, demands, day)
        totalCost += calculate_cost(nPallets, travel_duration)
        extraBus += 1

    # # if the number of trucks used exceeds the maximum trucks per day,  add $20000 to total cost for every truck rented
    # if((extraBus + len(routes))>MAXIMUM_NUMBER_OF_TRUCKS_PER_DAY):
    #     totalCost += ((extraBus + len(routes))-60) * 20000

    # return the total cost
    return(totalCost)

def get_cost_of_bootroute(routeO, demand, routes, day):
    """ returns the cost of a single route subject to the specified demand, and stores if constraints not met
        
        Parameters:
        -----------
        tupule      routeO: the original route in the day
        dictionary  demand: dictionary of the random demand of the particular day
        list        routes: all the routes for that day

        Returns:
        --------
        int      totalCost: the total cost of the optimal routes
        string   newRoute : stores taken off route if route does not meet constraint

        Notes:
        ------
        This function checks if the route subject to random demands still meets the constraints. 
        If not, it adjust the route and returns the cost of the newly calculated route
        Called in get_rand_cost(day)

    """

    # convert route to string from tuple for easier manipulation
    route = []
    for i in range(len(routeO)):
        route.append(routeO[i])

    newRoute = []   # this stores the new route

    # if the number of pallets exceeds the truck capacity
    if sum(demand.get(store,0) for store in route) > MAXIMUM_PALLETS_PER_DELIVERY:
        # record which route exceeded capacity
        i = 0
        while (routes[i] != routeO):
            i = i+1
        EXCEEDED[i] += 1

    # while the route has too many pallets or takes too long (more than 4hrs)
    while ((sum(demand.get(store,0) for store in route)>MAXIMUM_PALLETS_PER_DELIVERY) or ((sum(travel_durations[store1][store2] for store1, store2 in zip(route, route[1:]))) > MAXIMUM_SECONDS_PER_DELIVERY)):
        newRoute.append(route[-2])  # add the last store to nwew route
        route[-2] = route[-1]       # replace the last store with distribution centre
        route = route[:-1]          # make route shorter

    number_of_pallets = sum(demand.get(store,0) for store in route)   # get the number of pallets                         
    travel_duration = sum(random_congest_time(day, store1, store2) for store1, store2 in zip(route, route[1:]))    # get the travel duration

    # return the cost of the route and the stores that were removed
    return (calculate_cost(number_of_pallets, travel_duration), newRoute)

def calculate_cost(number_of_pallets, travel_duration):
    """ returns cost of a singular route
        
        Parameters:
        -----------
        int number_of_pallets:  the number of pallets in the route
        int travel_duration  :  the travl duration of the route

        Returns:
        --------
        int : cost of the route

        Notes:
        ------
        This function is called within get_total_cost() and get_cost_of_bootroute()

    """
    # this function calculates the cost of a route
    minutes = ceil((travel_duration + number_of_pallets * TIME_PER_PALLET)/60)                             # find the minutes it takes
    extrahrs = 0
    # if minutes over than four hours, apply the extra cost
    if (minutes) > 240:
        extrahrs = minutes-240
    return ((minutes * (COST_PER_HOUR/60) + extrahrs * (275/60)))

def get_newRoute_details(newRoute, demands, day):
    """ returns the pallets and travel duration

        Parameters:
        -----------
        list        newRoute:   new route to be chceked, contains stores only
        dictionary  demands :   randomly generated demands for a particular day

        Returns:
        --------
        int nPallets        : number of pallets in a day
        int travel_duration : the duration of time the route will take in seconds

        Notes:
        ------
        This function calculates the travel duration of the new route by adding durations to adn from the distribution centre
        This function is called within get)total_cost()

    """
    # thias function returns the number of pallets and the travel duration for a new route
    nPallets = sum(demands.get(store,0) for store in newRoute)
    travel_duration = sum(random_congest_time(day, store1, store2) for store1, store2 in zip(newRoute, newRoute[1:])) 

    # must add travel duration to and from distribution centre 
    travel_duration += random_congest_time(day, "Distribution Centre Auckland", newRoute[0]) + random_congest_time(day, newRoute[-1], "Distribution Centre Auckland")
    return (nPallets, travel_duration)

def plot_boot(pool, day):
    """ plots the bootstrap distribution of the plots and prints the mean and 95% bootstrap interval
        
        Parameters:
        -----------
        string  day:    the day of the pool that we must select from

        Returns:
        --------
        None

        Notes:
        ------
        when called in main, should plot the boot straop intervals and print the mean and 95% boot strap confidence interval
        for the sake of improving the model, it also prints the numbert of times each route in a day exceeds constrainsts so stores have to be removed.
        This data is printed in form of a list where position i corresponds to route i in a total route

    """

    # get 1000 random costs
    costs = [None] * 1000
    for i in range (1000):
        costs[i] = get_total_cost(pool, day)
    costs.sort()    # sort the cost

    no_stores_removed = True

    if(pool != day):
        no_stores_removed = False

    if(no_stores_removed):
        found = False
        i = 0
        original  = np.full(1000,19113.75)
        if(day == "m_t"):
            while((i < 1000) and (found == False)):
                if (costs[i] > 19113.75):
                    found = True
                i+=1

        elif(day == "fri"):
            original = np.full(1000, 18750)
            while((i < 1000) and (found == False)):
                if (costs[i] > 18750):
                    found = True
                i += 1

        else:
            original = np.full(1000, 11831.25)
            while((i < 1000) and (found == False)):
                if (costs[i] > 11831.25):
                    found = True
                i += 1

    global EXCEEDED
    global ORIGINALTOTAL


    if(no_stores_removed):
        errorRate = sum(np.greater(costs, original))/len(costs)
        if(pool == "m_t"):
            ORIGINALTOTAL += 4*statistics.mean(costs)
        else:
            ORIGINALTOTAL += statistics.mean(costs)


    print("///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////")
    print('The mean cost for '+ pool +' is', statistics.mean(costs))
    print('The 95%" bootstrap confidence interval is', costs[25], ",", costs[975], '\n')
    if(no_stores_removed):
        print('If we plan our project using expected times and the resulting optimal path, cost will be greater than expected, ', errorRate * 100, '% of the time')
        print('\nthese are the times each route exceeds the pallet limit:')
        print(EXCEEDED)
    print("/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////")

    # plot the data
    sns.displot(data = costs, binwidth = 200)

    plt.ylabel("frequency")
    plt.xlabel("cost of route (NZD)")
    plt.title("Bootstrap distribution for cost of "+ day)
    plt.tight_layout()
    if(no_stores_removed):
        plt.savefig("bootstrap plots" + os.sep + pool + " bootstrap")
    else:
        plt.savefig("bootstrap plots" + os.sep + "stores deleted on" + day)
    plt.show()

    EXCEEDED = np.zeros(26)

def scenario_t_test():
    # construct totals for each scenario

    print("\n----------------------------------------------------------Comparing scenarios----------------------------------------------------------\n")

    costsO = [None] * 1000
    for i in range (1000):
        costsO[i] = 4 * get_total_cost("m_t", "m_t")
        costsO[i] += get_total_cost("fri", "fri")
        costsO[i] += get_total_cost("sat", "sat")

    costsO.sort()    # sort the cost

    costsD = [None] * 1000
    for i in range (1000):
        costsD[i] = 4* get_total_cost("routes_deleted" + os.sep + "m_t_deleted", "m_t")
        costsD[i] += get_total_cost("routes_deleted" + os.sep + "fri_deleted", "fri")
        costsD[i] += get_total_cost("routes_deleted" + os.sep + "sat_deleted", "sat")
    costsD.sort()    # sort the cost

    C_I = sms.CompareMeans(sms.DescrStatsW(costsO), sms.DescrStatsW(costsD))

    # return the t test results
    print("This is the t-test result where H0 = the costs for scenarios with and without deletion of stores is the same:")
    print(stats.ttest_ind(costsO,costsD))
    print('\nThe 95%" confidence interval for difference in means assuming equal deviation is', C_I.tconfint_diff())
    print('\n---------------------------------------------------------------------------------------------------------------------------------------\n')



if __name__ == "__main__":

    plot_Simulation = False        # plot original distribution
    plot_with_stores_deleted = True # plot with some stores deleted
    get_CI_for_scenarios = True # get the condifence interval of difference between deleting and not deleting stores

    if(plot_Simulation):
        ORIGINALTOTAL = 0
        print("\n----------------------------------------------------Investigating original routes----------------------------------------------------\n")
        plot_boot("m_t", "m_t")
        plot_boot("fri", "fri")
        plot_boot("sat", "sat")
        print('\nthis scenario is', round((ORIGINALTOTAL - 107036)*100/107036,2), " %' higher than  our expected optimal cost")
        print('\n-------------------------------------------------------------------------------------------------------------------------------------\n')

    #plot bootstraps
    if(plot_with_stores_deleted):
        print("\n\n------------Investigating scenario where Countdown Manukau, Papakura, northwest, Higland Park, and Sylvia Park is deleted------------\n")
        plot_boot("routes_deleted" + os.sep + "m_t_deleted", "m_t")
        plot_boot("routes_deleted" + os.sep + "fri_deleted", "fri")
        plot_boot("routes_deleted" + os.sep + "sat_deleted", "sat")
        print('\n-------------------------------------------------------------------------------------------------------------------------------------\n')

    if(get_CI_for_scenarios):
        scenario_t_test()
