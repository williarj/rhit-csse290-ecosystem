from eco_project.random_walk import RandomWalker
from eco_project.agents import GrassPatch


class EcoAgent(RandomWalker):
    """
    A herbivore that walks around, reproduces (asexually) and gets eaten.

    The init is the same as the RandomWalker.
    """

    energy = None
    icon = "smile.png" #include a photo for your agent
    ID = 3  # set this to your team's assigned ID number
    name = "SpinyHerb"

    def __init__(self, unique_id, pos, model, moore, energy=None):
        super().__init__(unique_id, pos, model, moore=moore)
        self.energy = energy
        self.tags = ["herbivore", "spines"]
        self.metabolism_cost = model.herbivore_metabolism
        # you can add other tags to the list above, other agents can
        # investigate these tags and make decisions based on them
        # all herbivore agents MUST include the tag "herbivore"
        self.reproduction_threshold = 5
        model.register_tag("spines", EcoAgent.SpineAction)
        #you can change the parameter above, or delete it if you dont want to use it

    def SpineAction(actor, target):
        print("Get spined!")
        target.energy -= 10
        print(target.energy)

    def step(self):
        """
        A model step. Move, then eat grass and reproduce.
        """
        ######## MOVE ###########
        #this individual moves randomly
        #but you could do something more complicated
        #e.g. check your surroundings for resources/threats
        self.random_move()
        living = True

        ######## METABOLISM ###########
        # Reduce energy
        # all herbivorous organisms must lose 1 energy per step
        # don't change this
        self.energy -= self.metabolism_cost

        ######## EAT ###########
        # If there is grass available, eat it
        # herbivores eat grass don't change this section herbivore
        this_cell = self.model.grid.get_cell_list_contents([self.pos])
        grass_patch = [obj for obj in this_cell if isinstance(obj, GrassPatch)][0]
        # herbivores can only eat from fully grown grass
        if grass_patch.fully_grown:
            # the amount off food from grass is a set value for all herbivores
            self.energy += self.model.gain_from_food
            # update the grass so it knows it got eaten
            grass_patch.fully_grown = False

        ######## DEATH ###########
        #dont change this death section, everyone dies if they run out of energy
        if self.energy < 0:
            self.model.grid._remove_agent(self.pos, self)
            self.model.schedule.remove(self)
            living = False

        ######## REPRODUCTION ###########
        # check if I should reproduce
        #you can change this if statement however you please
        if living and self.energy > self.reproduction_threshold:
            #if self.random.random() < 0.10: # you could include something like this to make reproduction probabilistic
            # Create a new herboivore:
            reproductive_investment = self.reproduction_threshold #you can adjust this number here
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