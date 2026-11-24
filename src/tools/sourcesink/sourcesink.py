"""Source-sink module template following the shared simulation contract."""

from pathlib import Path
from runpy import run_path

from tools.core.state import SimulationState


class SourceSinkModule:
    """Apply launches, satellite aging, mission completion, and disposal."""

    def __init__(self, module_config):
        self.config = module_config  # Module config which you design.
        # Can be accessed similar to how you access a normal module or class object
        # TODO: This must take the module config file only via the module config input here.
        # The module config is entriely your design choice. Put everything and anything you
        # need to get your model set up. Please AVOID using global variables that would be
        # in the state class or the global config (see the docs, architecture for a better idea)
        return

    def step(self, state: SimulationState) -> None:
        # TODO: This is the only method that will be called by the controller. This should
        # perform your entire model simulation step over dt (start by accessing state.dt and setting dt = state.dt)
        return
