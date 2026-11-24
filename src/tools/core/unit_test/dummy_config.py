"""Required overrides: module_path and default_module_paths (rcp, ccp, acp, fgp, scp).
All normal global settings are inherited from tools.core.config.default_config.
The shared module_path must expose CollisionModule, FragmentationModule,
SourceSinkModule, AtmosphereModule, and RecorderModule, each accepting its config.
"""

from tools.core.config import default_config
from tools.core.unit_test.atmosphere import AtmosphereModule
from tools.core.unit_test.collision import CollisionModule
from tools.core.unit_test.fragmentation import FragmentationModule
from tools.core.unit_test.recorder import RecorderModule
from tools.core.unit_test.sourcesink import SourceSinkModule

module_path = __file__
default_module_paths = dict.fromkeys(("rcp", "ccp", "acp", "fgp", "scp"), __file__)


def __getattr__(name):
    return getattr(default_config, name)
