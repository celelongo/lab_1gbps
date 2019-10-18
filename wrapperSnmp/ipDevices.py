#!/bin/python3.4

from wrapperSnmp.snmpIf import SnmpIf


class IpDevice:
    __id = 0
    """Represents a Generic IP Device"""
    def __init__(self, ip_mngmt):
        
        # Device Ip management
        self.__ipMngmt = ip_mngmt
        
        # Information About the device i.e., SysDescr, Model, Firmware, etc
        self.__about = None
        
        # Id ti identify each IP device
        self.__id = IpDevice.__id

        IpDevice.__id += 1

        # SNMP InterFace used to get all the infomation about the device
        self.snmpIf = SnmpIf(self.__ipMngmt)
        
        # Later could be possible to add more interfaces like ssh, telnet, tr-069 within a class
        # ...
        # self.sshIf
        # self.telnetIf
        # self.tr069If
