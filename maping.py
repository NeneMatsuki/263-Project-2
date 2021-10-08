
import time

def mon_thrs_map():
    """Generate a folium map of the optimal truck routes for monday through thursday"""
    import pandas as pd
    import folium
    import openrouteservice as ors
    
    #entering key for ors
    ORSkey = '5b3ce3597851110001cf62480371af7700564e1990d43766e3c68834'

    #reading in store locations
    locations=pd.read_csv("WoolworthsLocations.csv")

    #getting store location coordinates
    coords  = locations[['Long','Lat']]
    coords  =  coords.to_numpy().tolist()   

    #initialisting Map with store locations 
    m  = folium.Map(location=list(reversed(coords[2])),zoom_start=11)

    #adding markers for stores coloured by store types
    for i in range(0, len(coords)):
        if locations.Type[i] == "Countdown":
            iconCol= "green"
        elif locations.Type[i]  == "FreshChoice":
            iconCol = "blue"
        elif locations.Type[i] == "SuperValue":
            iconCol = "red"
        elif locations.Type[i] == "Countdown Metro":
            iconCol = "orange"
        elif locations.Type[i] == "Distribution Centre":
            iconCol = "black"
        folium.Marker(list(reversed(coords[i])), popup=locations.Store[i],icon  = folium.Icon(color = iconCol)).add_to(m)

    #Booting up client in ORS
    client = ors.Client(key=ORSkey)

    #monday mapping

    #opening optimum routes file, reading in routes, and closing file
    f = open('m_t.optimal.routes.txt', 'r')
    lines = f.readlines()
    f.close()

    #initializing array for routes
    routes = []
    #creating array of colours to differenciate routes
    colours2 = ['#007DB5','#00FF00','#0000FF','#FF0000','#01FFFE','#FFA6FE','#FFDB66','#006401','#EEB422','#95003A','#000000','#FF00F6','#FFEEE8','#774D00','#90FB92','#0076FF','#D5FF00','#FF937E','#6A826C','#FCE205','#FE8900','#7A4782','#7E2DD2']

    #looping though each line of the file
    for line in lines:
        #initilizing array for the co-ordinates for that line's route
        coord = []
        #removing next line from string
        line = line.strip()
        #seperating the lnie string into store locations
        stores = line.split(',')
        #counting how many stores in the route
        numstores = len(stores)
        #looping though each store in the route
        for i in range(numstores):
            #finding the coresponding co-ordinate for that store.
            for j in range(len(locations)):
                if locations['Store'][j]== stores[i]:
                    #adding each stores coordinates to a list
                    coord.append(j)     
        #adding the route to a list
        routes.append(coord)
    
    #adding each route to the map
    for i in range(len(routes)):
        #accessing single route
        currentroute = routes[i]
        #initialising array for route coordinates
        coordinatess = []
        #adding each coordinate to the list for the route
        for j in range(len(currentroute)):
            coordinatess.append(coords[currentroute[j]])
        #creating the route
        route = client.directions(coordinates = coordinatess, profile = 'driving-hgv', format = 'geojson', validate = False)
        #adding the route as a polyline to the map
        folium.PolyLine(color = colours2[i],locations=[list(reversed(coord))for coord in route['features'][0]['geometry']['coordinates']]).add_to(m)

    #saving the map to file
    m.save("m_t_map.html")

def fri_map():
    """Generate a folium map of the optimal truck routes for friday"""
    import numpy as np
    import pandas as pd
    import folium
    import openrouteservice as ors
    
    #entering key for ors
    ORSkey = '5b3ce3597851110001cf62480371af7700564e1990d43766e3c68834'

    #reading in store locations
    locations=pd.read_csv("WoolworthsLocations.csv")

    #getting store location coordinates
    coords  = locations[['Long','Lat']]
    coords  =  coords.to_numpy().tolist()   

    #initialisting Map with store locations 
    m  = folium.Map(location=list(reversed(coords[2])),zoom_start=11)

    #adding markers for stores coloured by store types
    for i in range(0, len(coords)):
        if locations.Type[i] == "Countdown":
            iconCol= "green"
        elif locations.Type[i]  == "FreshChoice":
            iconCol = "blue"
        elif locations.Type[i] == "SuperValue":
            iconCol = "red"
        elif locations.Type[i] == "Countdown Metro":
            iconCol = "orange"
        elif locations.Type[i] == "Distribution Centre":
            iconCol = "black"
        folium.Marker(list(reversed(coords[i])), popup=locations.Store[i],icon  = folium.Icon(color = iconCol)).add_to(m)

    #Booting up client in ORS
    client = ors.Client(key=ORSkey)

    #monday mapping

    #opening optimum routes file, reading in routes, and closing file
    f = open('fri.optimal.routes.txt', 'r')
    lines = f.readlines()
    f.close()

    #initializing array for routes
    routes = []
    #creating array of colours to differenciate routes
    colours2 = ['#007DB5','#00FF00','#0000FF','#FF0000','#01FFFE','#FFA6FE','#FFDB66','#006401','#EEB422','#95003A','#000000','#FF00F6','#FFEEE8','#774D00','#90FB92','#0076FF','#D5FF00','#FF937E','#6A826C','#FCE205','#FE8900','#7A4782','#7E2DD2']

    #looping though each line of the file
    for line in lines:
        #initilizing array for the co-ordinates for that line's route
        coord = []
        #removing next line from string
        line = line.strip()
        #seperating the lnie string into store locations
        stores = line.split(',')
        #counting how many stores in the route
        numstores = len(stores)
        #looping though each store in the route
        for i in range(numstores):
            #finding the coresponding co-ordinate for that store.
            for j in range(len(locations)):
                if locations['Store'][j]== stores[i]:
                    #adding each stores coordinates to a list
                    coord.append(j)     
        #adding the route to a list
        routes.append(coord)
    
    #adding each route to the map
    for i in range(len(routes)):
        #accessing single route
        currentroute = routes[i]
        #initialising array for route coordinates
        coordinatess = []
        #adding each coordinate to the list for the route
        for j in range(len(currentroute)):
            coordinatess.append(coords[currentroute[j]])
        #creating the route
        route = client.directions(coordinates = coordinatess, profile = 'driving-hgv', format = 'geojson', validate = False)
        #adding the route as a polyline to the map
        folium.PolyLine(color = colours2[i],locations=[list(reversed(coord))for coord in route['features'][0]['geometry']['coordinates']]).add_to(m)

    #saving the map to file
    m.save("fri_map.html")


def sat_map():
    """Generate a folium map of the optimal truck routes for Saturday"""
    import numpy as np
    import pandas as pd
    import folium
    import openrouteservice as ors
    
    #entering key for ors
    ORSkey = '5b3ce3597851110001cf62480371af7700564e1990d43766e3c68834'

    #reading in store locations
    locations=pd.read_csv("WoolworthsLocations.csv")

    #getting store location coordinates
    coords  = locations[['Long','Lat']]
    coords  =  coords.to_numpy().tolist()   

    #initialisting Map with store locations 
    m  = folium.Map(location=list(reversed(coords[2])),zoom_start=11)

    #adding markers for stores coloured by store types
    for i in range(0, len(coords)):
        if locations.Type[i] == "Countdown":
            iconCol= "green"
        elif locations.Type[i]  == "FreshChoice":
            iconCol = "blue"
        elif locations.Type[i] == "SuperValue":
            iconCol = "red"
        elif locations.Type[i] == "Countdown Metro":
            iconCol = "orange"
        elif locations.Type[i] == "Distribution Centre":
            iconCol = "black"
        folium.Marker(list(reversed(coords[i])), popup=locations.Store[i],icon  = folium.Icon(color = iconCol)).add_to(m)

    #Booting up client in ORS
    client = ors.Client(key=ORSkey)

    #monday mapping

    #opening optimum routes file, reading in routes, and closing file
    f = open('sat.optimal.routes.txt', 'r')
    lines = f.readlines()
    f.close()

    #initializing array for routes
    routes = []
    #creating array of colours to differenciate routes
    colours2 = ['#007DB5','#00FF00','#0000FF','#FF0000','#01FFFE','#FFA6FE','#FFDB66','#006401','#EEB422','#95003A','#000000','#FF00F6','#FFEEE8','#774D00','#90FB92','#0076FF','#D5FF00','#FF937E','#6A826C','#FCE205','#FE8900','#7A4782','#7E2DD2']

    #looping though each line of the file
    for line in lines:
        #initilizing array for the co-ordinates for that line's route
        coord = []
        #removing next line from string
        line = line.strip()
        #seperating the lnie string into store locations
        stores = line.split(',')
        #counting how many stores in the route
        numstores = len(stores)
        #looping though each store in the route
        for i in range(numstores):
            #finding the coresponding co-ordinate for that store.
            for j in range(len(locations)):
                if locations['Store'][j]== stores[i]:
                    #adding each stores coordinates to a list
                    coord.append(j)     
        #adding the route to a list
        routes.append(coord)
    
    #adding each route to the map
    for i in range(len(routes)):
        #accessing single route
        currentroute = routes[i]
        #initialising array for route coordinates
        coordinatess = []
        #adding each coordinate to the list for the route
        for j in range(len(currentroute)):
            coordinatess.append(coords[currentroute[j]])
        #creating the route
        route = client.directions(coordinates = coordinatess, profile = 'driving-hgv', format = 'geojson', validate = False)
        #adding the route as a polyline to the map
        folium.PolyLine(color = colours2[i], locations=[list(reversed(coord))for coord in route['features'][0]['geometry']['coordinates']]).add_to(m)

    #saving the map to file
    m.save("sat_map.html")

    
if __name__ == "__main__":
    #just for testing
    mon_thrs_map()
    print('mon done')
    time.sleep(60)
    fri_map()
    print('fri done')
    time.sleep(60)
    sat_map()
