"""Data container shared by the simulation's external physics modules.

Array dimensions: S = shells, A = satellite-age bins, L = debris-length bins,
Q = debris area-to-mass bins. Histograms store integer object counts. Time and age
are unitless; physical quantities use the units indicated in their names.
Initialization supplies the arrays and parameters.
"""

from collections.abc import Sequence
from dataclasses import dataclass, field
from typing import Literal

import numpy as np
import numpy.typing as npt

from tools.core.randomness import RandomStreams

type CollisionParticipant = npt.ArrayLike[
    Literal["active", "derelict", "debris"], int, int
]

type Entity = npt.ArrayLike[Literal["active", "derelict", "debris"], int, int, int]


@dataclass(kw_only=True)
class SimulationState:
    """Current populations, prescribed inputs, and the collision handoff.

    External modules operate on this same object. Population totals and averages
    are derived from the histogram age distribution. Data recording, along with all
    associated model physics, happen externally in seperate modules.
    """

    # 1. Primary runtime information.
    # Authoritative evolving populations: nonnegative integer arrays.
    active_counts: np.ndarray  # [S, A]
    derelict_counts: np.ndarray  # [S, A]
    debris_counts: np.ndarray  # [S, L, Q], JOINT length / area-to-mass histogram

    # Runtime clock (in seconds) and random stream persist between timesteps.
    time: float = 0.0
    dt: float = 0.0  # controller sets a positive duration before each cycle

    # Random generator object, initialized beforehand
    random_streams: RandomStreams

    # Sampled events cannot be recovered from the population histograms alone.
    # Temporary tally: (first participant, second participant) ===> count.
    # Participants: ("active", shell, 0, 0), ("derelict", shell, 0, 0), or
    # ("debris", shell, length_bin, area_to_mass_bin). Store each unordered pair once.
    # Collision sampling writes collision tallies, and then fragmentation consumes them to update populations.
    # Clears before the next cycle.
    # the field(default_factory=dict) essentially ensures only copies of this can be assigned to variables.
    collisions_this_step: dict[npt.ArrayLike[Entity, Entity], int] = field(
        default_factory=dict
    )

    # 2. Primary unchanging definitions and prescribed inputs.
    # Configured time grid. Duration = count * width
    time_bin_count: int
    time_bin_width: float

    # Fixed shell geometry and prescribed relative collision speeds.
    shell_edges_m: np.ndarray  # [S + 1], increasing altitude boundaries
    relative_speed_m_s: np.ndarray  # [S], relative average collision speed in shell

    # Histogram boundaries are independent of controller-selected timesteps.
    age_edges: np.ndarray  # [A + 1], age in seconds, starting at zero
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

    # METHODS (1): Core Utility Methods
    # Below are the instance methods indicated to core utilities within the instance.

    def rng(self, component: str) -> np.random.Generator:
        """
        An externally accessed wrapper method. This takes the component name token as a string,
        and returns it's unique persistent random number generation stream.
        """
        return self.random_streams.get(component)

    # METHODS (2): Population Getter Methods
    # Below are the instance methods indicated for getting (reading) population attributes,
    # as well as some other simulation parameters.
    # Histogram getters return read-only views of all shells or one shell, without copying counts.
    # Getters do not modify state or use random streams.
    # Invalid entity types and negative or out-of-range indices will throw errors.

    def get_entity_counts(self, entities: Sequence[Entity]):
        """
        Code to get number of entities of given types
        Satellites (active or derelict) return total count across ages in their shell
        Debris entities return count in their specified shell, length, and area-to-mass bin
        Returns integer array [N] in the same order as the supplied entity references
        NOTE: Satellite entity references must use zero for both physical-bin indices
        """
        return

    def get_satellite_age_counts(
        self,
        population: Literal["active", "derelict"],
        shell: int | None = None,
    ):
        """
        Code to get satellite age histogram counts for active or derelict population
        Shell selection is optional. In the absence, returns a read-only view [S, A] of all shells
        Passing one shell index returns a read-only view [A] of that shell's age counts
        Uses basic indexing so population data is shared without copying or reconstruction
        NOTE: NOT FOR DEBRIS POPULATION, WILL THROW ERROR IF USED
        """
        return

    def get_debris_counts(self, shell: int | None = None):
        """
        Code to get joint debris histogram counts for all altitude shells or one shell
        Shell is optional. In the absence, returns a read-only view [S, L, Q] of all shells
        Passing one shell index returns a read-only view [L, Q] of that shell's debris counts
        Uses basic indexing so population data is shared without copying or reconstruction
        """
        return

    def get_collisions_this_step(self):
        """
        Code to get a read-only live mapping of the sparse collision tally for the current timestep
        Maps (first_entity, second_entity) to integer event count
        Both entity references include their shell. Each unordered pair is stored once.
        Empty mapping indicates no recorded collisions
        NOTE: Reading does not clear or consume the collision tally
        """
        return

    # METHODS (3): Population Setter Methods
    # Below are the instance methods indicated for setting (modifying) population attributes
    # Implicitly, all methods below will refuse setting negative population numbers under any circumstance,
    # and will throw a runtime warning if such a modification is requested.

    def remove_entities(
        self, entities: npt.ArrayLike[npt.Arraylike[Entity, int]], random_generator=None
    ):
        """
        Code to remove number of entities of given types
        Satelites (active or derelict) are removed randomly from age distribution
        NOTE: Recommend using dedicated remove_satelites method for launches and transfer_entities_shell for transfers
        If this is used for satelites, requires passing your random_generator stream
        """
        return

    def add_entities(
        self, entities: npt.ArrayLike[npt.ArrayLike[Entity, int]], random_generator=None
    ):
        """
        Code to add number of entities of given types
        Satelites (active or derelict) are added to youngest age bin (as if they were launched)
        NOTE: Recommend using dedicated add_satelites_new method for launches and transfer_entities_shell for transfers
        If this is used for satelites, requires passing your random_generator stream
        """
        return

    def transfer_entities_shell(
        self,
        entities: npt.ArrayLike[npt.ArrayLike[Entity, int]],
        new_altitude_shells: npt.ArrayLike,
        ages: npt.ArrayLike[int] = None,
        random_generator=None,
    ):
        """
        Code to transfer number of entities to new altitude shells
        Satelites (active or derelict) are sampled randomly from local
        age distribution and keep their age on transfer
        If this is used for satelites, requires passing your random_generator stream
        Supports optional passing of age argument, if age specific transfers are required.
        """
        return

    def derelict_satelites_active(
        self,
        entities: npt.ArrayLike[npt.ArrayLike[Entity, int]],
        ages: npt.ArrayLike[int] = None,
        random_generator=None,
    ):
        """
        Code to transition a number of satelites (active only) of various ages to derelicts
        Ages is optional. In the absence, satelites will be picked from local age distribution
        New derelicts inherit the age of the satelite they were born from
        NOTE: NOT FOR DERELICT OR DEBRIS ENTITIES, WILL THROW ERROR IF USED
        If this is used without ages, requires passing your random_generator stream
        """
        return

    def remove_satelites(
        self,
        entities: npt.ArrayLike[npt.ArrayLike[Entity, int]],
        ages: npt.ArrayLike[int] = None,
        random_generator=None,
    ):
        """
        Code to remove number of satelites (active or derelict) of various ages'
        Ages is optional. In the absence, satelites will be picked from local age distribution
        NOTE: NOT FOR DEBRIS ENTITIES, WILL THROW ERROR IF USED
        If this is used without ages, requires passing your random_generator stream
        """
        return

    def add_satelites_new(
        self, satelite_nums: npt.ArrayLike[npt.ArrayLike[Entity, int]]
    ):
        """
        Code to add satelites to first age bin
        NOTE: NOT FOR DERELICT OR DEBRIS ENTITIES, WILL THROW ERROR IF USED
        """
        return

    def advance_ages_satelites(self):
        """
        Code that checks if n != 0, where
        n = np.floor( ((time % time_bin_width) + dt)/time_bin_width )
        If this is true, it shifts (advances) satelite age histogram counts by n bins
        """
        return
