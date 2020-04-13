import matplotlib.pyplot as plt
import numpy as np
from WorldOfCitizens.config import Config
from WorldOfCitizens.population import X, Y, STATE, STATE_HEALTHY, STATE_SICK, STATE_DEAD, STATE_IMMUNE, DESTINATION
from WorldOfCitizens.destination import Destination
from WorldOfCitizens.stat_tracker import StatTracker


fig = plt.figure(figsize=(9, 7))
gspec = fig.add_gridspec(ncols=2, nrows=5, wspace=0.2, hspace=0.6, height_ratios=[1, 1, 1, 1, 2], width_ratios=[2, 1])

# Map
map_ax = fig.add_subplot(gspec[0:4, 0])
map_ax.set_title('World')
# - no ticks and labels
map_ax.set_xticklabels([])
map_ax.set_xticks([])
map_ax.set_yticklabels([])
map_ax.set_yticks([])

doubling_time_ax = fig.add_subplot(gspec[0, 1])

right2_ax = fig.add_subplot(gspec[1, 1])
right2_ax.set_title('$R_0$')
right3_ax = fig.add_subplot(gspec[2, 1])
right4_ax = fig.add_subplot(gspec[3, 1])

sir_ax = fig.add_subplot(gspec[4, :])
sir_ax.set_title('S/I/R')


def draw_frame(config: Config, population: np.ndarray, destinations: np.ndarray, stat_tracker: StatTracker, frame: int):
    _draw_map(config, population, destinations, frame)
    _draw_charts(config, population, stat_tracker, frame)
    _draw_doubling_time(config, stat_tracker, frame)

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
    map_ax.scatter(population[:, X][inds], population[:, Y][inds], color=config.color_healthy, s=2, label='immune')

    inds = population[:, STATE] == STATE_SICK
    map_ax.scatter(population[:, X][inds], population[:, Y][inds], color=config.color_sick, s=3, label='sick')

    inds = population[:, STATE] == STATE_DEAD
    map_ax.scatter(population[:, X][inds], population[:, Y][inds], color=config.color_dead, s=2, label='dead')

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


def _draw_charts(config: Config, population, stat_tracker, frame):
    _draw_sir_chart(config, stat_tracker, frame)
    _draw_doubling_time(config, stat_tracker, frame)


def _draw_sir_chart(config: Config, stat_tracker: StatTracker, frame: int):
    sir_ax.clear()

    sir_ax.set_ylim(0, config.popuplation_size + 100)
    sir_ax.set_title('Overview')

    sir_ax.plot(stat_tracker.susceptible, color=config.color_healthy, label='susceptible')
    sir_ax.plot(stat_tracker.infectious, color=config.color_sick, label='infectious')
    # chart_ax.plot(stat_tracker.fatalities, color=config.color_dead, label='fatalities')
    sir_ax.plot(stat_tracker.recovered, color='yellow', label='recovered')
    sir_ax.legend(loc='best', fontsize=6)

    _insert_first_infection_marker_to_axis(config, stat_tracker, sir_ax)


def _draw_doubling_time(config: Config, stat_tracker, frame):
    doubling_time_ax.clear()

    doubling_time_ax.set_title('Verdopplungszeit')
    doubling_time_ax.plot(stat_tracker.doubling_times)

    _insert_first_infection_marker_to_axis(config, stat_tracker, doubling_time_ax)


def _insert_first_infection_marker_to_axis(config: Config, stat_tracker: StatTracker, axes):
    if config.draw_first_infection_marker:
        first_infection_tick = stat_tracker.first_infection_tick
        if first_infection_tick is not None:
            axes.axvline(first_infection_tick, color=config.first_infection_marker_color, linestyle='--', linewidth=1)
