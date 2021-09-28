import pulp
from utilities import (
    get_cost_of_route,
    COST_PER_HOUR,
    MAXIMUM_NUMBER_OF_TRUCKS_PER_DAY,
    demands,
)
import math
import pprint


def get_optimal_routes(routes, day):
    x = pulp.LpVariable.dicts(
        "route", routes, lowBound=0, upBound=1, cat=pulp.LpInteger,
    )

    routing_model = pulp.LpProblem(
        f"Woolsworth Optimal Routes for {day}", pulp.LpMinimize
    )

    # specify minimise cost of routes
    routing_model += pulp.lpSum(
        [get_cost_of_route(route) * x[route] for route in routes]
    )

    routing_model += (
        pulp.lpSum([x[route] for route in routes]) <= MAXIMUM_NUMBER_OF_TRUCKS_PER_DAY,
        "Maximum_number_of_routes",
    )

    for store in demands[day].keys():
        routing_model += (
            pulp.lpSum([x[route] for route in routes if store in route]) == 1,
            f"Must_route_{store}",
        )

    routing_model.solve(pulp.PULP_CBC_CMD(msg=1))
    print("Status:", pulp.LpStatus[routing_model.status], routing_model.status)
    print("The choosen tables are out of a total of %s:" % len(routes))
    for route in routes:
        if x[route].value() == 1.0:
            print(route)

    routing_model.writeLP(f"out{day}.lp", max_length=500)


def main():
    with open("m_t.routes.txt") as f:
        routes = [tuple(line.strip().split(",")) for line in f.readlines()]
    get_optimal_routes(routes, "m_t")

    with open("fri.routes.txt") as f:
        routes = [tuple(line.strip().split(",")) for line in f.readlines()]
    get_optimal_routes(routes, "fri")

    with open("sat.routes.txt") as f:
        routes = [tuple(line.strip().split(",")) for line in f.readlines()]
    get_optimal_routes(routes, "sat")
    # s = set(sum(map(list, routes), []))
    # for store in demands["m_t"].keys():
    #     if store not in s:
    #         print(store)


if __name__ == "__main__":
    main()
