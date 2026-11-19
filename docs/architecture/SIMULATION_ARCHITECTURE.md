# Simulation module architecture

Each physics module is an independently configured class. It receives its own
configuration file and the common configuration at construction, then modifies
the shared state through `step(state)`. Modules execute sequentially.

**1. Global configuration**

- Contains shared run settings: simulation duration in seconds, satellite age-bin
  count, age-bin width in seconds, random seed, and initial-population data references.
- Defines shared shell geometry, age/length/area-to-mass bins, representative
  satellite properties, and prescribed relative collision velocities.
- Supplies consistent physical lookup tables used by multiple modules. Derived
  tables can be prepared once by initialization code.
- Is loaded by the framework and supplied to every module as the same read-only
  configuration/context object. 
- Specifically for global system configs. Settings specific to one model only belong
  in that module's configuration.

**2. Module configuration file**

- Contains that module's model selection, numerical settings, parameters, and
  model-specific input references.
- Has a format and structure owned by the module designer. The module loads and
  validates it; the controller only needs its path.
- May change without changing other modules, provided the public contract holds.
- Cannot silently override global definitions. Incompatible settings must cause
  an initialization error.

**3. Simulation state**

One data-only object contains:

| Attribute | Meaning |
| --- | --- |
| `time` | Elapsed simulation time in seconds. |
| `dt` | Current timestep duration in seconds, selected by the controller for this cycle. |
| `active_by_age[S, A]` | Active-satellite counts by shell and age bin. |
| `derelict_counts[S]` | Intact inactive-satellite counts by shell. |
| `debris_counts[S, L, Q]` | Joint debris counts by shell, length, and area-to-mass bin. |
| `collisions_this_step` | Accepted collision counts keyed by shell and participating population bins. |
| `random_generator` | Shared random stream used by stochastic steps. |

Here `S`, `A`, `L`, and `Q` are the corresponding global grid sizes.
Collision-bin references are `("active", age)`, `("derelict",)`, or
`("debris", length, area_to_mass)`. Each unordered pair is tallied once.
Masses, geometry, and encounter speeds are recovered from shared definitions.

Counts are nonnegative integers. Histograms are the authoritative inventories;
totals and averages are derived. Configuration, recording history, and local
working arrays do not belong in state. A temporary value belongs there only when
another module needs it, as with the collision handoff.

**4. Module instance and public interface**

```python
class ModelModule:
    def __init__(self, module_config_path, global_config):
        ...  # Load own config; prepare private parameters, methods, and caches.

    def step(self, state) -> None:
        ...  # Read the supplied state and apply this model's changes in place.
```

- Construction initializes the model, without receiving or modifying state.
- `step(state)` processes `[state.time, state.time + state.dt)`, using the
  controller-selected duration, which may change between cycles.
  It writes directly to `state`, rather than returning a replacement state.
- The module may read any agreed state field, but writes only its assigned fields.
  It must not change the state schema, shared grids, or simulation clock.
- Private calculations, temporary buffers, and model-specific memory may remain
  internal when necessary or computationally efficient. Information needed downstream uses an agreed state field.
- ANY randomness or sampling must use `state.random_generator` (whom has a unique seed).

**5. Controller and initialization**

The controller loads global configuration, invokes external initialization code
to populate the common state/tables, and constructs each module once with its
own configuration path and the shared configuration. Initialization checks shared
array shapes and configuration compatibility. The controller owns timestep selection and determines the step length at runtime.

Each cycle follows this order:

1. Select a positive `state.dt` for this cycle, respecting the remaining simulation
   horizon, and clear the previous collision handoff after its consumers finish.
2. Source-sink: apply launches, age progression, mission completion, and disposal.
3. Collision sampling: write feasible collision tallies without removing bodies.
4. Fragmentation: consume those tallies once and update affected populations.
5. Atmospheric decay: update shell populations using local transfer buffers.
6. Controller: advance `state.time` by `state.dt`.
7. Recorder: observe the completed state and write results.

All physics steps refer to the same controller-selected interval. Retirement/removal
must update the active-age histogram; shell transfers preserve the age or
physical-bin indices.
Age progression and retirement use elapsed time in seconds. Collision sampling
accounts for competing uses of the same population across pair types. Fragmentation owns collision removals and
reclassification, preventing duplicate updates.

**6. Recording module**

The recorder has its own configuration and can expose the same `step(state)`
interface, but treats simulation state as read-only. It owns saved snapshots,
statistics, and output files. Any additional transient measurements it needs are
captured where produced, without automatically becoming permanent state fields.

This document defines the intended contract.
