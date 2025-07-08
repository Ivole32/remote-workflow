"""
config.py

A file for managing the config file(s)
"""
import configparser
import os

config = configparser.ConfigParser()

config_path = r".\configuration\config.ini"

class Configuration:
    """
    The main class for handeling configurations
    """
    def __init__(self) -> None:
        from logger import Logger
        self.logger = Logger()

        self._config_options = {
            "debug-mode": True,
            "workflow-folder": r".\workflows"
        }

        self._ssh_options = {
            "ssh-user": "Username",
            "ssh-ip": "Linux Server Ip",
            "ssh-port": 22,
            "ssh-file": r".\.ssh",
            "ssh-key-name": "id_rsa"
        }

        self.logger.info("Checking for existence of config.ini")
        if not os.path.exists(config_path):
            self.logger.warn("config.ini was not found. Creating new config...")
            os.makedirs(config_path.replace(r"\config.ini", ""), exist_ok=True)

            self.__write_to_config(self._config_options, topic="config")
            self.__write_to_config(self._ssh_options, topic="SSH")
        else:
            self.logger.info("Configuration file found")
            config.read(config_path)

            self.logger.info("Checking for config completeness...")
            topic, self.__missing_options = self.__check_config_for_completeness(self._config_options, topic="config")
            if self.__missing_options:
                self.__write_to_config(self.__missing_options, topic=topic)
            
            topic, self.__missing_options = self.__check_config_for_completeness(self._ssh_options, topic="SSH")
            if self.__missing_options:
                self.__write_to_config(self.__missing_options, topic=topic)
                
            self.logger.ok("Config is complete")

    def __check_config_for_completeness(self, check_dict, topic="config") -> dict:
        """
        Check if config is not damaged
        """
        missing = {}
        if topic not in config:
            config[topic] = {}
            return topic, check_dict
            
        for key, value in check_dict.items():
            if key not in config[topic]:
                missing[key] = value

        return topic, missing

    def __write_to_config(self, options: dict, topic="config") -> None:
        """
        Takes a dict to write values to the config

        Agruments:
            options: dict
        """
        if topic not in config:
            config[topic] = {}

        for key, value in options.items():
            config[topic][key] = str(value)
            self.logger.ok(f"Wrote {key} : {value} to config.ini")

        with open(config_path, 'w') as configfile:
            config.write(configfile)
            if len(options) > 1:
                self.logger.info("Wrote everything to config.ini")

    def write_to_config(self, key: str, value: str, topic: str) -> None:
        config = {key: value}
        self.__write_to_config(config, topic=topic)

    def get_debug_mode(self) -> bool:
        """
        Gives back the debug mode

        Returns:
            bool: True if debug-mode is enabled, False when not
        """
        return config.getboolean('config', 'debug-mode')
    
    def get_config_value(self, value=None, topic="config", return_type=None) -> list:
        """
        Returns a specific value from the config

        Arguments:
            value: str (the value you want to get back)
            return_type: any (the type the return of value should be formatted)

        Returns:
            list: [If the return type is right, the value]
        """
        if return_type == None:
            return_type = str
            
        try:
            self.logger.info(f"Reading config value {value}")
            raw = config[topic][value]

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