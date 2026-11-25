"""Dummy config"""

# you need to specify the module you want to use here in the config, this is how the algorithm knows how to use it.
# default_module_paths = {"ccp": "src/tools/module/config/module_config.py"}

from tools.core.config import default_config

default_module_paths = {
    "rcp": "src/tools/core/unit_test/recorder_config.py",
    "ccp": "src/tools/core/unit_test/default_config.py",
    "acp": "src/tools/core/unit_test/atmosphere_config.py",
    "fgp": "src/tools/core/unit_test/fragmentation_config.py",
    "scp": "src/tools/core/unit_test/sourcesink_config.py",
}


def __getattr__(name):
    return getattr(default_config, name)
