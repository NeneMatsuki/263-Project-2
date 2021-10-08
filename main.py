from get_routes import get_routes
from get_optimal_routes import get_optimal_routes
from maping import fri_map, mon_thrs_map, sat_map
import time


def main():
    days = ["m_t", "fri", "sat"]

    # get the route for each of the relevants days
    for day in days:
        get_routes(day)

    # get the optimal route for each day
    optimal_routes = {}
    for day in days:
        optimal_routes[day] = get_optimal_routes(day)

    # write the optimal routes to a file
    with open("optimal.csv", "w") as f:
        for day in days:
            for route in optimal_routes[day]:
                f.write(f"{day}," + ",".join(route) + "\n")

    #mapping optimum routes for each day,  #waiting a minute in between to preven rate limit exceeding
    mon_thrs_map()
    time.sleep(60)
    fri_map()
    time.sleep(60)
    sat_map()

if __name__ == "__main__":
    main()
