from __future__ import annotations

import time
from typing import TYPE_CHECKING

import attr
from pyVmomi import vim
from typing_extensions import Protocol

from cloudshell.cp.vcenter.exceptions import BaseVCenterException
from cloudshell.cp.vcenter.handlers.managed_entity_handler import (
    ManagedEntityHandler,
    ManagedEntityNotFound,
)
from cloudshell.cp.vcenter.handlers.si_handler import ResourceInUse, SiHandler

if TYPE_CHECKING:
    from cloudshell.cp.vcenter.handlers.cluster_handler import HostHandler
    from cloudshell.cp.vcenter.handlers.switch_handler import AbstractSwitchHandler


class NetworkNotFound(BaseVCenterException):
    def __init__(self, entity: ManagedEntityHandler, name: str):
        self.name = name
        self.entity = entity
        super().__init__(f"Network {name} not found in {entity}")


class PortGroupNotFound(BaseVCenterException):
    MSG = ""

    def __init__(self, entity: ManagedEntityHandler | AbstractSwitchHandler, name: str):
        self.name = name
        self.entity = entity
        super().__init__(self.MSG.format(entity=entity, name=name))


class DVPortGroupNotFound(PortGroupNotFound):
    MSG = "Distributed Virtual Port Group {name} not found in {entity}"


class HostPortGroupNotFound(PortGroupNotFound):
    MSG = "Host Port Group with name {name} not found in {entity}"


class AbstractNetwork(ManagedEntityHandler):
    @property
    def _moId(self) -> str:
        # avoid using this property
        return self._entity._moId

    @property
    def _wsdl_name(self) -> str:
        return self._entity._wsdlName

    @property
    def in_use(self) -> bool:
        return bool(self._entity.vm)

    def wait_network_become_free(self, delay: int = 2, timeout: int = 30) -> bool:
        """Will wait for empty list of VMs."""
        end_time = time.time() + timeout
        while self.in_use and time.time() < end_time:
            time.sleep(delay)
        return not self.in_use

    def wait_network_disappears(self, delay: int = 2, timeout: int = 60 * 2) -> bool:
        end_time = time.time() + timeout
        while time.time() < end_time:
            try:
                _ = self.name
            except ManagedEntityNotFound:
                return True
            else:
                time.sleep(delay)
        return False


class NetworkHandler(AbstractNetwork):
    _entity: vim.Network

    def __str__(self) -> str:
        return f"Network '{self.name}'"


class AbstractPortGroupHandler(Protocol):
    @property
    def name(self) -> str:
        raise NotImplementedError

    @property
    def key(self) -> str:
        raise NotImplementedError

    @property
    def vlan_id(self) -> int:
        raise NotImplementedError

    def destroy(self):
        raise NotImplementedError


class DVPortGroupHandler(AbstractNetwork, AbstractPortGroupHandler):
    _entity: vim.dvs.DistributedVirtualPortgroup

    def __str__(self) -> str:
        return f"Distributed Virtual Port group '{self.name}'"

    @property
    def key(self) -> str:
        return self._entity.key

    @property
    def vlan_id(self) -> int:
        return self._entity.config.defaultPortConfig.vlan.vlanId

    @property
    def switch_uuid(self) -> str:
        return self._entity.config.distributedVirtualSwitch.uuid

    def destroy(self):
        try:
            self._entity.Destroy()
        except (vim.fault.NotFound, ManagedEntityNotFound):
            pass
        except vim.fault.ResourceInUse:
            raise ResourceInUse(self.name)


@attr.s(auto_attribs=True)
class HostPortGroupHandler(AbstractPortGroupHandler):
    _entity: vim.host.PortGroup
    _host: HostHandler

    def __str__(self) -> str:
        return f"Host Port Group '{self.name}'"

    @property
    def v_switch_key(self) -> str:
        return self._entity.vswitch

    @property
    def name(self) -> str:
        return self._entity.spec.name

    @property
    def key(self) -> str:
        return self._entity.key

    @property
    def vlan_id(self) -> int:
        return self._entity.spec.vlanId

    def destroy(self):
        self._host.remove_port_group(self.name)


def get_network_handler(
    net: vim.Network | vim.dvs.DistributedVirtualPortgroup, si: SiHandler
) -> NetworkHandler | DVPortGroupHandler:
    if isinstance(net, vim.dvs.DistributedVirtualPortgroup):
        return DVPortGroupHandler(net, si)
    elif isinstance(net, vim.Network):
        return NetworkHandler(net, si)
    else:
        raise NotImplementedError(f"Not supported {type(net)} as network")
