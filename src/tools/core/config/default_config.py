import numpy as np

default_module_paths = {
    "rcp": "src/tools/recorder/config/default_config.py",
    "ccp": "src/tools/collision/config/default_config.py",
    "acp": "src/tools/atmosphere/config/default_config.py",
    "fgp": "src/tools/fragmentation/config/default_config.py",
    "scp": "src/tools/sourcesink/config/default_config.py",
}

initial_state_path = "data/raw/satcat.csv"
initial_state_interpreter_path = "data/interpreters/satcat_interpreter.py"
reference_date = "2026-11-24"

shell_edges_m = np.arange(200e3, 2000e3 + 50e3, 50e3)
age_edges = np.arange(101) * 365.25 * 86400
length_edges_m = np.array([0.001, 0.01, 0.1, 1.0, 10.0, 100.0])
area_to_mass_edges_m2_per_kg = np.array([0.001, 0.01, 0.1, 1.0, 10.0])

default_seed = 42
dt = 10000.0
time_bin_count = len(age_edges) - 1
time_bin_width = float(age_edges[1] - age_edges[0])

earth_radius_m = 6371000.0
shell_midpoints_m = (shell_edges_m[:-1] + shell_edges_m[1:]) / 2
shell_volumes_m3 = 4 * np.pi / 3 * np.diff((earth_radius_m + shell_edges_m) ** 3)
relative_speed_m_s = np.full(len(shell_edges_m) - 1, 10000.0)
atmospheric_reference_altitude_m = 200e3
atmospheric_reference_density_kg_m3 = 2.789e-10
atmospheric_density_power = 7.235
atmospheric_density_kg_m3 = (
    atmospheric_reference_density_kg_m3
    * (atmospheric_reference_altitude_m / shell_midpoints_m)
    ** atmospheric_density_power
)

satellite_properties = {}
satellite_properties["active"] = {
    "mass_kg": 500.0,
    "collision_radius_m": 1.0,
    "drag_area_m2": 4.0,
    "drag_coefficient": 2.2,
}
satellite_properties["derelict"] = satellite_properties["active"].copy()

debris_lengths_m = np.sqrt(length_edges_m[:-1] * length_edges_m[1:])
debris_area_to_mass_m2_per_kg = np.sqrt(
    area_to_mass_edges_m2_per_kg[:-1] * area_to_mass_edges_m2_per_kg[1:]
)
debris_area_m2 = np.pi * debris_lengths_m**2 / 4
debris_mass_kg = debris_area_m2[:, None] / debris_area_to_mass_m2_per_kg[None, :]
