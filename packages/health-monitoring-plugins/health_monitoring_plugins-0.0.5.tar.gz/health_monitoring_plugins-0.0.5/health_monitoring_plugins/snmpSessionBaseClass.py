#!/usr/bin/python

# Copyright (C) 2016 rsmuc <rsmuc@mailbox.org>
# 
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with health_monitoring_plugins. If not, see <http://www.gnu.org/licenses/>.

from pynag.Plugins import unknown, critical
import netsnmp

def add_common_options(helper):
    # Define the common command line parameters
    helper.parser.add_option('-H', help="Hostname or ip address", dest="hostname")
    helper.parser.add_option('-C', '--community', dest='community', help='SNMP community of the SNMP service on target host.', default='public')
    helper.parser.add_option('-V', '--snmpversion', dest='version', help='SNMP version. (1 or 2)', default=2, type='int')

def get_common_options(helper):
    # get the common options
    host = helper.options.hostname
    version = helper.options.version
    community = helper.options.community
    return host, version, community

def verify_host(host, helper):
    if host == "" or host is None:
        helper.exit(summary="Hostname must be specified", exit_code=unknown, perfdata='')

# make a snmp get, if it fails (or returns nothing) exit the plugin
def get_data(session, oid, helper):
    var = netsnmp.Varbind(oid)
    varl = netsnmp.VarList(var)
    data = session.get(varl)
    value = data[0]
    if not value:
        helper.exit(summary="snmpget failed - no data for host " + session.DestHost + " OID: " +oid, exit_code=unknown, perfdata='')
    return value

# make a snmp get, but do not exit the plugin, if it returns nothing
# be careful! This funciton does not exit the plugin, if snmp get fails!
def attempt_get_data(session, oid):
    var = netsnmp.Varbind(oid)
    varl = netsnmp.VarList(var)
    data = session.get(varl)
    value = data[0]
    return value

# make a snmp walk, if it fails (or returns nothing) exit the plugin
def walk_data(session, oid, helper):
    tag = []
    var = netsnmp.Varbind(oid)
    varl = netsnmp.VarList(var)
    data = list(session.walk(varl))
    if len(data) == 0:
        helper.exit(summary="snmpwalk failed - no data for host " + session.DestHost + " OID: " +oid, exit_code=unknown, perfdata='')
    for x in range(0, len(data)):
        tag.append(varl[x].tag)
    return data, tag

# make a snmp walk, but do not exit the plugin, if it returns nothing
# be careful! This function does not exit the plugin, if snmp walk fails!
def attempt_walk_data(session, oid):
    tag = []
    var = netsnmp.Varbind(oid)
    varl = netsnmp.VarList(var)
    data = list(session.walk(varl))
    for x in range(0, len(data)):
        tag.append(varl[x].tag)
    return data, tag

def state_summary(value, name, state_list, helper, ok_value = 'ok', info = None):
    """
    Always add the status to the long output, and if the status is not ok (or ok_value), 
    we show it in the summary and set the status to critical
    """
    # translate the value (integer) we receive to a human readable value (e.g. ok, critical etc.) with the given state_list
    state_value = state_list[int(value)]    
    summary_output = ''
    long_output = ''
    if not info:
        info = ''
    if state_value != ok_value:
        summary_output += ('%s status: %s %s ' % (name, state_value, info))
        helper.status(critical)
    long_output += ('%s status: %s %s\n' % (name, state_value, info))
    return (summary_output, long_output)

def add_output(summary_output, long_output, helper):
    """
    if the summary output is empty, we don't add it as summary, otherwise we would have empty spaces (e.g.: '. . . . .') in our summary report
    """
    if summary_output != '':
        helper.add_summary(summary_output)
    helper.add_long_output(long_output)
