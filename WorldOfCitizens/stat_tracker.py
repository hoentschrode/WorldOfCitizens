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

        self._t0 = None
        self._X0 = None

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

    def update(self, config: Config, population: np.ndarray, tick):
        self._susceptible.append(len(population[population[:, STATE] == STATE_HEALTHY]))
        self._infectious.append(len(population[population[:, STATE] == STATE_SICK]))
        self._recovered.append(len(population[population[:, STATE] == STATE_IMMUNE]))
        self._fatalities.append(len(population[population[:, STATE] == STATE_DEAD]))

        # Calculation double time number
        if self._t0 is None and len(population[population[:, STATE] == STATE_SICK]) > 0:
            self._t0 = tick
            self._X0 = len(population[population[:, STATE] == STATE_SICK])
            return

        if self._t0 is not None and len(population[population[:, STATE] == STATE_SICK]) > 0:
            mu = (np.log(len(population[population[:, STATE] == STATE_SICK])) - np.log(self._X0)) / (tick - self._t0)
            if mu != 0.0:
                td = np.log(2) / mu
                print(td)
