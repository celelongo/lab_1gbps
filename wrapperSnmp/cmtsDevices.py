# -*- coding: utf-8 -*-

from wrapperSnmp.docsisDevice import DocsisDevice
from wrapperSnmp.ipDevices import IpDevice
from wrapperSnmp.mibs import Mibs

import wrapperSnmp.private as defaults


class Cmts(IpDevice):
    """ Represents a CMTS
        
    """
    
    def __init__(self, ip):
        # inheritance from IP_device
        IpDevice.__init__(self, ip)
        # Setting SNMP community
        self.snmpIf.SnmpAttr.set_community(defaults. Communities.COMM_CMTS)
        
        # setting deviceType to CMTS type
        self.__deviceType = DocsisDevice.cmts()
        
        # cm virtual is a CM object in a CMTS
        self.cm = CmInCmts
    
    def get_cm(self, cm_mac):
        return self.cm(self.snmpIf, cm_mac)


class CmInCmts:
    """Represents a CM in a CMTS acceced via snmpIf"""        
    def __init__(self, snmp_if, cm_mac):
        self.snmpIf = snmp_if
        self.__deviceType = DocsisDevice.cm_in_cmts()
        self.__mac = cm_mac
        self.__ptr = self.get_ptr()
        self.__ip = self.get_ip()
        self.__DocsIfCmts = DocsIfCmts(self.snmpIf, self.__ptr)

    def get_docs_if_cmts(self):
        return self.__DocsIfCmts

    def get_ptr(self):
        oid = (Mibs.oid['docsIfCmtsCmPtr'] + '.' + get_mac_dec(self.__mac),)
        snmp_obj = self.snmpIf.get(*oid)
        return snmp_obj[Mibs.oid['docsIfCmtsCmPtr'] + '.' + get_mac_dec(self.__mac)]

    def get_ip(self):
        if not self.__ptr:
            return None
        oid = (Mibs.oid['docsIfCmtsCmStatusIpAddress'] + '.'+self.__ptr,)
        snmp_obj = self.snmpIf.get(*oid)
        return snmp_obj[Mibs.oid['docsIfCmtsCmStatusIpAddress'] + '.'+self.__ptr]
    
    def get_status(self):
        if not self.__ptr:
            return None
        oid = (Mibs.oid['docsIfCmtsCmStatusValue'] + '.' + self.__ptr,)
        snmp_obj = self.snmpIf.get(*oid)
        return snmp_obj[Mibs.oid['docsIfCmtsCmStatusValue'] + '.' + self.__ptr]


class DocsIfCmts:
    """Represents Docsis Interfaces in a CM in a CMTS"""
    downstream_id = "DS"
    upstream_id = "US"

    def __init__(self, snmp_if, ptr):
        self.__snmpIf = snmp_if  # Passing snmpif to access Docsis Interface
        self.__corrCodewords = {}
        self.__uncorrCodewords = {}
        self.__unerrCodewords = {}
        self.__usSnr = {}  # SNR values for all USDocsIf
        self.__usPwr = {}
        self.__ptr = ptr
        self.__usCorrCodewords = {}
        self.__usUncorrCodewords = {}
        self.__usUnerrCodewords = {}
        self.__index = []
        self.__type = {}
        self.__macIfIndex = None
        self.__chFreq = self.__update_up_ch_freq()

    def __update_up_ch_freq(self):
        ch_freq = {}
        name_oid = "docsIfUpChannelFrequency"
        oid = (Mibs.oid[name_oid],)
        snmp_obj = self.__snmpIf.get_next(*oid)
        if not snmp_obj:
            return
        dict_ch_freq = dict(snmp_obj)
        for i in dict_ch_freq:
            key_val = i.split(Mibs.oid[name_oid] + ".")[1]
            ch_freq[key_val] = dict_ch_freq[i]
        return ch_freq

    def get_ch_freq(self):
        return self.__chFreq

    def update_us_corr_codewords(self):
        # return {freq1: ccer1, freq2: ccer2, ...}
        name_oid = "docsIf3CmtsCmUsStatusCorrecteds"
        self.__usCorrCodewords = {}
        if not self.__ptr:
            return None
        oid = (Mibs.oid[name_oid] + '.' + self.__ptr,)
        snmp_obj = self.__snmpIf.get_next(*oid)

        for key in snmp_obj:
            ch = key.split(Mibs.oid[name_oid] + '.' + self.__ptr + '.')[1]
            self.__usCorrCodewords[self.__chFreq[ch]] = snmp_obj[key]
        return self.__usCorrCodewords

    def update_us_uncorr_codewords(self):
        # return {freq1: uccer1, freq2: uccer2}
        name_oid = "docsIf3CmtsCmUsStatusUncorrectables"
        self.__usUncorrCodewords = {}
        if not self.__ptr:
            return None
        oid = (Mibs.oid[name_oid] + '.' + self.__ptr,)
        snmp_obj = self.__snmpIf.get_next(*oid)

        for key in snmp_obj:
            ch = key.split(Mibs.oid[name_oid] + '.' + self.__ptr + '.')[1]
            self.__usUncorrCodewords[self.__chFreq[ch]] = snmp_obj[key]
        return self.__usUncorrCodewords

    def update_us_unerr_codewords(self):
        # return {freq1: ucer1, freq2: ucer2, ...}
        name_oid = "docsIf3CmtsCmUsStatusUnerroreds"
        self.__usUnerrCodewords = {}
        if not self.__ptr:
            return None
        oid = (Mibs.oid[name_oid] + '.' + self.__ptr,)
        snmp_obj = self.__snmpIf.get_next(*oid)

        for key in snmp_obj:
            ch = key.split(Mibs.oid[name_oid] + '.' + self.__ptr + '.')[1]
            self.__usUnerrCodewords[self.__chFreq[ch]] = snmp_obj[key]
        return self.__usUnerrCodewords

    def update_up_snr(self):
        # return {"freq1": snr1, "freq2": snr2, ...}
        name_oid = "docsIf3CmtsCmUsStatusSignalNoise"
        self.__usSnr = {}
        if not self.__ptr:
            return None
        oid = (Mibs.oid[name_oid] + '.' + self.__ptr,)
        snmp_obj = self.__snmpIf.get_next(*oid)

        for key in snmp_obj:
            ch = key.split(Mibs.oid[name_oid] + '.' + self.__ptr + '.')[1]
            self.__usSnr[self.__chFreq[ch]] = snmp_obj[key]
        return self.__usSnr

    def update_up_power(self):
        # return {"freq1": pwr1, "freq2": pwr2, ...}
        name_oid = "docsIf3CmtsCmUsStatusRxPower"
        self.__usPwr = {}
        if not self.__ptr:
            return None
        oid = (Mibs.oid[name_oid] + '.' + self.__ptr,)
        snmp_obj = self.__snmpIf.get_next(*oid)
        for key in snmp_obj:
            ch = key.split(Mibs.oid[name_oid] + '.' + self.__ptr + '.')[1]
            self.__usPwr[self.__chFreq[ch]] = snmp_obj[key]
        return self.__usPwr

    def get_us_corr_codewords(self):
        return self.__usCorrCodewords

    def get_us_uncorr_codewords(self):
        return self.__usUncorrCodewords

    def get_us_unerr_codewords(self):
        return self.__usUnerrCodewords

    def get_us_snr(self):
        return self.__usSnr


def get_mac_dec(cm_mac):
    mac_dec = str(int('0x' + cm_mac[0:2], 16)) +\
                    '.' + str(int('0x' + cm_mac[2:4], 16)) +\
                    '.' + str(int('0x' + cm_mac[4:6], 16)) +\
                    '.' + str(int('0x' + cm_mac[6:8], 16)) +\
                    '.' + str(int('0x' + cm_mac[8:10], 16)) +\
                    '.' + str(int('0x' + cm_mac[10:12], 16))
    return mac_dec
