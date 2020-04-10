from enum import Enum, unique
import numpy as np
from WorldOfCitizens.config import Config
from WorldOfCitizens.population import DESTINATION, DESTINATION_ARRIVED, X, Y, HEADING_X, HEADING_Y, SPEED
from WorldOfCitizens.movement import update_out_of_bounds


@unique
class Destination(Enum):
    X = 0
    Y = 1
    WANDER_RANGE_X = 2
    WANDER_RANGE_Y = 3


def initialize_destinations(config: Config):
    destinations = np.zeros((3, 4))

    # Center
    destinations[0][Destination.X.value] = (config.world_x_bounds[1] - config.world_x_bounds[0]) / 2
    destinations[0][Destination.Y.value] = (config.world_y_bounds[1] - config.world_y_bounds[0]) / 2
    destinations[0][Destination.WANDER_RANGE_X.value] = 0.1
    destinations[0][Destination.WANDER_RANGE_Y.value] = 0.1

    # Left top
    destinations[1][Destination.WANDER_RANGE_X.value] = 0.1
    destinations[1][Destination.WANDER_RANGE_Y.value] = 0.1
    destinations[1][Destination.X.value] = 0 + 0.1
    destinations[1][Destination.Y.value] = 0 + 0.1

    # Right bottom
    destinations[2][Destination.WANDER_RANGE_X.value] = 0.1
    destinations[2][Destination.WANDER_RANGE_Y.value] = 0.1
    destinations[2][Destination.X.value] = config.world_x_bounds[1] - 0.1
    destinations[2][Destination.Y.value] = config.world_y_bounds[1] - 0.1

    return destinations


def go_to_location(patient, destination_index):
    """
    Sends patient to destination
    """
    patient[DESTINATION] = destination_index
    patient[DESTINATION_ARRIVED] = 0


def update_heading_to_destination(population, destinations):
    active_destinations = np.unique(population[:, DESTINATION][population[:, DESTINATION] != 0])
    for destination_index in active_destinations:
        destination_index = int(destination_index) - 1
        x = destinations[destination_index, Destination.X.value]
        y = destinations[destination_index, Destination.Y.value]

        citizen_index = (population[:, DESTINATION] == (destination_index + 1)) & (population[:, DESTINATION_ARRIVED] == 0)
        population[:, HEADING_X][citizen_index] = x - population[:, X][citizen_index]
        population[:, HEADING_Y][citizen_index] = y - population[:, Y][citizen_index]

    return population


def update_at_destination(population, destinations):
    """
    Check if citizen arrived at destination
    """
    active_destinations = np.unique(population[:, DESTINATION][population[:, DESTINATION] != 0])
    for destination_index in active_destinations:
        destination_index = int(destination_index) - 1
        x = destinations[destination_index, Destination.X.value]
        y = destinations[destination_index, Destination.Y.value]
        range_x = destinations[destination_index, Destination.WANDER_RANGE_X.value] / 2
        range_y = destinations[destination_index, Destination.WANDER_RANGE_Y.value] / 2

        arrivals_index = (population[:, DESTINATION_ARRIVED] == 0) & \
            (population[:, DESTINATION] == destination_index + 1) & \
            (population[:, X] >= x - range_x) & \
            (population[:, X] <= x + range_x) & \
            (population[:, Y] >= y - range_y) & \
            (population[:, Y] <= y + range_y)
        population[:, DESTINATION_ARRIVED][arrivals_index] = 1

    return population


def stay_at_destination(population, destinations):
    """
    Ensure that citizens who arrived at destination will stay in perimeter
    """
    active_destinations = np.unique(population[:, DESTINATION][population[:, DESTINATION] != 0])
    for destination_index in active_destinations:
        destination_index = int(destination_index) - 1
        x = destinations[destination_index, Destination.X.value]
        y = destinations[destination_index, Destination.Y.value]
        range_x = destinations[destination_index, Destination.WANDER_RANGE_X.value] / 2
        range_y = destinations[destination_index, Destination.WANDER_RANGE_Y.value] / 2

        arrivals_index = (population[:, DESTINATION_ARRIVED] == 1) & (population[:, DESTINATION] == destination_index + 1)
        number_of_arrived = len(population[arrivals_index])
        if number_of_arrived > 0:
            xbounds = np.array([[x - range_x, x + range_x]] * number_of_arrived)
            ybounds = np.array([[y - range_y, y + range_y]] * number_of_arrived)
            population[arrivals_index] = update_out_of_bounds(population[arrivals_index], xbounds, ybounds)
    return population
