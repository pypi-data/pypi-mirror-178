import toml
import logging
import binascii

from .Strings import *

DEFAULT_LOGGING_LEVEL=logging.DEBUG


class TomlConfig:
    """
    provided to read in a toml config file and store
    data into a dictionary

    WARNING: Validity of entries in config.toml is not checked

    """

    config=None

    def __init__(self,configFile,logging_level=DEFAULT_LOGGING_LEVEL):
        """
        Load the config data from file

        This is never written back to by this program
        """
        self.logger=logging.getLogger("Config")
        self.logger.setLevel(logging_level)

        try:
            self.config=toml.load(configFile)

        except Exception as e:
            self.logger.error(f"config load error {e}")

    def getConfig(self):
        """
        returns the config dictionary

        Use to simplify access to user settings

        e.g.

        A=TomlConfig()
        Retries=A.["LoraWan"]["Retries"]

        """

        def convert_address(address):
            return list(binascii.unhexlify(address))

        for auth_mode in [AUTH_OTAA, AUTH_ABP]:
            for item in [APPKEY, APPEUI, DEVEUI]:
                value=self.config[TTN][auth_mode][item]
                if isinstance(value, str):
                    value=convert_address(value)
                self.config[TTN][auth_mode][item]=value

        return self.config


class LoRaWANAuthentication:
    """
    Represents a pure-Python configuration object for LoRaWAN authentication.
    """

    def __init__(self, auth_mode=None, devaddr=None, nwskey=None, appskey=None, deveui=None, appeui=None, appkey=None):

        # Authentication mode (ABP or OTAA)
        self.auth_mode = auth_mode

        # ABP
        self.devaddr = devaddr
        self.nwskey = nwskey
        self.appskey = appskey

        # OTAA
        self.deveui = deveui
        self.appeui = appeui
        self.appkey = appkey


class LoRaWANConfig:
    """
    Represents a pure-Python configuration object for LoRaWAN.
    """
    def __init__(self, auth: LoRaWANAuthentication=None, spreading_factor=7, max_power=0x0F, output_power=0x0E, sync_word=0x34, rx_crc=True, fcount_filename=".lora_fcount"):

        if auth.auth_mode.upper() == "ABP":
            self.auth = AUTH_ABP
            self.devaddr = self._convert_address(auth.devaddr)
            self.nwskey = self._convert_address(auth.nwskey)
            self.appskey = self._convert_address(auth.appskey)

        elif auth.auth_mode.upper() == "OTAA":
            self.auth = AUTH_OTAA
            self.deveui = self._convert_address(auth.deveui)
            self.appeui = self._convert_address(auth.appeui)
            self.appkey = self._convert_address(auth.appkey)

        self.spreading_factor = spreading_factor
        self.max_power = max_power
        self.output_power = output_power
        self.sync_word = sync_word
        self.rx_crc = rx_crc
        self.fcount_filename = fcount_filename

    def _convert_address(self, address):
        return list(binascii.unhexlify(address))
