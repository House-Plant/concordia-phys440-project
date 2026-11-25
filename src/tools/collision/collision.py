"""Collision-sampling module template following the simulation contract."""

from pathlib import Path
from runpy import run_path

import numpy as np

from tools.core.state import SimulationState

"""Monte Carlo simulation of collisions between orbital objects."""


class CollisionModule:
    """Sample feasible collisions without modifying object populations."""

    # ------------------------------------------------------------
    # 1. INITIALIZATION
    # ------------------------------------------------------------

    def __init__(self, module_config):
        """Initialize the collision model using its configuration."""

        self.config = module_config

    # ------------------------------------------------------------
    # 2. COLLISION CROSS-SECTION
    # ------------------------------------------------------------

    @staticmethod
    def collision_cross_section(r_A, r_B):
        """Calculate the collision cross-section between two objects.

        Parameters
        ----------
        r_A : float
            Collision radius of object A [m].
        r_B : float
            Collision radius of object B [m].

        Returns
        -------
        float
            Collision cross-section [m^2].
        """

        return np.pi * (r_A + r_B) ** 2

    # ------------------------------------------------------------
    # 3. NUMBER OF POSSIBLE COLLISION PAIRS
    # ------------------------------------------------------------

    @staticmethod
    def number_of_pairs(N_A, N_B, same_population=False):
        """Calculate the number of distinct possible collision pairs."""

        if same_population:
            return N_A * (N_A - 1) // 2

        return N_A * N_B

    # ------------------------------------------------------------
    # 4. COLLISION RATE
    # ------------------------------------------------------------

    @staticmethod
    def collision_rate(number_pairs, sigma_AB, v_rel, V_shell):
        """Calculate the expected collision rate.

        Parameters
        ----------
        number_pairs : int
            Number of possible collision pairs.
        sigma_AB : float
            Collision cross-section [m^2].
        v_rel : float
            Relative collision velocity [m/s].
        V_shell : float
            Volume of the orbital shell [m^3].

        Returns
        -------
        float
            Expected number of collisions per second [1/s].
        """

        return number_pairs * sigma_AB * v_rel / V_shell

    # ------------------------------------------------------------
    # 5. IDENTIFY OBJECT POPULATIONS WITHIN A SHELL
    # ------------------------------------------------------------

    @staticmethod
    def get_shell_entities(state, shell):
        """Identify all populated object categories within a shell."""

        entities = [
            ("active", shell, 0, 0),
            ("derelict", shell, 0, 0),
        ]

        debris = state.get_debris_counts(shell)

        # Identify populated debris bins.
        for length_bin, area_mass_bin in np.argwhere(debris > 0):
            entities.append(
                (
                    "debris",
                    shell,
                    int(length_bin),
                    int(area_mass_bin),
                )
            )

        # Retrieve the number of objects in each category.
        counts = state.get_entity_counts(entities)

        # Exclude empty populations.
        entities = [entity for entity, count in zip(entities, counts) if count > 0]

        counts = counts[counts > 0]

        return entities, counts

    # ------------------------------------------------------------
    # 6. DETERMINE OBJECT COLLISION RADII
    # ------------------------------------------------------------

    @staticmethod
    def get_collision_radius(state, entity):
        """Retrieve or calculate the collision radius of an entity."""

        population, shell, length_bin, area_mass_bin = entity

        # Active and derelict satellites.
        if population in ("active", "derelict"):
            radius = state.satellite_properties[population]["collision_radius_m"]

        # Debris objects.
        else:
            area = state.debris_area_m2[length_bin]

            # Equivalent circular radius.
            radius = np.sqrt(area / np.pi)

        return radius

    # ------------------------------------------------------------
    # 7. IDENTIFY ENABLED COLLISION CATEGORIES
    # ------------------------------------------------------------

    def collision_enabled(self, entity_A, entity_B):
        """Check whether a collision category is enabled."""

        order = {
            "active": 0,
            "derelict": 1,
            "debris": 2,
        }

        types = sorted(
            [entity_A[0], entity_B[0]],
            key=order.get,
        )

        category = "_".join(types)

        return getattr(self.config, category)

    # ------------------------------------------------------------
    # 8. CONSTRUCT POSSIBLE COLLISION CHANNELS
    # ------------------------------------------------------------

    def get_collision_channels(self, state, entities, shell):
        """Construct unique collision pairs and their rate coefficients."""

        v_rel = state.relative_speed_m_s[shell]
        V_shell = state.shell_volumes_m3[shell]

        radii = [self.get_collision_radius(state, entity) for entity in entities]

        channels = []
        coefficients = []

        for i in range(len(entities)):
            for j in range(i, len(entities)):
                if not self.collision_enabled(entities[i], entities[j]):
                    continue

                sigma_AB = self.collision_cross_section(radii[i], radii[j])

                # Collision rate per possible object pair.
                coefficient = self.collision_rate(1, sigma_AB, v_rel, V_shell)

                channels.append((i, j))
                coefficients.append(coefficient)

        return channels, np.asarray(coefficients, dtype=float)

    # ------------------------------------------------------------
    # 9. CALCULATE COLLISION RATES
    # ------------------------------------------------------------

    def get_collision_rates(self, channels, coefficients, counts):
        """Calculate instantaneous rates for all collision channels."""

        rates = np.zeros(len(channels), dtype=float)

        for k, (i, j) in enumerate(channels):
            N_A = int(counts[i])
            N_B = int(counts[j])

            number_pairs = self.number_of_pairs(
                N_A,
                N_B,
                same_population=(i == j),
            )

            rates[k] = number_pairs * coefficients[k]

        return rates

    # ------------------------------------------------------------
    # 10. MONTE CARLO COLLISION SAMPLING
    # ------------------------------------------------------------

    def sample_shell_collisions(self, state, shell, rng):
        """Randomly sample feasible collision events in one shell."""

        dt = state.dt

        entities, counts = self.get_shell_entities(state, shell)

        # Local inventory: does not modify the shared state.
        remaining_counts = counts.copy()

        channels, coefficients = self.get_collision_channels(state, entities, shell)

        collisions = {}
        elapsed_time = 0.0

        while elapsed_time < dt:
            # Recalculate rates using remaining available objects.
            rates = self.get_collision_rates(
                channels,
                coefficients,
                remaining_counts,
            )

            total_rate = rates.sum()

            # No more possible collisions.
            if total_rate <= 0:
                break

            # Random waiting time before the next collision.
            waiting_time = rng.exponential(scale=1.0 / total_rate)

            elapsed_time += waiting_time

            # Stop if the event occurs outside the timestep.
            if elapsed_time >= dt:
                break

            # Probability of selecting each collision channel.
            probabilities = rates / total_rate

            channel_index = rng.choice(
                len(channels),
                p=probabilities,
            )

            i, j = channels[channel_index]

            # Create a unique, unordered collision key.
            pair = tuple(sorted((entities[i], entities[j])))

            # Record the collision.
            collisions[pair] = collisions.get(pair, 0) + 1

            # Reserve both participants locally.
            remaining_counts[i] -= 1
            remaining_counts[j] -= 1

        return collisions

    # ------------------------------------------------------------
    # 11. SIMULATION STEP
    # ------------------------------------------------------------

    def step(self, state: SimulationState) -> None:
        """Execute the collision model over one simulation timestep."""

        dt = state.dt

        if not np.isfinite(dt) or dt <= 0:
            raise ValueError("Timestep must be finite and positive.")

        # Use the simulation's persistent collision random stream.
        rng = state.rng("collision")

        number_shells = state.active_counts.shape[0]

        collisions = {}

        # Simulate collisions independently in each orbital shell.
        for shell in range(number_shells):
            shell_collisions = self.sample_shell_collisions(state, shell, rng)

            collisions.update(shell_collisions)

        # Replace the previous collision tally with the current one.
        state.collisions_this_step.clear()
        state.collisions_this_step.update(collisions)
