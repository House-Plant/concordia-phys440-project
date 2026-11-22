# Simulation module architecture

Each physics module is an independently configured class. It receives its own
configuration file and the common configuration at construction, then modifies
the shared state through `step(state)`. Modules execute sequentially.
Collision and fragmentation code lives in `src/tools/collision/` and
`src/tools/fragmentation/`, respectively (`tools.collision` and
`tools.fragmentation` when imported).

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

The `SimulationState` dataclass is constructed with keyword arguments. Its runtime
fields are:

| Attribute | Meaning |
| --- | --- |
| `time` | Elapsed simulation time in seconds. |
| `dt` | Current timestep duration in seconds, selected by the controller for this cycle. |
| `active_counts[S, A]` | Active-satellite counts by shell and age bin. |
| `derelict_counts[S, A]` | Intact inactive-satellite counts by shell and age bin. |
| `debris_counts[S, L, Q]` | Joint debris counts by shell, length, and area-to-mass bin. |
| `collisions_this_step` | Sparse collision tally mapping an unordered pair of entity references to an integer event count. |
| `random_streams` | Run-seeded collection of persistent component streams, accessed through `state.rng(component)`. |

Here `S`, `A`, `L`, and `Q` are the corresponding global grid sizes.
Entity references are `("active", shell, 0, 0)`, `("derelict", shell, 0, 0)`, or
`("debris", shell, length_bin, area_to_mass_bin)`. Collision keys are
`(first_entity, second_entity)`; both participants must occupy the same shell.
Each unordered pair is tallied once, and absent pairs have no recorded events.
Masses, geometry, and encounter speeds are recovered from shared definitions.
Satellite collision selection is age-independent. When applying removals or
disabling, select ages from the remaining age histogram without replacement.

Both satellite populations use the same fixed-width age bins. Age means age since
launch: active-to-derelict transitions and shell transfers preserve it. Age
progression advances both histograms by the number of age-bin intervals crossed
during the timestep. The configured shift width must match `age_edges`.

Counts are nonnegative integers. Histograms are the authoritative inventories;
totals and averages are derived. The current state also holds initialized shared
grids, prescribed physical inputs, and derived lookup tables; these remain fixed
during evolution. Model-specific configuration, recording history, and local
working arrays remain outside state. A temporary value belongs there only when
another module needs it, as with the collision handoff.

State methods provide access to runtime resources and population edits; physics
calculations remain in the modules. Population mutation interfaces currently exist
as stubs in `src/tools/core/state.py`, covering additions/removals, age-preserving
shell transfers, active-to-derelict transitions, and age progression. Methods with
an optional `ages` argument use explicit age selections when supplied; otherwise,
satellite selection requires the calling component's random generator. Population
getter and sampling-helper interfaces are not yet implemented.

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
  It updates the supplied state in place through population methods, rather than
  returning a replacement state.
- The module may read any agreed state field, but writes only its assigned fields.
  It must not change the state schema, shared grids, or simulation clock.
- Private calculations, temporary buffers, and model-specific memory may remain
  internal when necessary or computationally efficient. Information needed downstream uses an agreed state field.
- All randomness must use the module's persistent generator from
  `state.rng(component)`, including sampling inside population methods. Pass that
  generator through their `random_generator` argument when required; modules must
  not create independently seeded generators or use global random functions.
  `RandomStreams` derives streams from the run seed and stable component IDs:
  `initialization`, `source_sink`, `collision`, `fragmentation`, and `atmosphere`.
  Extra draws in one stream do not advance another component's stream.

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
must update the active-age histogram; failed disposal and disabling without
destruction transfer the selected age counts to the derelict histogram. Shell
transfers preserve the age or physical-bin indices.
Age progression and retirement use elapsed time in seconds. Collision sampling
accounts for competing uses of the same population across pair types. Fragmentation owns collision removals and
reclassification, preventing duplicate updates.

**6. Recording module**

The recorder has its own configuration and can expose the same `step(state)`
interface, but treats simulation state as read-only. It owns saved snapshots,
statistics, and output files. Any additional transient measurements it needs are
captured where produced, without automatically becoming permanent state fields.

This document defines the intended contract.
