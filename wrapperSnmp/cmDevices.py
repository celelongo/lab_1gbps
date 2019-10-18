# -*- coding: utf-8 -*-

from wrapperSnmp.docsisDevice import DocsisDevice
from wrapperSnmp.ipDevices import IpDevice
from wrapperSnmp.mibs import Mibs
import re
import wrapperSnmp.private as defaults


class Cm(IpDevice):
    """Represents a CM"""

    # initialization based on cm IPv4
    def __init__(self, ip):
        # Inheritancee from class IP_device
        IpDevice.__init__(self, ip)
        self.__hw_rev = None
        self.__vendor = None
        self.__bootr = None
        self.__sw_rev = None
        self.__model = None

        # Setting device type to "CM"
        self.__deviceType = DocsisDevice.cm()

        # Setting the snmp cm community
        self.snmpIf.SnmpAttr.set_community(defaults.Communities.COMM_CM)
        # Pass to DocsisIf the snmpIf used to get all the data
        self.__DocsIf = DocsIf(self.snmpIf)
        self.__fbc = FullbandCapture(self.snmpIf)
        self.update_sysdescr()

    # method: Interfaces Docsis active in cm
    def docs_if(self):
        return self.__DocsIf

    def fbc(self):
        return self.__fbc

    def update_sysdescr(self):
        oid = (Mibs.oid['sysdescr.0'],)
        snmp_obj = self.snmpIf.get(*oid)
        if not snmp_obj:
            return None
        sysdescr = list(snmp_obj.values())[0]
        result = re.search('HW_REV:(?P<hw_rev>[^;<>]+); VENDOR:(?P<vendor>[^;<>]+); '
                           'BOOTR:(?P<bootr>[^;<>]+); SW_REV:(?P<sw_rev>[^;<>]+); '
                           'MODEL:(?P<model>[^;<>]+)', sysdescr)
        self.__hw_rev = result.group('hw_rev').lstrip()
        self.__vendor = result.group('vendor').lstrip()
        self.__bootr = result.group('bootr').lstrip()
        self.__sw_rev = result.group('sw_rev').lstrip()
        self.__model = result.group('model').lstrip()
        return
   
    def get_in_octets(self):
        oid = (Mibs.oid['ifHCInOctets'] + '.' + self.__DocsIf.get_if_mac_index(),)
        snmp_obj = self.snmpIf.get(*oid)
        return snmp_obj[Mibs.oid['ifHCInOctets'] + '.' + self.__DocsIf.get_if_mac_index()]

    def get_model(self): return self.__model

    def get_sw_rev(self): return self.__sw_rev

    def get_vendor(self): return self.__vendor

    def get_hw_rev(self): return self.__hw_rev

    # method: Propietary SA mib
    def get_lan_devices(self):
        oid = (Mibs.oid['saRgIpMgmtLanAddrHostName'],)
        snmp_obj = self.snmpIf.get_next(*oid)
        return list(snmp_obj.values())


class FullbandCapture:

    def __init__(self, snmp_if):
        self.__snmpIf = snmp_if
        self.inactivityTimeout = 480
        self.firstFrequency = 50000000
        self.lastFrequency = 1000000000
        self.span = 10000000
        self.binsPerSegment = 250
        self.noisebandwidth = 150
        self.windowsFunction = 0
        self.numberOfAverages = 1

    def turn_off(self):
        set_values = [(Mibs.oid['docsIf3CmSpectrumAnalysisEnable'], 'Integer', 2)]
        self.__snmpIf.set(*set_values)
        return True

    def config(self):
        set_values = [(Mibs.oid['docsIf3CmSpectrumAnalysisInactivityTimeout'], 'Integer', self.inactivityTimeout),
                      (Mibs.oid['docsIf3CmSpectrumAnalysisFirstSegmentCenterFrequency'], 'Gauge', self.firstFrequency),
                      (Mibs.oid['docsIf3CmSpectrumAnalysisLastSegmentCenterFrequency'], 'Gauge', self.lastFrequency),
                      (Mibs.oid['docsIf3CmSpectrumAnalysisSegmentFrequencySpan'], 'Gauge', self.span),
                      (Mibs.oid['docsIf3CmSpectrumAnalysisBinsPerSegment'], 'Gauge', self.binsPerSegment),
                      (Mibs.oid['docsIf3CmSpectrumAnalysisEquivalentNoiseBandwidth'], 'Gauge', self.noisebandwidth),
                      (Mibs.oid['docsIf3CmSpectrumAnalysisNumberOfAverages'], 'Gauge', self.numberOfAverages),
                      (Mibs.oid['docsIf3CmSpectrumAnalysisEnable'], 'Integer', 1)]
        self.__snmpIf.set(*set_values)
        return True

    def get(self):
        oids = (Mibs.oid['docsIf3CmSpectrumAnalysisMeasAmplitudeData'],)
        snmp_obj = self.__snmpIf.get_table(*oids)
        if not snmp_obj:
            return None
        oid = Mibs.oid['docsIf3CmSpectrumAnalysisMeasAmplitudeData'] + '.'
        pattern = re.compile(oid)
        data = {}
        for key in snmp_obj.keys():
            if pattern.match(key):
                freq = re.sub(pattern, '', key, count=0, flags=0)
                data[freq] = snmp_obj[key]
        return data


class DocsIf:
    """Represents Docsis Interfaces in a CM"""
    downstream_id = "DS"
    upstream_id = "US"

    def __init__(self, snmp_if):
        self.__snmpIf = snmp_if  # Passing snmpif to access Docsis Interface
        self.__macIfIndex = None
        self.__index = []  # DocsisIf OID Index
        self.__type = {}  # DocsisIf type: UP/DOWN
        self.__downSnr = {}  # SNR values for all DownDocsIf
        self.__corrCodewords = {}
        self.__uncorrCodewords = {}
        self.__unerrCodewords = {}
        self.__upSnr = {}  # SNR values for all USDocsIf
        self.__chId = {}  # Channel ID values for all DocsIf
        self.__chFreq = {}  # Channel ID values for all DocsIf
        self.__downPower = {}  # Power values for all DownDocsIf
        self.__upPower = {}
        self.__partialSrvCh = {}
        self.__operStatus = {}  # Operational status of all DocsIf
        self.__usRangingStatus = {}  # Operational status of all UpstreamDocsIf
        self.update()
        self.__mac = self.__update_mac()

    def __update_mac(self):
        oid = (Mibs.oid['ifPhysAddress'] + '.' + self.__macIfIndex,)
        snmp_obj = self.__snmpIf.get(*oid)
        if not snmp_obj:
            return None
        return snmp_obj[Mibs.oid['ifPhysAddress'] + '.' + self.__macIfIndex]

    # __________________________ Private Methods __________________________

    def __update_down_ch_values(self, oid, value):
        snmp_obj = self.__snmpIf.get_next(*oid)
        if not snmp_obj:
            return
        for i in self.__get_down_ch_index():
            value[self.__chFreq[i]] = snmp_obj[oid[0]+'.'+i]
        return

    def __update_down_ch_values_ids(self, oid, value):
        snmp_obj = self.__snmpIf.get_next(*oid)
        if not snmp_obj:
            return
        for i in self.__get_down_ch_index():
            value[i] = snmp_obj[oid[0]+'.'+i]
        return

    def __update_up_ch_values(self, oid, value):
        snmp_obj = self.__snmpIf.get_next(*oid)
        if not snmp_obj:
            return
        for i in self.__get_up_ch_index():
            value[self.__chFreq[i]] = snmp_obj[oid[0]+'.'+i]
        return

    def __update_up_ch_values_ids(self, oid, value):
        snmp_obj = self.__snmpIf.get_next(*oid)
        if not snmp_obj:
            return
        channels = self.__get_up_ch_index()
        for i in channels:
            value[i] = snmp_obj[oid[0]+'.'+i]
        return

    def __get_down_ch_index(self):
        down_ch_index = []
        if not self.__index:
            self.update_index()
        for i in self.__index:
            if self.__type[i] == DocsIf.downstream_id:
                down_ch_index.append(i)
        return down_ch_index

    def __get_up_ch_index(self):
        up_ch_index = []
        if not self.__index:
            self.update_index()
        for i in self.__index:
            if self.__type[i] == DocsIf.upstream_id:
                up_ch_index.append(i)
        return up_ch_index

    def __update_down_ch_id(self):
        if not self.__index:
            self.update_index()
        self.__update_down_ch_values_ids((Mibs.oid['docsIfDownChannelId'],), self.__chId)
        return

    def __update_down_ch_freq(self):
        if not self.__index:
            self.update_index()
        self.__update_down_ch_values_ids((Mibs.oid['docsIfDownChannelFrequency'],), self.__chFreq)
        return

    def __update_up_ch_id(self):
        if not self.__index:
            self.update_index()
        self.__update_up_ch_values_ids((Mibs.oid['docsIfUpChannelId'],), self.__chId)
        return

    def __update_up_ch_freq(self):
        if not self.__index:
            self.update_index()
        self.__update_up_ch_values_ids((Mibs.oid['docsIfUpChannelFrequency'],), self.__chFreq)
        return

    # __________________________ Public Methods __________________________

    def update(self):
        self.update_index()
        self.update_ch_id()
        self.update_ch_freq()
        self.update_oper_status()
        self.update_partial_srv()
        return

    def update_index(self):
        self.__index = []
        self.__type = {}
        oid = (Mibs.oid['ifIndex'],)
        snmp_obj = self.__snmpIf.get_next(*oid)
        index = list(snmp_obj.values())
        oid = (Mibs.oid['ifType'],)
        snmp_obj = self.__snmpIf.get_next(*oid)
        for i in index:
            if snmp_obj[Mibs.oid['ifType']+'.'+i] == '128' or snmp_obj[Mibs.oid['ifType']+'.'+i] == '129':
                self.__index.append(i)
                if snmp_obj[Mibs.oid['ifType']+'.'+i] == '128':
                    self.__type[i] = DocsIf.downstream_id
                if snmp_obj[Mibs.oid['ifType']+'.'+i] == '129':
                    self.__type[i] = DocsIf.upstream_id
            if snmp_obj[Mibs.oid['ifType']+'.'+i] == '127':
                self.__macIfIndex = i
        return

    def get_if_mac_index(self): return self.__macIfIndex

    def update_oper_status(self):
        self.__operStatus = {}
        self.__usRangingStatus = {}
        if not self.__index:
            self.update_index()
        oid = (Mibs.oid['ifOperStatus'],)
        snmp_obj = self.__snmpIf.get_next(*oid)
        for i in self.__index:
            self.__operStatus[i] = snmp_obj[Mibs.oid['ifOperStatus'] + '.' + i]
        oid = (Mibs.oid['docsIf3CmStatusUsRangingStatus'],)
        snmp_obj = self.__snmpIf.get_next(*oid)
        for i in self.__index:
            if self.__type[i] == DocsIf.upstream_id:
                self.__usRangingStatus[i] = snmp_obj[Mibs.oid['docsIf3CmStatusUsRangingStatus']+'.'+i]
        return

    def update_ch_id(self):
        self.__chId = {}
        self.__update_down_ch_id()
        self.__update_up_ch_id()
        return self.__chId

    def update_ch_freq(self):
        self.__chFreq = {}
        self.__update_down_ch_freq()
        self.__update_up_ch_freq()
        return self.__chFreq

    def update_down_snr(self):
        self.__downSnr = {}
        if not self.__index:
            self.update_index()
        self.__update_down_ch_values((Mibs.oid['docsIfSigQSignalNoise'],), self.__downSnr)
        return self.__downSnr

    def update_down_power(self):
        self.__downPower = {}
        if not self.__index:
            self.update_index()
        self.__update_down_ch_values((Mibs.oid['docsIfDownChannelPower'],), self.__downPower)
        return self.__downPower

    def update_up_power(self):
        self.__upPower = {}
        if not self.__index:
            self.update_index()
        self.__update_up_ch_values((Mibs.oid['docsIf3CmStatusUsTxPower'],), self.__upPower)
        return self.__upPower

    def update_corr_codewords(self):
        self.__corrCodewords = {}
        if not self.__index:
            self.update_index()
        self.__update_down_ch_values((Mibs.oid['docsIfSigQCorrecteds'],), self.__corrCodewords)
        return self.__corrCodewords

    def update_unerr_codewords(self):
        self.__unerrCodewords = {}
        if not self.__index:
            self.update_index()
        self.__update_down_ch_values((Mibs.oid['docsIfSigQUnerroreds'],), self.__unerrCodewords)
        return self.__unerrCodewords

    def update_uncorr_codewords(self):
        self.__uncorrCodewords = {}
        if not self.__index:
            self.update_index()
        self.__update_down_ch_values((Mibs.oid['docsIfSigQUncorrectables'],), self.__uncorrCodewords)
        return self.__uncorrCodewords

    def update_partial_srv(self):
        self.__partialSrvCh = {}
        if self.__downSnr == {}:
            self.update_down_snr()
        for index in self.__type.keys():
            if self.__type[index] == DocsIf.downstream_id:
                if self.__downSnr[self.__chFreq[index]] == '0' or self.__operStatus[index] == '2':
                    self.__partialSrvCh[index] = self.__chId[index]
            if self.__type[index] == DocsIf.upstream_id:
                if self.__usRangingStatus[index] != '4':
                    self.__partialSrvCh[index] = self.__chId[index]
        return self.__partialSrvCh

    def get_partial_srv_ch(self): return self.__partialSrvCh

    def get_partial_srv_status(self):
        if self.__partialSrvCh == {}:
            return False
        else:
            return True

    def get_index(self): return self.__index

    def get_type(self): return self.__type

    def get_down_snr(self): return self.__downSnr

    def get_down_power(self): return self.__downPower

    def get_corr_codewords(self): return self.__corrCodewords

    def get_uncorr_codewords(self): return self.__uncorrCodewords

    def get_unerr_codewords(self): return self.__unerrCodewords

    def get_ch_id(self): return self.__chId

    def get_ch_freq(self): return self.__chFreq

    def get_oper_status(self): return self.__operStatus

    def get_mac(self): return self.__mac
