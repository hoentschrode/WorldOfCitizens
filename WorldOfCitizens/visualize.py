import matplotlib.pyplot as plt
import numpy as np
from WorldOfCitizens.config import Config
from WorldOfCitizens.population import X, Y, STATE, STATE_HEALTHY, STATE_SICK, STATE_DEAD, STATE_IMMUNE, DESTINATION
from WorldOfCitizens.destination import Destination
from WorldOfCitizens.stat_tracker import StatTracker


fig = plt.figure(figsize=(5, 7))
gspec = fig.add_gridspec(ncols=1, nrows=2, height_ratios=[5, 2])

map_ax = fig.add_subplot(gspec[0, 0])
chart_ax = fig.add_subplot(gspec[1, 0])


def draw_frame(config: Config, population: np.ndarray, destinations: np.ndarray, stat_tracker: StatTracker, frame: int):
    _draw_map(config, population, destinations, frame)
    _draw_chart(config, population, stat_tracker, frame)

    plt.draw()
    plt.pause(0.0000001)


def _draw_map(config: Config, population, destinations, frame):
    map_ax.clear()

    # Set axis limits every frame to avoid flickering
    map_ax.set_xlim(config.world_x_bounds[0], config.world_x_bounds[1])
    map_ax.set_ylim(config.world_y_bounds[0], config.world_y_bounds[1])
    map_ax.set_title('World map, time={}'.format(frame))

    inds = population[:, STATE] == STATE_HEALTHY
    map_ax.scatter(population[:, X][inds], population[:, Y][inds], color=config.color_healthy, s=2, label='healthy')
    inds = population[:, STATE] == STATE_IMMUNE
    map_ax.scatter(population[:, X][inds], population[:, Y][inds], color=config.color_healthy, s=2, label='healthy')

    inds = population[:, STATE] == STATE_SICK
    map_ax.scatter(population[:, X][inds], population[:, Y][inds], color=config.color_sick, s=2, label='healthy')

    inds = population[:, STATE] == STATE_DEAD
    map_ax.scatter(population[:, X][inds], population[:, Y][inds], color=config.color_dead, s=2, label='healthy')

    # Draw destinations
    if config.draw_active_destinations:
        active_destinations = np.unique(population[:, DESTINATION][population[:, DESTINATION] != 0])
        for destination_index in active_destinations:
            destination_index = int(destination_index) - 1
            x = destinations[destination_index, Destination.X.value]
            y = destinations[destination_index, Destination.Y.value]
            range_x = destinations[destination_index, Destination.WANDER_RANGE_X.value] / 2
            range_y = destinations[destination_index, Destination.WANDER_RANGE_Y.value] / 2

            col = config.color_active_destinations
            map_ax.plot([x - range_x, x + range_x], [y - range_y, y - range_y], color=col, linewidth=1)
            map_ax.plot([x + range_x, x + range_x], [y - range_y, y + range_y], color=col, linewidth=1)
            map_ax.plot([x - range_x, x + range_x], [y + range_y, y + range_y], color=col, linewidth=1)
            map_ax.plot([x - range_x, x - range_x], [y + range_y, y - range_y], color=col, linewidth=1)


def _draw_chart(config: Config, population, stat_tracker, frame):
    chart_ax.clear()

    chart_ax.set_ylim(0, config.popuplation_size + 100)
    chart_ax.set_title('Overview')

    chart_ax.plot(stat_tracker.susceptible, color=config.color_healthy, label='susceptible')
    chart_ax.plot(stat_tracker.infectious, color=config.color_sick, label='infectious')
    # chart_ax.plot(stat_tracker.fatalities, color=config.color_dead, label='fatalities')
    chart_ax.plot(stat_tracker.recovered, color='yellow', label='recovered')
    chart_ax.legend(loc='best', fontsize=6)

    pass
