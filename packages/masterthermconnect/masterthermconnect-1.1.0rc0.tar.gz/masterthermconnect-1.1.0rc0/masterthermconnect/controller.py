"""Mastertherm Controller, for handling Mastertherm Data."""
import logging

from datetime import datetime, timedelta

from aiohttp import ClientSession

from .api import MasterthermAPI
from .const import (
    CHAR_MAP,
    DEVICE_DATA_MAP,
    DEVICE_DATA_PADMAP,
    DEVICE_INFO_MAP,
    DEVICE_SWITCH_MAP,
    PAD_MAP,
)

_LOGGER: logging.Logger = logging.getLogger(__package__)


class MasterthermController:
    """Mastertherm Integration Contoller."""

    def __init__(
        self,
        username: str,
        password: str,
        session: ClientSession,
        api_version: str = "v1",
    ) -> None:
        """Initialize the MasterthermController and connection to the web API.

        Parameters:
            username (str): The mastertherm login username
            password (str): The mastertherm login password
            session (ClientSession): An aiohttp Client Session
            api_version (str): The version of the API, mainly the host
                "v1"  : Original version, data response in varfile_mt1_config1
                "v1b" : Original version, data response in varfile_mt1_config2
                "v2"  : New version since 2022 response in varFileData

        Return:
            The MasterthermController object

        Raises:
            MasterthermUnsupportedVersion: API Version is not supported."""
        self.__api = MasterthermAPI(
            username, password, session, api_version=api_version
        )
        self.__device_map = DEVICE_DATA_MAP
        self.__inverted_map = self.__invert_device_map(self.__device_map)
        self.__api_connected = False

        # The device structure is held as a dictionary with the following format:
        # {
        #   "module_id_unit_id": {
        #       "lastDataUpdate": <datetime>,
        #       "lastInfoUpdate": <datetime>,
        #       "lastUpdateTime": "1192282722"
        #       "info": { Various Information },
        #       "data": { Normalized Data Information }
        #       "updatedData": { All Updated Data since last update },
        #       "fullData": { Full Data including last updated },
        #   }
        # }
        self.__devices = {}

    def __invert_device_map(self, device_map, key_list=None) -> dict:
        """Invert the given map and return, this is a nested method."""
        if key_list is None:
            key_list = []

        inverted_map = {}
        for key, item in device_map.items():
            new_key_list = key_list.copy()
            new_key_list.append(key)
            if not isinstance(item, dict):
                item_value = item[1]
                if isinstance(item_value, list):
                    for list_value in item_value:
                        inverted_map[list_value] = new_key_list
                else:
                    item_type = item[0]
                    if not (item_value == "" or item_type == "fixed"):
                        inverted_map[item_value] = new_key_list
            else:
                inverted_map.update(self.__invert_device_map(item, new_key_list))

        return inverted_map

    def __populate_data(self, device_map, registers) -> dict:
        """Populate the Data from the fullData and DeviceMap."""
        data = {}
        for key, item in device_map.items():
            if not isinstance(item, dict):
                item_type = item[0]
                item_value = item[1]
                if item_type == "fixed":
                    data[key] = item_value
                elif item_type == "bool":
                    if item_value == "":
                        data[key] = False
                    else:
                        data[key] = registers[item_value] == "1"
                elif item_type == "float":
                    if item_value == "":
                        data[key] = 0.0
                    else:
                        data[key] = float(registers[item_value])
                elif item_type == "int":
                    if item_value == "":
                        data[key] = 0
                    else:
                        data[key] = int(registers[item_value])
                elif item_type == "string":
                    if item_value == "":
                        data[key] = ""
                    else:
                        item_str = ""
                        for list_value in item_value:
                            item_str = item_str + CHAR_MAP[int(registers[list_value])]
                        data[key] = item_str
            else:
                data[key] = self.__populate_data(device_map[key], registers)

        return data

    def __get_pad_name(self, pad, device_key) -> str:
        """Build the Pad Name from the full data."""
        if pad not in DEVICE_DATA_PADMAP:
            return "0"

        pad_name = ""
        pad_empty = ""
        full_data = self.__devices[device_key]["fullData"]
        for key in DEVICE_DATA_PADMAP[pad]["name"][1]:
            pad_name = pad_name + CHAR_MAP[int(full_data[key])]
            pad_empty = pad_empty + "-"

        if pad_name == pad_empty:
            pad_name = "0"
        return pad_name

    def __enabled_pads(self, device_key) -> dict:
        """Enable the Pads for the devices, decoded as best as possible."""
        full_data = self.__devices[device_key]["fullData"]
        pad_info = {}

        # Pad 0 and 1 I believe are the Main Heating and Cooling circuites
        # I have heating enabled and cooling disabled but both show disabled.
        # TODO: Check what happens if I enable/ Disable what registers get updated.
        for i in range(2):
            pad_info[PAD_MAP[i]] = full_data[DEVICE_SWITCH_MAP[i]] == "1"

        # Following Code is to manage Switch Pad a to f which
        # these are various typs of circuites Water Heating/ Thermal etc.
        # TODO: see if we can identify where the types are stored.

        # Used in the process of Enabling/ Disabling Pads.
        check_code = int(full_data["I_104"])
        if check_code < 11:
            check_code = 10
        else:
            if check_code <= 200:
                check_code = 11

        # Setup and Enable Pad a to f
        for i in range(2, 8):
            pad_name = self.__get_pad_name(PAD_MAP[i], device_key)
            if pad_name != "0" and check_code >= 11:
                pad_info[PAD_MAP[i]] = full_data[DEVICE_SWITCH_MAP[i]] == "1"
            else:
                pad_info[PAD_MAP[i]] = False

        # Pad Switch 8, no idea where a name comes from so its always disabled.
        # maby its SOLAR?
        pad_name = self.__get_pad_name(PAD_MAP[8], device_key)
        pad_info[PAD_MAP[8]] = False
        if pad_name != "0":
            if check_code >= 11:
                # If any switch a to f is enabled then enable.
                for i in range(7, 1, -1):
                    if pad_info[PAD_MAP[i]]:
                        pad_info[PAD_MAP[8]] = True
                        break
            else:
                pad_info[PAD_MAP[8]] = (
                    full_data[DEVICE_SWITCH_MAP[8]] == "1"
                    and float(full_data["A_190"]) > 0.1
                )

        return pad_info

    async def connect(self, reload_modules: bool = False) -> bool:
        """Connect to the API, check the supported roles and update if required.

        Parameters:
            reload_modules (bool): Optional, default False, True to reload modules.

        Returns:
            connected (bool): True if connected Raises Error if not

        Raises:
            MasterthermConnectionError - Failed to Connect
            MasterthermAuthenticationError - Failed to Authenticate
            MasterthermUnsportedRole - Role is not supported by API"""
        result = await self.__api.connect()

        # Initialize the Dictionary.
        if not self.__devices or reload_modules:
            self.__devices = {}
            for module in result["modules"]:
                for unit in module["config"]:
                    device_id = module["id"] + "_" + str(unit["mb_addr"])

                    self.__devices[device_id] = {
                        "lastUpdateTime": "0",
                        "info": {
                            "module_id": module["id"],
                            "module_name": module["module_name"],
                            "unit_id": str(unit["mb_addr"]),
                            "unit_name": unit["mb_name"],
                        },
                        "updatedData": {},
                        "fullData": {},
                        "data": {},
                    }

        self.__api_connected = True
        return self.__api_connected

    async def refresh_info(self, override: bool = False) -> bool:
        """Refresh the information for all the devices, separated to reduce calls.
        There is a delay of 6 hours between updates to protect too many calls.

        Parameters:
            override: Optional, default False used for testing.

        Returns:
            success (bool): true if loaded

        Raises
            MasterthermConnectionError - Failed to Connect
            MasterthermAuthenticationError - Failed to Authenticate
            MasterthermUnsupportedRole - Role is not in supported roles"""
        for device in self.__devices.values():
            module_id = device["info"]["module_id"]
            unit_id = device["info"]["unit_id"]
            if "lastInfoUpdate" in device:
                last_info_update = device["lastInfoUpdate"]
            else:
                last_info_update = None

            # Refresh Device Info, this will only allow update every 6 hours to protect
            # too many requests to the new Servers as they are a little sensitive to this.
            if (
                override
                or last_info_update is None
                or datetime.now() >= last_info_update + timedelta(hours=6)
            ):
                device_info = await self.__api.get_device_info(module_id, unit_id)
                device["lastInfoUpdate"] = datetime.now()
                if device_info["returncode"] == "0":
                    for key, item in DEVICE_INFO_MAP.items():
                        if item in device_info:
                            device["info"][key] = device_info[item]

        return True

    async def refresh_data(
        self, full_load: bool = False, override: bool = False
    ) -> bool:
        """Refresh the data for all the devices, separated to reduce calls.
        There is a delay of 1 minutes allowed between data refresh calls.

        Parameters:
            full_load: Optional Force a full load of the data, defaultis false
            override: Optional, default False used for testing.

        Returns:
            success (bool): true if loaded

        Raises
            MasterthermConnectionError - Failed to Connect
            MasterthermAuthenticationError - Failed to Authenticate
            MasterthermUnsupportedRole - Role is not in supported roles"""
        for device_id, device in self.__devices.items():
            module_id = device["info"]["module_id"]
            unit_id = device["info"]["unit_id"]

            last_data_update = None
            if "lastDataUpdate" in device and not full_load:
                last_data_update = device["lastDataUpdate"]

            # Refresh Device Data, this will only allow update every 1minutes to protect
            # too many requests to the new Servers as they are a little sensitive to this.
            if (
                override
                or last_data_update is None
                or datetime.now() >= last_data_update + timedelta(minutes=1)
            ):
                device_data = await self.__api.get_device_data(
                    module_id, unit_id, last_update_time=device["lastUpdateTime"]
                )
                device["lastDataUpdate"] = datetime.now()

                # Check that we have data, sometimes nothing is returned.
                if device_data["data"]:
                    device["lastUpdateTime"] = device_data["timestamp"]
                    device["updatedData"] = device_data["data"]["varData"]["001"].copy()
                    device["fullData"].update(device["updatedData"])

                    # Refresh/ Construct Normalized Data, using device map
                    update_data = False
                    for register_key in device["updatedData"]:
                        if register_key in self.__inverted_map:
                            update_data = True
                            break

                    if update_data:
                        enabled_pads = self.__enabled_pads(device_id)
                        for pad, pad_enabled in enabled_pads.items():
                            if not pad_enabled:
                                self.__device_map["pads"].pop(pad, None)

                        device["data"] = self.__populate_data(
                            self.__device_map, device["fullData"]
                        )

        return True

    def get_devices(self) -> dict:
        """Return a List of the Devices with plus information.

        Returns:
            devices (dict): All the devices associated with the login"""
        device_return = {}
        for device_id, device in self.__devices.items():
            device_return[device_id] = device["info"]

        return device_return

    def get_device_info(self, module_id, unit_id) -> dict:
        """Get the Information for a specific device.

        Parameters:
            module_id (str): The id of the module
            unit_id (str): the id fo the unit

        Returns:
            info (dict): Device information."""
        info = {}
        key = module_id + "_" + unit_id
        if key in self.__devices:
            info = self.__devices[key]["info"]

        return info

    def get_device_registers(self, module_id, unit_id, last_updated=False) -> dict:
        """Get the Device Register Data, if lastUpdated is True then get the latest update data.

        Parameters:
            module_id (str): The id of the module
            unit_id (str): the id fo the unit
            last_updated (bool): Optional, true to return all data

        Returns:
            data (dict): Device Raw Data or Updated Data."""
        data = {}
        key = module_id + "_" + unit_id
        if key in self.__devices:
            if last_updated:
                data = self.__devices[key]["updatedData"]
            else:
                data = self.__devices[key]["fullData"]

        return data

    def get_device_data(self, module_id, unit_id) -> dict:
        """Get the Device Data, if lastUpdated is True then get the latest update data.
        Parameters:
            module_id (str): The id of the module
            unit_id (str): the id fo the unit

        Returns:
            data (dict): Device Normalised Data."""
        data = {}
        key = module_id + "_" + unit_id
        if key in self.__devices:
            data = self.__devices[key]["data"]

        return data
