import yaml

from src.timeseries import get_days_and_bounds
from src.dataset_builder import (
    create_template_nc,
    add_variable,
)


def create_glaciermip_dataset(
    frequency,
    start_date,
    end_date,
    epoch_date,
    variable_yml,
):
    """
    Create an empty GlacierMIP-style CF dataset.
    """

    # ---------------------------------
    # Build time axis
    # ---------------------------------

    epoch, time, bounds = get_days_and_bounds(
        start_date=start_date,
        end_date=end_date,
        epoch_date=epoch_date,
        frequency=frequency,
    )

    # ---------------------------------
    # Create template dataset
    # ---------------------------------

    ds = create_template_nc(
        time=time,
        bounds=bounds,
        frequency=frequency,
        epoch=epoch,
    )

    # ---------------------------------
    # Load variable metadata
    # ---------------------------------

    with open(variable_yml, "r") as f:

        vars_meta = yaml.safe_load(f)["variables"][frequency]

    # ---------------------------------
    # Add variables
    # ---------------------------------

    for var_key, meta in vars_meta.items():

        ds = add_variable(
            ds,
            var_key,
            meta=meta,
            time_dim="time",
        )

    return ds