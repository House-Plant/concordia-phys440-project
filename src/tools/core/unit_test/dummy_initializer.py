from tools.test_tools.simple_state import create_test_state


def build_state(config, seed, modules):
    state, _ = create_test_state(seed=seed)
    state.recorderModule = config.RecorderModule(modules["rcp"])
    state.collisionModule = config.CollisionModule(modules["ccp"])
    state.atmospherModule = config.AtmosphereModule(modules["acp"])
    state.fragmentationModule = config.FragmentationModule(modules["fgp"])
    state.sourcesinkModule = config.SourceSinkModule(modules["scp"])
    return state
