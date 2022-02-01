import importlib

from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import CanvasGrid, ChartModule
from mesa.visualization.UserParam import UserSettableParameter

from eco_project.agents import GrassPatch
from eco_project.model import Ecosystem

############import all the agents from the students###############
from os.path import dirname, basename, isfile, join
import glob
modules = glob.glob(join(dirname(__file__)+"/student_agents/", "*.py"))
__all__ = [ "eco_project.student_agents."+basename(f)[:-3] for f in modules if isfile(f) and not f.endswith('__init__.py')]
print("Loading these Agents: " + ",".join(__all__))
agent_types = [importlib.import_module(classname).EcoAgent for classname in __all__]
##################################################################

def ecosystem_portrayal(agent):
    if agent is None:
        return

    portrayal = {}
    if type(agent) is GrassPatch:
        if agent.fully_grown:
            portrayal["Color"] = ["#00FF00", "#00CC00", "#009900"]
        else:
            portrayal["Color"] = ["#84e184", "#adebad", "#d6f5d6"]
        portrayal["Shape"] = "rect"
        portrayal["Filled"] = "true"
        portrayal["Layer"] = 0
        portrayal["w"] = 1
        portrayal["h"] = 1
    else:
        portrayal["Shape"] = "eco_project/student_agents/"+agent.icon
        portrayal["scale"] = 0.9
        portrayal["Layer"] = agent.ID
        #portrayal["text"] = round(agent.energy, 1)
        portrayal["text_color"] = "red" #this parameter doesnt seem to work

    return portrayal


colors = ["#666666", "#00FFFF", "#838B8B", "#E3CF57", "#8B7D6B", "	#0000FF", "#8A2BE2", "#FF4040", "#FF6103",
          "#458B00", "#3D59AB", "#BCEE68", "#AA0000"]
height = 200
width = height
canvas_element = CanvasGrid(ecosystem_portrayal, height, width, 750, 750) #last two parameters here affect the drawing area
chart_element_count = ChartModule(
    [{"Label": a.name, "Color": colors[i]} for (i, a) in enumerate(agent_types)] #+
     #[{"Label": "Bear", "Color": "#BCEE68"}]
)
chart_element_energy = ChartModule(
    [{"Label": a.name+"E", "Color": colors[i]} for (i, a) in enumerate(agent_types)] #+
)

model_params = {
    "agent_types": agent_types,
    "height":height,
    "width":width,
    "grass": UserSettableParameter("checkbox", "Grass Enabled", True),
    "grass_regrowth_time": UserSettableParameter(
        "slider", "Grass Regrowth Time", 20, 1, 50
    )#,
    # "initial_sheep": UserSettableParameter(
    #     "slider", "Initial Sheep Population", 100, 10, 300
    # ),
    # "sheep_reproduce": UserSettableParameter(
    #     "slider", "Sheep Reproduction Rate", 0.04, 0.01, 1.0, 0.01
    # ),
    # "initial_wolves": UserSettableParameter(
    #     "slider", "Initial Wolf Population", 50, 10, 300
    # ),
    # "wolf_reproduce": UserSettableParameter(
    #     "slider",
    #     "Wolf Reproduction Rate",
    #     0.05,
    #     0.01,
    #     1.0,
    #     0.01,
    #     description="The rate at which wolf agents reproduce.",
    # ),
    # "wolf_gain_from_food": UserSettableParameter(
    #     "slider", "Wolf Gain From Food Rate", 20, 1, 50
    # ),
    # "sheep_gain_from_food": UserSettableParameter(
    #     "slider", "Sheep Gain From Food", 4, 1, 10
    # ),
}

server = ModularServer(
    Ecosystem, [canvas_element, chart_element_count, chart_element_energy], "Ecosystem", model_params
)
server.port = 8521
