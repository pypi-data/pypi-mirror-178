import sys
import ipaddress
import json
import snimpy
import yaml
from snimpy.config import Conf
from snimpy import manager

# Local Imports
from .ui import UI
# SNMP Client Modules
from .CdpNeighbors import CdpClient, CdpNeighborsUI

class SnmpError(Exception):
    pass

class SnmpVersionError(Exception):
    pass

class DeadCodeClass:
    def getNetTables(self):
        results = {}
        m = self.M
        results['ifTable'] = self.getIfTables(m)
        return results

    def __init__(self,
            host,
            version,
            community=None,
            userName=None,
            authPass=None,
            privPass=None,
            privProtocol="AES",
            authProtocol="SHA",
            port=161):
        self.host = host
        self.community = community
        self.version = version
        self.port = port
        manager.load("IF-MIB")
        manager.load("ENTITY-MIB")
        manager.load("/home/michael/.snmp/mibs/CISCO-SMI")
        manager.load("/home/michael/.snmp/mibs/CISCO-TC")
        manager.load("/home/michael/.snmp/mibs/CISCO-IF-EXTENSION-MIB")
        manager.load("/home/michael/.snmp/mibs/CISCO-VTP-MIB")
        manager.load("/home/michael/.snmp/mibs/CISCO-CDP-MIB")
        self.M = manager.Manager(
                host=host,
                version=version,
                secname=userName,
                authprotocol=authProtocol,
                authpassword=authPass,
                privprotocol=privProtocol,
                privpassword=privPass)

class SnmpUI:
    def __exit(self):
        sys.exit(0)

    def run(self):
        self._ui.start()

    def __init__(
            self,
            host,
            version,
            userName,
            authPass,
            privPass,
            extraMibs
            ):
        self._ui = UI()
        cdpScreen = self._ui.add_screen("CDP")
        cdpUI = CdpNeighborsUI(cdpScreen)
        cdpUI.setSNMP(
            host=host,
            version=version,
            userName=userName,
            authPass=authPass,
            privPass=privPass,
            extraMibs=extraMibs)
        cdpUI.run()
        self._ui.activate_screen("CDP")
