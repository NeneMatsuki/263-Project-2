from configparser import DuplicateOptionError
from utilities import (
    TIME_PER_PALLET,
    MAXIMUM_PALLETS_PER_DELIVERY,
    DISTRIBUTION_CENTER,
    MAXIMUM_SECONDS_PER_DELIVERY,
    demands,
    travel_durations,
    travel_distances,
    write_routes,
)

i = 0


def get_routes(route, demands, travel_durations):
    """
    find all routes that can extend the current one

    params:
        route: a list of stores in the route
            eg. route = ["airport", "metro", "beach"]
        demand: a dict containing the demand for each store
        travel_durations: a dict containing the travel times between each store
    """

    # calculate duration and pallets for the route
    number_of_pallets = sum(demands.get(store, 0) for store in route)
    travel_duration = sum(
        travel_durations[store1][store2] for store1, store2 in zip(route, route[1:])
    )
    total_duration = travel_duration + number_of_pallets * TIME_PER_PALLET
    last_stop = route[-1]

    # can the truck return back to the distribution center.
    # if not, then this and all child routes are invalid and so we should return nothing.
    if (
        total_duration + travel_durations[last_stop][DISTRIBUTION_CENTER]
        >= MAXIMUM_SECONDS_PER_DELIVERY
        and len(route) > 1
    ):
        return []

    # global i
    # i += 1
    # if i % 100_000 == 0:
    #     print(",".join(route))

    # if it can then valid routes at least contains that return journey
    if last_stop != DISTRIBUTION_CENTER:
        valid_routes = [route + [DISTRIBUTION_CENTER]]
    else:
        valid_routes = []

    # find all valid stores the route can connect too and find all valid extensions to that store
    for store in demands.keys():
        # exclude this store if it has already been visited
        if store in route:
            continue

        # exclude this store if it would exceed the allowed number of pallets
        if number_of_pallets + demands[store] > MAXIMUM_PALLETS_PER_DELIVERY:
            continue

        # exclude this store if it would exceed the allowed length of a delivery
        if (
            travel_duration
            + travel_durations[last_stop][store]
            + (number_of_pallets + demands[store]) * TIME_PER_PALLET
            > MAXIMUM_SECONDS_PER_DELIVERY
        ):
            continue

        # HEURISTIC: store to far away? Exclude!
        if travel_distances[last_stop][store] > 20_000:
            continue

        # the store is valid so find all valid extensions to that route as well
        valid_routes += get_routes(route + [store], demands, travel_durations)

    return valid_routes


def main():
    # routes for monday thursday
    routes = get_routes([DISTRIBUTION_CENTER], demands["m_t"], travel_durations)
    write_routes(routes, "m_t.routes.txt")
    print(f"m_t {len(routes):,}")

    # routes for friday
    routes = get_routes([DISTRIBUTION_CENTER], demands["fri"], travel_durations)
    write_routes(routes, "fri.routes.txt")
    print(f"fri {len(routes):,}")

    # routes for saturday
    routes = get_routes([DISTRIBUTION_CENTER], demands["sat"], travel_durations)
    write_routes(routes, "sat.routes.txt")
    print(f"sat {len(routes):,}")


if __name__ == "__main__":
    main()
