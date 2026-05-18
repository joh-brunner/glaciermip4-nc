import cftime
import iris.plot as iplt
import matplotlib.pyplot as plt


def plot_cf_cubes(
    cubes,
    start_test=None,
    end=None,
    figsize=(12, 6),
    shrink_fraction=0.1,
):
    """
    Plot all cubes in a CF-aware way.

    Supported cell_methods:
        - point
        - sum

    point:
        plotted as markers

    sum:
        plotted as interval bars using time bounds
    """

    fig, ax = plt.subplots(figsize=figsize)

    colors = plt.rcParams["axes.prop_cycle"].by_key()["color"]

    for cube_idx, cube in enumerate(cubes):

        color = colors[cube_idx % len(colors)]

        # Skip bounds variables themselves
        if "bounds" in cube.name():
            continue

        # Optional slicing
        if start_test is not None:
            cube = cube[start_test:]
        if end is not None:
            cube = cube[:end]

        # Determine plotting behavior from CF cell methods
        if len(cube.cell_methods) > 0:

            method = cube.cell_methods[0].method

        else:
            ValueError("no valid cell method found")

        label = cube.var_name + " (" + method + ")"

        # -------------------------
        # POINT VARIABLES
        # -------------------------
        if method == "point":

            iplt.plot(
                cube,
                axes=ax,
                linestyle="-",
                alpha=0.3,
                color=color,
            )
            iplt.plot(
                cube,
                axes=ax,
                linestyle="",
                marker="x",
                alpha=1.0,
                color=color,
                label=label,
            )

        # -------------------------
        # SUM VARIABLES
        # -------------------------
        elif method == "sum":

            coord = cube.coord()

            bounds = coord.bounds

            if bounds is None:
                continue

            bound_datetimes = cftime.num2pydate(
                bounds,
                units=coord.units.origin,
                calendar=coord.units.calendar,
            )
            mids = []
            ys = []
            for i, b in enumerate(bound_datetimes):

                start = b[0]
                end_ = b[1]

                width = end_ - start
                shrink = shrink_fraction * width

                y = cube.data[i]

                # interval bar
                ax.plot([start + shrink, end_ - shrink], [y, y], linewidth=6, alpha=0.3, solid_capstyle="round", color=color)

                # midpoint marker
                mid = start + width / 2

                ax.plot(
                    mid,
                    y,
                    marker="o",
                    markersize=5,
                    color=color,
                    linestyle="--",
                )
                mids.append(mid)
                ys.append(y)

            # O marker for summed vars
            ax.plot(mids, ys, marker="o", linestyle="-", color=color, alpha=0.3)
            # Add dummy handle for legend
            ax.plot([], [], linewidth=6, alpha=0.3, label=label, color=color, marker="o")

    ax.legend()

    plt.show()
