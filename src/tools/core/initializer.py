from importlib import import_module

import tools.core.state as state
from tools.core.controller import PROJECT_ROOT
from tools.core.randomness import RandomStreams


def build_state(config, seed, module_configs):
    # Config parameters
    initial_state_interpreter_module = config.initial_state_interpreter_module
    initial_state_path = PROJECT_ROOT / config.initial_state_path
    reference_date = config.reference_date
    shell_edges_m = config.shell_edges_m
    age_edges = config.age_edges
    length_edges_m = config.length_edges_m
    area_to_mass_edges_m2_per_kg = config.area_to_mass_edges_m2_per_kg

    initial_state_interpreter = import_module(initial_state_interpreter_module)
    initial_state = initial_state_interpreter.read_satcat(
        initial_state_path,
        shell_edges_m=shell_edges_m,
        age_edges=age_edges,
        length_edges_m=length_edges_m,
        area_to_mass_edges_m2_per_kg=area_to_mass_edges_m2_per_kg,
        reference_date=reference_date,
    )
    collision_module = import_module(module_configs["ccp"].module_name)
    fragmentation_module = import_module(module_configs["fgp"].module_name)
    sourcesink_module = import_module(module_configs["scp"].module_name)
    atmosphere_module = import_module(module_configs["acp"].module_name)
    recorder_module = import_module(module_configs["rcp"].module_name)

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
    attributes["collisionModule"] = collision_module.CollisionModule(
        module_configs["ccp"]
    )
    attributes["fragmentationModule"] = fragmentation_module.FragmentationModule(
        module_configs["fgp"]
    )
    attributes["sourcesinkModule"] = sourcesink_module.SourceSinkModule(
        module_configs["scp"]
    )
    attributes["atmospherModule"] = atmosphere_module.AtmosphereModule(
        module_configs["acp"]
    )
    attributes["recorderModule"] = recorder_module.RecorderModule(module_configs["rcp"])

    return state.SimulationState(**attributes)
