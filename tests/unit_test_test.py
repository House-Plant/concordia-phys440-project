from tools.core.controller import controller
from tools.core.unit_test import dummy_config

simulation = controller(dummy_config.__file__)

simulation.step()
