from mesa import Agent

class TagMap():

    def __init__(self):
        self.tag_map = {}

    def has_tag(self, tag):
        return tag in self.tag_map.keys()

    def register_tag(self, tag, function):
        self.tag_map[tag] = function

    def get_tag_function(self, tag):
        if tag in self.tag_map.keys():
            return self.tag_map[tag]
        return None

class GrassPatch(Agent):
    """
    A patch of grass that grows at a fixed rate and it is eaten by sheep
    """

    def __init__(self, unique_id, pos, model, fully_grown, countdown):
        """
        Creates a new patch of grass

        Args:
            grown: (boolean) Whether the patch of grass is fully grown or not
            countdown: Time for the patch of grass to be fully grown again
        """
        super().__init__(unique_id, model)
        self.fully_grown = fully_grown
        self.countdown = countdown
        self.pos = pos

    def step(self):
        if not self.fully_grown:
            if self.countdown <= 0:
                # Set as fully grown
                self.fully_grown = True
                self.countdown = self.model.grass_regrowth_time
            else:
                self.countdown -= 1
