# -*- coding: utf-8 -*-

from wrapperSnmp.docsisDevice import DocsisDevice
from wrapperSnmp.cmDevices import Cm
from wrapperSnmp.cmDevices import DocsIf
#import re
from wrapperSnmp.mibs import Mibs


class Cm31(Cm):

    def __init__(self, ip):
        Cm.__init__(self, ip)
        self.__deviceType = DocsisDevice.cm31()
        self.__DocsIf31 = DocsIf31(self.snmpIf)

    # method: Interfaces Docsis active in cm
    def docs_if31(self):
        return self.__DocsIf31
        
        
class DocsIf31(DocsIf):
    
    def __init__(self, snmp_if):
        DocsIf.__init__(self, snmp_if)
        self.__chOfdmFreq = {}
        self.__chOfdmPwr = {}
        self.__downOfmdAveMer = 0

    def update_ofdm_freq(self):
        oid = (Mibs.oid['docsIf31CmDsOfdmChannelPowerCenterFrequency'],)
        snmp_obj = self.snmpIf.get_table(*oid)
        if not snmp_obj:
            return None
        return list(snmp_obj.values())

    def update_ofdm_rx_pwr(self):
        oid = (Mibs.oid['docsIf31CmDsOfdmChannelPowerRxPower'],)
        snmp_obj = self.snmpIf.get_table(*oid)
        if not snmp_obj:
            return None
        return list(snmp_obj.values())
    
    def update_ofdm_ave_mer(self):
        oid = (Mibs.oid['docsPnmCmDsOfdmRxMerMean'],)
        snmp_obj = self.__snmpIf.get(*oid)
        if not snmp_obj:
            return None
        return snmp_obj[Mibs.oid['docsPnmCmDsOfdmRxMerMean']]

    
    def get_in_ofdm_octets(self):
        oid = (Mibs.oid['ifHCInOctets'] + '.' + self.__DocsIf.get_if_mac_index(),)
        snmp_obj = self.snmpIf.get(*oid)
        return snmp_obj[Mibs.oid['ifHCInOctets'] + '.' + self.__DocsIf.get_if_mac_index()]

    def get_ofdm_freq(self): return self.__chOfdmFreq

    def get_ofdm_rx_pwr(self): return self.__chOfdmPwr

    def get_ofdm_ave_mer(self): return self.__downOfdmAveMer
    
    #def update_corr_codewords31(self):
    
    #def update_uncorr_codewords31(self):
    
    #def update_unerr_codewords31(self):

    #def update_ofdm_rx_power(self):
    
    #def update_ofdm_ave_mer(self):
        