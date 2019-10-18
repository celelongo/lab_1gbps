#!/bin/python3.4

from pysnmp.entity.rfc3413.oneliner import cmdgen
from pysnmp.proto import rfc1902


class SnmpError(Exception):
    """Class to manage SNMP errors"""
    pass


class SnmpSetError(Exception):
    """Class to manage SNMP errors"""
    pass


def make_snmp_obj_rfc1902(*args):
    oid_type = []
    for oid, _type, value in args:
        if _type == 'Integer':
            obj = rfc1902.Integer(value)
        else:
            if _type == 'Gauge':
                obj = rfc1902.Gauge32(value)
            else:
                raise SnmpSetError
        oid_type.append((oid, obj))   
    return oid_type


def set_snmp(ip, snmp_attr, *oid_type_value):
    obj_set_names = make_snmp_obj_rfc1902(*oid_type_value)
    cmd_gen = cmdgen.CommandGenerator()
    error_indication, error_status, error_index, var_binds = cmd_gen.setCmd(
        cmdgen.CommunityData(snmp_attr.get_community()),
        cmdgen.UdpTransportTarget((ip, snmp_attr.get_port()), timeout=int(snmp_attr.get_timeout()),
                                  retries=int(snmp_attr.get_retries())), *obj_set_names,
        lookupMib=snmp_attr.get_lookupmib()
    )
    # Check for errors and print out results
    if error_indication:
        raise SnmpError(error_indication)
    else:
        if error_status:
            raise SnmpError(error_status, error_index, var_binds)
        else:
            vars_values = {}
            for val, name in var_binds:
                vars_values[val.prettyPrint()] = name.prettyPrint()
    return vars_values


def get_snmp(ip, snmp_attr, *objnames):
    cmd_gen = cmdgen.CommandGenerator()
    error_indication, error_status, error_index, var_binds = cmd_gen.getCmd(
        cmdgen.CommunityData(snmp_attr.get_community()),
        cmdgen.UdpTransportTarget((ip, snmp_attr.get_port()), timeout=int(snmp_attr.get_timeout()),
                                  retries=int(snmp_attr.get_retries())), *objnames,
        lookupMib=snmp_attr.get_lookupmib()
    )
    # Check for errors and print out results
    if error_indication:
        raise SnmpError(error_indication)
    else:
        if error_status:
            raise SnmpError(error_status, error_index, var_binds)
        else:
            vars_values = {}
            for val, name in var_binds:
                vars_values[val.prettyPrint()] = name.prettyPrint()
    return vars_values


def get_next_snmp(ip, snmp_attr, *objnames):
    cmd_gen = cmdgen.CommandGenerator()
    error_indication, error_status, error_index, var_bind_table = cmd_gen.nextCmd(
        cmdgen.CommunityData(snmp_attr.get_community()),
        cmdgen.UdpTransportTarget((ip, snmp_attr.get_port()), timeout=int(snmp_attr.get_timeout()),
                                  retries=int(snmp_attr.get_retries())), maxRows=snmp_attr.get_maxrows(),
        ignoreNonIncreasingOid=snmp_attr.get_ignorenonincreasingoid(),
        lookupMib=snmp_attr.get_lookupmib(),
        *objnames
    )
    # Check for errors and print out results
    if error_indication:
        raise SnmpError(error_indication)
    else:
        if error_status:
            raise SnmpError(error_status, error_index, var_bind_table)
        else:
            vars_values = {}
            for varBindTableRow in var_bind_table:
                for val, name in varBindTableRow:
                    vars_values[val.prettyPrint()] = name.prettyPrint()
    return vars_values


def get_table_snmp(ip, snmp_attr, *objnames):
    cmd_gen = cmdgen.CommandGenerator()
    error_indication, error_status, error_index, var_bind_table = cmd_gen.bulkCmd(
        cmdgen.CommunityData(snmp_attr.get_community()),
        cmdgen.UdpTransportTarget((ip, snmp_attr.get_port()), timeout=int(snmp_attr.get_timeout()),
                                  retries=int(snmp_attr.get_retries())), 0, snmp_attr.get_bulkcount(), *objnames,
        lookupMib=snmp_attr.get_lookupmib(), maxRows=snmp_attr.get_maxrows()
    )
    # Check for errors and print out results
    if error_indication:
        raise SnmpError(error_indication)
    else:
        if error_status:
            raise SnmpError(error_status, error_index, var_bind_table[-1][int(error_index)-1])
        else:
            vars_values = {}
            for varBindTableRow in var_bind_table:
                for ObjectName, ObjectValue in varBindTableRow:
                    if not ObjectValue:
                        break
                    vars_values[ObjectName.prettyPrint()] = ObjectValue.prettyPrint()
    return vars_values
