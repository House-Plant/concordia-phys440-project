from pathlib import Path

from tools.core.dummy_classes.atmosphere import AtmosphereModule
from tools.core.dummy_classes.collision import CollisionModule
from tools.core.dummy_classes.fragmentation import FragmentationModule
from tools.core.dummy_classes.recorder import RecorderModule
from tools.core.dummy_classes.sourcesink import SourceSinkModule

initializer_path = str(Path(__file__).with_name("dummy_initializer.py"))
default_seed = 42
default_module_paths = dict.fromkeys(("rcp", "ccp", "acp", "fgp", "scp"), __file__)
