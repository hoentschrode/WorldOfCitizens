import numpy as np
from WorldOfCitizens.config import Config
from WorldOfCitizens.population import ID, X, Y, STATE, RECOVERY_DURATION, STATE_HEALTHY, STATE_SICK, INFECTED_SINCE, STATE_DEAD, STATE_IMMUNE, HEADING_X, HEADING_Y, SPEED


def infect(config: Config, population, frame: int):

    if frame == 20:
        id = int(np.random.uniform(low=0, high=config.popuplation_size))
        population[:, STATE][population[:, ID] == id] = STATE_SICK
        population[:, RECOVERY_DURATION][population[:, ID] == id] = int(np.random.uniform(low=config.recovery_duration[0], high=config.recovery_duration[1]))
        population[:, INFECTED_SINCE][population[:, ID] == id] = frame
        return population

    infectious = population[population[:, STATE] == STATE_SICK]
    for patient in infectious:
        infection_zone = [
            patient[X] - config.infection_range,
            patient[Y] - config.infection_range,
            patient[X] + config.infection_range,
            patient[Y] + config.infection_range
        ]
        # Find healthy people inside infection zone
        healthy_ids = _find_nearby_ids(population, infection_zone, STATE_HEALTHY)
        for ind in healthy_ids:
            if np.random.random() < config.infection_range:
                population[ind][STATE] = STATE_SICK
                population[ind][RECOVERY_DURATION] = int(np.random.uniform(low=config.recovery_duration[0], high=config.recovery_duration[1]))
                population[ind][INFECTED_SINCE] = frame

    return population


def recover_or_die(config: Config, population, frame: int):
    infected = population[population[:, STATE] == STATE_SICK]

    infected[:, RECOVERY_DURATION] = infected[:, RECOVERY_DURATION] - 1
    infection_done_ids = infected[:, ID][infected[:, RECOVERY_DURATION] == 0]
    for id in infection_done_ids:
        mortality_chance = 0.2
        if np.random.random() <= mortality_chance:
            # Die
            infected[:, STATE][infected[:, ID] == id] = STATE_DEAD
        else:
            # Recover
            infected[:, STATE][infected[:, ID] == id] = STATE_IMMUNE
    population[population[:, STATE] == STATE_SICK] = infected
    return population


def _find_nearby_ids(population, zone, state):
    inds = np.int32(
        population[:, ID][
            (population[:, STATE] == state) &
            (population[:, X] > zone[0]) &
            (population[:, Y] > zone[1]) &
            (population[:, X] < zone[2]) &
            (population[:, Y] < zone[3])
        ]
    )
    return inds
