#!/bin/python3.4

import wrapperSnmp.defaults as defaults
from wrapperSnmp.snmp import get_snmp, get_next_snmp, get_table_snmp, set_snmp


class SnmpIf:
    def __init__(self, ip_mgmt):
        self.__ipMgmt = ip_mgmt
        self.SnmpAttr = SnmpAttr()

    def get(self, *objnames):
        return get_snmp(self.__ipMgmt, self.SnmpAttr, *objnames)

    def get_next(self, *objnames):
        return get_next_snmp(self.__ipMgmt, self.SnmpAttr, *objnames)

    def get_table(self, *objnames):
        return get_table_snmp(self.__ipMgmt, self.SnmpAttr, *objnames)

    def set(self, *objnames):
        return set_snmp(self.__ipMgmt, self.SnmpAttr, *objnames)


class SnmpAttr:
    def __init__(self):
        self.COMMUNITY = defaults.Snmp.SNMP_COMMUNITY
        self.TIMEOUT = defaults.Snmp.SNMP_TIMEOUT
        self.RETRIES = defaults.Snmp.SNMP_RETRIES
        self.BULKCOUNT = defaults.Snmp.SNMP_BULKCOUNT
        self.IgnoreNonIncreasingOid = defaults.Snmp.SNMP_ignoreNonIncreasingOid
        self.LookupMib = defaults.Snmp.SNMP_lookupMib
        self.PORT = defaults.Snmp.SNMP_PORT
        self.MAXROWS = defaults.Snmp.MAX_ROWS

    def get_community(self):
        return self.COMMUNITY

    def get_timeout(self):
        return self.TIMEOUT

    def get_retries(self):
        return self.RETRIES

    def get_bulkcount(self):
        return self.BULKCOUNT

    def get_ignorenonincreasingoid(self):
        return self.IgnoreNonIncreasingOid

    def get_lookupmib(self):
        return self.LookupMib

    def get_port(self):
        return self.PORT

    def get_maxrows(self):
        return self.MAXROWS
    
    def set_community(self, comm):
        self.COMMUNITY = comm

    def set_timeout(self, timeout):
        self.TIMEOUT = timeout

    def set_retries(self, retries):
        self.RETRIES = retries

    def set_bulkcount(self, bulkcount):
        self.BULKCOUNT = bulkcount

    def set_ignorenonincreasingoid(self):
        self.IgnoreNonIncreasingOid = True

    def unset_ignorenonincreasingoid(self):
        self.IgnoreNonIncreasingOid = False

    def set_lookupmib(self):
        self.LookupMib = True

    def unset_lookupmib(self):
        self.LookupMib = False

    def set_port(self, port):
        self.PORT = port

    def set_maxrows(self, maxrows):
        self.MAXROWS = maxrows
