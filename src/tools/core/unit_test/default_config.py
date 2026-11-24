"""Required for controller use: module_path pointing to a .py implementation
exposing CollisionModule, which accepts this config and provides step(state).
This legacy template still needs module_path added before controller use.
The config dictionary below is optional model data. Relative paths resolve
from the working directory; run from the repository root.
"""

config = {
    "model": "template",
    "parameters": {
        # place to put fixed parameters, maybe even function references if you want
    },
    "input_paths": {
        # place to put input paths to recall raw data
    },
}
