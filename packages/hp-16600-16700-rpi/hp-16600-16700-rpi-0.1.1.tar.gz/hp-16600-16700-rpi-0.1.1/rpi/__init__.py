"""
HP-16600-16700-RPI

This module allows for interacting with HP / Agilent 16600A and 16700 logic analyzer main frames.
Copyright (C) 2022 Martin Miedema <git@number42.net>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import math
import shlex
import socket
from dataclasses import dataclass
from typing import Union, Optional

import pandas as pd


@dataclass
class ColumnObject:
    """Track column data"""

    name: str
    length: int
    signed: bool


@dataclass
class LabelObject:
    """Track column data"""

    name: str
    channels: str


class Rpi:
    """
    Connect and manage a HP 16600 / 16700 Logic Analyzer

    Args:
        host: A host name or IP address to connect to
        port: The port number to connect to
        timeout: Number of seconds to timeout if no response is received from the logic analyzer It's recommended to keep this value relatively high, especially loading configuration files can take a long time.
    """

    def __init__(self, host: str, port: int = 6500, timeout: int = 120):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # self.socket.connect((host, port))
        self.socket.settimeout(timeout)

    def read_until(self, string: str = "->", exclude: bool = True) -> bytes:
        """
        Read data from the RPI interface until a specific string is encountered.

        Args:
            string: A list of string service UUIDs to be discovered.
            exclude: If the string should be included with the return data or not
        Returns:
            All data received from the RPI inteface
        """
        if isinstance(string, str):
            string = string.encode()

        data = bytes()
        while True:
            tmp = self.socket.recv(1)
            if not tmp:
                continue
            data += tmp
            if data.endswith(string) and exclude:
                return data[0 : -len(string)]
            elif data.endswith(string):
                return data

    def read(self, length: int) -> bytes:
        """
        Read a specific number of bytes from the RPI interface

        Args:
            length: The amount of bytes that are expected
        Returns:
            All data received from the RPI interface
        """
        data = bytes()
        while True:
            tmp = self.socket.recv(1)
            data += tmp
            if len(data) == length:
                return data

    def send(self, data: str, newline_first: bool = True) -> None:
        """
        Send data (commands) to the RPI interface

        Args:
            data: The string that needs to be send to the RPI interface
            newline_first: If this parameter is True, a new line character will first be send and the function
                will wait for a prompt to appear. This clears the prompt of any existing data.
        """
        if newline_first:
            self.socket.sendall(b"\n")
            self.read_until("->")

        if isinstance(data, str):
            data = data.encode("ascii")

        self.socket.sendall(data)

    def get_modules(self) -> list["Analyzer"]:
        """
        Get the modules installed in the logic analyzer, returned as objects which can be used to manipulate those modules.
        Currently only Logic Analyzer modules are supported

        Returns:
            List of Logic Analyzer objects
        """
        modules = []
        self.send("modules\n")
        for module in [shlex.split(_.decode("ascii")) for _ in self.read_until("->").split(b"\n\r") if _]:
            if module[0] == "LA":
                modules.append(
                    Analyzer(
                        slot=module[1],
                        name=module[3],
                        model=module[4],
                        description=module[5],
                        parent=self,
                    )
                )
        return modules

    def get_configs(self, path: str = "/logic/configs") -> Optional[list[str]]:
        """
        List available configuration files in path

        Args:
            path: The path where configuration files can be found
        Returns:
            List of string on success or None if no configuration files are found
        """
        self.send(f"la_configs -d {path}\n")
        response = self.read_until("->")

        if response.startswith(b"There are no"):
            return None

        data = [_.decode("ascii") for _ in response.split(b"\r\n") if _]
        return data

    def get_dirs(self, path: str = "/logic/configs") -> Optional[list[str]]:
        """
        List available directories in path

        Args:
            path: The path where direcotories can be found
        Returns:
            List of string on success or None if no directories are found
        """
        self.send(f"la_configs -l {path}\n")
        response = self.read_until("->")

        if response.startswith(b"There are no"):
            return None

        data = [_.decode("ascii") for _ in response.split(b"\r\n") if _]
        return data

    def load_config(self, path: str) -> None:
        """
        Load current configuration from a file

        Args:
            path: The path to the configuration file
        """
        self.send(f"config -l {path}\n")
        response = self.read_until("->")
        if response:
            raise ValueError(response.decode("ascii"))

    def save_config(self, path, override=False) -> None:
        """
        Save the current configuration to a file

        Args:
            path: The path to the configuration file
            override: If the file will be overwritten if it already exists
        Raises:
            ValueError: Returned error description
        """
        if override:
            override = " -f"
        else:
            override = ""

        self.send(f"config -s{override} {path}\n")
        response = self.read_until("->")
        if response:
            raise ValueError(response.decode("ascii"))


class Analyzer(Rpi):
    """
    Object used to control the Logic Analyzer modules. Automatically generated and returned by Rpi.modules()
    """

    def __init__(self, slot: str, name: str, model: str, description: str, parent: "Rpi"):
        self.socket = parent.socket
        self._slot = slot
        self._name = name
        self._model = model
        self._description = description

    def start(self, rep: bool = False) -> None:
        """
        Start the logic analyzer

        Args:
            rep: Start in repetative mode, defaults to False
        Raises:
            ValueError: Returned error description
        """
        if rep:
            rep = " -rep"
        else:
            rep = ""

        self.send(f"start -n {self._name}{rep}\n")
        response = self.read_until("->")
        if response:
            raise ValueError(response.decode("ascii"))

    def stop(self) -> None:
        """
        Stop the logic analyzer
        """

        self.send(f"stop -n {self._name}\n")
        response = self.read_until("->")
        if response:
            raise ValueError(response.decode("ascii"))

    def get_status(self) -> str:
        """
        Get logic analyzer detailed status. Use analyzer.running() to just determine if the analyzer is running

        Returns:
            String with the status of the analyzer
        """

        self.send(f"status -n {self._name} -v\n")
        data = self.read_until("->").decode("ascii")
        return data.replace(f"{self._name}: ", "").strip()

    def running(self) -> bool:
        """
        Determine if the logic analyzer is running. Use analyzer.status() to get a more detailed status message

        Returns:
            True if the analyzer is in running state, otherwise False
        """

        self.send(f"status -n {self._name}\n")
        data = self.read_until("->").decode("ascii").strip()

        if data == "stopped":
            return False
        else:
            return True

    def _get_columns(self) -> list["ColumnObject"]:
        self.send(f"analyzer -n {self._name} -i\n")
        data = self.read_until("->")

        columns = []
        data = data.decode("ascii")
        for column in (_.split(('"')) for _ in data.split("\n\r") if len(_.split('"')) > 1):
            tmp = column[2].split()
            # Sanity checks
            if not tmp[1] == "bits":
                raise ValueError(f"Unsupported column type, expected type 'bits', but got type: '{tmp[1]}' ")
            if not tmp[2] in ["signed", "unsigned"]:
                raise ValueError(f"Unsupported column type, expected signed or unsigned, but got type: '{tmp[2]}' ")
            if not tmp[3] == "integer":
                raise ValueError(f"Unsupported column type, expected type 'integer', but got type: '{tmp[3]}' ")

            if tmp[2] == "signed":
                signed = True
            else:
                signed = False
            columns.append(ColumnObject(name=column[1], length=math.ceil(int(tmp[0]) / 8), signed=signed))

        return columns

    def get_listing(self) -> pd.DataFrame:
        """
        Get a listing from the logic analyzer

        Returns:
            Pandas dataframe with all data collected by the logic analyzer
        """
        columns = self._get_columns()

        self.send(f"analyzer -n {self._name} -d -l all -r all\n")

        num_states = int.from_bytes(self.socket.recv(4), byteorder="big")
        bytes_per_state = int.from_bytes(self.socket.recv(4), byteorder="big")

        states = []
        for i in range(0, num_states):
            tmp = self.read(bytes_per_state)
            state = []
            pointer = 0
            for column in columns:
                state.append(int.from_bytes(tmp[pointer : pointer + column.length], byteorder="big", signed=column.signed))
                pointer += column.length

            states.append(state)

        return pd.DataFrame(states, columns=[_.name for _ in columns])

    def get_mode(self) -> str:
        """
        Get acquisition mode, returns one of the following values:
            + stnorn *(state normal)*
            + stfast *(turbostate)*
            + tmfull *(timing full channel)*
            + tmhalf *(timing half channel)*
            + tmtrans *(transitional timing)*

        Returns:
            string with one of the above values
        """

        self.send(f"analyzer -n {self._name} -mode ?\n")
        data = self.read_until("->").decode("ascii")
        return data.strip()

    def set_mode(self, mode: str) -> None:
        """
        Get acquisition mode, the following values are accepted:
            + stnorn *(state normal)*
            + stfast *(turbostate)*
            + tmfull *(timing full channel)*
            + tmhalf *(timing half channel)*
            + tmtrans *(transitional timing)*

        Args:
            mode: string with the mode that should be set

        Example:
            analyzer.set_mode(\\"stnorn\\")

        Raises:
            ValueError: Returned error description
        """
        self.send(f"analyzer -n {self._name} -mode {mode}\n")
        response = self.read_until("->")
        if response:
            raise ValueError(response.decode("ascii"))

    def get_depth(self) -> Union[str, int]:
        """
        Get acquisition depth

        Returns:
            Either a string "minimum" / "maximum" or an integer representing n * 1000 samples
        """

        self.send(f"analyzer -n {self._name} -depth ?\n")
        data = self.read_until("->").decode("ascii")
        return data.strip()

    def set_depth(self, depth: Union[str, int]):
        """
        Set acquisition depth:
            * min (minimum)
            * max (maximum)
            * 0-100 (number of samples in thousands of states

        Args:
            depth: The depth that should be configured as either a string or integer
        Example:
            analyzer.set_depth(\\"50\\")
        Raises:
            ValueError: Returned error description
        """
        self.send(f"analyzer -n {self._name} -depth {depth}\n")
        response = self.read_until("->")
        if response:
            raise ValueError(response.decode("ascii"))

    def get_pods(self) -> str:
        """
        Get pods assigned to analyzer

        Returns:
            String with comma seperated list of modules
        """

        self.send(f"analyzer -n {self._name} -assign ?\n")
        data = self.read_until("->").decode("ascii")
        return data.strip()

    def set_pods(self, pods: str) -> None:
        """
        Set pods assigned to analyzer as comma seperated list

        Args:
            pods: comma seperated list of pods
        Example:
            analyzer.set_pods(\\"A1,A2\\")
        Raises:
            ValueError: Returned error description
        """
        self.send(f"analyzer -n {self._name} -assign {pods}\n")
        response = self.read_until("->")
        if response:
            raise ValueError(response.decode("ascii"))

    def get_trigger_position(self) -> Union[str, int]:
        """
        Get the trigger position:
            * center
            * start
            * end
            * percentage - an integer between 0 - 100 to represent the amount of data captured before trigger

        Returns:
            Either a string (center, start, end) or an integer (percentage)
        """

        self.send(f"analyzer -n {self._name} -trig position ?\n")
        data = self.read_until("->").decode("ascii").strip()

        if data.startswith("poststore,"):
            data = int(data.replace("poststore,", ""))

        return data

    def set_trigger_position(self, position: Union[str, int]) -> None:
        """
        Set the trigger position:
            * center
            * start
            * end
            * percentage - an integer between 0 - 100 to represent the amount of data captured before trigger

        Args:
            position: string or integer containing the desired trigger position
        Raises:
            ValueError: Returned error description
        """
        self.send(f"analyzer -n {self._name} -trig position {position}\n")
        response = self.read_until("->")
        if response:
            raise ValueError(response.decode("ascii"))

    def get_labels(self) -> list[str]:
        """
        Get logic analyzer labels as a list of strings

        Returns:
            List of strings with label names
        """

        self.send(f"analyzer -n {self._name} -label ?\n")
        data = [_.decode("ascii") for _ in self.read_until("->").split(b"\n") if _]
        data = [LabelObject(_.split(",")[0].strip(), _.split(",")[1].strip()) for _ in data]

        return data

    def set_label(self, name: str, channel_list: str, active_low: bool = False) -> None:
        """
        Set a logic analyser label

        Args:
            name: Name of the label
            channel_list: List of channels to use
            active_low: Set the channels to active LOW
        Raises:
            ValueError: Returned error description
        Example:
            analyzer.set_label(\\"ADDR\\", \\"A1[15:0];A2[1,3,5]\\")
        """
        if active_low:
            polarity = "-"
        else:
            polarity = "+"

        self.send(f'analyzer -n {self._name} -label {name},"{polarity}{channel_list}"\n')
        response = self.read_until("->")
        if response:
            raise ValueError(response.decode("ascii"))

    def del_label(self, name: str) -> None:
        """
        Delete logic analyser label

        Args:
            name: Name of the label, or list of labels. Specify name=\\"all\\" to delete all labels
        Raises:
            ValueError: Returned error description
        """
        if isinstance(name, str):
            name = name
        elif isinstance(name, list):
            name = ",".join(name)
        else:
            raise ValueError("name needs to be either a string or a liist")

        self.send(f"analyzer -n {self._name} -label -d {name}\n")
        response = self.read_until("->")
        if response:
            raise ValueError(response.decode("ascii"))

    def set_trigger(self, trigger: str) -> None:
        """
        Configure the logic analyzer trigger

        Args:
            trigger: See page 38-41 of the "Remote Programming Interface (RPI) for the Agilent Technologies 16700 Logic Analysis System" guide for examples
        Raises
            ValueError: Returned error description
        """

        self.send(f"analyzer -n {self._name} -trig {trigger}\n")
        response = self.read_until("->")
        if response:
            raise ValueError(response.decode("ascii"))
