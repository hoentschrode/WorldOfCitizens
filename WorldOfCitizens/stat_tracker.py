import numpy as np
from WorldOfCitizens.config import Config
from WorldOfCitizens.population import STATE, STATE_SICK, STATE_IMMUNE, STATE_DEAD, STATE_HEALTHY


class StatTracker(object):
    def __init__(self):
        # Initialize the counters
        self._susceptible = []
        self._infectious = []
        self._recovered = []
        self._fatalities = []

    @property
    def susceptible(self):
        return self._susceptible

    @property
    def infectious(self):
        return self._infectious

    @property
    def recovered(self):
        return self._recovered

    @property
    def fatalities(self):
        return self._fatalities

    def update(self, config: Config, population: np.ndarray):
        self._susceptible.append(len(population[population[:, STATE] == STATE_HEALTHY]))
        self._infectious.append(len(population[population[:, STATE] == STATE_SICK]))
        self._recovered.append(len(population[population[:, STATE] == STATE_IMMUNE]))
        self._fatalities.append(len(population[population[:, STATE] == STATE_DEAD]))
