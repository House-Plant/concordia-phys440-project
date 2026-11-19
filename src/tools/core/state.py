"""Data container shared by the simulation's external physics modules.

Array dimensions: S = shells, A = satellite-age bins, L = debris-length bins,
Q = area-to-mass bins. Histograms store integer object counts. Time and age
are unitless; physical quantities use the units indicated in their names.
Initialization supplies the arrays and parameters. This file only declares data.
"""

from dataclasses import dataclass, field

import numpy as np


@dataclass
class SimulationState:
    """Current populations, prescribed inputs, and the collision handoff.

    External modules operate on this same object. Population totals and averages
    are derived from the histograms; recording data and local working buffers
    are kept outside this container.
    """

    # Configured time grid. Duration = count * width; integration dt is independent.
    time_bin_count: int
    time_bin_width: float

    # Fixed shell geometry and prescribed relative collision speeds.
    shell_edges_m: np.ndarray  # [S + 1], increasing altitude boundaries
    shell_volumes_m3: np.ndarray  # [S]
    relative_speed_m_s: np.ndarray  # [S]

    # Histogram boundaries are independent of controller-selected timesteps.
    age_edges: np.ndarray  # [A + 1], unitless age, starting at zero
    length_edges_m: np.ndarray  # [L + 1], characteristic fragment length
    area_to_mass_edges_m2_per_kg: np.ndarray  # [Q + 1]

    # Fixed physical lookup tables used by collision, breakup, and decay models.
    debris_area_m2: np.ndarray  # [L], representative projected area
    debris_mass_kg: np.ndarray  # [L, Q], from area / representative area-to-mass
    debris_drag_coefficient: float
    # Keys "active" and "derelict", each mapping to mass_kg, collision_radius_m,
    # drag_area_m2, and drag_coefficient for one representative satellite.
    satellite_properties: dict[str, dict[str, float]]
    atmospheric_density_kg_m3: np.ndarray  # [S], prescribed static profile

    # Prescribed source/sink inputs for the initial model.
    launch_rate: np.ndarray  # [S], launches per second model-time unit
    mission_survival_probability: np.ndarray  # [A + 1], survival at age boundaries
    disposal_compliance: float

    # Authoritative evolving populations: nonnegative integer arrays.
    active_by_age: np.ndarray  # [S, A]
    derelict_counts: np.ndarray  # [S]
    debris_counts: np.ndarray  # [S, L, Q], JOINT length / area-to-mass histogram

    collision_avoidance_probability: float = 0.0  # prescribed input

    # Runtime clock (in seconds) and random stream persist between timesteps.
    time: float = 0.0
    dt: float = 0.0  # controller sets a positive duration before each cycle
    random_generator: np.random.Generator = field(default_factory=np.random.default_rng)

    # Temporary tally: (shell, first population bin, second population bin) -> count.
    # Bins: ("active", age), ("derelict",), or ("debris", length, area_to_mass).
    # Store each unordered pair once. Bin indices recover the physical inputs.
    # Collision sampling writes this; fragmentation reads it; replace next cycle.
    collisions_this_step: dict[tuple[int, tuple, tuple], int] = field(
        default_factory=dict
    )
