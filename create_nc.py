# Create nc-axes with dimensions and coordinates (yearly time dimension with bounds)
# Make either glacier-region axis or glacier-id axis depending if you submit regional or glacier specific results

# What unit should be used for time? CF says days since epoch
# Years since epoch could also be an option

import xarray as xr

import numpy as np
import xarray as xr

# 1) Declare axis names (these are the names of dimensions you'll use)
TIME_DIM = "time_year"  # yearly time axis
NB_BOUNDS = "nv"  # small secondary dim for bounds (size 2)
GLACIER_DIM = "glacier"

num_of_glaciers = 5  # or regions

# Make the timeseries one timestep longer for the bounds variables
epoch_date = "2000-01-01"
start_date = "1999-01-01"
end_date = "2101-01-02"  # set to 2301 if necessary

# 2) Prepare coordinate arrays / labels you want to use

# TIME
timestep = "annual"  # either "annual" or "monthly"

##  Create the numpy timeseries
epoch = np.datetime64(epoch_date, "D")
start = np.datetime64(start_date, "D")
end = np.datetime64(end_date, "D")
np_days = np.arange(start, end, dtype="datetime64[D]")

if timestep == "annual":
    # ANNUAL
    # Extract first days of each year
    dates = np_days[np_days == np_days.astype("datetime64[Y]")]

elif timestep == "monthly":
    # MONTHLY
    # Extract first days of each month
    dates = np_days[np_days == np_days.astype("datetime64[M]")]

# convert to days-since-epoch (integers)
days_since_epoch = (dates - epoch).astype("timedelta64[D]").astype(np.int64)

## ADD bounds for time
# Create bounds (time_bounds)
bounds = np.empty((len(days_since_epoch) - 2, 2), dtype=np.int64)  # One less row
bounds[:, 0] = days_since_epoch[0:-2]
bounds[:, 1] = days_since_epoch[1:-1]


# Example
n_time = 101
mass = np.linspace(10, 5, n_time)
mass_loss = np.diff(mass)
mass_loss = np.concatenate(([0], mass_loss))

ds = xr.Dataset({"mass": (["time"], mass), "mass_loss": (["time"], mass_loss), "time_bounds": (["time", "nbounds"], bounds)}, coords={"time": days_since_epoch[1:-1]})

ds["time"].attrs["units"] = "days since 1970-01-01"
ds["time"].attrs["bounds"] = "time_bounds"


ds["mass_loss"].attrs["cell_methods"] = "time: sum"
ds["mass"].attrs["cell_methods"] = "time: point"

# Save to NetCDF file
ds.to_netcdf("example.nc")

print(ds)
