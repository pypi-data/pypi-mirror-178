from __future__ import annotations

from abc import abstractmethod
from typing import TYPE_CHECKING

from pyVmomi import vim

from cloudshell.cp.vcenter.exceptions import BaseVCenterException
from cloudshell.cp.vcenter.handlers.datastore_handler import DatastoreHandler
from cloudshell.cp.vcenter.handlers.managed_entity_handler import (
    ManagedEntityHandler,
    ManagedEntityNotFound,
)
from cloudshell.cp.vcenter.handlers.network_handler import HostPortGroupHandler
from cloudshell.cp.vcenter.handlers.resource_pool import ResourcePoolHandler
from cloudshell.cp.vcenter.handlers.si_handler import ResourceInUse
from cloudshell.cp.vcenter.handlers.switch_handler import (
    VSwitchHandler,
    VSwitchNotFound,
)
from cloudshell.cp.vcenter.handlers.vcenter_path import VcenterPath
from cloudshell.cp.vcenter.utils.units_converter import (
    BASE_10,
    BASE_SI,
    PREFIX_MB,
    PREFIX_MHZ,
    UsageInfo,
    format_bytes,
    format_hertz,
)

if TYPE_CHECKING:
    from cloudshell.cp.vcenter.handlers.dc_handler import DcHandler


class ClusterNotFound(BaseVCenterException):
    def __init__(self, dc: DcHandler, name: str):
        self.dc = dc
        self.name = name
        super().__init__(f"Cluster with name '{name}' not found in the {dc}")


class HostNotFound(BaseVCenterException):
    def __init__(self, cluster: ClusterHandler, name: str):
        self.cluster = cluster
        self.name = name
        super().__init__(f"Host with name '{name}' not found in the {cluster}")


class BasicComputeEntityHandler(ManagedEntityHandler):
    @property
    def datastores(self) -> list[DatastoreHandler]:
        return [DatastoreHandler(store, self._si) for store in self._entity.datastore]

    @property
    @abstractmethod
    def cpu_usage(self) -> UsageInfo:
        ...

    @property
    @abstractmethod
    def ram_usage(self) -> UsageInfo:
        ...

    @abstractmethod
    def get_v_switch(self, name: str) -> VSwitchHandler:
        ...


class ClusterHandler(BasicComputeEntityHandler):
    _entity: vim.ComputeResource | vim.ClusterComputeResource

    def __str__(self) -> str:
        return f"Cluster '{self.name}'"

    @property
    def cpu_usage(self) -> UsageInfo:
        usage = self._entity.GetResourceUsage()
        capacity = usage.cpuCapacityMHz
        used = usage.cpuUsedMHz
        return UsageInfo(
            capacity=format_hertz(capacity, prefix=PREFIX_MHZ),
            used=format_hertz(used, prefix=PREFIX_MHZ),
            free=format_hertz(capacity - used, prefix=PREFIX_MHZ),
            used_percentage=str(round(used / capacity * 100)),
        )

    @property
    def ram_usage(self) -> UsageInfo:
        usage = self._entity.GetResourceUsage()
        capacity = usage.memCapacityMB
        used = usage.memUsedMB
        return UsageInfo(
            capacity=format_bytes(capacity, prefix=PREFIX_MB),
            used=format_bytes(used, prefix=PREFIX_MB),
            free=format_bytes(capacity - used, prefix=PREFIX_MB),
            used_percentage=str(round(used / capacity * 100)),
        )

    @property
    def hosts(self) -> list[HostHandler]:
        return [HostHandler(host, self._si) for host in self._entity.host]

    def get_host(self, name: str) -> HostHandler:
        for host in self.hosts:
            if host.name == name:
                return host
        raise HostNotFound(self, name)

    def get_resource_pool(self, path: str | None) -> ResourcePoolHandler:
        rp = ResourcePoolHandler(self._entity.resourcePool, self._si)
        for name in VcenterPath(path or ""):
            rp = rp.get_resource_pool(name)
        return rp

    def get_v_switch(self, name: str) -> VSwitchHandler:
        for host in self.hosts:
            try:
                v_switch = host.get_v_switch(name)
            except VSwitchNotFound:
                pass
            else:
                return v_switch
        raise VSwitchNotFound(self, name)


class HostHandler(BasicComputeEntityHandler):
    _entity: vim.HostSystem

    def __str__(self) -> str:
        return f"Host '{self.name}'"

    @property
    def cluster(self) -> ClusterHandler:
        return ClusterHandler(self._entity.parent, self._si)

    @property
    def cpu_usage(self) -> UsageInfo:
        used = self._entity.summary.quickStats.overallCpuUsage * BASE_SI * BASE_SI
        capacity = (
            self._entity.hardware.cpuInfo.hz * self._entity.hardware.cpuInfo.numCpuCores
        )
        return UsageInfo(
            capacity=format_hertz(capacity),
            used=format_hertz(used),
            free=format_hertz(capacity - used),
            used_percentage=str(round(used / capacity * 100)),
        )

    @property
    def ram_usage(self) -> UsageInfo:
        used = self._entity.summary.quickStats.overallMemoryUsage * BASE_10 * BASE_10
        capacity = self._entity.hardware.memorySize
        return UsageInfo(
            capacity=format_bytes(capacity),
            used=format_bytes(used),
            free=format_bytes(capacity, used),
            used_percentage=str(round(used / capacity * 100)),
        )

    @property
    def port_groups(self) -> list[HostPortGroupHandler]:
        return [
            HostPortGroupHandler(pg, self)
            for pg in self._entity.config.network.portgroup
        ]

    def get_resource_pool(self, path: str | None) -> ResourcePoolHandler:
        return self.cluster.get_resource_pool(path)

    def get_v_switch(self, name: str) -> VSwitchHandler:
        for v_switch in self._entity.config.network.vswitch:
            if v_switch.name == name:
                return VSwitchHandler(v_switch, self)
        raise VSwitchNotFound(self, name)

    def remove_port_group(self, name: str):
        try:
            self._entity.configManager.networkSystem.RemovePortGroup(name)
        except (vim.fault.NotFound, ManagedEntityNotFound):
            pass
        except vim.fault.ResourceInUse:
            raise ResourceInUse(name)

    def add_port_group(self, port_group_spec):
        self._entity.configManager.networkSystem.AddPortGroup(port_group_spec)
