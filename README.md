# fire-sim
This is a simulation of fire spread using PyGame. Users can create unique environments by drawing on roads, rivers, housing, and grass. This allows for communities to understand vulnerabilities in their fire safety.  This project was created in 24 hours at TriValleyHacks with Emilio Lim, Arhum Khan, and Sunny Jayaram.

# How to run fire-sim
Clone the repository and then run the command ```pip install -r requirements.txt```. This will install all the needed dependancies to run the project. Once this is done you can start the program by running ```main.py```.

# Main Menu
<img width="400" alt="fireSim1" src="https://github.com/BryanTurns/fire-sim/assets/95263942/6c5ac7fe-00c2-4dde-b139-e3c2ebdb9c92">

The help button can be used for a quick reference on how to use the simulation. When you're ready to initialize the simulation click ```Start Simulation```.

# Basic Simulation
<img width="400" alt="fireSim2" src="https://github.com/BryanTurns/fire-sim/assets/95263942/55f4872e-eb82-42c7-af7f-9597697d95a7">

During the initialization of the simulation a 2D array of fuel and flamability values was generated. Fuel indicates how long an "entity" can burn and flamability relates to the odds that the tile will catch fire when exposed to flame. The lighter the color of a tile the more fuel it has remaining. To start the simulation hit ```Basic Sim```. Once the button is pressed, a random tile will be lit on fire. From here the simulation will continue until every bit of fuel is used up. 

<img width="400" alt="fireSim3" src="https://github.com/BryanTurns/fire-sim/assets/95263942/25aabdd4-63f9-4f9a-8aac-9a474c230fd8">
