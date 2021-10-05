from get_routes import get_routes
from get_optimal_routes import get_optimal_routes, arr


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

    print(arr)


if __name__ == "__main__":
    main()
