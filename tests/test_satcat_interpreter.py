import numpy as np
import pandas as pd

from data.interpreters.satcat_interpreter import read_satcat


def test_satcat_population_mapping(tmp_path):
    base = {
        "OBJECT_TYPE": "PAY",
        "OPS_STATUS_CODE": "+",
        "ORBIT_CENTER": "EA",
        "ORBIT_TYPE": "ORB",
        "LAUNCH_DATE": "2026-11-24",
        "DECAY_DATE": None,
        "APOGEE": 200,
        "PERIGEE": 200,
    }
    rows = [base | {"OPS_STATUS_CODE": status} for status in ["+", "P", "B", "S", "X"]]
    rows += [
        base | {"OPS_STATUS_CODE": "-", "APOGEE": 300},
        base | {"OPS_STATUS_CODE": None, "LAUNCH_DATE": "1900-01-01"},
    ]
    rows += [base | {"OBJECT_TYPE": kind} for kind in ["DEB", "R/B", "UNK"]]
    path = tmp_path / "satcat.csv"
    pd.DataFrame(rows).to_csv(path, index=False)

    result = read_satcat(
        path,
        shell_edges_m=[200e3, 250e3, 400e3],
        age_edges=[0, 365.25 * 86400, 100 * 365.25 * 86400],
        length_edges_m=[0.01, 0.1, 1.0],
        area_to_mass_edges_m2_per_kg=[0.001, 0.01, 0.1],
    )

    assert result["active_counts"].shape == (2, 2)
    assert result["derelict_counts"].shape == (2, 2)
    assert result["debris_counts"].shape == (2, 2, 2)
    assert result["active_counts"].sum() == 5
    assert result["active_counts"][0, 0] == 5
    assert result["derelict_counts"].sum() == 2
    assert result["derelict_counts"][1, 0] == 1
    assert result["derelict_counts"][0, -1] == 1
    assert result["debris_counts"].sum() == 3
    assert result["debris_counts"][0, 1, 1] == 3
    for name in ("active_counts", "derelict_counts", "debris_counts"):
        assert np.issubdtype(result[name].dtype, np.integer)


def test_satcat_excludes_objects_outside_model(tmp_path):
    base = {
        "OBJECT_TYPE": "PAY",
        "OPS_STATUS_CODE": "+",
        "ORBIT_CENTER": "EA",
        "ORBIT_TYPE": "ORB",
        "LAUNCH_DATE": "2026-11-24",
        "DECAY_DATE": None,
        "APOGEE": 200,
        "PERIGEE": 200,
    }
    rows = [
        base | {"DECAY_DATE": "2026-11-20"},
        base | {"ORBIT_CENTER": "MO"},
        base | {"ORBIT_TYPE": "DOC"},
        base | {"LAUNCH_DATE": "2026-11-25"},
        base | {"APOGEE": None},
        base | {"PERIGEE": None},
        base | {"APOGEE": 199, "PERIGEE": 199},
        base | {"APOGEE": 2001, "PERIGEE": 2001},
    ]
    path = tmp_path / "satcat.csv"
    pd.DataFrame(rows).to_csv(path, index=False)

    result = read_satcat(
        path,
        shell_edges_m=[200e3, 2000e3],
        age_edges=[0, 100 * 365.25 * 86400],
        length_edges_m=[0.01, 1.0],
        area_to_mass_edges_m2_per_kg=[0.001, 0.1],
    )

    for name in ("active_counts", "derelict_counts", "debris_counts"):
        assert result[name].sum() == 0
