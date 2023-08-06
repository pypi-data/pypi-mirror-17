"""Contains the ShowController base class."""

import logging
from queue import Queue

from mpf.core.utility_functions import Util
from mpf.assets.show import Show


class ShowController(object):
    """Manages all the shows in a pinball machine.

    'hardware shows' are coordinated light, flasher, coil, and event effects.
    The ShowController handles priorities, restores, running and stopping
    Shows, etc. There should be only one per machine.

    Args:
        machine: Parent machine object.
    """

    def __init__(self, machine):
        self.log = logging.getLogger("ShowController")
        self.machine = machine

        self.running_shows = list()
        self.registered_tick_handlers = set()
        self.current_tick_time = 0

        self.external_show_connected = False
        self.external_show_command_queue = Queue()
        """A thread-safe queue that receives BCP external show commands in
        the BCP worker
        thread. The light controller reads and processes these commands in
        the main
        thread via a tick handler.
        """
        self.running_external_show_keys = dict()
        """Dict of active external light shows that were created via BCP
        commands. This is
        useful for stopping shows later. Keys are based on the 'name'
        parameter specified
        when an external show was started, values are references to the
        external show object.
        """

        # Setup the callback schedule (every frame)
        self.machine.clock.schedule_interval(self._tick, 0)

        # Registers Show with the asset manager
        Show.initialize(self.machine)

        self.machine.events.add_handler('init_phase_3', self._initialize)

        self.machine.mode_controller.register_load_method(
            self._process_config_shows_section, 'shows')

    def _initialize(self):
        if 'shows' in self.machine.config:
            self._process_config_shows_section(self.machine.config['shows'])

    def _process_config_shows_section(self, config, **kwargs):
        # processes the shows: section of a mode or machine config
        del kwargs

        for show, settings in config.items():
            self.register_show(show, settings)

    def get_running_shows(self, name):
        """Returns a list of running shows by show name or instance name.

        Args:
            name: String name of the running shows you want to get. This can
                be a show name (which will return all running instances of that
                show) or a key (which will also return all running
                show instances that have that instance name).

        Returns:
            A list of RunningShow() objects.

        """

        return [x for x in self.running_shows if x.name == name]

    def register_show(self, name, settings):
        if name in self.machine.shows:
            raise ValueError("Show named '{}' was just registered, but "
                             "there's already a show with that name. Shows are"
                             " shared machine-wide".format(name))
        else:
            self.machine.shows[name] = Show(self.machine,
                                            name=name,
                                            data=settings,
                                            file=None)

    def unload_show_player_shows(self, removal_tuple):
        event_keys, shows = removal_tuple

        self.log.debug("Removing show_player events & stopping shows")
        self.machine.events.remove_handlers_by_keys(event_keys)

        for show in shows:
            try:
                show.stop()
            except AttributeError:
                pass

    def notify_show_starting(self, show):
        self.running_shows.append(show)
        self.running_shows.sort(key=lambda x: x.priority)

    def notify_show_stopping(self, show):
        self.running_shows.remove(show)

    def get_next_show_step(self):
        next_show_step_time = False
        for show in self.running_shows:
            if (not next_show_step_time or
                    show.next_step_time < next_show_step_time):
                next_show_step_time = show.next_step_time

        return next_show_step_time

    def register_tick_handler(self, handler):
        self.registered_tick_handlers.add(handler)

    def deregister_tick_handler(self, handler):
        if handler in self.registered_tick_handlers:
            self.registered_tick_handlers.remove(handler)

    def _tick(self, dt):
        # Runs once per machine frame. Calls the tick processing function
        # for any running shows
        # and processes any device updates and/or show actions that are needed.
        del dt
        self.current_tick_time = self.machine.clock.get_time()

        # Process the running Shows
        # for show in self.running_shows:
        #     show.tick(self.current_tick_time)

        for handler in self.registered_tick_handlers:
            handler()

    # pylint: disable-msg=too-many-arguments
    def add_external_show_start_command_to_queue(self, name, priority=0,
                                                 leds=None,
                                                 lights=None, flashers=None,
                                                 gis=None, coils=None):
        """Called by BCP worker thread when an external show start command
        is received
        via BCP.  Adds the command to a thread-safe queue where it will be
        processed
        by the main thread.

        Args:
            name: The name of the external show, used as a key for
            subsequent show commands.
            priority: Integer value of the relative priority of this show.
            leds: A list of led device names that will be used in this show.
            lights: A list of light device names that will be used in this
            show.
            flashers: A list of flasher device names that will be used in
            this show.
            gis: A list of GI device names that will be used in this show.
            coils: A list of coil device names that will be used in this show.
        """
        if not self.external_show_connected:
            self.register_tick_handler(
                self._update_external_shows)
            self.external_show_connected = True

        self.external_show_command_queue.put(
            (self._process_external_show_start_command,
             (name, priority, leds,
              lights, flashers, gis, coils)))

    def add_external_show_stop_command_to_queue(self, name):
        """Called by BCP worker thread when an external show stop command is
        received
        via BCP.  Adds the command to a thread-safe queue where it will be
        processed
        by the main thread.

        Args:
            name: The name of the external show.
        """
        self.external_show_command_queue.put(
            (self._process_external_show_stop_command, (name,)))

    # pylint: disable-msg=too-many-arguments
    def add_external_show_frame_command_to_queue(self, name, led_data=None,
                                                 light_data=None,
                                                 flasher_data=None,
                                                 gi_data=None,
                                                 coil_data=None, events=None):
        """Called by BCP worker thread when an external show frame command
        is received
        via BCP.  Adds the command to a thread-safe queue where it will be
        processed
        by the main thread.

        Args:
            name: The name of the external show.
            led_data: A string of concatenated hex color values for the leds
            in the show.
            light_data: A string of concatenated hex brightness values for
            the lights in the show.
            flasher_data: A string of concatenated pulse time (ms) values
            for the flashers in the show.
            gi_data: A string of concatenated hex brightness values for the
            GI in the show.
            coil_data: A string of concatenated coil values
            events: A comma-separated list of events to fire
        """
        self.external_show_command_queue.put(
            (self._process_external_show_frame_command,
             (name, led_data, light_data,
              flasher_data, gi_data, coil_data, events)))

    def _update_external_shows(self):
        """Processes any pending BCP external show commands.  This function
        is called
        in the main processing thread and is a tick handler function.
        """
        while not self.external_show_command_queue.empty():
            update_method, args = self.external_show_command_queue.get(False)
            update_method(*args)

    # pylint: disable-msg=too-many-arguments
    def _process_external_show_start_command(self, name, priority, leds,
                                             lights, flashers, gis, coils):
        """Processes an external show start command.  Runs in the main
        processing thread.

        Args:
            name: The name of the external show, used as a key for
            subsequent show commands.
            priority: Integer value of the relative priority of this show.
            leds: A list of led device names that will be used in this show.
            lights: A list of light device names that will be used in this
            show.
            flashers: A list of flasher device names that will be used in
            this show.
            gis: A list of GI device names that will be used in this show.
        """
        if name not in self.running_external_show_keys:
            self.running_external_show_keys[name] = ExternalShow(self.machine,
                                                                 name,
                                                                 priority,
                                                                 leds,
                                                                 lights,
                                                                 flashers, gis,
                                                                 coils)

    def _process_external_show_stop_command(self, name):
        """Processes an external show stop command.  Runs in the main
        processing thread.

        Args:
            name: The name of the external show.
        """
        try:
            self.running_external_show_keys[name].stop()
            del self.running_external_show_keys[name]
        except KeyError:
            pass

            # TODO: Would like to de-register the tick handler for external
            # shows here
            # However, since this function is called from the tick handler
            # while
            # iterating over the set of handlers, the list cannot be
            # modified at
            # this point in time.  Since this function is so quick,
            # it's probably
            # okay to leave it for now rather than figure out a complicated
            # way to
            # remove it.

            # def _process_external_show_frame_command(self, name, led_data, light_data,
            #                                          flasher_data, gi_data, coil_data,
            #                                          events):
            #     """Processes an external show frame command.  Runs in the main
            #     processing thread.
            #
            #     Args:
            #         name: The name of the external show.
            #         led_data: A string of concatenated hex color values for the leds
            #         in the show.
            #         light_data: A string of concatenated hex brightness values for
            #         the lights in the show.
            #         flasher_data: A string of concatenated pulse time (ms) values
            #         for the flashers in the show.
            #         gi_data: A string of concatenated hex brightness values for the
            #         GI in the show.
            #         coil_data: A string of concatenated coil values ????
            #         events: A comma-separated list of event names to fire immediately.
            #     """
            #     if name not in self.running_external_show_keys:
            #         return
            #
            #     if led_data:
            #         self.running_external_show_keys[name].update_leds(led_data)
            #
            #     if light_data:
            #         self.running_external_show_keys[name].update_lights(light_data)
            #
            #     if flasher_data:
            #         self.running_external_show_keys[name].update_gis(flasher_data)
            #
            #     if gi_data:
            #         self.running_external_show_keys[name].update_flashers(gi_data)
            #
            #     if coil_data:
            #         self.running_external_show_keys[name].update_coils(coil_data)
            #
            #     if events:
            #         for event in events.split(","):
            #             self.machine.show_controller._add_to_event_queue(event)


class ExternalShow(object):
    # pylint: disable-msg=too-many-arguments
    def __init__(self, machine, name, priority=0, leds=None,
                 lights=None, flashers=None, gis=None, coils=None):

        self.machine = machine
        self.name = name
        self.priority = priority
        self.name = None
        self.leds = list()
        self.lights = list()
        self.flashers = list()
        self.gis = list()
        self.coils = list()

        if leds:
            self.leds = [self.machine.leds[x] for x in
                         Util.string_to_list(leds)]

        if lights:
            self.lights = [self.machine.lights[x] for x in
                           Util.string_to_list(lights)]

        if flashers:
            self.flashers = [self.machine.flashers[x] for x in
                             Util.string_to_list(flashers)]

        if gis:
            self.gis = [self.machine.gis[x] for x in Util.string_to_list(gis)]

        if coils:
            self.coils = [self.machine.coils[x] for x in
                          Util.string_to_list(coils)]

    def stop(self):
        for led in self.leds:
            if led.cache['priority'] <= self.priority:
                led.restore()

        for light in self.lights:
            if light.cache['priority'] <= self.priority:
                light.restore()
