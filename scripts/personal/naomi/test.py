from tools.core.controller import controller
from tools.core.unit_test import dummy_config

from tools.collision.config import default_config as collision_config

simulation = controller(
    dummy_config.__file__,
    overload_collision_config_path=collision_config.__file__
)


simulation.run(10000000)

