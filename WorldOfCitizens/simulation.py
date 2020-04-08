import os
import sys
import numpy as np

_here = os.path.dirname(__file__)
sys.path.insert(0, os.path.abspath(os.path.join(_here, '..')))
from WorldOfCitizens.log import root_logger
from WorldOfCitizens.config import Config
from WorldOfCitizens.population import initialize_population, STATE, STATE_DEAD, HEADING_X, HEADING_Y
from WorldOfCitizens.movement import update_out_of_bounds, update_headings, update_movement
from WorldOfCitizens.infection import infect, recover_or_die
from WorldOfCitizens.stat_tracker import StatTracker
from WorldOfCitizens.visualize import draw_frame

logger = root_logger


class Simulation(object):
    def __init__(self, config: Config):
        self._population = initialize_population(config)
        self._frame = 0
        self._config = config
        self._stat_tracker = StatTracker()

    @property
    def config(self):
        return self._config

    def do_step(self):
        logger.debug('Perform step')

        xbounds = np.array([[self.config.world_x_bounds[0] + 0.02, self.config.world_x_bounds[1] - 0.02]] * self.config.popuplation_size)
        ybounds = np.array([[self.config.world_y_bounds[0] + 0.02, self.config.world_y_bounds[1] - 0.02]] * self.config.popuplation_size)
        self._population = update_out_of_bounds(self._population, xbounds, ybounds)
        self._population = update_headings(self.config, self._population)
        self._population = update_movement(self.config, self._population)
        self._population = infect(self.config, self._population, self._frame)
        self._population = recover_or_die(self.config, self._population, self._frame)

        # Deads cannot move anymore
        self._population[:, HEADING_X][self._population[:, STATE] == STATE_DEAD] = 0
        self._population[:, HEADING_Y][self._population[:, STATE] == STATE_DEAD] = 0

        self._stat_tracker.update(self.config, self._population)
        draw_frame(self.config, self._population, self._stat_tracker, self._frame)

        self._frame += 1
        if self._frame == 30:
            print(self._frame)


if __name__ == '__main__':
    config = Config('woc-config.ini')

    simulation = Simulation(config)
    for step in range(1000):
        simulation.do_step()

    while (True):
        pass
