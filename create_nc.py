# GlacierMIP output following the Climate and Forecast (CF) metadata conventions

# toDo: Add more attributes to data vars
# toDo: Add defintions from csv-table as data variables
# toDo: Add glacier-id as axes for per-glacier files

import xarray as xr
import numpy as np
import subprocess

# Start the timeseries one timestep earlier for the bounds variables
# This could be improved by automatically loading the the timestep (monthly and annual) prior to the epoch date
epoch_date = "2000-01-01"
start_date_month = "1999-12-01"
start_date_year = "1999-01-01"
end_date = "2100-01-02"  # set to 2301 if necessary

check_cf = True


def main():
    # Build the timeseries
    epoch, annual_time, annual_bounds, monthly_time, monthly_bounds = init_timeseries()

    # Create an empty template nc with the timeseries axes
    ds = create_template_nc(epoch, annual_time, annual_bounds, monthly_time, monthly_bounds)
    ds.to_netcdf("template.nc", engine="netcdf4", format="NETCDF4")

    # Add some sample data to the nc
    filled_ds = add_sample_data(ds)
    filled_ds.to_netcdf("template_with_data.nc", engine="netcdf4", format="NETCDF4")

    if check_cf:
        run_cfchecker("template_with_data.nc")


def init_timeseries():
    epoch = np.datetime64(epoch_date, "D")
    end = np.datetime64(end_date, "D")

    annual_time, annual_bounds = get_days_and_bounds(start_date_year, end, epoch, "datetime64[Y]")
    monthly_time, monthly_bounds = get_days_and_bounds(start_date_month, end, epoch, "datetime64[M]")

    return epoch, annual_time, annual_bounds, monthly_time, monthly_bounds


def create_template_nc(epoch, annual_time, annual_bounds, monthly_time, monthly_bounds):

    # TEMPLATE NC
    ds = xr.Dataset(
        coords={
            "annual_time": annual_time,
            "monthly_time": monthly_time,
            "nbounds": [0, 1],
        },
        data_vars={
            "annual_time_bounds": (["annual_time", "nbounds"], annual_bounds),
            "monthly_time_bounds": (["monthly_time", "nbounds"], monthly_bounds),
        },
    )

    # Set attributes for the time axes
    set_time_attributes(ds, "annual", epoch)
    set_time_attributes(ds, "monthly", epoch)

    # Bounds need to be int32 for cfchecker
    ds["annual_time_bounds"] = ds["annual_time_bounds"].astype("int32")
    ds["monthly_time_bounds"] = ds["monthly_time_bounds"].astype("int32")

    return ds


def add_sample_data(ds):
    ds = xr.open_dataset("template.nc")

    # Example data: Annual mass balance
    n_time = 101
    annual_mass = np.linspace(10, 5, n_time)

    # Create a new variable
    ds["mass"] = (["annual_time"], annual_mass)
    # Set its attribute
    ds["mass"].attrs["cell_methods"] = "annual_time: point"

    # More example data: Monthly mass balance change
    n_time_month = 1201
    mass_month = np.linspace(10, 5, n_time_month)
    mass_change_monthly = np.diff(mass_month)
    mass_change_monthly = np.concatenate(([0], mass_change_monthly))
    ds["mass_change"] = (["monthly_time"], mass_change_monthly)
    ds["mass_change"].attrs["cell_methods"] = "monthly_time: sum"

    return ds


def get_days_and_bounds(start_date, end, epoch, datetime_type="datetime64[Y]"):
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
    ds[var].attrs["calendar"] = "gregorian"


def run_cfchecker(nc_path):
    cmd = ["cfchecks", nc_path]  # or ["cfcheck", nc_path] depending on your install

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=False)  # CF checker returns nonzero exit code on warnings/errors
    except FileNotFoundError:
        raise RuntimeError("cfchecks command not found. Try:\n" "  pip install cfchecker\n" "or check that ~/.local/bin is in your PATH.")

    print("STDOUT:\n", result.stdout)
    print("STDERR:\n", result.stderr)

    return result.stdout, result.stderr


main()
