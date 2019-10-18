# -*- coding: utf-8 -*-


class Mibs:
    oid = {
            # Propietary
            'saRgIpMgmtLanAddrHostName': '1.3.6.1.4.1.1429.79.2.3.4.1.7',

            # SYS OIDS
            'sysdescr.0': '1.3.6.1.2.1.1.1.0',
            'ifDescr': '1.3.6.1.2.1.2.2.1.2',
            'ifName': '1.3.6.1.2.1.31.1.1.1.1',
            'ifType': '1.3.6.1.2.1.2.2.1.3',
            'ifIndex': '1.3.6.1.2.1.2.2.1.1',
            'ifSpeed': '1.3.6.1.2.1.2.2.1.5',
            'ifPhysAddress': '1.3.6.1.2.1.2.2.1.6',
            'ifOperStatus': '1.3.6.1.2.1.2.2.1.8',

            # ifTable
            'ifHCInOctets': '1.3.6.1.2.1.31.1.1.1.6',

            # CMTS DOCSIS 2.0 / DOCSIS 3.0 / DOCSIS 3.1 OIDS
            'docsIfCmtsCmStatusMacAddress': '1.3.6.1.2.1.10.127.1.3.3.1.2',
            'docsIfCmtsCmStatusIpAddress': '1.3.6.1.2.1.10.127.1.3.3.1.3',
            'docsIfCmtsCmStatusDownChannelIfIndex': '1.3.6.1.2.1.10.127.1.3.3.1.4',
            'docsIfCmtsCmStatusUpChannelIfIndex': '1.3.6.1.2.1.10.127.1.3.3.1.5',
            'docsIfCmtsCmStatusInetAddress': '1.3.6.1.2.1.10.127.1.3.3.1.21',
            'docsIfCmtsCmStatusRxPower': '1.3.6.1.2.1.10.127.1.3.3.1.6',  # En el CM existe docsIf3CmStatusUsTxPower
            'docsIfCmtsCmStatusTimingOffset': '1.3.6.1.2.1.10.127.1.3.3.1.7',
            'docsIfCmtsCmStatusEqualizationData': '1.3.6.1.2.1.10.127.1.3.3.1.8',
            'docsIfCmtsCmStatusValue': '1.3.6.1.2.1.10.127.1.3.3.1.9',
            'docsIfCmtsCmStatusTable': '1.3.6.1.4.1.2011.2.25.127.1.3.3',
            'docsIfCmtsCmStatusUnerroreds': '1.3.6.1.2.1.10.127.1.3.3.1.10',
            'docsIfCmtsCmStatusCorrecteds': '1.3.6.1.2.1.10.127.1.3.3.1.11',
            'docsIfCmtsCmStatusUncorrectables': '1.3.6.1.2.1.10.127.1.3.3.1.12',
            'docsIfCmtsCmStatusSignalNoise': '1.3.6.1.2.1.10.127.1.3.3.1.13',
            'docsIfCmtsCmStatusMicroreflections': '1.3.6.1.2.1.10.127.1.3.3.1.14',
            'docsIfCmtsCmPtr': '1.3.6.1.2.1.10.127.1.3.7.1.2',

            'docsIf3CmtsCmUsStatusSignalNoise': '1.3.6.1.4.1.4491.2.1.20.1.4.1.4',
            'docsIf3CmtsCmUsStatusChIfIndex': '1.3.6.1.4.1.4491.2.1.20.1.4.1.1',
            'docsIf3CmtsCmUsStatusRxPower': '1.3.6.1.4.1.4491.2.1.20.1.4.1.3',  # En el CM existe docsIf3CmStatusUsTxPower
            'docsIf3CmtsCmUsStatusUnerroreds': '1.3.6.1.4.1.4491.2.1.20.1.4.1.7',
            'docsIf3CmtsCmUsStatusCorrecteds': '1.3.6.1.4.1.4491.2.1.20.1.4.1.8',
            'docsIf3CmtsCmUsStatusUncorrectables': '1.3.6.1.4.1.4491.2.1.20.1.4.1.9',

            'cadCmtsCmStatusMacChNumOther': '1.3.6.1.4.1.4998.1.1.20.2.27.1.1',
            'cadCmtsCmStatusMacChNumInitRanging': '1.3.6.1.4.1.4998.1.1.20.2.27.1.2',
            'cadCmtsCmStatusMacChNumRangingComplete': '1.3.6.1.4.1.4998.1.1.20.2.27.1.3',
            'cadCmtsCmStatusMacChNumStartEae': '1.3.6.1.4.1.4998.1.1.20.2.27.1.4',
            'cadCmtsCmStatusMacChNumStartDhcpv4': '1.3.6.1.4.1.4998.1.1.20.2.27.1.5',
            'cadCmtsCmStatusMacChNumStartDhcpv6': '1.3.6.1.4.1.4998.1.1.20.2.27.1.6',
            'cadCmtsCmStatusMacChNumDhcpv4Complete': '1.3.6.1.4.1.4998.1.1.20.2.27.1.7',
            'cadCmtsCmStatusMacChNumDhcpv6Complete': '1.3.6.1.4.1.4998.1.1.20.2.27.1.8',
            'cadCmtsCmStatusMacChNumStartCfgFileDownload': '1.3.6.1.4.1.4998.1.1.20.2.27.1.9',
            'cadCmtsCmStatusMacChNumCfgFileDownloadComplete': '1.3.6.1.4.1.4998.1.1.20.2.27.1.10',
            'cadCmtsCmStatusMacChNumStartRegistration': '1.3.6.1.4.1.4998.1.1.20.2.27.1.11',
            'cadCmtsCmStatusMacChNumRegistrationComplete': '1.3.6.1.4.1.4998.1.1.20.2.27.1.12',
            'cadCmtsCmStatusMacChNumOperational': '1.3.6.1.4.1.4998.1.1.20.2.27.1.13',
            'cadCmtsCmStatusMacChNumBpiInit': '1.3.6.1.4.1.4998.1.1.20.2.27.1.14',
            'cadCmtsCmStatusMacChNumForwardingDisabled': '1.3.6.1.4.1.4998.1.1.20.2.27.1.15',
            'cadCmtsCmStatusMacChNumRfMuteAll': '1.3.6.1.4.1.4998.1.1.20.2.27.1.16',
            'cadCmtsCmStatusMacChNumTotal': '1.3.6.1.4.1.4998.1.1.20.2.27.1.17',
            'cadCmtsCmStatusMacChNumRangingAborted': '1.3.6.1.4.1.4998.1.1.20.2.27.1.18',
            'cadCmtsCmStatusMacChNumRangFlaps': '1.3.6.1.4.1.4998.1.1.20.2.27.1.19',
            'cadCmtsCmStatusMacChNumProvFlaps': '1.3.6.1.4.1.4998.1.1.20.2.27.1.20',
            'cadCmtsCmStatusMacChNumRegFlaps': '1.3.6.1.4.1.4998.1.1.20.2.27.1.21',
            
            'docsIf31CmtsDsOfdmProfileStatsFullChannelSpeed': '.1.3.6.1.4.1.4491.2.1.28.1.20.1.3',
            #'',


            'docsIfUpChannelFrequency': '1.3.6.1.2.1.10.127.1.1.2.1.2',
            # docsIfDownChannelPower Puede ser aplicado en CM y CMTS y se obtendra transmit y receive power respectiv.
            'docsIfDownChannelPower': '1.3.6.1.2.1.10.127.1.1.1.1.6',  # Both downstream transmit and receive power
            'docsIfDownChannelFrequency': '1.3.6.1.2.1.10.127.1.1.1.1.2',
            'docsIfDownChannelModulation': '1.3.6.1.2.1.10.127.1.1.1.1.4',
            'docsIfUpChannelWidth': '1.3.6.1.2.1.10.127.1.1.2.1.3',
            'docsIfUpChannelType': '1.3.6.1.2.1.10.127.1.1.2.1.15',
            'docsIfSigQSignalNoise': '1.3.6.1.2.1.10.127.1.1.4.1.5',
            'docsIfSigQUncorrectables': '1.3.6.1.2.1.10.127.1.1.4.1.4',
            'docsIfSigQUnerroreds': '1.3.6.1.2.1.10.127.1.1.4.1.2',
            'docsIfSigQCorrecteds': '1.3.6.1.2.1.10.127.1.1.4.1.3',

            'docsIfCmStatusTxPower': '1.3.6.1.2.1.10.127.1.2.2.1.3',  # en 3.0: docsIf3CmStatusUsTxPower
            'docsIfCmStatusModulationType': '1.3.6.1.2.1.10.127.1.2.2.1.16',
            'docsIfCmStatusEqualizationData': '1.3.6.1.2.1.10.127.1.2.2.1.17',
            'docsIfDownChannelId': '1.3.6.1.2.1.10.127.1.1.1.1.1',
            'docsIfUpChannelId': '1.3.6.1.2.1.10.127.1.1.2.1.1',
            'docsIfUpstreamChannelEntry': '1.3.6.1.2.1.10.127.1.1.2.1',

            'docsIf3CmSpectrumAnalysisEnable': '1.3.6.1.4.1.4491.2.1.20.1.34.1.0',
            'docsIf3CmSpectrumAnalysisInactivityTimeout': '1.3.6.1.4.1.4491.2.1.20.1.34.2.0',
            'docsIf3CmSpectrumAnalysisFirstSegmentCenterFrequency': '1.3.6.1.4.1.4491.2.1.20.1.34.3.0',
            'docsIf3CmSpectrumAnalysisLastSegmentCenterFrequency': '1.3.6.1.4.1.4491.2.1.20.1.34.4.0',
            'docsIf3CmSpectrumAnalysisSegmentFrequencySpan': '1.3.6.1.4.1.4491.2.1.20.1.34.5.0',
            'docsIf3CmSpectrumAnalysisBinsPerSegment': '1.3.6.1.4.1.4491.2.1.20.1.34.6.0',
            'docsIf3CmSpectrumAnalysisEquivalentNoiseBandwidth': '1.3.6.1.4.1.4491.2.1.20.1.34.7.0',
            'docsIf3CmSpectrumAnalysisWindowFunction': '1.3.6.1.4.1.4491.2.1.20.1.34.8.0',
            'docsIf3CmSpectrumAnalysisNumberOfAverages': '1.3.6.1.4.1.4491.2.1.20.1.34.9.0',
            'docsIf3CmSpectrumAnalysisMeasFrequency': '',
            'docsIf3CmSpectrumAnalysisMeasAmplitudeData': '1.3.6.1.4.1.4491.2.1.20.1.35.1.2',
            'docsIf3CmSpectrumAnalysisMeasTotalSegmentPower': '1.3.6.1.4.1.4491.2.1.20.1.35.1.3.0',
            'docsIf3CmStatusUsTxPower': '1.3.6.1.4.1.4491.2.1.20.1.2.1.1',
            'docsIf3CmStatusUsRangingStatus': '1.3.6.1.4.1.4491.2.1.20.1.2.1.9',

            'docsIf31CmDsOfdmChannelPowerCenterFrequency': '1.3.6.1.4.1.4491.2.1.28.1.11.1.2',
            'docsIf31CmDsOfdmChannelPowerRxPower': '1.3.6.1.4.1.4491.2.1.28.1.11.1.3',
            'docsIf31CmDsOfdmChannelPowerTable': '1.3.6.1.4.1.4491.2.1.28.1.11',
            'docsPnmCmDsOfdmRxMerMean': '.1.3.6.1.4.1.4491.2.1.27.1.2.5.1.3',
            'docsIf31CmDsOfdmProfileStatsInOctets': '.1.3.6.1.4.1.4491.2.1.28.1.10.1.6',
            
    }
