from tools.core.controller import controller
from tools.core.unit_test import dummy_config

simulation = controller(
    dummy_config.__file__,
    overload_recorder_config_path=None,
    overload_collision_config_path=None,
    overload_atmosphere_config_path=None,
    overload_fragmentation_config_path=None,
    overload_sourcesink_config_path=None,
)
state = simulation.step()
