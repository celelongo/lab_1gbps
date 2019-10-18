# -*- coding: utf-8 -*-
"""
Created on 2019-09-24
@author: Celeste Longo
"""
import wrapperSnmp.cm31Devices as cm31Devices
import wrapperSnmp.cmtsDevices as cmtsDevices
import time
from wrapperSnmp.snmp import SnmpError
import csv
import re
import copy


def get_data_cm(cmts_doc_if, cm_doc_if, cm):
    dict_return = {"error": False}
    try:
        octets_in_f = cm.get_in_octets()
        dict_return["timestampOctets"] = time.time()
        if get_ds:
            corr_c, uncorr_c, unerr_c = cm_doc_if.update_corr_codewords(), cm_doc_if.update_uncorr_codewords(), \
                                              cm_doc_if.update_unerr_codewords()

            pwr = cm_doc_if.update_down_power()
            snr = cm_doc_if.update_down_snr()
        else:
            pwr = {}
            snr = {}
            corr_c = {}
            uncorr_c = {}
            unerr_c = {}

        if get_us:
            # Actualizo los diccionarios con los valores para upstream.
            snr.update(cmts_doc_if.update_up_snr())
            pwr.update(cm_doc_if.update_up_power())
            corr_c.update(cmts_doc_if.update_us_corr_codewords())
            uncorr_c.update(cmts_doc_if.update_us_uncorr_codewords())
            unerr_c.update(cmts_doc_if.update_us_unerr_codewords())

        dict_return["octetsIn"] = octets_in_f
        dict_return["corrC"] = corr_c
        dict_return["uncorrC"] = uncorr_c
        dict_return["unerrC"] = unerr_c
        dict_return["pwr"] = pwr
        dict_return["snr"] = snr

    except SnmpError:
        dict_return = {"error": False}

    return dict_return


def get_ccer_and_cer(data, prev_data, freqs):
    cm_ccer = {}
    cm_cer = {}
    for freq in freqs:
        try:
            # Ccer = 100 * CorrC / (CorrC + UncorrC + UnerrC)
            # Cer = 100 * UncorrC / (CorrC + UncorrC + UnerrC)
            aux = int(data["corrC"][freq]) - int(prev_data["corrC"][freq]) + int(data["uncorrC"][freq]) - \
                   int(prev_data["uncorrC"][freq]) + int(data["unerrC"][freq]) - int(prev_data["unerrC"][freq])

            cm_ccer[freq] = round(100 * (int(data["corrC"][freq]) - int(prev_data["corrC"][freq])) / aux, 2)
            cm_cer[freq] = round(100 * (int(data["uncorrC"][freq]) - int(prev_data["uncorrC"][freq])) / aux, 4)

        except ZeroDivisionError:
            cm_ccer[freq] = "PS"
            cm_cer[freq] = "PS"

        except KeyError:
            cm_ccer[freq] = "Sin datos"
            cm_cer[freq] = "Sin datos"

    return cm_ccer, cm_cer

def get_data_cm31(cm_doc_if31, cm):
    dict_return = {"error": False}
    try:
        #ofdm_octets_in_f = cm.get_in_ofdm_octets()
        #dict_return["timestampOctets"] = time.time()
        #ofdm_corrc, ofdm_uncorrc, ofdm_unerrc = cm_doc_if.update_ofdm_corr_codewords(), cm_doc_if.update_ofdm_uncorr_codewords(), \
        #                                      cm_doc_if.update_ofdm_unerr_codewords()
        ofdm_freq = {}
        ofdm_pwr = {}
        ofdm_avg_mer = 0
        
        ofdm_freq = cm_doc_if31.update_ofdm_freq()
        ofdm_pwr = cm_doc_if31.update_ofdm_rx_power()
        ofdm_avg_mer = cm_doc_if31.update_ofdm_ave_mer()
            
        #ofdm_corrc = {}
        #ofdm_uncorrc = {}
        #ofdm_unerrc = {}

        #dict_return["octetsIn"] = ofdm_octets_in_f
        #dict_return["corrC"] = ofdm_corrc
        #dict_return["uncorrC"] = ofdm_uncorrc
        #dict_return["unerrC"] = ofdm_unerrc
        dict_return["freq"] = ofdm_freq
        dict_return["pwr"] = ofdm_pwr
        dict_return["snr"] = ofdm_avg_mer

    except SnmpError:
        dict_return = {"error": False}

    return dict_return


# cm_mac1 = "84a06e65c5e3" # Sagemcom
#cm_mac1 = "e8ada610898e"   # Sagemcom
cm_mac1 = "84a06e65c5e3"   # Sagemcom
cm_mac2 = "441c1264606c"  # Technicolor

cmts_Ip = '10.101.248.8'  # Arris E6000 Lab Hornos
# cmtsIp = '10.100.150.149'

get_us = True  # Poner False si solo se quiere DS.
get_ds = True  # Poner False si solo se quiere US.

fileName = cm_mac1 + "_" + cm_mac2 + ".csv"  # El nombre del archivo que escribe.
interval = 2  # Tiempo que espera antes de volver a pedir los datos.
duration = 1 * 60  # Tiempo total de la captura.

# Se verifica el formato de las MAC
cm_mac1 = re.sub('[^a-f0-9]', '', cm_mac1, flags=re.IGNORECASE)
cm_mac1 = cm_mac1.lower()
if len(cm_mac1) != 12:
    print("Error, MAC1 with unknown format.")
    exit()

cm_mac2 = re.sub('[^a-f0-9]', '', cm_mac2, flags=re.IGNORECASE)
cm_mac2 = cm_mac2.lower()
if len(cm_mac2) != 12:
    print("Error, MAC2 with unknown format.")
    exit()

# create a cmts object
cmts = cmtsDevices.Cmts(cmts_Ip)

print("Modelando al CMTS y obteniendo la IP de los CMs...\n")
# Defining a CM inside the CMTS as an object
cm_virtual1 = cmts.get_cm(cm_mac1)
cm_virtual2 = cmts.get_cm(cm_mac2)
cm_ip1 = cm_virtual1.get_ip()
cm_ip2 = cm_virtual2.get_ip()
# create CM
print("Obteniendo relacion de frecuencias/canales para US (docsIfUpChannelFrequency) y DS.\n"
      "Creando CMs virtuales dentro del CMTS. Puede demorar...\n")

cm1 = cm31Devices.Cm31(cm_ip1)
cm2 = cm31Devices.Cm31(cm_ip2)

ptr_cm1 = cm_virtual1.get_ptr()
ptr_cm2 = cm_virtual2.get_ptr()

print("Virtual CMs inside the CMTS:\n\n")
print("CM1:\nMAC: " + cm_mac1 + "\nIP: " + cm_ip1 + "\nPtrCM in CMTS: ", ptr_cm1 + "\n")
print("CM2:\nMAC: " + cm_mac2 + "\nIP: " + cm_ip2 + "\nPtrCM in CMTS: ", ptr_cm2 + "\n")


cmts_doc_if1 = cm_virtual1.get_docs_if_cmts()
cmts_doc_if2 = cm_virtual2.get_docs_if_cmts()

#cm1_doc_if = cm1.docs_if()
#cm2_doc_if = cm2.docs_if()

cm1_doc_if31 = cm1.docs_if31()
cm2_doc_if31 = cm2.docs_if31()

# ----------- Para Testear frecuencias/ids ---------------------------------------------------------------
print("--------> CM: ", cm_mac1.upper(), "tiene la siguiente relación id/frecuencias: ")
print("Upstream: ")
print(cmts_doc_if1.get_ch_freq())
print("Downstream: ")
print(cm1_doc_if31.get_ch_freq())
print("\n")
print("--------> CM: ", cm_mac2.upper(), "tiene la siguiente relación id/frecuencias: ")
print("Upstream: ")
print(cmts_doc_if2.get_ch_freq())
print("Downstream: ")
print(cm2_doc_if31.get_ch_freq())
print("\n")
# --------------------------------------------------------------------------------------------------------


# Obtengo las frecuencias de upstream.
keys_us = set()
snr1 = cmts_doc_if1.update_up_snr()
for freq in snr1.keys():
    keys_us.add(freq)
snr2 = cmts_doc_if2.update_up_snr()
for freq in snr2.keys():
    keys_us.add(freq)

keys_us = list(keys_us)

prev_data_cm1 = get_data_cm(cmts_doc_if1, cm1_doc_if31, cm1)
prev_data_cm2 = get_data_cm(cmts_doc_if2, cm2_doc_if31, cm2)

data_cm1 = get_data_cm31(cm1_doc_if31, cm1)
data_cm2 = get_data_cm31(cm2_doc_if31, cm2)


if prev_data_cm1["error"]:
    print("No se pudieron obtener los datos de CM1")
    exit(1)

if prev_data_cm2["error"]:
    print("No se pudieron obtener los datos de CM2")
    exit(1)


start = time.time()

# Ofdm_Freq = Cm1.getOfdmFreq()
# Cm1_Ofdm_Pwr = {}
# Cm1_Ofdm_Mer = {}
#
# Ofdm_Freq.update(Cm2.getOfdmFreq())
# Cm2_Ofdm_Pwr = {}
# Cm2_Ofdm_Mer = {}


with open(fileName, "w", newline='') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=",")

    row = ["Timestamp", "CH TYPE", "FREQ [MHz]", "MAC 1", "Nivel1 [dBmV]", "SNR1 [dB]", "CCER1 [%]", "CER1 [%]",
           "Bandwidth1 [Mbps]", "MAC 2", "Nivel2 [dBmV]", "SNR2 [dB]", "CCER2 [%]", "CER2 [%]", "Bandwidth2 [Mbps]"]

    spamwriter.writerow(row)
    print(row)

    while time.time() - start < duration:
        time.sleep(interval)
        timestamp = int(time.time())

        data_cm1 = get_data_cm(cmts_doc_if1, cm1_doc_if31, cm1)
        data_cm2 = get_data_cm(cmts_doc_if2, cm2_doc_if31, cm2)

        if data_cm1["error"]:
            print("No se pudieron obtener los datos de CM1")
            continue

        if data_cm2["error"]:
            print("No se pudieron obtener los datos de CM2")
            continue

        bandwidth_mbps1 = round(((int(data_cm1["octetsIn"]) - int(prev_data_cm1["octetsIn"])) /
                                 (data_cm1["timestampOctets"] - prev_data_cm1["timestampOctets"])) * 8 / 1E6, 2)
        bandwidth_mbps2 = round(((int(data_cm2["octetsIn"]) - int(prev_data_cm2["octetsIn"])) /
                                 (data_cm2["timestampOctets"] - prev_data_cm2["timestampOctets"])) * 8 / 1E6, 2)

        # define all freqs:
        all_freqs = set()
        for freq in data_cm1["snr"]:
            all_freqs.add(freq)
        for freq in data_cm2["snr"]:
            all_freqs.add(freq)
        all_freqs = list(all_freqs)

        cm1_ccer, cm1_cer = get_ccer_and_cer(data_cm1, prev_data_cm1, all_freqs)
        cm2_ccer, cm2_cer = get_ccer_and_cer(data_cm2, prev_data_cm2, all_freqs)

        for freq in all_freqs:
            type_ch = "DS"
            if freq in keys_us:
                type_ch = "US"
                bandwidth_Mbps1 = "--"
                bandwidth_Mbps2 = "--"

            if freq not in data_cm1["pwr"]:
                data_cm1["pwr"][freq] = "Sin Datos"
                data_cm1["snr"][freq] = "Sin Datos"
                pwr1 = "Sin Datos"
                snr1 = "Sin Datos"
            else:
                pwr1 = round(int(data_cm1["pwr"][freq]) / 10, 2)
                snr1 = round(int(data_cm1["snr"][freq]) / 10, 2)

            if freq not in data_cm2["pwr"]:
                data_cm2["pwr"][freq] = "Sin Datos"
                data_cm2["snr"][freq] = "Sin Datos"
                pwr2 = "Sin Datos"
                snr2 = "Sin Datos"
            else:
                pwr2 = round(int(data_cm2["pwr"][freq]) / 10, 2)
                snr2 = round(int(data_cm2["snr"][freq]) / 10, 2)

            row = [timestamp, type_ch, round(int(freq) / 1E6, 2), str(cm_mac1[2:]),
                   pwr1, snr1, cm1_ccer[freq], cm1_cer[freq], bandwidth_mbps1, str(cm_mac2[2:]), pwr2, snr2,
                   cm2_ccer[freq], cm2_cer[freq], bandwidth_mbps2]

            spamwriter.writerow(row)
            print(row)

        prev_data_cm1 = copy.deepcopy(data_cm1)
        prev_data_cm2 = copy.deepcopy(data_cm2)

csvfile.close()
