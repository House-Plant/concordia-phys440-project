import numpy as np

from tools.core.randomness import RandomStreams
from tools.core.state import SimulationState

"""
Little tool for debugging to help make a simple simulation state object since it's a big process. 
This is a small couple dozen entity 3 shell toy model. You can import this into one of your test 
scripts and call it to instance a new simulation state object. You can play around with the internal
methods from there!
"""


def create_test_state(seed=42, dt=10.0):
    earth_radius_m = 6371000.0
    shell_edges_m = np.array([300e3, 350e3, 400e3, 450e3])
    shell_volumes_m3 = np.zeros(3)

    for shell in range(3):
        inner_radius_m = earth_radius_m + shell_edges_m[shell]
        outer_radius_m = earth_radius_m + shell_edges_m[shell + 1]
        shell_volumes_m3[shell] = (
            4.0 / 3.0 * np.pi * (outer_radius_m**3 - inner_radius_m**3)
        )

    satellite_properties = {
        "active": {
            "mass_kg": 500.0,
            "collision_radius_m": 1.0,
            "drag_area_m2": 4.0,
            "drag_coefficient": 2.2,
        },
        "derelict": {
            "mass_kg": 500.0,
            "collision_radius_m": 1.0,
            "drag_area_m2": 4.0,
            "drag_coefficient": 2.2,
        },
    }

    state = SimulationState(
        active_counts=np.array([[5, 0, 3, 2], [0, 6, 0, 4], [2, 1, 4, 3]]),
        derelict_counts=np.array([[1, 2, 0, 1], [3, 0, 1, 2], [0, 2, 3, 1]]),
        debris_counts=np.arange(12).reshape(3, 2, 2),
        time=0.0,
        dt=dt,
        random_streams=RandomStreams(seed),
        time_bin_count=20,
        time_bin_width=10.0,
        shell_edges_m=shell_edges_m,
        relative_speed_m_s=np.full(3, 10000.0),
        age_edges=np.arange(5) * 10.0,
        length_edges_m=np.array([0.001, 0.01, 0.1]),
        area_to_mass_edges_m2_per_kg=np.array([0.01, 0.1, 1.0]),
        satellite_properties=satellite_properties,
        atmospheric_density_kg_m3=np.array([2e-11, 8e-12, 3e-12]),
        shell_volumes_m3=shell_volumes_m3,
        debris_area_m2=np.array([0.00001, 0.001]),
        debris_mass_kg=np.array([[0.0002, 0.00002], [0.02, 0.002]]),
        collisionModule=None,
        fragmentationModule=None,
        sourcesinkModule=None,
        atmospherModule=None,
        recorderModule=None,
    )

    global_config = {
        "random_seed": seed,
        "simulation_duration_s": state.time_bin_count * state.time_bin_width,
        "time_bin_count": state.time_bin_count,
        "time_bin_width": state.time_bin_width,
        "age_bin_count": len(state.age_edges) - 1,
        "age_bin_width_s": state.time_bin_width,
        "earth_radius_m": earth_radius_m,
        "shell_edges_m": state.shell_edges_m,
        "relative_speed_m_s": state.relative_speed_m_s,
        "age_edges": state.age_edges,
        "length_edges_m": state.length_edges_m,
        "area_to_mass_edges_m2_per_kg": state.area_to_mass_edges_m2_per_kg,
        "satellite_properties": state.satellite_properties,
        "atmospheric_density_kg_m3": state.atmospheric_density_kg_m3,
        "shell_volumes_m3": state.shell_volumes_m3,
        "debris_area_m2": state.debris_area_m2,
        "debris_mass_kg": state.debris_mass_kg,
    }

    return state, global_config
