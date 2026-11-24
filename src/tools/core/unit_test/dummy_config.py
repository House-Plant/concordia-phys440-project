from tools.core.config import default_config
from tools.core.unit_test.atmosphere import AtmosphereModule
from tools.core.unit_test.collision import CollisionModule
from tools.core.unit_test.fragmentation import FragmentationModule
from tools.core.unit_test.recorder import RecorderModule
from tools.core.unit_test.sourcesink import SourceSinkModule

default_module_paths = dict.fromkeys(("rcp", "ccp", "acp", "fgp", "scp"), __file__)


def __getattr__(name):
    return getattr(default_config, name)
