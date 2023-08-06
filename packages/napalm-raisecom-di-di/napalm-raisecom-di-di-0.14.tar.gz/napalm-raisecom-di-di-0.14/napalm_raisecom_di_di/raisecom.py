"""NAPALM driver for Raisecom"""

from raisecom_netmiko.raisecom import RaisecomDriver
from napalm.base import NetworkDriver
from dcim.models import Device



class NapalmRaisecomDriver(NetworkDriver):
    platform = 'raisecom_di_di'

    def __init__(self, hostname, username, password, timeout, optional_args):
        self.device = RaisecomDriver(hostname, username, password)
        self.hostname = hostname

    def open(self):
        pass

    def close(self):
        pass

    def get_facts(self):
        facts = self.device.get_facts()

        # print(facts)

        list_mask = ['/24', '/0', '/32', '/30', '/29', '/28']

        select_device = None
        for mask in list_mask:
            hostname = self.hostname + mask
            select_device = Device.objects.filter(primary_ip4__address=hostname)
            # print(select_device, hostname)
            if select_device:
                break

        select_device = select_device[0]

        if facts['serial_number'] != select_device.serial:
            facts['serial_number'] += '  !!!Отличается от указанного серийного номера в нетбоксе!!!'

        return facts

    def get_environment(self):
        pass
        # return self.device.get_environment()

    def get_lldp_neighbors_detail(self):
        lldp = self.device.get_lldp_neighbors_detail()
        print(lldp)
        for key in lldp:
            for i in range(len(lldp[key])):
                lldp[key][i]['remote_system_name'] = lldp[key][i]['remote_system_name'].replace('.', '_')
        print(lldp)
        return lldp

    def get_interfaces(self):
        return self.device.get_interfaces()

    def get_config(self):
        return self.device.get_config()
