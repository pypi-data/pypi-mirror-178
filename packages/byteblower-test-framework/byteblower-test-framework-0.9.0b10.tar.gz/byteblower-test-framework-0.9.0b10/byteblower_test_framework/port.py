"""ByteBlower Port interface module."""
import logging
from abc import ABC, abstractmethod, abstractproperty
from ipaddress import IPv4Address, IPv4Network, IPv6Address, IPv6Network
from typing import Dict, List, Optional, Sequence, Union  # for type hinting

from byteblowerll.byteblower import (  # for type hinting
    ByteBlowerPort,
    EthernetConfiguration,
    Layer3Configuration,
)

from .server import Server  # for type hinting

_MAC_FORMAT = "{BYTE0:02x}:{BYTE1:02x}:{BYTE2:02x}" \
    ":{BYTE3:02x}:{BYTE4:02x}:{BYTE5:02x}"


class _MacGenerator(object):
    """Mac generator helper class."""

    __slots__ = ('_prefix', )

    _start = 1

    def __init__(self):
        self._prefix = [0x00, 0xFF, 0x0A]

    def generate_mac(self):
        result = _MAC_FORMAT.format(
            BYTE0=self._prefix[0],
            BYTE1=self._prefix[1],
            BYTE2=self._prefix[2],
            BYTE3=(int(_MacGenerator._start / (256 * 256))) % 256,
            BYTE4=int((_MacGenerator._start / (256))) % 256,
            BYTE5=_MacGenerator._start % 256,
        )
        _MacGenerator._start += 1
        return result


class Port(ABC):
    """ByteBlower Port interface."""

    __slots__ = (
        '_server',
        '_interface',
        '_bb_port',
        '_port_l2',
        '_port_l3',
        '_conf',
        '_tags',
        '_name',
    )

    _number = 1
    _mac_generator = _MacGenerator()

    def __init__(
        self,
        server: Server,
        interface: str = None,
        mac: Optional[str] = None,
        name: Optional[str] = None,
        tags: Optional[Sequence[str]] = None,
        **kwargs,
    ) -> None:
        """
        Initialize a ByteBlowerPort.

        .. note::
           L2 is *only* configured if:

           1. Explicitly given MAC address
           2. Layer 3 is configured

           A port without L2/L3 configuration can for example be used
           for pure 'promiscuous' capturing of data.
        """
        self._server = server
        self._interface = interface

        self._bb_port: ByteBlowerPort = None
        self._port_l2: EthernetConfiguration = None
        self._port_l3: Layer3Configuration = None
        self._conf: Dict[str, Union[str, IPv4Address, IPv6Address]] = {}
        self._tags: List[str] = []

        if name is not None:
            self._name = name
        else:
            self._name = 'Port ' + str(Port._number)

        if kwargs:
            logging.error('Unsupported keyword arguments for %r on %r: %r',
                          self._name, self._interface, [
                              '{}={!r}'.format(key, value)
                              for key, value in kwargs.items()
                          ])
            raise ValueError(
                'Unsupported configuration parameters for {!r} on {!r}: {!r}'.
                format(self._name, self._interface, [key for key in kwargs]))

        if self._interface is None:
            raise ValueError(
                'Missing interface name for ByteBlower Port {!r}'.format(
                    self._name))

        if mac is not None:
            self._conf['mac'] = mac

        if tags is not None:
            for tag in tags:
                self.add_tag(tag)

        Port._number += 1

    def _configure(self):
        self._bb_port = self._server.bb_server.PortCreate(self._interface)

        mac_addr = self._conf.get('mac')
        if mac_addr is not None:
            logging.info('Setting MAC to %r', mac_addr)
            try:
                self._configure_L2(mac_addr)
            except Exception:
                logging.exception(
                    'Failed to set MAC of ByteBlower port: value: %r.'
                    ' Fall-back to auto-generated MAC address.', mac_addr)
                self._configure_L2_mac()

        self._port_l3 = self._configure_L3()
        logging.debug(self._bb_port.DescriptionGet())

    def _configure_L2(self, mac_addr: Optional[str] = None) -> None:
        # Check if Layer 2 is already configured on this port
        if self._port_l2 is None:
            self._port_l2 = self._bb_port.Layer2EthIISet()
            self._configure_L2_mac(mac_addr=mac_addr)

    def _configure_L2_mac(self, mac_addr: Optional[str] = None) -> None:
        """Configure L2 MAC address.

        .. note::
           Use at base Port only!
           Forces generating and setting MAC when configuration
           with user-provided MAC address fails.

        :param mac_addr:
           If given, configure that MAC address, defaults to None
        :type mac_addr: Optional[str], optional
        """
        if mac_addr is None:
            mac_addr = Port._mac_generator.generate_mac()
        self._port_l2.MacSet(mac_addr)

    @abstractmethod
    def _configure_L3(self) -> Layer3Configuration:
        pass

    def __del__(self) -> None:
        # self.server.bb_server.PortDestroy(self._bb_port)
        logging.debug("Should destroy port")

    @property
    def mac(self) -> str:
        return self._port_l2.MacGet()

    @abstractproperty
    def failed(self) -> bool:
        """Return whether (IP) address configuration failed."""
        pass

    @abstractproperty
    def ip(self) -> Union[IPv4Address, IPv6Address]:
        """
        Return the *preferred* IP address.

        .. note::
           Subject to change in dual stack implementations.
        """
        pass

    @abstractproperty
    def network(self) -> Union[IPv4Network, IPv6Network]:
        """
        Return the network of the *preferred* IP address.

        .. note::
           Subject to change in dual stack implementations.
        """
        pass

    @abstractproperty
    def gateway(self) -> Union[IPv4Address, IPv6Address]:
        """
        Return the default gateway.

        .. note::
           Subject to change in dual stack implementations.
        """
        pass

    @property
    def is_natted(self) -> bool:
        """
        Return whether this port is behind a NAT gateway.

        .. note::
           Hook function for extending Port implementations.
        """
        return False

    @property
    def server(self) -> Server:
        return self._server

    @property
    def bb_port(self) -> ByteBlowerPort:
        return self._bb_port

    @property
    def layer3(self) -> Layer3Configuration:
        """
        Layer 3 configuration of the ByteBlower Lower Layer API.

        .. note::
           Subject to change in dual stack implementations.
        """
        return self._port_l3

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, new_name: str) -> None:
        self._name = new_name

    @property
    def tags(self) -> Sequence[str]:
        return self._tags

    def add_tag(self, new_tag: str) -> None:
        new_tag = new_tag.lower()
        if new_tag not in self._tags:
            self._tags.append(new_tag)

    @property
    def port_type(self) -> str:
        return "Wired"
