"""Event Config Player."""
from mpf.core.delays import DelayManager

from mpf.core.config_player import ConfigPlayer
from mpf.core.utility_functions import Util


class EventPlayer(ConfigPlayer):

    """Posts events based on config."""

    config_file_section = 'event_player'
    show_section = 'events'
    device_collection = None

    def __init__(self, machine):
        """Initialise EventPlayer."""
        super().__init__(machine)
        self.delay = DelayManager(self.machine.delayRegistry)

    def play(self, settings, context, priority=0, **kwargs):
        """Post (delayed) events."""

        for event, s in settings.items():
            s.update(kwargs)
            if ':' in event:
                event, delay = event.split(":")
                delay = Util.string_to_ms(delay)
                self.delay.add(callback=self._post_event, ms=delay, event=event, s=s)
            else:
                self.machine.events.post(event, **s)

    def _post_event(self, event, s):
        self.machine.events.post(event, **s)

    def get_express_config(self, value):
        """Parse short config."""
        return_dict = dict()
        return_dict[value] = dict()
        return return_dict

    def validate_config(self, config):
        """Validate the config.

        Override because we want to let events just be a list of events.
        """
        new_config = dict()

        for event, settings in config.items():
            if isinstance(settings, dict):
                # dicts are fine
                new_config[event] = settings

                # just check that all values are dicts again
                for event1, args in settings.items():
                    if not isinstance(args, dict):
                        raise AssertionError("Invalid args {}:{} in {} event_player".format(event, settings, event1))
            elif isinstance(settings, str):
                # convert str to list and then to dict
                new_config[event] = dict()

                for event1 in Util.string_to_list(settings):
                    new_config[event][event1] = dict()
            elif isinstance(settings, list):
                # convert list to dict
                new_config[event] = dict()

                for event1 in settings:
                    new_config[event][event1] = dict()
            else:
                raise AssertionError("Invalid entry {}:{} in event_player".format(event, settings))

        super().validate_config(new_config)

        return new_config

player_cls = EventPlayer
