import tools.core.state as state
from tools.core.controller import controller
from tools.core.randomness import RandomStreams


def build_state(config, seed, modules):
    # Config parameters
    initial_state_interpreter_path = config.initial_state_interpreter_path
    initial_state_path = config.initial_state_path
    reference_date = config.reference_date
    shell_edges_m = config.shell_edges_m
    age_edges = config.age_edges
    length_edges_m = config.length_edges_m
    area_to_mass_edges_m2_per_kg = config.area_to_mass_edges_m2_per_kg

    initial_state_interpreter = controller._load_module(initial_state_interpreter_path)
    initial_state = initial_state_interpreter.read_satcat(
        initial_state_path,
        shell_edges_m=shell_edges_m,
        age_edges=age_edges,
        length_edges_m=length_edges_m,
        area_to_mass_edges_m2_per_kg=area_to_mass_edges_m2_per_kg,
        reference_date=reference_date,
    )
    attributes = {}
    attributes["active_counts"] = initial_state["active_counts"]
    attributes["derelict_counts"] = initial_state["derelict_counts"]
    attributes["debris_counts"] = initial_state["debris_counts"]
    attributes["time"] = 0.0
    attributes["dt"] = config.dt
    attributes["time_bin_count"] = config.time_bin_count
    attributes["time_bin_width"] = config.time_bin_width
    attributes["shell_edges_m"] = shell_edges_m
    attributes["relative_speed_m_s"] = config.relative_speed_m_s
    attributes["age_edges"] = age_edges
    attributes["length_edges_m"] = length_edges_m
    attributes["area_to_mass_edges_m2_per_kg"] = area_to_mass_edges_m2_per_kg
    attributes["satellite_properties"] = config.satellite_properties
    attributes["atmospheric_density_kg_m3"] = config.atmospheric_density_kg_m3
    attributes["shell_volumes_m3"] = config.shell_volumes_m3
    attributes["debris_area_m2"] = config.debris_area_m2
    attributes["debris_mass_kg"] = config.debris_mass_kg
    attributes["random_streams"] = RandomStreams(seed)
    attributes["seed"] = seed
    attributes["collisionModule"] = modules["ccp"].CollisionModule(modules["ccp"])
    attributes["fragmentationModule"] = modules["fgp"].FragmentationModule(
        modules["fgp"]
    )
    attributes["sourcesinkModule"] = modules["scp"].SourceSinkModule(modules["scp"])
    attributes["atmospherModule"] = modules["acp"].AtmosphereModule(modules["acp"])
    attributes["recorderModule"] = modules["rcp"].RecorderModule(modules["rcp"])

    return state.SimulationState(**attributes)
