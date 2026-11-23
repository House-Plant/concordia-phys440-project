class controller:
    """
    Controller class responsible for executing the main simulation loop
    """

    def __init__(self, config_file_path: str | None = None, seed: int | None = None):
        # Build the state through the config specified initializer
        # Dalls back on default initializer (tools.core.initializer) if none is specified in config
        # Falls back to default config file (tools.core.config.default_config) if none is provided
        self.config = None
        self.State = None
        try:
            state = self._build_state(config_file_path, seed=seed)
            pass
        except Exception as e:
            print(
                f"Initializer failed to build state with it's config. Check for config/initializer mismatch. Error is {e}"
            )
            self.state = None
        else:
            self.state = state

        # Store persistent module instance references for later step calling
        self.recorder = state.recorderModule
        self.collision = state.collisionModule
        self.atmosphere = state.atmosphereModule
        self.fragmentation = state.fragmentationModule
        self.sourcesink = state.sourcesinkModule

    def run(self, duration_seconds):
        while self.state.time < duration_seconds:
            self.step()
        return self.recorder

    def step(self):
        # pull dt (set each step in the run loop) out from state
        dt = self.state.dt
        # run the physics timestep for each module, providing dt
        self.recorder.step(dt)
        self.sourcesink.step(dt)
        self.collision.step(dt)
        self.fragmentation.step(dt)
        self.atmosphere.step(dt)
        return

    def _build_state(
        self, config_file_path: str | None = None, seed: int | None = None
    ):
        # config is imported either from the path provided, or from it's default location in tools.core.config
        if config_file_path is None:
            import tools.core.config.default_config as config
        else:
            config = self._load_module(config_file_path)

        initializer_path = getattr(config, "initializer_path", None)
        if initializer_path is None:
            import tools.core.initializer as initializer
        else:
            initializer = self._load_module(initializer_path)

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

        return initializer.build_state(config, seed)

    def _load_module(module_file_path: str | None = None):
        import importlib.util
        from pathlib import Path

        path = Path(module_file_path).resolve()
        name = path.stem
        if not path.is_file():
            raise FileNotFoundError(f"File not found at: {path}")

        spec = importlib.util.spec_from_file_location(name, str(path))
        if spec is None or spec.loader is None:
            raise ImportError(f"Could not load spec from {path}")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        return module
