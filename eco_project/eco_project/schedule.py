from collections import defaultdict

from mesa.time import RandomActivation


class RandomActivationByBreed(RandomActivation):
    """
    A scheduler which activates each type of agent once per step, in random
    order, with the order reshuffled every step.

    This is equivalent to the NetLogo 'ask breed...' and is generally the
    default behavior for an ABM.

    Assumes that all agents have a step() method.
    """

    def __init__(self, model):
        super().__init__(model)
        self.agents_by_breed = defaultdict(dict)

    def add(self, agent):
        """
        Add an Agent object to the schedule

        Args:
            agent: An Agent to be added to the schedule.
        """

        self._agents[agent.unique_id] = agent
        agent_class = type(agent)
        self.agents_by_breed[agent_class][agent.unique_id] = agent

    def remove(self, agent):
        """
        Remove all instances of a given agent from the schedule.
        """

        del self._agents[agent.unique_id]

        agent_class = type(agent)
        del self.agents_by_breed[agent_class][agent.unique_id]

    def step(self, by_breed=True):
        """
        Executes the step of each agent breed, one at a time, in random order.

        Args:
            by_breed: If True, run all agents of a single breed before running
                      the next one.
        """
        if by_breed:
            breeds_list = list(self.agents_by_breed.keys())
            self.model.random.shuffle(breeds_list)
            herbivores = [] # Holds the herbivore classes
            carnivores = [] # Holds the carnivore classes
            grass_class = None # Only one grass class
            for agent_class in breeds_list:
                if len(self.agents_by_breed[agent_class].keys()) <= 0:
                    continue # Ignore extinct classes
                else:
                    try:
                        sample = self.agents_by_breed[agent_class][list(self.agents_by_breed[agent_class].keys())[0]] # So we can access its tags
                    except KeyError:
                        continue #some individual dies before we tried to update it
                    if hasattr(sample, "tags"):
                        if "carnivore" in sample.tags:
                            carnivores.append(agent_class)
                        elif "herbivore" in sample.tags:
                            herbivores.append(agent_class)
                        else:
                            raise ValueError("Found an organism that's neither herbivore nor carnivore!")
                    else:
                        if grass_class is not None:
                            raise ValueError("Found more than one class without tags!")
                        else:
                            grass_class = agent_class
    
            for herbivore_class in herbivores: # Herbivores move first, randomized
                self.step_breed(herbivore_class)
            for carnivore_class in carnivores: # Then carnivores
                self.step_breed(carnivore_class)
            self.step_breed(grass_class)       # Then grass grows

            # Example of turns: (aardvark, zebra, wolf, tiger, grass); (zebra, aardvard, tiger, wolf, grass). Herbivores always get one and only one turn between each carnivore turn.

            self.steps += 1
            self.time += 1
        else:
            super().step()

    def step_breed(self, breed):
        """
        Shuffle order and run all agents of a given breed.

        Args:
            breed: Class object of the breed to run.
        """
        agent_keys = list(self.agents_by_breed[breed].keys())
        self.model.random.shuffle(agent_keys)
        for agent_key in agent_keys:
            try:
                self.agents_by_breed[breed][agent_key].step()
            except KeyError:
                continue

    def get_breed_count(self, breed_class):
        """
        Returns the current number of agents of certain breed in the queue.
        """
        return len(self.agents_by_breed[breed_class].values())

    def get_breed_energy(self, breed_class):
        """
        Returns the average energy of agents of a certain breed.
        """
        energies = [a.energy for a in self.agents_by_breed[breed_class].values()]
        return float(sum(energies))/(len(energies)+1)
