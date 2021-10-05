from math import ceil
from csv import reader

TIME_PER_PALLET = 7.5 * 60  # seconds,  450
COST_PER_HOUR = 225  # dollars

MAXIMUM_SECONDS_PER_DELIVERY = 4 * 60 * 60  # seconds,  14,400
MAXIMUM_PALLETS_PER_DELIVERY = 26  # pallets
MAXIMUM_NUMBER_OF_TRUCKS_PER_DAY = 60

DISTRIBUTION_CENTER = "Distribution Centre Auckland"


def get_demand_dict():
    """Get a dictionary of the ceiling of each stores demand for monday_thursday, friday, saturday"""
    d = {"m_t": {}, "fri": {}, "sat": {}}
    with open("EstimatedDemands.csv") as f:
        f.readline()
        c = reader(f)
        for store, m_t, fri, sat in c:
            d["m_t"][store] = int(m_t)
            d["fri"][store] = int(fri)
            d["sat"][store] = int(sat)
    d = {k1: {k2: v2 for k2, v2 in v1.items() if v2 != 0} for k1, v1 in d.items()}
    return d


def get_duration_dict():
    """Get the 2D dictionary of the travel times between stores """
    d = {}
    with open("WoolworthsTravelDurations.csv") as f:
        c = reader(f)
        _, *stores = next(c)

        for store1, *durations in c:
            d[store1] = {store2: float(duration) for store2, duration in zip(stores, durations)}
    return d


def get_location_dict():
    """Get the 2D dictionary of the travel times between stores """
    d = {}
    with open("WoolworthsDistances.csv") as f:
        c = reader(f)
        _, *stores = next(c)

        for store1, *durations in c:
            d[store1] = {store2: float(duration) for store2, duration in zip(stores, durations)}
    return d

def get_store_demand():
    """Get the 2D dictionary of the demans of a store """
    d = {}
    with open("WoolworthsDistances.csv") as f:
        c = reader(f)
        _, *stores = next(c)

        for store1, *durations in c:
            d[store1] = {store2: float(duration) for store2, duration in zip(stores, durations)}
    return d


def write_routes(routes, fp):
    with open(fp, "w") as f:
        for route in routes:
            f.write(",".join(route) + "\n")


demands = get_demand_dict()
travel_durations = get_duration_dict()
travel_distances = get_location_dict()


def get_cost_of_route(route,day):
   
    # reference line 28 get routes  
    number_of_pallets = sum(demands[day].get(store,0) for store in route)  # this returns 0 though as stores are not stored as array?
    travel_duration = sum(travel_durations[store1][store2] for store1, store2 in zip(route, route[1:]))
    minutes = ceil((travel_duration + number_of_pallets * TIME_PER_PALLET)/60)

    extrahrs = 0
    if (minutes) > 240:
        extrahrs = minutes-240
    return ( minutes * (COST_PER_HOUR/60) + extrahrs * (275/60))

