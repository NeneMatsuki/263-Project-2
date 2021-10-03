import pulp
from utilities import (
    get_cost_of_route,
    COST_PER_HOUR,
    MAXIMUM_NUMBER_OF_TRUCKS_PER_DAY,
    demands,
    write_routes,
)
import math
import pprint


def _get_optimal_routes(routes, stores, day):
    """return the most optimal route given a list of routes, stores, and the day"""

    # Create a decision variable for each route store in a dict
    x = pulp.LpVariable.dicts("route", routes, lowBound=0, upBound=1, cat=pulp.LpInteger,)

    # construct the the model
    routing_model = pulp.LpProblem(f"Woolsworth Optimal Routes for {day}", pulp.LpMinimize)

    # specify objective function as the sum of the cost of routes
    routing_model += pulp.lpSum([get_cost_of_route(route,day) * x[route] for route in routes])

    # specify maximum number of routes
    routing_model += (
        pulp.lpSum([x[route] for route in routes]) <= MAXIMUM_NUMBER_OF_TRUCKS_PER_DAY,
        "Maximum_number_of_routes",
    )

    # for each store constrain so that only one route goes to that store
    for store in stores:
        routing_model += (
            pulp.lpSum([x[route] for route in routes if store in route]) == 1,
            f"Must_route_{store}",
        )

    # solve linear model, print status, and write to lp file
    routing_model.solve(pulp.PULP_CBC_CMD(msg=1))
    print("Status:", pulp.LpStatus[routing_model.status], routing_model.status)
    print("The choosen tables are out of a total of %s:" % len(routes))
    routing_model.writeLP(f"out-{day}.lp", max_length=500)

    # return the chosen routes
    chosen_routes = [route for route in routes if x[route].value() == 1.0]
    return chosen_routes


def get_optimal_routes(day):
    """get the optimal route for a given day"""
    with open(f"{day}.routes.txt") as f:
        routes = [tuple(line.strip().split(",")) for line in f.readlines()]
    stores = list(demands[day].keys())
    routes = _get_optimal_routes(routes, stores, day)
    write_routes(routes, f"{day}.optimal.routes.txt")
    return routes


def main():
    """get the optimal routes for each day from all possible routes on that day"""
    get_optimal_routes("m_t")
    get_optimal_routes("fri")
    get_optimal_routes("sat")


if __name__ == "__main__":
    main()
