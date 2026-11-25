from importlib import import_module
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[3]


class controller:
    """
    Controller class responsible for executing the main simulation loop
    """

    def __init__(
        self,
        config_file_path: str | None = None,
        seed: int | None = None,
        overload_recorder_config_path: str | None = None,
        overload_collision_config_path: str | None = None,
        overload_atmosphere_config_path: str | None = None,
        overload_fragmentation_config_path: str | None = None,
        overload_sourcesink_config_path: str | None = None,
    ):
        # Build the state through the config specified initializer
        # Dalls back on default initializer (tools.core.initializer) if none is specified in config
        # Falls back to default config file (tools.core.config.default_config) if none is provided
        self.config = None
        self.State = None

        overload_module_paths = {
            "rcp": overload_recorder_config_path,
            "ccp": overload_collision_config_path,
            "acp": overload_atmosphere_config_path,
            "fgp": overload_fragmentation_config_path,
            "scp": overload_sourcesink_config_path,
        }

        state = self._build_state(
            config_file_path, seed=seed, overload_module_paths=overload_module_paths
        )
        self.state = state

        # Store persistent module instance references for later step calling
        self.recorder = state.recorderModule
        self.collision = state.collisionModule
        self.atmosphere = state.atmospherModule
        self.fragmentation = state.fragmentationModule
        self.sourcesink = state.sourcesinkModule

    def run(self, duration_seconds):
        while self.state.time < duration_seconds:
            self.step()
        return self.state

    def step(self):
        dt = self.state.dt
        self.sourcesink.step(self.state)
        self.collision.step(self.state)
        self.fragmentation.step(self.state)
        self.atmosphere.step(self.state)
        self.state.time += dt
        self.recorder.step(self.state)
        return self.state

    def _build_state(
        self,
        config_file_path: str | None = None,
        seed: int | None = None,
        overload_module_paths: dict | None = None,
    ):
        # config is imported either from the path provided, or from it's default location in tools.core.config
        if config_file_path is None:
            import tools.core.config.default_config as config
        else:
            config = self._load_module(config_file_path)

        module_configs = overload_module_paths.copy()
        for key in overload_module_paths:
            if overload_module_paths[key] is None:
                module_configs[key] = self._load_module(
                    config.default_module_paths[key]
                )
            else:
                module_configs[key] = self._load_module(overload_module_paths[key])

        initializer = import_module(
            getattr(config, "initializer_module", "tools.core.initializer")
        )

        self.config = config
        self.initializer = initializer
        if seed is None:
            default_seed = getattr(config, "default_seed", None)
            if default_seed is not None:
                seed = default_seed
                print(f"falling back on config default_seed: {seed}")
            else:
                seed = 1000
                print(
                    "No config default seed, and no seed provided. Running default seed of 1000. Did you mean to input a seed?"
                )

        return initializer.build_state(config, seed, module_configs)

    @staticmethod
    def _load_module(module_file_path: str | None = None):
        import importlib.util

        path = (PROJECT_ROOT / module_file_path).resolve()
        name = path.stem
        if not path.is_file():
            raise FileNotFoundError(f"File not found at: {path}")

        spec = importlib.util.spec_from_file_location(name, str(path))
        if spec is None or spec.loader is None:
            raise ImportError(f"Could not load spec from {path}")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        return module
