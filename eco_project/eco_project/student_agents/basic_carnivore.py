from eco_project.random_walk import RandomWalker
from eco_project.agents import GrassPatch


class EcoAgent(RandomWalker):
    """
    A herbivore that walks around, reproduces (asexually) and gets eaten.

    The init is the same as the RandomWalker.
    """

    energy = None
    icon = "frown.png" #include a photo for your agent
    ID = 4  # set this to your team's assigned ID number
    name = "BasicCarn"

    def __init__(self, unique_id, pos, model, moore, energy=None):
        super().__init__(unique_id, pos, model, moore=moore)
        self.energy = energy
        self.tags = ["carnivore"]
        # you can add other tags to the list above, other agents can
        # investigate these tags and make decisions based on them
        # all carnivore agents MUST include the tag "carnivore"
        self.reproduction_threshold = 7
        #you can change the parameter above, or delete it if you dont want to use it

    def step(self):
        """
        A model step. Move, then look for food, and reproduce.
        """
        ######## MOVE ###########
        #this individual moves randomly
        #but you could do something more complicated
        #e.g. check your surroundings for resources/threats
        self.random_move()
        living = True

        ######## METABOLISM ###########
        # Reduce energy
        # all carnivorous organisms must lose 0.7 energy per step
        # don't change this
        self.energy -= 0.7

        ######## EAT ###########
        x, y = self.pos
        #this figures out what other agents are in the same cell as me
        this_cell = self.model.grid.get_cell_list_contents([self.pos])
        agents_here = [obj for obj in this_cell if isinstance(obj, RandomWalker)]
        herbivores_here = [obj for obj in agents_here if obj.has_tag("herbivore")]
        if len(herbivores_here) > 0:
            herb_to_eat = self.random.choice(herbivores_here) #pick a random individual to eat
                                #you can pick individuals differently, however
            self.energy += herb_to_eat.energy * 0.8 #all carnivores get energy equal to
                                #80% of the energy in their prey
                                #do not change this

            # Kill the herbivore
            self.model.grid._remove_agent(self.pos, herb_to_eat)
            self.model.schedule.remove(herb_to_eat)

        ######## DEATH ###########
        #dont change this death section, everyone dies if they run out of energy
        if self.energy < 0:
            self.model.grid._remove_agent(self.pos, self)
            self.model.schedule.remove(self)
            living = False

        ######## REPRODUCTION ###########
        # check if I should reproduce
        #you can change this if statement however you please
        if living and self.energy > self.reproduction_threshold and self.random.random() < 0.50:
            # you could include something like above to make reproduction probabilistic
            # Create a new herboivore:
            reproductive_investment = 5 #you can adjust this number here
            self.energy -= reproductive_investment #cost for reproducing - dont change this
            offspring = EcoAgent(
                self.model.next_id(), #generate a new ID for the offspring - dont change this
                self.pos, #make the offspring appear here - changeable but,
                            # within reason, it should cost you 1 energy for each tile
                            #away from parent you move the offspring
                self.model, #reference to the model - dont change this
                self.moore, #for movement - dont change this
                reproductive_investment #this parameter sets how much energy you "start off" your offsring with
                            #this should always be equal to the amount of energy you lose for the reproduction
                            #do not change this here
            )
            #these two lines send the offspring to the model - dont change these
            self.model.grid.place_agent(offspring, self.pos)
            self.model.schedule.add(offspring)