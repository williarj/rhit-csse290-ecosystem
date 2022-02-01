# CSSE 290 Ecosystem model - derived from the Sheep-Wolf Model

## Summary

A model where agents are added in and can interact with each other to get energy. 

## Files
run.py -- use this to start the server (e.g. python run.py)
eco_project/agents.py -- generic agents used by the model (grass is defined here) 
eco_project/model.py -- where the model is constructed, populations are made, and time steps for the entire system are defined
eco_project/random_walk.py -- defines the RandomWalk class that all animal agents extend
eco_project/schedule.py -- defines data analysis and gathering parts of the model
eco_project/server.py -- sets up the web browser interface
eco_project/test_random_walk.py -- a test file for the RandomWalk class
student_agents/ -- this directory is where all the agent files and their photos are placed
student_agents/*.png -- the photo files for each agent's display 
student_agents/basic_carnivore.py -- this Agent demonstrates the basic behavior of a carnivore, looking for prey, and consuming them
student_agents/basic_herbivore.py -- this Agent demonstrates the basic behavior of a herbivore, look for grass, consume it
student_agents/sheep_wolf_edited/* -- the modified Sheep and Wolf agents from the model this was built from, you can use these for inspiration, but dont use them directly.

## Instructions for students
Your team will create a new agents to add to this model, your team will be assigned a unique number. To do so you need to add 2 files:

1. a new .py file names after your agent -- the name be "AgentXX.py" where the SS is your team's unique number (e.g. 'Agent42.py' if your team is number 42).
2. a png for displaying your agent -- the name should be "IconXX.png" where XX is your number again (e.g. 'Icon42.png')

You can start with the basic_carnivore or basic_herbivore file and edit its behavior. You will chose one of these two kinds of Agents
to implement. Ensure you do the following:

1. set the 'icon' variable to your png name from above (e.g. "Icon42.png")
2. set the ID number to your team's unique number (e.g. ID = 42)
3. name your agent, this can be anything, but should include your team number (e.g. name = "AwesomeBear42")
4. carefully read the comments in the file to ensure you are following directions, both the herbivore and carnivore have slightly different requirements (and a few hard coded constants) that must be followed. 

You can edit code in a few places:
1. in __init__() you can add any tags you want to the list, and any other parameters your agent might need (reproduction_threshold is an example -- you can use or remove this)
2. in step() there are several parts of the code
 1. 'MOVE' - change the code here for how your Agent moves, or leave it random
 2. 'METABOLISM' - do not change this block
 3. 'EAT' - this is where your Agent seeks and acquires energy, follow the constraints in the comments
 4. 'DEATH' - do not change this block
 5. 'REPRODUCTION' - this is where your Agent seeks to make copies of itself, follow the constraints in the code

Your new files (.py and .png) simply need to be dropped into the 'student_agents' folder and then you can execute 'python run.py' from the root directory to run your model with your new Agents. If you want to remove the 'basic' agents feel free to just move the .py files to the 'sheep_wolf_folder' and they will be ignored.

## Installation

To install the dependencies use pip and the requirements.txt in this directory. e.g.

```
    $ pip install -r requirements.txt
```

## How to Run

To run the model interactively, run ``mesa runserver`` in this directory. e.g.

```
    $ mesa runserver
```

Then open your browser to [http://127.0.0.1:8521/](http://127.0.0.1:8521/) and press Reset, then Run.

