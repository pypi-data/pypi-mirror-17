"""Contains the MachineController base class."""
import errno
import hashlib
import importlib
import logging
import os
import pickle
import tempfile

import queue
import sys
import threading
from pkg_resources import iter_entry_points

from mpf._version import __version__
from mpf.core.bcp import BCP
from mpf.core.case_insensitive_dict import CaseInsensitiveDict
from mpf.core.clock import ClockBase
from mpf.core.config_processor import ConfigProcessor
from mpf.core.config_validator import ConfigValidator
from mpf.core.data_manager import DataManager
from mpf.core.delays import DelayManager, DelayManagerRegistry
from mpf.core.device_manager import DeviceCollection
from mpf.core.events import EventManager
from mpf.core.utility_functions import Util
from mpf.modes.game.code.game import Game


# pylint: disable-msg=too-many-instance-attributes
class MachineController(object):

    """Base class for the Machine Controller object.

    The machine controller is the main entity of the entire framework. It's the
    main part that's in charge and makes things happen.

    Args:
        options: Dictionary of options the machine controller uses to configure
            itself.

    Attributes:
        options(dict): A dictionary of options built from the command line options
            used to launch mpf.py.
        config(dict): A dictionary of machine's configuration settings, merged from
            various sources.
        done(bool): Boolean. Set to True and MPF exits.
        game(Game): the current game
        machine_path: The root path of this machine_files folder
        plugins:
        scriptlets:
        hardware_platforms:
        events(EventManager):

    """

    def __init__(self, mpf_path: str, machine_path: str, options: dict):
        self.log = logging.getLogger("Machine")
        self.log.info("Mission Pinball Framework Core Engine v%s", __version__)

        self.log.debug("Command line arguments: %s", options)
        self.options = options

        self.log.debug("MPF path: %s", mpf_path)
        self.mpf_path = mpf_path

        self.log.info("Machine path: %s", machine_path)
        self.machine_path = machine_path

        self.log.debug("Command line arguments: %s", self.options)
        self.verify_system_info()

        self._boot_holds = set()
        self.register_boot_hold('init')

        self.done = False
        self.monitors = dict()
        self.plugins = list()
        self.scriptlets = list()
        self.modes = DeviceCollection(self, 'modes', None)
        self.game = None
        self.active_debugger = dict()
        self.machine_vars = CaseInsensitiveDict()
        self.machine_var_monitor = False
        self.machine_var_data_manager = None
        self.thread_stopper = threading.Event()

        self.delayRegistry = DelayManagerRegistry(self)
        self.delay = DelayManager(self.delayRegistry)

        self.crash_queue = queue.Queue()

        self.is_init_done = False
        self.config = None
        self.events = None
        self.machine_config = None
        self._set_machine_path()

        self.config_validator = ConfigValidator(self)

        self._load_config()

        self.clock = ClockBase(self.config['mpf']['hz'])
        self.log.info("Starting clock at %sHz", self.clock.max_fps)
        self.clock.schedule_interval(self._check_crash_queue, 1)
        self.configure_debugger()

        self.hardware_platforms = dict()
        self.default_platform = None

        self._load_hardware_platforms()

        self._initialize_credit_string()

        self._load_core_modules()
        # order is specified in mpfconfig.yaml

        # This is called so hw platforms have a chance to register for events,
        # and/or anything else they need to do with core modules since
        # they're not set up yet when the hw platforms are constructed.
        self._initialize_platforms()

        self._validate_config()

        self._register_config_players()
        self._register_system_events()
        self._load_machine_vars()
        self._run_init_phases()

        ConfigValidator.unload_config_spec()

        self.clear_boot_hold('init')

    @property
    def bcp_client_connected(self):
        return BCP.active_connections > 0

    def _run_init_phases(self):
        self.events.post("init_phase_1")
        '''event: init_phase_1

        desc: Posted during the initial boot up of MPF.
        '''

        self.events.process_event_queue()
        self.events.post("init_phase_2")
        '''event: init_phase_2

        desc: Posted during the initial boot up of MPF.
        '''
        self.events.process_event_queue()
        self._load_plugins()
        self.events.post("init_phase_3")
        '''event: init_phase_3

        desc: Posted during the initial boot up of MPF.
        '''
        self.events.process_event_queue()
        self._load_scriptlets()
        self.events.post("init_phase_4")
        '''event: init_phase_4

        desc: Posted during the initial boot up of MPF.
        '''
        self.events.process_event_queue()
        self.events.post("init_phase_5")
        '''event: init_phase_5

        desc: Posted during the initial boot up of MPF.
        '''
        self.events.process_event_queue()

    def _initialize_platforms(self):
        for platform in list(self.hardware_platforms.values()):
            platform.initialize()

    def _initialize_credit_string(self):
        # Do this here so there's a credit_string var even if they're not using
        # the credits mode
        try:
            credit_string = self.config['credits']['free_play_string']
        except KeyError:
            credit_string = 'FREE PLAY'

        self.create_machine_var('credits_string', credit_string, silent=True)

    def _validate_config(self):
        self.validate_machine_config_section('machine')
        self.validate_machine_config_section('hardware')
        self.validate_machine_config_section('game')

    def validate_machine_config_section(self, section):
        if section not in ConfigValidator.config_spec:
            return

        if section not in self.config:
            self.config[section] = dict()

        self.config[section] = self.config_validator.validate_config(
            section, self.config[section], section)

    def _register_system_events(self):
        self.events.add_handler('shutdown', self.power_off)
        self.events.add_handler(self.config['mpf']['switch_tag_event'].
                                replace('%', 'shutdown'), self.power_off)
        self.events.add_handler('quit', self.stop)
        self.events.add_handler(self.config['mpf']['switch_tag_event'].
                                replace('%', 'quit'), self.stop)

    def _register_config_players(self):
        # todo move this to config_player module
        for name, module in self.config['mpf']['config_players'].items():
            imported_module = importlib.import_module(module)
            setattr(self, '{}_player'.format(name),
                    imported_module.player_cls(self))

        self._register_plugin_config_players()

    def _register_plugin_config_players(self):

        self.log.debug("Registering Plugin Config Players")
        for entry_point in iter_entry_points(group='mpf.config_player',
                                             name=None):
            self.log.debug("Registering %s", entry_point)
            entry_point.load()(self)

    def _load_machine_vars(self):
        self.machine_var_data_manager = DataManager(self, 'machine_vars')

        current_time = self.clock.get_time()

        for name, settings in (
                iter(self.machine_var_data_manager.get_data().items())):

            if ('expire' in settings and settings['expire'] and
                    settings['expire'] < current_time):

                settings['value'] = 0

            self.create_machine_var(name=name, value=settings['value'])

    def _check_crash_queue(self, time):
        del time
        try:
            crash = self.crash_queue.get(block=False)
        except queue.Empty:
            pass
        else:
            print("MPF Shutting down due to child thread crash")
            print("Crash details: %s", crash)
            self.stop()

    def _set_machine_path(self):
        self.log.debug("Machine path: %s", self.machine_path)

        # Add the machine folder to sys.path so we can import modules from it
        sys.path.insert(0, self.machine_path)

    def _get_mpfcache_file_name(self):
        cache_dir = tempfile.gettempdir()
        path_hash = hashlib.md5(bytes(self.machine_path, 'UTF-8')).hexdigest()
        path_hash += '-'.join(self.options['configfile'])
        result = os.path.join(cache_dir, path_hash)
        return result

    def _load_config(self):
        if self.options['no_load_cache']:
            load_from_cache = False
        else:
            try:
                if self._get_latest_config_mod_time() > os.path.getmtime(self._get_mpfcache_file_name()):
                    load_from_cache = False  # config is newer
                else:
                    load_from_cache = True  # cache is newer

            except OSError as exception:
                if exception.errno != errno.ENOENT:
                    raise  # some unknown error?
                else:
                    load_from_cache = False  # cache file doesn't exist

        config_loaded = False
        if load_from_cache:
            config_loaded = self._load_config_from_cache()

        if not config_loaded:
            self._load_config_from_files()

    def _load_config_from_files(self):
        self.log.info("Loading config from original files")

        self.config = self._get_mpf_config()

        for num, config_file in enumerate(self.options['configfile']):

            if not (config_file.startswith('/') or
                    config_file.startswith('\\')):

                config_file = os.path.join(self.machine_path, self.config['mpf']['paths']['config'], config_file)

            self.log.info("Machine config file #%s: %s", num + 1, config_file)

            self.config = Util.dict_merge(self.config,
                                          ConfigProcessor.load_config_file(
                                              config_file,
                                              config_type='machine'))
            self.machine_config = self.config

        if self.options['create_config_cache']:
            self._cache_config()

    def _get_mpf_config(self):
        return ConfigProcessor.load_config_file(self.options['mpfconfigfile'],
                                                config_type='machine')

    def _load_config_from_cache(self):
        self.log.info("Loading cached config: %s", self._get_mpfcache_file_name())

        with open(self._get_mpfcache_file_name(), 'rb') as f:

            try:
                self.config = pickle.load(f)
                self.machine_config = self.config

            # unfortunately pickle can raise all kinds of exceptions and we dont want to crash on corrupted cache
            # pylint: disable-msg=broad-except
            except Exception:
                self.log.warning("Could not load config from cache")
                return False

            return True

    def _get_latest_config_mod_time(self):

        latest_time = os.path.getmtime(self.options['mpfconfigfile'])

        for root, dirs, files in os.walk(
                os.path.join(self.machine_path, 'config')):
            for name in files:
                if not name.startswith('.'):
                    if os.path.getmtime(os.path.join(root, name)) > latest_time:
                        latest_time = os.path.getmtime(os.path.join(root, name))

            for name in dirs:
                if not name.startswith('.'):
                    if os.path.getmtime(os.path.join(root, name)) > latest_time:
                        latest_time = os.path.getmtime(os.path.join(root, name))

        return latest_time

    def _cache_config(self):
        with open(self._get_mpfcache_file_name(), 'wb') as f:
            pickle.dump(self.config, f, protocol=4)
            self.log.info('Config file cache created: %s', self._get_mpfcache_file_name())

    def verify_system_info(self):
        """Dumps information about the Python installation to the log.

        Information includes Python version, Python executable, platform, and
        core architecture.

        """
        python_version = sys.version_info

        if not (python_version[0] == 3 and (
                python_version[1] == 4 or python_version[1] == 5)):
            raise AssertionError("Incorrect Python version. MPF requires "
                                 "Python 3.4 or 3.5. You have Python {}.{}.{}."
                                 .format(python_version[0], python_version[1],
                                         python_version[2]))

        self.log.debug("Python version: %s.%s.%s", python_version[0],
                       python_version[1], python_version[2])
        self.log.debug("Platform: %s", sys.platform)
        self.log.debug("Python executable location: %s", sys.executable)
        self.log.debug("32-bit Python? %s", sys.maxsize < 2**32)

    def _load_core_modules(self):
        self.log.debug("Loading core modules...")
        for name, module in self.config['mpf']['core_modules'].items():
            self.log.debug("Loading '%s' core module", module)
            m = Util.string_to_class(module)(self)
            setattr(self, name, m)

    def _load_hardware_platforms(self):
        if not self.options['force_platform']:
            for section, platform in self.config['hardware'].items():
                if platform.lower() != 'default' and section != 'driverboards':
                    self.add_platform(platform)
            self.set_default_platform(self.config['hardware']['platform'])

        else:
            self.add_platform(self.options['force_platform'])
            self.set_default_platform(self.options['force_platform'])

    def _load_plugins(self):
        self.log.debug("Loading plugins...")

        # TODO: This should be cleaned up. Create a Plugins base class and
        # classmethods to determine if the plugins should be used.

        for plugin in Util.string_to_list(
                self.config['mpf']['plugins']):

            self.log.debug("Loading '%s' plugin", plugin)

            plugin_obj = Util.string_to_class(plugin)(self)
            self.plugins.append(plugin_obj)

    def _load_scriptlets(self):
        if 'scriptlets' in self.config:
            self.config['scriptlets'] = self.config['scriptlets'].split(' ')

            self.log.debug("Loading scriptlets...")

            for scriptlet in self.config['scriptlets']:

                self.log.debug("Loading '%s' scriptlet", scriptlet)

                i = __import__(self.config['mpf']['paths']['scriptlets'] + '.' + scriptlet.split('.')[0], fromlist=[''])

                self.scriptlets.append(getattr(i, scriptlet.split('.')[1])
                                       (machine=self,
                                        name=scriptlet.split('.')[1]))

    def reset(self):
        """Resets the machine.

        This method is safe to call. It essentially sets up everything from
        scratch without reloading the config files and assets from disk. This
        method is called after a game ends and before attract mode begins.

        Note: This method is not yet implemented.

        """
        self.log.debug('Resetting...')
        self.events.process_event_queue()
        self.events.post('machine_reset_phase_1')
        '''Event: machine_reset_phase_1

        Desc: The first phase of resetting the machine.

        These events are posted when MPF boots (after the init_phase events are
        posted), and they're also posted subsequently when the machine is reset
        (after existing the service mode, for example).

        '''
        self.events.process_event_queue()
        self.events.post('machine_reset_phase_2')
        '''Event: machine_reset_phase_2

        Desc: The second phase of resetting the machine.

        These events are posted when MPF boots (after the init_phase events are
        posted), and they're also posted subsequently when the machine is reset
        (after existing the service mode, for example).

        '''
        self.events.process_event_queue()
        self.events.post('machine_reset_phase_3')
        '''Event: machine_reset_phase_3

        Desc: The third phase of resetting the machine.

        These events are posted when MPF boots (after the init_phase events are
        posted), and they're also posted subsequently when the machine is reset
        (after existing the service mode, for example).

        '''
        self.events.process_event_queue()
        self.log.debug('Reset Complete')
        self._reset_complete()

    def add_platform(self, name):
        """Makes an additional hardware platform interface available to MPF.

        Args:
            name: String name of the platform to add. Must match the name of a
                platform file in the mpf/platforms folder (without the .py
                extension).

        """

        if name not in self.hardware_platforms:

            try:
                hardware_platform = Util.string_to_class(self.config['mpf']['platforms'][name])
            except ImportError:
                raise ImportError("Cannot add hardware platform {}. This is "
                                  "not a valid platform name".format(name))

            self.hardware_platforms[name] = (
                hardware_platform(self))

    def set_default_platform(self, name):
        """Sets the default platform which is used if a device class-specific or
        device-specific platform is not specified. The default platform also
        controls whether a platform timer or MPF's timer is used.

        Args:
            name: String name of the platform to set to default.

        """
        try:
            self.default_platform = self.hardware_platforms[name]
            self.log.debug("Setting default platform to '%s'", name)
        except KeyError:
            self.log.error("Cannot set default platform to '%s', as that's not"
                           " a currently active platform", name)

    def register_monitor(self, monitor_class, monitor):
        """Registers a monitor.

        Args:
            monitor_class: String name of the monitor class for this monitor
                that's being registered.
            monitor: String name of the monitor.

        MPF uses monitors to allow components to monitor certain internal
        elements of MPF.

        For example, a player variable monitor could be setup to be notified of
        any changes to a player variable, or a switch monitor could be used to
        allow a plugin to be notified of any changes to any switches.

        The MachineController's list of registered monitors doesn't actually
        do anything. Rather it's a dictionary of sets which the monitors
        themselves can reference when they need to do something. We just needed
        a central registry of monitors.

        """
        if monitor_class not in self.monitors:
            self.monitors[monitor_class] = set()

        self.monitors[monitor_class].add(monitor)

    def run(self):
        """Starts the main machine run loop."""
        self.log.debug("Starting the main run loop.")

        self._run_loop()

    def stop(self):
        """Performs a graceful exit of MPF."""
        self.log.info("Shutting down...")
        self.events.post('shutdown')
        '''event: shutdown
        desc: Posted when the machine is shutting down to give all modules a
        chance to shut down gracefully.

        '''
        self.events.process_event_queue()
        self.thread_stopper.set()
        self._platform_stop()
        # todo change this to look for the shutdown event
        self.done = True

    def _run_loop(self):
        # Main machine run loop with when the default platform interface
        # specifies the MPF should control the main timer

        try:
            while not self.done:
                self.process_frame()
        except KeyboardInterrupt:
            pass

        self.stop()
        self.log_loop_rate()

    def process_frame(self):
        """Processes the current frame and ticks the clock to wait for the
        next one"""
        # TODO: Replace the function call below
        # todo should the platforms register for their own ticks?
        self.default_platform.tick(self.clock.frametime)

        # Process events before processing the clock
        self.events.process_event_queue()

        # update dt
        self.clock.tick()

        # tick before draw
        self.clock.tick_draw()

    def _platform_stop(self):
        for platform in list(self.hardware_platforms.values()):
            platform.stop()

    def power_off(self):
        """Attempts to perform a power down of the pinball machine and ends MPF.

        This method is not yet implemented.
        """
        pass

    def log_loop_rate(self):
        self.log.info("Actual MPF loop rate: %s Hz",
                      round(self.clock.get_fps(), 2))

    def bcp_reset_complete(self):
        pass

    def _reset_complete(self):
        self.log.debug('Reset Complete')
        self.events.post('reset_complete')
        '''event: reset_complete

        desc: The machine reset process is complete

        '''

    def configure_debugger(self):
        pass

    def set_machine_var(self, name, value, force_events=False):
        """Sets the value of a machine variable.

        Args:
            name: String name of the variable you're setting the value for.
            value: The value you're setting. This can be any Type.
            force_events: Boolean which will force the event posting, the
                machine monitor callback, and writing the variable to disk (if
                it's set to persist). By default these things only happen if
                the new value is different from the old value.

        """
        if name not in self.machine_vars:
            self.log.warning("Received request to set machine_var '%s', but "
                             "that is not a valid machine_var.", name)
            return

        prev_value = self.machine_vars[name]['value']
        self.machine_vars[name]['value'] = value

        try:
            change = value - prev_value
        except TypeError:
            change = prev_value != value

        if change or force_events:

            if self.machine_vars[name]['persist'] and self.config['mpf']['save_machine_vars_to_disk']:
                disk_var = CaseInsensitiveDict()
                disk_var['value'] = value

                if self.machine_vars[name]['expire_secs']:
                    disk_var['expire'] = self.clock.get_time() + self.machine_vars[name]['expire_secs']

                self.machine_var_data_manager.save_key(name, disk_var)

            self.log.debug("Setting machine_var '%s' to: %s, (prior: %s, "
                           "change: %s)", name, value, prev_value,
                           change)
            self.events.post('machine_var_' + name,
                             value=value,
                             prev_value=prev_value,
                             change=change)
            '''event: machine_var_(name)

            desc: Posted when a machine variable is added or changes value.
            (Machine variables are like player variables, except they're
            maintained machine-wide instead of per-player or per-game.)

            args:

            value: The new value of this machine variable.

            prev_value: The previous value of this machine variable, e.g. what
            it was before the current value.

            change: If the machine variable just changed, this will be the
            amount of the change. If it's not possible to determine a numeric
            change (for example, if this machine variable is a list), then this
            *change* value will be set to the boolean *True*.
            '''

            if self.machine_var_monitor:
                for callback in self.monitors['machine_vars']:
                    callback(name=name, value=value,
                             prev_value=prev_value, change=change)

    def get_machine_var(self, name):
        """Returns the value of a machine variable.

        Args:
            name: String name of the variable you want to get that value for.

        Returns:
            The value of the variable if it exists, or None if the variable
            does not exist.

        """
        try:
            return self.machine_vars[name]['value']
        except KeyError:
            return None

    def is_machine_var(self, name):
        return name in self.machine_vars

    # pylint: disable-msg=too-many-arguments
    def create_machine_var(self, name, value=0, persist=False,
                           expire_secs=None, silent=False):
        """Creates a new machine variable:

        Args:
            name: String name of the variable.
            value: The value of the variable. This can be any Type.
            persist: Boolean as to whether this variable should be saved to
                disk so it's available the next time MPF boots.
            expire_secs: Optional number of seconds you'd like this variable
                to persist on disk for. When MPF boots, if the expiration time
                of the variable is in the past, it will be loaded with a value
                of 0. For example, this lets you write the number of credits on
                the machine to disk to persist even during power off, but you
                could set it so that those only stay persisted for an hour.

        """
        var = CaseInsensitiveDict()

        var['value'] = value
        var['persist'] = persist
        var['expire_secs'] = expire_secs

        self.machine_vars[name] = var

        if not silent:
            self.set_machine_var(name, value, force_events=True)

    def remove_machine_var(self, name):
        """Removes a machine variable by name. If this variable persists to
        disk, it will remove it from there too.

        Args:
            name: String name of the variable you want to remove.

        """
        try:
            del self.machine_vars[name]
            self.machine_var_data_manager.remove_key(name)
        except KeyError:
            pass

    def remove_machine_var_search(self, startswith='', endswith=''):
        """Removes a machine variable by matching parts of its name.

        Args:
            startswith: Optional start of the variable name to match.
            endswith: Optional end of the variable name to match.

        For example, if you pass startswit='player' and endswith='score', this
        method will match and remove player1_score, player2_score, etc.

        """
        for var in list(self.machine_vars.keys()):
            if var.startswith(startswith) and var.endswith(endswith):
                del self.machine_vars[var]
                self.machine_var_data_manager.remove_key(var)

    def get_platform_sections(self, platform_section, overwrite):
        if not self.options['force_platform']:
            if not overwrite:
                if self.config['hardware'][platform_section] != 'default':
                    return self.hardware_platforms[self.config['hardware'][platform_section]]
                else:
                    return self.default_platform
            else:
                try:
                    return self.hardware_platforms[overwrite]
                except KeyError:
                    self.add_platform(overwrite)
                    return self.hardware_platforms[overwrite]
        else:
            return self.default_platform

    def register_boot_hold(self, hold):
        self._boot_holds.add(hold)

    def clear_boot_hold(self, hold):
        self._boot_holds.remove(hold)
        self.log.debug('Clearing boot hold %s. Holds remaining: %s', hold, self._boot_holds)
        if not self._boot_holds:
            self.init_done()

    def init_done(self):
        self.is_init_done = True

        self.events.post("init_done")
        '''event: init_done

        desc: Posted when the initial (one-time / boot) init phase is done. In
        other words, once this is posted, MPF is booted and ready to go.
        '''
        self.events.process_event_queue()

        ConfigValidator.unload_config_spec()
        self.reset()
