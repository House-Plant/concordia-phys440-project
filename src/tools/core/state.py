"""Data container shared by the simulation's external physics modules.

Array dimensions: S = shells, A = satellite-age bins, L = debris-length bins,
Q = area-to-mass bins. Histograms store integer object counts. Time and age
are unitless; physical quantities use the units indicated in their names.
Initialization supplies the arrays and parameters. This file only declares data.
"""

from dataclasses import dataclass, field
from typing import Literal

import numpy as np

from tools.core.randomness import RandomStreams

type CollisionParticipant = tuple[Literal["active", "derelict", "debris"], int, int]


@dataclass(kw_only=True)
class SimulationState:
    """Current populations, prescribed inputs, and the collision handoff.

    External modules operate on this same object. Population totals and averages
    are derived from the histograms; recording data and local working buffers
    are kept outside this container.
    """

    # 1. Primary runtime information.
    # Authoritative evolving populations: nonnegative integer arrays.
    active_counts: np.ndarray  # [S, A]
    derelict_counts: np.ndarray  # [S]
    debris_counts: np.ndarray  # [S, L, Q], JOINT length / area-to-mass histogram

    # Runtime clock (in seconds) and random stream persist between timesteps.
    time: float = 0.0
    dt: float = 0.0  # controller sets a positive duration before each cycle

    # Random generator object, initialized beforehand
    random_streams: RandomStreams

    # Sampled events cannot be recovered from the population histograms alone.
    # Temporary tally: (shell, first participant, second participant) ===> count.
    # Participants: ("active", 0, 0), ("derelict", 0, 0), or
    # ("debris", length_bin, area_to_mass_bin). Store each unordered pair once.
    # Collision sampling writes collision tallies, and then fragmentation consumes them to update populations.
    # Clears before the next cycle.
    # the field(default_factory=dict) essentially ensures only copies of this can be assigned to variables.
    collisions_this_step: dict[
        tuple[int, CollisionParticipant, CollisionParticipant], int
    ] = field(default_factory=dict)

    # 2. Primary unchanging definitions and prescribed inputs.
    # Configured time grid. Duration = count * width; integration dt is independent.
    time_bin_count: int
    time_bin_width: float

    # Fixed shell geometry and prescribed relative collision speeds.
    shell_edges_m: np.ndarray  # [S + 1], increasing altitude boundaries
    relative_speed_m_s: np.ndarray  # [S], relative average collision speed in shell

    # Histogram boundaries are independent of controller-selected timesteps.
    age_edges: np.ndarray  # [A + 1], unitless age, starting at zero
    length_edges_m: np.ndarray  # [L + 1], characteristic fragment length
    area_to_mass_edges_m2_per_kg: np.ndarray  # [Q + 1]

    # debris_drag_coefficient: float
    # Keys "active" and "derelict", each mapping to mass_kg, collision_radius_m,
    # drag_area_m2, and drag_coefficient for one representative satellite.
    satellite_properties: dict[str, dict[str, float]]
    atmospheric_density_kg_m3: np.ndarray  # [S], prescribed static profile

    # 3. Derived quantities stored for convenience.
    # Calculated from shell edges and the initializer's chosen Earth radius.
    shell_volumes_m3: np.ndarray  # [S]

    # Calculated using the initializer's representative-size/shape and
    # representative area-to-mass conventions; bin edges alone are insufficient.
    debris_area_m2: np.ndarray  # [L], representative projected area
    debris_mass_kg: np.ndarray  # [L, Q], from area / representative area-to-mass

    def rng(self, component: str) -> np.random.Generator:
        """
        An externally accessed wrapper method. This takes the component name token as a string,
        and returns it's unique persistent random number generation stream.
        """
        return self.random_streams.get(component)

    def remove_entities(entities: tuple[tuple[int, tuple[str, int, int], int]]):
        # code to remove number of entities of given types
        # satelites are removed randomly from age distribution
        return

    def add_entities(
        entities: tuple[tuple[int, tuple[str, int, int], int]], warn_bypass=False
    ):
        # NOTE: NOT FOR ADDING 'ACTIVE' ENTITIES, WILL THROW WARNING UNLESS BYPASS FLAG TOGGLED
        # code to add number of entities of given types
        # satelites are added randomly matching age distribution, if spawned
        return

    def shell_transfer_entities(
        entities: tuple[tuple[int, tuple[str, int, int], int]],
        new_altitude_shells: tuple,
    ):
        # code to transfer number of entities of given types to new altitude shells
        # satelites tranfered are chosen randomly from age distribution
        return

    def remove_satelite(satelite_nums_per_age: tuple[int, int, int]):
        # code to remove number of satelites from respective indicated age bin
        return

    def add_satelite_new(satelite_nums: tuple[int, int]):
        # code to add satelites to first age bin
        return
