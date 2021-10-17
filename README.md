# ENGSCI 263 Project 2 Truck Scheduling and Efficiency for Woolworths NZ
Project 2 for ENGSCI 263 2021

- The folder "data"               contains data that was used when making the mode
- The folder "generated_routes"   contains routes that were generated that the optimal was chosen from
- The folder "linear model"       contains all the files that the linear model generated
- The folder "maps"               contains the maps generated 
- The folder  "optimal routes"     contains the optimal routes for each day

- The file "get_optimal_routes.py"     returns the optimal solution from the generated routes using pulp library
- The file "get_routes.py"             generates all possible routes subject to constraints.
- The file "utilities.py"              stores the constraints for route generation
- The file "maping.py"                 creates a map visualisation of the trucking routes using folium and open route source.
- The file "bootsrap_scenarios"        plots a bootstap confidence interval for the demands 
- The file "bootstap plots"            contains plots after bootstrap simulations

***path ---> 263-PROJECT-2/main.py***

Run main.py to obtain files that contain optimal routes;
- m_t.optimal.routes.txt, fri.optimal.routes.txt, sat.optimal.routes.txt

To run simulations, run bootstrap_scenarios
-   If plot_Simulation is set to true, the simulation of the original scenario is run
-   If plot_with_stores_deleted is set to true, simulation with some stores removed is run
-   If get_CI_for_scenarios is set to true, the confidence interval for costs of the 2 scenarios above is printed

Authors: Shannon Blackhall, Maia Darling, Tom Purkis, Nene Matsuki
