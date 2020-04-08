import os
import configparser
from WorldOfCitizens.log import root_logger


logger = root_logger.getChild('config')


class Config(object):
    def __init__(self, filename=None):
        self._configparser = configparser.ConfigParser(
            defaults={

            }
        )
        if filename is not None and os.path.isfile(filename):
            logger.info('Loading configuration from {}'.format(filename))
            self._configparser.read(filename)

    # Population/Simulation
    # ---------------------

    @property
    def popuplation_size(self) -> int:
        return int(self._configparser.get('simulation', 'populationSize'))

    @property
    def init_avg_speed(self) -> float:
        return float(self._configparser.get('simulation', 'initAvgSpeed'))

    # Movement
    # --------

    @property
    def heading_update_probability(self) -> float:
        return float(self._configparser.get('movement', 'headingUpdateProbability'))

    @property
    def heading_multiplicator(self) -> float:
        return float(self._configparser.get('movement', 'headingMultiplicator'))

    @property
    def speed_multiplicator(self) -> float:
        return float(self._configparser.get('movement', 'speedMultiplicator'))

    # Infection
    # ---------

    @property
    def infection_range(self) -> float:
        return float(self._configparser.get('infection', 'infectionRange'))

    @property
    def infection_probability(self) -> float:
        return float(self._configparser.get('infection', 'infectionPropability'))

    @property
    def recovery_duration(self):
        rec_from = int(self._configparser.get('infection', 'recoveryDurationFrom'))
        rec_to = int(self._configparser.get('infection', 'recoveryDurationTo'))
        return (rec_from, rec_to)

    # World
    # -----

    @property
    def world_x_bounds(self):
        xbounds = [
            int(self._configparser.get('world', 'xMin')),
            int(self._configparser.get('world', 'xMax'))
        ]
        return xbounds

    @property
    def world_y_bounds(self):
        ybounds = [
            int(self._configparser.get('world', 'yMin')),
            int(self._configparser.get('world', 'yMax'))
        ]
        return ybounds

    # Visualization
    # -------------

    @property
    def map_padding(self) -> float:
        return float(self._configparser.get('visualize', 'padding'))

    @property
    def color_healthy(self) -> str:
        return self._configparser.get('visualize', 'colorHealthy')

    @property
    def color_sick(self) -> str:
        return self._configparser.get('visualize', 'colorSick')

    @property
    def color_dead(self) -> str:
        return self._configparser.get('visualize', 'colorDead')
