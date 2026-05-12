import numpy as np

FREQUENCY_DTYPES = {
    "annual": "datetime64[Y]",
    "monthly": "datetime64[M]",
}


def get_days_and_bounds(
    start_date,
    end_date,
    epoch_date,
    frequency,
):
    if frequency == "annual":
        start_date = offset_date(start_date, -1, 0, 0)
    elif frequency == "monthly":
        start_date = offset_date(start_date, 0, -1, 0)
    else:
        raise ValueError("Enter a valid time frequency (annual or monthly)")

    epoch = np.datetime64(epoch_date, "D")

    end = np.datetime64(end_date, "D")

    datetime_type = FREQUENCY_DTYPES[frequency]

    np_days = np.arange(
        np.datetime64(start_date, "D"),
        end,
        dtype="datetime64[D]",
    )

    dates = np_days[np_days == np_days.astype(datetime_type)]

    days_since_epoch = (dates - epoch).astype("timedelta64[D]").astype(np.int64)

    bounds = np.empty(
        (len(days_since_epoch) - 1, 2),
        dtype=np.int64,
    )

    bounds[:, 0] = days_since_epoch[:-1]
    bounds[:, 1] = days_since_epoch[1:]

    return epoch, days_since_epoch[1:], bounds


def offset_date(date, years=0, months=0, days=0):
    """
    Return a new date offset from the given date using numpy datetime arithmetic.
    """

    date = np.datetime64(date, "D")

    # Years offset
    if years != 0:
        date = (date.astype("datetime64[Y]") + years).astype("datetime64[D]")

    # Months offset
    if months != 0:
        date = (date.astype("datetime64[M]") + months).astype("datetime64[D]")

    # Days offset
    if days != 0:
        date = date + np.timedelta64(days, "D")

    return str(date)
