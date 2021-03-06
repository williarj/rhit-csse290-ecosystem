from eco_project.random_walk import RandomWalker
from eco_project.student_agents.Sheep import EcoAgent as Sheep

class EcoAgent(RandomWalker):
    """
    A wolf that walks around, reproduces (asexually) and eats sheep.
    """

    energy = None
    icon = "wolf.png"
    ID = 2
    name = "Wolf"

    def __init__(self, unique_id, pos, model, moore, energy=None):
        super().__init__(unique_id, pos, model, moore=moore)
        self.energy = energy

    def step(self):
        self.random_move()
        self.energy -= 1

        # If there are sheep present, eat one
        x, y = self.pos
        this_cell = self.model.grid.get_cell_list_contents([self.pos])
        sheep = [obj for obj in this_cell if isinstance(obj, Sheep)]
        if len(sheep) > 0:
            sheep_to_eat = self.random.choice(sheep)
            self.energy += self.model.gain_from_food

            # Kill the sheep
            self.model.grid._remove_agent(self.pos, sheep_to_eat)
            self.model.schedule.remove(sheep_to_eat)

        # Death or reproduction
        if self.energy < 0:
            self.model.grid._remove_agent(self.pos, self)
            self.model.schedule.remove(self)
        else:
            if self.random.random() < self.model.reproduce:
                # Create a new wolf cub
                self.energy /= 2
                cub = EcoAgent(
                    self.model.next_id(), self.pos, self.model, self.moore, self.energy
                )
                self.model.grid.place_agent(cub, cub.pos)
                self.model.schedule.add(cub)
