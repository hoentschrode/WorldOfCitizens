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
        return self._configparser.getint('simulation', 'populationSize')

    @property
    def init_avg_speed(self) -> float:
        return self._configparser.getfloat('simulation', 'initAvgSpeed')

    @property
    def log_level(self) -> str:
        return self._configparser.get('simulation', 'logLevel')

    # Movement
    # --------

    @property
    def heading_update_probability(self) -> float:
        return self._configparser.getfloat('movement', 'headingUpdateProbability')

    @property
    def heading_multiplicator(self) -> float:
        return self._configparser.getfloat('movement', 'headingMultiplicator')

    @property
    def speed_multiplicator(self) -> float:
        return self._configparser.getfloat('movement', 'speedMultiplicator')

    # Infection
    # ---------

    @property
    def infection_range(self) -> float:
        return self._configparser.getfloat('infection', 'infectionRange')

    @property
    def infection_probability(self) -> float:
        return self._configparser.getfloat('infection', 'infectionPropability')

    @property
    def recovery_duration(self):
        rec_from = self._configparser.getint('infection', 'recoveryDurationFrom')
        rec_to = self._configparser.getint('infection', 'recoveryDurationTo')
        return (rec_from, rec_to)

    @property
    def first_infection_delay_ticks(self) -> int:
        return self._configparser.getint('infection', 'firstInfectionDelayTicks')

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

    @property
    def draw_active_destinations(self) -> bool:
        return self._configparser.getboolean('visualize', 'drawActiveDestinations')

    @property
    def color_active_destinations(self) -> str:
        return self._configparser.get('visualize', 'colorActiveDestinations')

    @property
    def draw_first_infection_marker(self) -> bool:
        return self._configparser.getboolean('visualize', 'drawFirstInfectionMarker')

    @property
    def first_infection_marker_color(self) -> str:
        return self._configparser.get('visualize', 'firstInfectionMarkerColor')
