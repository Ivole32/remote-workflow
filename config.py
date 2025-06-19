"""
config.py

A file for managing the config file(s)
"""
import configparser
import os

config = configparser.ConfigParser()

class Configuration:
    """
    The main class for handeling configurations
    """
    def __init__(self) -> None:
        from logger import Logger
        self.logger = Logger(debug_mode=True)

        self._config_options = {
            "debug-mode": True,
            "ssh-user": "Username",
            "ssh-ip": "Linux Server Ip",
            "ssh-port": 22,
            "ssh-file": r".\.ssh",
            "ssh-key-name": "id_rsa" 
        }

        self.logger.info("Checking for existence of config.ini")
        if not os.path.exists("config.ini"):
            self.logger.warn("config.ini was not found. Creating new config...")
            config['config'] = {}
            self.__write_to_config(self._config_options)
        else:
            self.logger.info("Configuration file found")
            config.read("config.ini")
            self.logger.info("Checking for config completeness...")
            self.__missing_options = self.__check_config_for_completeness()
            if self.__missing_options:
                self.__write_to_config(self.__missing_options)
            self.logger.ok("Config is complete")

        self.logger = Logger(debug_mode=self.get_debug_mode())

    def __check_config_for_completeness(self) -> dict:
        """
        Check if config is not damaged
        """
        missing = {}
        if 'config' not in config:
            config['config'] = {}
            return self._config_options
            
        for key, value in self._config_options.items():
            if key not in config['config']:
                missing[key] = value

        return missing

    def __write_to_config(self, options: dict) -> None:
        """
        Takes a dict to write values to the config

        Agruments:
            options: dict
        """
        if 'config' not in config:
            config['config'] = {}

        for key, value in options.items():
            config['config'][key] = str(value)
            self.logger.ok(f"Wrote {key} : {value} to config.ini")

        with open('config.ini', 'w') as configfile:
            config.write(configfile)
            self.logger.info("Wrote everything to config.ini")

    def get_debug_mode(self) -> bool:
        """
        Gives back the debug mode

        Returns:
            bool: True if debug-mode is enabled, False when not
        """
        return config.getboolean('config', 'debug-mode')
    
    def get_config_value(self, value=None, return_type=None) -> list:
        if return_type == None:
            return_type = str
            
        try:
            self.logger.info(f"Reading config value {value}")
            raw = config['config'][value]

            if return_type:
                try:
                    raw = return_type(raw)
                except Exception as convert_error:
                    self.logger.warn(f"Could not convert '{value}' to {return_type}: {convert_error}")
                    return [False, raw]

            self.logger.ok(f"Returning {raw} in the requested type")
            return [True, raw]

        except Exception as e:
            self.logger.error(f"Error while reading {value}: {e}")
            return [None, None]

if __name__ == "__main__":
    configuration = Configuration()
    configuration.get_config_value(value="ssh-port", return_type=int)