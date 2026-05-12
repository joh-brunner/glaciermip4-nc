import numpy as np
import xarray as xr


def set_time_attributes(ds, frequency, epoch):

    time_var = f"{frequency}_time"

    ds[time_var].attrs["long_name"] = (
        f"{frequency} time (days since {epoch})"
    )

    ds[time_var].attrs["units"] = (
        f"days since {epoch}"
    )

    ds[time_var].attrs["bounds"] = (
        f"{frequency}_time_bounds"
    )

    ds[time_var].attrs["calendar"] = "gregorian"


def create_template_nc(
    time,
    bounds,
    frequency,
    epoch,
):

    time_var = f"{frequency}_time"

    bounds_var = f"{frequency}_time_bounds"

    ds = xr.Dataset(
        coords={
            time_var: time,
            "nbounds": [0, 1],
        },
        data_vars={
            bounds_var: (
                [time_var, "nbounds"],
                bounds,
            ),
        },
    )

    ds[bounds_var] = ds[bounds_var].astype("int32")

    set_time_attributes(ds, frequency, epoch)

    return ds

def add_variable(ds, var_key, meta, time_dim):
    ds[var_key] = (
        [time_dim],
        np.zeros(len(ds[time_dim]), dtype=meta["dtype"]),
    )

    ds[var_key].attrs.update({
        "long_name": meta["long_name"],
        "units": meta["units"],
        "cell_methods": f"{time_dim}: {meta['cell_method']}",
        "description": meta["description"],
    })

    return ds