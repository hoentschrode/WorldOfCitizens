import os
import sys
import numpy as np

_here = os.path.dirname(__file__)
sys.path.insert(0, os.path.abspath(os.path.join(_here, '..')))
from WorldOfCitizens.log import root_logger
from WorldOfCitizens.config import Config
from WorldOfCitizens.population import initialize_population, STATE, STATE_DEAD, HEADING_X, HEADING_Y, DESTINATION, DESTINATION_ARRIVED
from WorldOfCitizens.destination import initialize_destinations, go_to_location, update_heading_to_destination, update_at_destination, stay_at_destination
from WorldOfCitizens.movement import update_out_of_bounds, update_headings, update_movement
from WorldOfCitizens.infection import infect, recover_or_die
from WorldOfCitizens.stat_tracker import StatTracker
from WorldOfCitizens.visualize import draw_frame

logger = root_logger


class Simulation(object):
    def __init__(self, config: Config):
        self._population = initialize_population(config)
        self._destinations = initialize_destinations(config)
        self._frame = 0
        self._config = config
        self._stat_tracker = StatTracker()

        logger.setLevel(self.config.log_level)

    @property
    def config(self):
        return self._config

    def do_step(self):
        logger.debug('Perform step')

        # Check for destinations in use
        have_active_destinations = len(self._population[self._population[:, DESTINATION] != 0]) > 0
        if have_active_destinations:
            update_at_destination(self._population, self._destinations)
            update_heading_to_destination(self._population, self._destinations)
            stay_at_destination(self._population, self._destinations)

        # Check world boundaries
        xbounds = np.array([[self.config.world_x_bounds[0] + 0.02, self.config.world_x_bounds[1] - 0.02]] * self.config.popuplation_size)
        ybounds = np.array([[self.config.world_y_bounds[0] + 0.02, self.config.world_y_bounds[1] - 0.02]] * self.config.popuplation_size)
        update_out_of_bounds(self._population, xbounds, ybounds)
        update_headings(self.config, self._population)
        update_movement(self.config, self._population)
        infect(self.config, self._population, self._frame)
        recover_or_die(self.config, self._population, self._frame)

        # Deads cannot move anymore
        self._population[:, HEADING_X][self._population[:, STATE] == STATE_DEAD] = 0
        self._population[:, HEADING_Y][self._population[:, STATE] == STATE_DEAD] = 0

        self._stat_tracker.update(self.config, self._population, self._frame)
        draw_frame(self.config, self._population, self._destinations, self._stat_tracker, self._frame)

        self._frame += 1
        """
        if self._frame == 60:
            update = np.random.random(size=(self._config.popuplation_size))
            shp = update[update < 0.5].shape
            self._population[:, DESTINATION][update < 0.5] = 2
            self._population[:, DESTINATION_ARRIVED][update < 0.5] = 0

            self._population[:, DESTINATION][update >= 0.5] = 3
            self._population[:, DESTINATION_ARRIVED][update > 0.5] = 0
        """


if __name__ == '__main__':
    config = Config('woc-config.ini')

    simulation = Simulation(config)
    for step in range(1000):
        simulation.do_step()

    while (True):
        pass
