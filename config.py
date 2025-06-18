"""
config.py

A file for managing the config file(s)
"""
#from logger import Logger
import configparser
import os

#logger = Logger()
config = configparser.ConfigParser()

class Configuration:
    """
    The main class for handeling configurations
    """
    def __init__(self) -> None:
        self._config_options = {
            "debug-mode": "True"
        }

        if not os.path.exists("config.ini"):
            config['config'] = {}
            self.__write_to_config(self._config_options)
        else:
            config.read("config.ini")
            self.__missing_options = self.__check_config_for_completeness()
            if self.__missing_options:
                self.__write_to_config(self.__missing_options)

    def __check_config_for_completeness(self) -> dict:
        missing = {}
        if 'config' not in config:
            config['config'] = {}
            return self._config_options
            
        for key, value in self._config_options.items():
            if key not in config['config']:
                missing[key] = value

        return missing

    def __write_to_config(self, options: dict):
        if 'config' not in config:
            config['config'] = {}

        for key, value in options.items():
            config['config'][key] = str(value)

        with open('config.ini', 'w') as configfile:
            config.write(configfile)

    def get_debug_mode(self) -> bool:
        """
        Gives back the debug mode

        Returns:
            bool: True if debug-mode is enabled, False when not
        """
        return config.getboolean('config', 'debug-mode')