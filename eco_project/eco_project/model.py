"""
Modified from Wolf-Sheep Predation Model
by RJ Williamson Jan 2022

================================

Replication of the model found in NetLogo:
    Wilensky, U. (1997). NetLogo Wolf Sheep Predation model.
    http://ccl.northwestern.edu/netlogo/models/WolfSheepPredation.
    Center for Connected Learning and Computer-Based Modeling,
    Northwestern University, Evanston, IL.
"""

from mesa import Model
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector

from eco_project.agents import GrassPatch
from eco_project.schedule import RandomActivationByBreed


class Ecosystem(Model):
    """
    Ecosystem Model
    """

    height = 50
    width = 50

    initial_agents = 20

    reproduce = 0.05

    grass = False
    grass_regrowth_time = 30
    gain_from_food = 4

    verbose = False  # Print-monitoring

    description = (
        "A model for simulating ecosystem modelling."
    )

    agent_types = []

    def __init__(
        self,
        agent_types,
        canvas,
        initial_agents=100,
        reproduce=0.04,
        gain_from_food=2,
        grass=True,
        grass_regrowth_time=30,
        world_size = 20,
        herbivore_metabolism = 1,
        carnivore_metabolism = 0.7,
        **kwargs
    ):
        """
        Create a new Wolf-Sheep model with the given parameters.

        """
        super().__init__()
        # Set parameters
        #this doesnt work yet
        canvas.grid_height = world_size
        canvas.grid_width = world_size
        #print(world_size)
        self.agent_types = agent_types
        self.height = world_size
        self.width = world_size
        self.initial_agents = initial_agents
        self.reproduce = reproduce
        self.gain_from_food = gain_from_food
        self.grass = grass
        self.grass_regrowth_time = grass_regrowth_time
        self.herbivore_metabolism = herbivore_metabolism
        self.carnivore_metabolism = carnivore_metabolism

        self.schedule = RandomActivationByBreed(self)
        self.grid = MultiGrid(self.height, self.width, torus=True)
        #only keep the agents that are currently turned on
        self.active_agents = filter(lambda a: kwargs[a.name], agent_types)

        data_dict = {
                a.name: (lambda y: (lambda x: x.schedule.get_breed_count(y)))(a) for a in self.agent_types
            }

        data_dict.update(
            {
                a.name+"E": (lambda y: (lambda x: x.schedule.get_breed_energy(y)))(a) for a in self.agent_types
            }
        )
        #print(data_dict)
        self.datacollector = DataCollector(
            data_dict
        )
        #print(self.datacollector.model_reporters)

        # Create active agents:
        for agent_type in self.active_agents:
            for i in range(self.initial_agents):
                x = self.random.randrange(self.width)
                y = self.random.randrange(self.height)
                energy = self.random.randrange(2 * self.gain_from_food)
                new_id = self.next_id()
                my_model = self
                agent = agent_type(new_id, (x, y), my_model, True, energy)
                self.grid.place_agent(agent, (x, y))
                self.schedule.add(agent)


        # Create grass patches
        if self.grass:
            for agent, x, y in self.grid.coord_iter():

                fully_grown = self.random.choice([True, False])

                if fully_grown:
                    countdown = self.grass_regrowth_time
                else:
                    countdown = self.random.randrange(self.grass_regrowth_time)

                patch = GrassPatch(self.next_id(), (x, y), self, fully_grown, countdown)
                self.grid.place_agent(patch, (x, y))
                self.schedule.add(patch)

        self.running = True
        self.datacollector.collect(self)

    def step(self):
        self.schedule.step()
        # collect data
        self.datacollector.collect(self)
        if self.verbose:
            print(
                str(self.schedule.time) + "\n" +
                str({a:self.schedule.get_breed_count(a) for a in self.agent_types})
            )

    def run_model(self, step_count=200):
        for i in range(step_count):
            self.step()
