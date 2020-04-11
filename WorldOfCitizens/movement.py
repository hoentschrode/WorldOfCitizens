import numpy as np
from WorldOfCitizens.config import Config
from WorldOfCitizens.population import X, Y, HEADING_Y, HEADING_X, SPEED


def update_out_of_bounds(population, xbounds, ybounds):
    # Check x lower boundary
    shp = population[:, HEADING_X][
        (population[:, X] <= xbounds[:, 0]) & (population[:, HEADING_X] < 0)
    ].shape
    population[:, HEADING_X][
        (population[:, X] < xbounds[:, 0]) & (population[:, HEADING_X] < 0)
    ] = np.clip(
        np.random.normal(
            loc=0.5,
            scale=0.5 / 3,
            size=shp
        ),
        a_min=0.05,
        a_max=1
    )

    # Check x upper boundary
    shp = population[:, HEADING_X][
        (population[:, X] >= xbounds[:, 1]) & (population[:, HEADING_X] > 0)
    ].shape
    population[:, HEADING_X][
        (population[:, X] >= xbounds[:, 1]) & (population[:, HEADING_X] > 0)
    ] = np.clip(
        -np.random.normal(
            loc=0.5,
            scale=0.5 / 3,
            size=shp
        ),
        a_min=-1,
        a_max=-0.05
    )

    # Check y lower boundary
    shp = population[:, HEADING_Y][
        (population[:, Y] <= ybounds[:, 0]) & (population[:, HEADING_Y] < 0)
    ].shape
    population[:, HEADING_Y][
        (population[:, Y] <= ybounds[:, 0]) & (population[:, HEADING_Y] < 0)
    ] = np.clip(
        np.random.normal(
            loc=0.5,
            scale=0.5 / 3,
            size=shp
        ),
        a_min=0.05,
        a_max=1
    )

    # Check y upper boundary
    shp = population[:, HEADING_Y][
        (population[:, Y] >= ybounds[:, 1]) & (population[:, HEADING_Y] > 0)
    ].shape
    population[:, HEADING_Y][
        (population[:, Y] >= ybounds[:, 1]) & (population[:, HEADING_Y] > 0)
    ] = np.clip(
        -np.random.normal(
            loc=0.5,
            scale=0.5 / 3,
            size=shp
        ),
        a_min=-1,
        a_max=-0.05
    )


def update_headings(config: Config, population):
    # Update heading x
    update = np.random.random(size=(config.popuplation_size,))
    shp = update[update <= config.heading_update_probability].shape
    population[:, HEADING_X][update < config.heading_update_probability] = np.random.normal(
        loc=0,
        scale=1 / 3,
        size=shp
    ) * config.heading_multiplicator

    # Update heading y
    update = np.random.random(size=(config.popuplation_size))
    shp = update[update <= config.heading_update_probability].shape
    population[:, HEADING_Y][update < config.heading_update_probability] = np.random.normal(
        loc=0,
        scale=1 / 3,
        size=shp
    ) * config.heading_multiplicator

    update = np.random.random(size=(config.popuplation_size,))
    shp = update[update <= config.heading_update_probability].shape
    population[:, SPEED][update <= config.heading_update_probability] = np.random.normal(
        loc=config.init_avg_speed,
        scale=config.init_avg_speed / 3,
        size=shp
    ) * config.speed_multiplicator


def update_movement(config: Config, population):
    population[:, X] = population[:, X] + (population[:, HEADING_X] * population[:, SPEED])
    population[:, Y] = population[:, Y] + (population[:, HEADING_Y] * population[:, SPEED])
    # return population
