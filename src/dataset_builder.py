import numpy as np
import xarray as xr


def set_time_attributes(ds, frequency, epoch, time_var="time"):

    ds[time_var].attrs["long_name"] = f"{frequency} time (days since {epoch})"

    ds[time_var].attrs["units"] = f"days since {epoch}"

    ds[time_var].attrs["calendar"] = "gregorian"

    ds[time_var].attrs["bounds"] = f"time_bounds"


def create_template_nc(
    time,
    bounds,
    frequency,
    epoch,
):

    time_var = "time"
    bounds_var = "time_bounds"

    ds = xr.Dataset(
        coords={
            time_var: time,
            "nv": [0, 1],
        },
        data_vars={
            bounds_var: (
                [time_var, "nv"],
                bounds,
            ),
        },
    )

    ds[time_var] = ds[time_var].astype("int32")
    ds[bounds_var] = ds[bounds_var].astype("int32")
    ds["nv"] = ds["nv"].astype("int8")

    set_time_attributes(ds, frequency, epoch, time_var)
    set_time_attributes(ds, frequency, epoch, bounds_var)

    # Link bounds to time
    ds[time_var].attrs["bounds"] = "time_bounds"

    return ds


def add_variable(ds, var_key, meta, time_dim):
    ds[var_key] = (
        [time_dim],
        np.zeros(len(ds[time_dim]), dtype=meta["dtype"]),
    )

    ds[var_key].attrs.update(
        {
            "long_name": meta["long_name"],
            "units": meta["units"],
            "cell_methods": f"{time_dim}: {meta['cell_method']}",
            "description": meta["description"],
        }
    )

    return ds
