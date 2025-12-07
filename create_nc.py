# What unit should be used for time? CF says "days since epoch", but years since epoch could also be an option

# toDo: Add sample data from csv-table as variables

import xarray as xr
import numpy as np

# Start the timeseries one timestep earlier for the bounds variables
# This could be improved by automatically loading the the timestep (monthly and annual) prior to the epoch date
epoch_date = "2000-01-01"
start_date_month = "1999-12-01"
start_date_year = "1999-01-01"
end_date = "2100-01-02"  # set to 2301 if necessary,


def main():
    # Create an empty template nc with correct axes
    ds = create_template_nc()
    ds.to_netcdf("template.nc")

    # Add some sample data to the nc
    filled_ds = add_sample_data(ds)
    filled_ds.to_netcdf("template_with_data.nc")


def create_template_nc():
    # TIME
    ##  Create the numpy timeseries
    epoch = np.datetime64(epoch_date, "D")
    end = np.datetime64(end_date, "D")

    annual_time, annual_bounds = get_time_and_bounds(start_date_year, end, epoch, "datetime64[Y]")
    monthly_time, monthly_bounds = get_time_and_bounds(start_date_month, end, epoch, "datetime64[M]")

    # TEMPLATE NC
    ds = xr.Dataset(
        coords={
            "annual_time": annual_time,
            "monthly_time": monthly_time,
            "nbounds": [0, 1],
            "glacier_id": [""],
        },
        data_vars={
            "annual_time_bounds": (["annual_time", "nbounds"], annual_bounds),
            "monthly_time_bounds": (["monthly_time", "nbounds"], monthly_bounds),
        },
    )

    set_time_attributes(ds, "annual", epoch)
    set_time_attributes(ds, "monthly", epoch)

    # Save to NetCDF file
    return ds


def add_sample_data(ds):
    # Example data
    n_time = 101
    annual_mass = np.linspace(10, 5, n_time)

    n_time_month = 1201
    mass_month = np.linspace(10, 5, n_time_month)
    mass_change_monthly = np.diff(mass_month)
    mass_change_monthly = np.concatenate(([0], mass_change_monthly))

    # Add annual_mass and and mass_change_monthly to nc-file
    ds = xr.open_dataset("template.nc")

    # Add a new glacier to the dataset
    my_glacier_ids = np.array(["RGI7_123456"])
    ds.coords["glacier_id"] = my_glacier_ids

    # Find the index of the target glacier_id in the 'glacier_id' coordinate
    glacier_idx = np.where(ds.coords["glacier_id"].values == "RGI7_123456")[0][0]

    # Create a new variable
    ds["mass"] = (["glacier_id", "annual_time"], np.zeros((len(ds.coords["glacier_id"]), len(ds.coords["annual_time"]))))
    # Copy the data into the ds
    ds["mass"].values[glacier_idx, :] = annual_mass
    # Set its attribute
    ds["mass"].attrs["cell_methods"] = "time: point"

    # Create a second variable (code duplication)
    ds["mass_change"] = (["glacier_id", "monthly_time"], np.zeros((len(ds.coords["glacier_id"]), len(ds.coords["monthly_time"]))))
    ds["mass_change"].values[glacier_idx, :] = mass_change_monthly
    ds["mass_change"].attrs["cell_methods"] = "time: sum"

    return ds


def get_time_and_bounds(start_date, end, epoch, datetime_type="datetime64[Y]"):
    np_days = np.arange(np.datetime64(start_date, "D"), end, dtype="datetime64[D]")
    dates = np_days[np_days == np_days.astype(datetime_type)]

    days_since_epoch = (dates - epoch).astype("timedelta64[D]").astype(np.int64)

    bounds = np.empty((len(days_since_epoch) - 1, 2), dtype=np.int64)
    bounds[:, 0] = days_since_epoch[0:-1]
    bounds[:, 1] = days_since_epoch[1:]

    return days_since_epoch[1:], bounds


def set_time_attributes(ds, resolution, epoch):
    var = resolution + "_time"
    ds[var].attrs["long_name"] = resolution + " time (days since " + str(epoch) + ")"
    ds[var].attrs["units"] = "days since " + str(epoch)
    ds[var].attrs["bounds"] = resolution + "_time_bounds"


main()
