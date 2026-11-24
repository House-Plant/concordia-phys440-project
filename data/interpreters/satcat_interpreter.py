import numpy as np
import pandas as pd


def read_satcat(
    path,
    shell_edges_m,
    age_edges,
    length_edges_m,
    area_to_mass_edges_m2_per_kg,
    reference_date="2026-11-24",
):
    reference_date = pd.Timestamp(reference_date)
    shell_edges_m = np.asarray(shell_edges_m, dtype=float)
    age_edges = np.asarray(age_edges, dtype=float)
    length_edges_m = np.asarray(length_edges_m, dtype=float)
    area_to_mass_edges_m2_per_kg = np.asarray(area_to_mass_edges_m2_per_kg, dtype=float)
    debris_length_m = 0.1
    debris_area_to_mass_m2_per_kg = 0.01

    data = pd.read_csv(path, parse_dates=["LAUNCH_DATE", "DECAY_DATE"])
    data = data.loc[
        data["ORBIT_CENTER"].eq("EA")
        & data["ORBIT_TYPE"].eq("ORB")
        & data["DECAY_DATE"].isna()
        & data["LAUNCH_DATE"].le(reference_date)
    ].dropna(subset=["APOGEE", "PERIGEE"])
    data["altitude_m"] = (data["APOGEE"] + data["PERIGEE"]) * 500
    data["age_s"] = (reference_date - data["LAUNCH_DATE"]).dt.total_seconds()
    data["age_s"] = data["age_s"].clip(upper=np.nextafter(age_edges[-1], 0))

    payloads = data["OBJECT_TYPE"].eq("PAY")
    active = data["OPS_STATUS_CODE"].isin(["+", "P", "B", "S", "X"])

    def satellite_counts(mask):
        return np.histogram2d(
            data.loc[mask, "altitude_m"],
            data.loc[mask, "age_s"],
            bins=[shell_edges_m, age_edges],
        )[0].astype(int)

    debris = data.loc[~payloads]
    debris_counts = np.histogramdd(
        (
            debris["altitude_m"],
            np.full(len(debris), debris_length_m),
            np.full(len(debris), debris_area_to_mass_m2_per_kg),
        ),
        bins=[shell_edges_m, length_edges_m, area_to_mass_edges_m2_per_kg],
    )[0].astype(int)

    return {
        "shell_edges_m": shell_edges_m,
        "age_edges": age_edges,
        "length_edges_m": length_edges_m,
        "area_to_mass_edges_m2_per_kg": area_to_mass_edges_m2_per_kg,
        "active_counts": satellite_counts(payloads & active),
        "derelict_counts": satellite_counts(payloads & ~active),
        "debris_counts": debris_counts,
    }
