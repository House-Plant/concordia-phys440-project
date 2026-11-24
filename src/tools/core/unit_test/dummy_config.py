from pathlib import Path

from tools.core.unit_test.atmosphere import AtmosphereModule
from tools.core.unit_test.collision import CollisionModule
from tools.core.unit_test.fragmentation import FragmentationModule
from tools.core.unit_test.recorder import RecorderModule
from tools.core.unit_test.sourcesink import SourceSinkModule

initializer_path = str(Path(__file__).with_name("dummy_initializer.py"))
default_seed = 42
default_module_paths = dict.fromkeys(("rcp", "ccp", "acp", "fgp", "scp"), __file__)
