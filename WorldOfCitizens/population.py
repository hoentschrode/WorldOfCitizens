import numpy as np
from WorldOfCitizens.log import root_logger
from WorldOfCitizens.config import Config


# Keys
ID = 0
X = 1
Y = 2
HEADING_X = 3
HEADING_Y = 4
SPEED = 5
STATE = 6
INFECTED_SINCE = 7
RECOVERY_DURATION = 8
DESTINATION = 9             # Destionation: 0:randomly moving around (wander), >1:Index of destionation matrix
DESTINATION_ARRIVED = 10    # 0:No, 1:Arrived at destination (switch to wandering here)
WANDER_RANGE_X = 11         # x-range of wandering when reached a destination
WANDER_RANGE_Y = 12         # y-range of wandering when reached a destination

# Valid state values
STATE_HEALTHY = 0
STATE_SICK = 1
STATE_IMMUNE = 2
STATE_DEAD = 3
STATE_IMMUNDE_BUT_INFECTIOUS = 4

# Destination
DESTINATION_WANDERING = 0


logger = root_logger.getChild('population')


def initialize_population(config: Config) -> np.ndarray:
    logger.info('Initialize population, popSize={}'.format(config.popuplation_size))

    population = np.zeros((config.popuplation_size, 13))

    # Create id's
    logger.debug('Apply ids')
    population[:, ID] = [id for id in range(config.popuplation_size)]

    # Random positions
    logger.debug('Apply random positions')
    population[:, X] = np.random.uniform(
        low=config.world_x_bounds[0] + config.map_padding,
        high=config.world_x_bounds[1] - config.map_padding,
        size=config.popuplation_size
    )
    population[:, Y] = np.random.uniform(
        low=config.world_y_bounds[0] + config.map_padding,
        high=config.world_y_bounds[1] - config.map_padding,
        size=config.popuplation_size
    )

    # Random headings -1/1
    logger.debug('Apply random headings')
    population[:, HEADING_X] = np.random.normal(
        loc=0,
        scale=1 / 3,
        size=(config.popuplation_size,)
    )
    population[:, HEADING_Y] = np.random.normal(
        loc=0,
        scale=1 / 3,
        size=(config.popuplation_size,)
    )

    # Random speed
    logger.debug('Apply random speed')
    population[:, SPEED] = np.random.normal(
        loc=config.init_avg_speed,
        scale=config.init_avg_speed / 3
    )

    logger.debug('Apply random recovery vector')
    population[:, RECOVERY_DURATION] = int(np.random.uniform(
        low=config.recovery_duration[0],
        high=config.recovery_duration[1]
    ))

    # All alive
    population[:, STATE] = STATE_HEALTHY

    # No destinations, wandering mod
    population[:, DESTINATION] = 0
    population[:, WANDER_RANGE_X] = 0.01
    population[:, WANDER_RANGE_Y] = 0.01

    return population
