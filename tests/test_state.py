import numpy as np
import pytest

from tools.core.randomness import RandomStreams
from tools.core.state import SimulationState


@pytest.fixture
def state():
    return SimulationState(
        active_counts=np.array([[5, 0, 3, 2], [0, 6, 0, 4], [2, 1, 4, 3]]),
        derelict_counts=np.array([[1, 2, 0, 1], [3, 0, 1, 2], [0, 2, 3, 1]]),
        debris_counts=np.arange(12).reshape(3, 2, 2),
        random_streams=RandomStreams(42),
        time_bin_count=20,
        time_bin_width=10.0,
        shell_edges_m=np.array([300e3, 350e3, 400e3, 450e3]),
        relative_speed_m_s=np.full(3, 10000.0),
        age_edges=np.arange(5) * 10.0,
        length_edges_m=np.array([0.001, 0.01, 0.1]),
        area_to_mass_edges_m2_per_kg=np.array([0.01, 0.1, 1.0]),
        satellite_properties={},
        atmospheric_density_kg_m3=np.ones(3),
        shell_volumes_m3=np.ones(3),
        debris_area_m2=np.ones(2),
        debris_mass_kg=np.ones((2, 2)),
    )


def test_entity_counts_preserve_order_and_duplicates(state):
    entities = [
        ("debris", 2, 1, 0),
        ("active", 0, 0, 0),
        ("derelict", 1, 0, 0),
        ("debris", 2, 1, 0),
    ]
    np.testing.assert_array_equal(state.get_entity_counts(entities), [10, 10, 6, 10])
    assert state.get_entity_counts([]).shape == (0,)


@pytest.mark.parametrize("population", ["active", "derelict", "debris"])
@pytest.mark.parametrize("shell", [None, 1])
def test_histogram_getters_return_live_read_only_views(state, population, shell):
    counts = getattr(state, population + "_counts")
    if population == "debris":
        view = state.get_debris_counts(shell)
    else:
        view = state.get_satellite_age_counts(population, shell)

    assert np.shares_memory(counts, view)
    assert not view.flags.writeable
    assert counts.flags.writeable

    if shell is None:
        assert view.shape == counts.shape
        counts.flat[0] += 1
        assert view.flat[0] == counts.flat[0]
    else:
        assert view.shape == counts.shape[1:]
        counts[shell].flat[0] += 1
        assert view.flat[0] == counts[shell].flat[0]

    with pytest.raises(ValueError):
        view.flat[0] = 0


@pytest.mark.parametrize(
    "entity, error",
    [
        (("other", 0, 0, 0), ValueError),
        (("active", 0, 1, 0), ValueError),
        (("derelict", 0, 0, 1), ValueError),
        (("active", -1, 0, 0), IndexError),
        (("derelict", 3, 0, 0), IndexError),
        (("debris", -1, 0, 0), IndexError),
        (("debris", 3, 0, 0), IndexError),
        (("debris", 0, -1, 0), IndexError),
        (("debris", 0, 2, 0), IndexError),
        (("debris", 0, 0, -1), IndexError),
        (("debris", 0, 0, 2), IndexError),
    ],
)
def test_entity_getter_rejects_documented_invalid_inputs(state, entity, error):
    with pytest.raises(error):
        state.get_entity_counts([entity])


@pytest.mark.parametrize("shell", [-1, 3])
def test_histogram_getters_reject_invalid_shells(state, shell):
    with pytest.raises(IndexError):
        state.get_satellite_age_counts("active", shell)
    with pytest.raises(IndexError):
        state.get_debris_counts(shell)


def test_collision_getter_is_read_only_live_and_does_not_consume(state):
    collisions = state.get_collisions_this_step()
    assert len(collisions) == 0
    pair = (("active", 0, 0, 0), ("debris", 0, 1, 1))
    state.collisions_this_step[pair] = 2
    assert collisions[pair] == 2
    with pytest.raises(TypeError):
        collisions[pair] = 3
    assert state.collisions_this_step[pair] == 2
    state.collisions_this_step.clear()
    assert len(collisions) == 0


def test_getters_leave_random_streams_unchanged(state):
    generator = state.rng("collision")
    before = generator.bit_generator.state
    assert state.rng("collision") is generator
    state.get_entity_counts([("active", 0, 0, 0)])
    state.get_satellite_age_counts("active")
    state.get_debris_counts()
    state.get_collisions_this_step()
    assert generator.bit_generator.state == before


def test_generic_additions_use_youngest_age_bin_and_exact_debris_bin(state):
    active_before = state.active_counts.copy()
    derelict_before = state.derelict_counts.copy()
    debris_before = state.debris_counts.copy()
    generator = state.rng("source_sink")
    stream_before = generator.bit_generator.state
    state.add_entities(
        [
            (("active", 1, 0, 0), 3),
            (("derelict", 2, 0, 0), 4),
            (("debris", 0, 1, 0), 5),
        ],
        random_generator=generator,
    )
    active_before[1, 0] += 3
    derelict_before[2, 0] += 4
    debris_before[0, 1, 0] += 5
    np.testing.assert_array_equal(state.active_counts, active_before)
    np.testing.assert_array_equal(state.derelict_counts, derelict_before)
    np.testing.assert_array_equal(state.debris_counts, debris_before)
    assert generator.bit_generator.state == stream_before


def test_generic_removals_handle_satellites_and_debris(state):
    active_before = state.active_counts.copy()
    derelict_before = state.derelict_counts.copy()
    debris_before = state.debris_counts.copy()
    state.remove_entities(
        [
            (("active", 0, 0, 0), 4),
            (("derelict", 1, 0, 0), 3),
            (("debris", 2, 0, 1), 2),
        ],
        random_generator=state.rng("fragmentation"),
    )
    assert state.active_counts[0].sum() == active_before[0].sum() - 4
    assert state.derelict_counts[1].sum() == derelict_before[1].sum() - 3
    assert np.all(state.active_counts >= 0)
    assert np.all(state.derelict_counts >= 0)
    np.testing.assert_array_equal(state.active_counts[1:], active_before[1:])
    np.testing.assert_array_equal(
        state.derelict_counts[[0, 2]], derelict_before[[0, 2]]
    )
    debris_before[2, 0, 1] -= 2
    np.testing.assert_array_equal(state.debris_counts, debris_before)


def test_explicit_satellite_removals_apply_one_age_bin_per_entry(state):
    before = state.active_counts.copy()
    state.remove_satelites(
        [(("active", 0, 0, 0), 2), (("active", 0, 0, 0), 1)],
        ages=[0, 2],
    )
    before[0, 0] -= 2
    before[0, 2] -= 1
    np.testing.assert_array_equal(state.active_counts, before)


def test_repeated_random_removals_sample_remaining_inventory(state):
    state.remove_satelites(
        [(("active", 0, 0, 0), 6), (("active", 0, 0, 0), 4)],
        random_generator=state.rng("fragmentation"),
    )
    np.testing.assert_array_equal(state.active_counts[0], [0, 0, 0, 0])


@pytest.mark.parametrize("population", ["active", "derelict"])
def test_random_shell_transfers_preserve_age_histogram(state, population):
    counts = getattr(state, population + "_counts")
    before = counts.copy()
    state.transfer_entities_shell(
        [((population, 0, 0, 0), 3)],
        [2],
        random_generator=state.rng("atmosphere"),
    )
    removed = before[0] - counts[0]
    added = counts[2] - before[2]
    assert removed.sum() == 3
    assert np.all(removed >= 0)
    assert np.all(counts >= 0)
    np.testing.assert_array_equal(removed, added)
    np.testing.assert_array_equal(counts.sum(axis=0), before.sum(axis=0))
    np.testing.assert_array_equal(counts[1], before[1])


def test_explicit_shell_transfer_preserves_selected_age(state):
    before = state.derelict_counts.copy()
    state.transfer_entities_shell([(("derelict", 0, 0, 0), 2)], [2], ages=[1])
    before[0, 1] -= 2
    before[2, 1] += 2
    np.testing.assert_array_equal(state.derelict_counts, before)


def test_debris_shell_transfer_preserves_physical_bins(state):
    before = state.debris_counts.copy()
    state.transfer_entities_shell([(("debris", 2, 1, 0), 4)], [0])
    before[2, 1, 0] -= 4
    before[0, 1, 0] += 4
    np.testing.assert_array_equal(state.debris_counts, before)


def test_same_shell_transfer_leaves_inventory_unchanged(state):
    before = state.active_counts.copy()
    state.transfer_entities_shell(
        [(("active", 0, 0, 0), 4)],
        [0],
        random_generator=state.rng("atmosphere"),
    )
    np.testing.assert_array_equal(state.active_counts, before)


@pytest.mark.parametrize("explicit_age", [False, True])
def test_derelict_transition_preserves_ages_and_total_inventory(state, explicit_age):
    active_before = state.active_counts.copy()
    derelict_before = state.derelict_counts.copy()
    ages = None
    generator = state.rng("fragmentation")
    if explicit_age:
        ages = [2]
        generator = None
    state.derelict_satelites_active(
        [(("active", 0, 0, 0), 2)], ages=ages, random_generator=generator
    )
    removed = active_before[0] - state.active_counts[0]
    added = state.derelict_counts[0] - derelict_before[0]
    assert removed.sum() == 2
    np.testing.assert_array_equal(removed, added)
    np.testing.assert_array_equal(
        state.active_counts + state.derelict_counts, active_before + derelict_before
    )
    if explicit_age:
        np.testing.assert_array_equal(removed, [0, 0, 2, 0])


def test_new_satellites_enter_only_youngest_age_bin(state):
    before = state.active_counts.copy()
    state.add_satelites_new([(("active", 1, 0, 0), 7)])
    before[1, 0] += 7
    np.testing.assert_array_equal(state.active_counts, before)


@pytest.mark.parametrize(
    "method, args, kwargs",
    [
        ("add_entities", [[(("debris", 0, 0, 0), -1)]], {}),
        ("remove_entities", [[(("debris", 0, 0, 0), 1)]], {}),
        ("add_satelites_new", [[(("active", 0, 0, 0), -1)]], {}),
        ("remove_satelites", [[(("active", 0, 0, 0), -1)]], {"ages": [0]}),
        ("remove_satelites", [[(("active", 0, 0, 0), 6)]], {"ages": [0]}),
        ("remove_satelites", [[(("active", 0, 0, 0), 11)]], {}),
        ("transfer_entities_shell", [[(("debris", 0, 0, 0), 1)], [1]], {}),
        (
            "transfer_entities_shell",
            [[(("active", 0, 0, 0), 6)], [1]],
            {"ages": [0]},
        ),
        ("derelict_satelites_active", [[(("active", 0, 0, 0), 6)]], {"ages": [0]}),
    ],
)
def test_negative_population_changes_warn_and_leave_inventory_unchanged(
    state, method, args, kwargs
):
    active_before = state.active_counts.copy()
    derelict_before = state.derelict_counts.copy()
    debris_before = state.debris_counts.copy()
    with pytest.warns(RuntimeWarning):
        getattr(state, method)(*args, **kwargs)
    np.testing.assert_array_equal(state.active_counts, active_before)
    np.testing.assert_array_equal(state.derelict_counts, derelict_before)
    np.testing.assert_array_equal(state.debris_counts, debris_before)


@pytest.mark.parametrize(
    "method, args",
    [
        ("get_satellite_age_counts", ["debris"]),
        ("remove_satelites", [[(("debris", 0, 0, 0), 1)]]),
        ("derelict_satelites_active", [[(("derelict", 0, 0, 0), 1)]]),
        ("derelict_satelites_active", [[(("debris", 0, 0, 0), 1)]]),
        ("add_satelites_new", [[(("derelict", 0, 0, 0), 1)]]),
        ("add_satelites_new", [[(("debris", 0, 0, 0), 1)]]),
    ],
)
def test_satellite_methods_reject_documented_invalid_populations(state, method, args):
    with pytest.raises(ValueError):
        getattr(state, method)(*args)


@pytest.mark.parametrize(
    "method, args",
    [
        ("add_entities", [[(("active", 0, 0, 0), 1)]]),
        ("remove_entities", [[(("derelict", 0, 0, 0), 1)]]),
        ("remove_satelites", [[(("active", 0, 0, 0), 1)]]),
        ("derelict_satelites_active", [[(("active", 0, 0, 0), 1)]]),
        ("transfer_entities_shell", [[(("active", 0, 0, 0), 1)], [1]]),
    ],
)
def test_random_satellite_operations_require_supplied_generator(state, method, args):
    with pytest.raises(ValueError):
        getattr(state, method)(*args)


def test_supplied_random_stream_is_reproducible_and_component_isolated(state):
    state.rng("collision").random(100)
    before_other_stream = state.rng("source_sink").bit_generator.state
    before = state.active_counts[0].copy()
    state.remove_satelites(
        [(("active", 0, 0, 0), 4)], random_generator=state.rng("fragmentation")
    )
    remaining = state.active_counts[0].copy()
    state.active_counts[0] = before
    streams = RandomStreams(42)
    state.remove_satelites(
        [(("active", 0, 0, 0), 4)], random_generator=streams.get("fragmentation")
    )
    np.testing.assert_array_equal(state.active_counts[0], remaining)
    assert state.rng("source_sink").bit_generator.state == before_other_stream


@pytest.mark.parametrize(
    "time, dt, expected",
    [
        (0.0, 5.0, [1, 2, 3, 4]),
        (7.0, 3.0, [0, 1, 2, 7]),
        (10.0, 10.0, [0, 1, 2, 7]),
        (7.0, 23.0, [0, 0, 0, 10]),
        (0.0, 20.0, [0, 0, 1, 9]),
        (0.0, 40.0, [0, 0, 0, 10]),
        (0.0, 100.0, [0, 0, 0, 10]),
    ],
)
def test_age_progression_keeps_overflow_and_existing_views(state, time, dt, expected):
    state.active_counts[:] = [1, 2, 3, 4]
    state.derelict_counts[:] = [2, 4, 6, 8]
    active_view = state.get_satellite_age_counts("active")
    derelict_view = state.get_satellite_age_counts("derelict")
    state.time = time
    state.dt = dt
    state.advance_ages_satelites()
    for shell in range(3):
        np.testing.assert_array_equal(active_view[shell], expected)
        np.testing.assert_array_equal(derelict_view[shell], np.array(expected) * 2)
    assert state.time == time
    assert state.dt == dt


def test_single_age_bin_retains_all_satellites(state):
    state.active_counts = np.array([[3], [5], [7]])
    state.derelict_counts = np.array([[2], [4], [6]])
    state.dt = 50.0
    state.advance_ages_satelites()
    np.testing.assert_array_equal(state.active_counts[:, 0], [3, 5, 7])
    np.testing.assert_array_equal(state.derelict_counts[:, 0], [2, 4, 6])
