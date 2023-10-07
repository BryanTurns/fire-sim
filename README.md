# fire-sim
This is a simulation of fire spread using PyGame. Users can create unique environments by drawing on roads, rivers, housing, and grass. This allows for communities to understand vulnerabilities in their fire safety.  This project was created in 24 hours at TriValleyHacks with Emilio Lim, Arhum Khan, and Sunny Jayaram.

# How to run fire-sim
Clone the repository and then run the command ```pip install -r requirements.txt```. This will install all the needed dependancies to run the project. Once this is done you can start the program by running ```main.py```.

# Main Menu
<img width="400" alt="fireSim1" src="https://github.com/BryanTurns/fire-sim/assets/95263942/6c5ac7fe-00c2-4dde-b139-e3c2ebdb9c92">

The help button can be used for a quick reference on how to use the simulation. When you're ready to initialize the simulation click ```Start Simulation```.

# Basic Simulation
<img width="400" alt="fireSim2" src="https://github.com/BryanTurns/fire-sim/assets/95263942/55f4872e-eb82-42c7-af7f-9597697d95a7">

During the initialization of the simulation a 2D array of fuel and flamability values was generated. Fuel indicates how long an "entity" can burn and flamability relates to the odds that the tile will catch fire when exposed to flame. The lighter the color of a tile the more fuel it has remaining. To start the simulation hit ```Basic Sim```. Once the button is pressed, a random tile will be lit on fire. From here the simulation will continue until every bit of fuel is used up. The simulation may be exited at any time by hitting the x on the tab. This will cause a, currently broken, graph that displays a variety of values over time. 

<img width="400" alt="fireSim3" src="https://github.com/BryanTurns/fire-sim/assets/95263942/25aabdd4-63f9-4f9a-8aac-9a474c230fd8">
<img width="476" alt="fireSim6" src="https://github.com/BryanTurns/fire-sim/assets/95263942/292488c2-479f-4b96-b194-87e8e4a50e97">

# Custom Simulations

To create your own custom enviroment to test fire safety you can use the buttons on the top right of the window to draw onto the simulation and change it's values. The mechanism is pretty slow at processing clicks/drags so for higher definition simulations it can be quite hard to create cusom enviroments. We recomend you use one of our custom simulations, Pleasanton, CA. This simulation is loaded by first pulling data from the Google Maps API. This is then converted into an appropriately pixelated map. The colors in each tile is then evaluated and converted into the apropriate entity type (grass, house, road, and water). 

<img width="400" alt="fireSim4" src="https://github.com/BryanTurns/fire-sim/assets/95263942/e3027172-d85a-485b-96d9-8b90d487f2f6">

# Advanced Custom Simulations

You can change a variety of parameters within the code to change how the simulation will run. Adjusting `FLAME_RADIUS` will change how many tiles a flame can jump. Increasing this value will significantly impact performance. Adjust `ENTITY_WIDTH` to change the resolution of the simulation (smaller width = more tiles). Note that decreasing this value will decrease performance. Adjust `SCREEN_HEIGHT` in order to change the size of the window. 

<img width="400" alt="fireSim10" src="https://github.com/BryanTurns/fire-sim/assets/95263942/e27a231d-c762-42d1-bb11-dff78a66f194">
<img width="362" alt="fireSim7png" src="https://github.com/BryanTurns/fire-sim/assets/95263942/f57c9014-6201-43ae-9e7a-66ed4e5e7864">



