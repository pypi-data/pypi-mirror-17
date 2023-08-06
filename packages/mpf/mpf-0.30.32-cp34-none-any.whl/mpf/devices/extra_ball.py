"""Device that implements an extra ball."""
from mpf.core.mode_device import ModeDevice


class ExtraBall(ModeDevice):
    config_section = 'extra_balls'
    collection = 'extra_balls'
    class_label = 'extra_ball'

    def __init__(self, machine, name):
        super().__init__(machine, name)
        self.player = None

    def award(self, **kwargs):
        del kwargs
        # if there is no player active or the ball was already awareded to the player
        if not self.player or self.player.extra_balls_awarded[self.name]:
            return

        # mark as awarded
        self.player.extra_balls_awarded[self.name] = True

        self.log.debug("Awarding additional ball to player %s", self.player.number)

        self.player.extra_balls += 1

    def reset(self, **kwargs):
        del kwargs
        # if there is no player active
        if not self.player:
            return

        # reset flag
        self.player.extra_balls_awarded[self.name] = False

    def device_added_to_mode(self, mode, player):
        super().device_added_to_mode(mode, player)
        self.player = player
        if not self.player.extra_balls:
            self.player.extra_balls_awarded = dict()

        if self.name not in self.player.extra_balls_awarded:
            self.player.extra_balls_awarded[self.name] = False

    def device_removed_from_mode(self, mode):
        del mode
        self.player = None
