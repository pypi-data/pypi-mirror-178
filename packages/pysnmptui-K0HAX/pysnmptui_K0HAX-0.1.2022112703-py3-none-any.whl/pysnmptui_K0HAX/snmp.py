import sys
import snimpy
from snimpy.config import Conf
from snimpy import manager
import ipaddress
import json

from .ui import UI

class SnmpError(Exception):
    pass

class SnmpVersionError(Exception):
    pass

class Client:
    host = None
    community = None
    version = None
    port = None
    userName = None
    authPass = None
    privPass = None
    authData = None

    def getIfTables(self, m):
        results = {}
        for i in m.ifDescr:
            if m.ifType[i] != 6:
                continue
            if m.ifAdminStatus[i] != 1:
                continue
            results[i] = {
                    'ifDescr': m.ifDescr[i],
                    'ifType': m.ifType[i],
                    'ifSpeed': m.ifSpeed[i],
                    'ifPhysAddress': m.ifPhysAddress[i],
                    'ifAdminStatus': m.ifAdminStatus[i],
                    'ifOperStatus': m.ifOperStatus[i],
                    'ifInDiscards': m.ifInDiscards[i],
                    'ifInErrors': m.ifInErrors[i],
                    'ifOutDiscards': m.ifOutDiscards[i],
                    'ifOutErrors': m.ifOutErrors[i],
                    }
        return results

    def doTryGet(self, func, i):
        m = self.M
        try:
            return m.__getattribute__(func)[i]
        except Exception as e:
            print(e)
            return None

    CdpCapabilities = {
            0b1000000: "Repeater",
            0b100000: "IGMP Capable",
            0b10000: "Host",
            0b1000: "Switch",
            0b100: "Source Route Bridge",
            0b10: "Transparent Bridge",
            0b1: "Router"
            }

    def parseCapabilities(self, val):
        retval = {}
        retval['decoded'] = []
        for cap, capVal in self.CdpCapabilities.items():
            if val & cap:
                retval['decoded'].append(capVal)
        remainder = "{:025b}".format(val >> 7)
        retval['remainder'] = remainder
        return retval

    def getCdpCacheTable(self):
        results = {}
        m = self.M
        for i in m.cdpCacheAddress:
            result = {
                    'ifDescr': self.doTryGet("ifDescr", i[0]),
                    'cdpCacheAddress': self.doTryGet("cdpCacheAddress", i),
                    'cdpCacheVersion': self.doTryGet("cdpCacheVersion", i),
                    'cdpCacheDeviceId': self.doTryGet("cdpCacheDeviceId", i),
                    'cdpCacheDevicePort': self.doTryGet("cdpCacheDevicePort", i),
                    'cdpCachePlatform': self.doTryGet("cdpCachePlatform", i),
                    'cdpCacheCapabilities': self.parseCapabilities(int.from_bytes(self.doTryGet("cdpCacheCapabilities", i), "big")),
                    'cdpCacheVTPMgmtDomain': self.doTryGet("cdpCacheVTPMgmtDomain", i),
                    'cdpCacheNativeVLAN': self.doTryGet("cdpCacheNativeVLAN", i),
                    'cdpCacheDuplex': self.doTryGet("cdpCacheDuplex", i),
                    'cdpCacheApplianceID': self.doTryGet("cdpCacheApplianceID", i),
                    'cdpCacheVlanID': self.doTryGet("cdpCacheVlanID", i),
                    'cdpCachePowerConsumption': self.doTryGet("cdpCachePowerConsumption", i),
                    'cdpCacheMTU': self.doTryGet("cdpCacheMTU", i),
                    'cdpCacheSysName': self.doTryGet("cdpCacheSysName", i),
                    'cdpCacheSysObjectID': self.doTryGet("cdpCacheSysObjectID", i),
                    'cdpCachePrimaryMgmtAddrType': self.doTryGet("cdpCachePrimaryMgmtAddrType", i),
                    'cdpCachePrimaryMgmtAddr': self.doTryGet("cdpCachePrimaryMgmtAddr", i),
                    'cdpCacheSecondaryMgmtAddrType': self.doTryGet("cdpCacheSecondaryMgmtAddrType", i),
                    'cdpCacheSecondaryMgmtAddr': self.doTryGet("cdpCacheSecondaryMgmtAddr", i),
                    'cdpCachePhysLocation': self.doTryGet("cdpCachePhysLocation", i),
                    'cdpCacheLastChange': self.doTryGet("cdpCacheLastChange", i)
                    }
            try:
                ipAddress = ipaddress.ip_address(result['cdpCacheAddress'])
                result['cdpCacheAddress'] = ipAddress
            except Exception as e:
                print(f"ipAddress Error: {e}")
                pass
            if result['ifDescr'] not in results.keys():
                results[result['ifDescr']] = {}
            results[result['ifDescr']][i[1]] = result
        return results

    def getCieIfStatusListTable(self, m, i):
        results = {}
        operMode = m.cieInterfacesOperMode[1]
        results['cieInterfacesOperMode'] = []
        try:
            for k, v in operMode.iteritems():
                results['cieInterfacesOperMode'].append((k, v))
        except:
            pass
        results['cieInterfacesOperCause'] = m.cieInterfacesOperCause[i]
        results['cieInterfaceOwnershipBitmap'] = m.cieInterfaceOwnershipBitmap[i]
        return results

    def getNetTables(self):
        #g = pysnmp.hlapi.getCmd(
        #        snmpEngine,
        #        self.authData,
        #        pysnmp.hlapi.UdpTransportTarget((self.host, self.port)),
        #        pysnmp.hlapi.ContextData(),
        #        pysnmp.hlapi.ObjectType(pysnmp.hlapi.ObjectIdentity('IF-MIB', 'ifDescr')),
        #        pysnmp.hlapi.ObjectType(pysnmp.hlapi.ObjectIdentity('IF-MIB', 'ifType')),
        #        pysnmp.hlapi.ObjectType(pysnmp.hlapi.ObjectIdentity('IF-MIB', 'ifMtu')),
        #        pysnmp.hlapi.ObjectType(pysnmp.hlapi.ObjectIdentity('IF-MIB', 'ifSpeed')),
        #        pysnmp.hlapi.ObjectType(pysnmp.hlapi.ObjectIdentity('IF-MIB', 'ifPhysAddress')),
        #        pysnmp.hlapi.ObjectType(pysnmp.hlapi.ObjectIdentity('IF-MIB', 'ifType')),
        #        )
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
                authprotocol="SHA",
                authpassword=authPass,
                privprotocol="AES",
                privpassword=privPass)
        #if version == 3:
        #    self.authData = pysnmp.hlapi.UsmUserData(
        #            userName=userName,
        #            authKey=authPass,
        #            privKey=privPass,
        #            authProtocol=pysnmp.hlapi.usmHMACSHAAuthProtocol,
        #            privProtocol=pysnmp.hlapi.usmAesCfb256Protocol)
        #elif version == 2:
        #    self.authData = pysnmp.hlapi.CommunityData(self.community)
        #else:
        #    raise SnmpVersionError

class MenuValue:
    def __init__(self, key, val):
        self._key = key
        self._val = val

    def get(self):
        return self._val

    def __str__(self):
        return self._key

class SnmpUI:
    clients = {}
    snmp_data = {}

    def __exit(self):
        sys.exit(0)

    def _onClientChanged(self):
        uxCdpInterfaces = self._ui.get('uxCdpInterfaces')
        uxCdpInterfaces.clear()
        selectedClient = self._ui.get('uxClients').get()
        for key, val in self.snmp_data[selectedClient].items():
            thisVal = MenuValue(key, val)
            uxCdpInterfaces.add_item(thisVal)
        self._onCdpInterfaceChanged()

    def _printDict(self, data):
        strData = json.dumps(data, indent=2, default=str)
        retval = strData.splitlines()
        return retval

    def _onCdpInterfaceChanged(self):
        uxCdpDetail = self._ui.get('uxCdpDetail')
        selectedInterface = self._ui.get('uxCdpInterfaces').get().get()
        uxCdpDetail.clear()
        for sKey, sVal in selectedInterface.items():
            for key, val in sVal.items():
                thisVal = ""
                if (type(val) == type(None)):
                    continue
                if (
                        (type(val) == str)
                        or (type(val) == snimpy.basictypes.String)
                        or (type(val) == ipaddress.IPv4Address)
                        or (type(val) == snimpy.basictypes.Integer)
                        or (type(val) == snimpy.basictypes.Enum)
                        or (type(val) == snimpy.basictypes.Unsigned32)
                        ):
                    firstLine = True
                    for line in str(val).splitlines():
                        if firstLine == True:
                            firstLine = False
                            thisVal = f"{key}: {str(line)}"
                            uxCdpDetail.add_item(thisVal)
                        else:
                            thisVal = f"    {str(line)}"
                            uxCdpDetail.add_item(thisVal)
                elif (type(val) == dict):
                    lines = self._printDict(val)
                    firstLine = True
                    for line in lines:
                        if firstLine == True:
                            firstLine = False
                            thisVal = f"{key}: {str(line)}"
                            uxCdpDetail.add_item(thisVal)
                        else:
                            thisVal = f"    {str(line)}"
                            uxCdpDetail.add_item(thisVal)
                else:
                    thisVal = f"{key}: {type(val)}"
                    uxCdpDetail.add_item(thisVal)

    def getSNMP(self):
        uxClients = self._ui.get("uxClients")
        uxClients.clear()
        for client, m in self.clients.items():
            self.snmp_data[client] = m.getCdpCacheTable()
            uxClients.add_item(client)
        self._onClientChanged()
        return self.snmp_data

    def run(self):
        self.getSNMP()
        self._ui.start()

    def setSNMP(self, host, version, userName, authPass, privPass):
        self.clients[host] = Client(
                host=host,
                version=3,
                userName=userName,
                authPass=authPass,
                privPass=privPass
                )

    def __init__(self):
        self._ui = UI(x=4, y=3)
        self._ui.add("uxExitLabel", self._ui.root.add_button('Exit', 3, 0, command=self.__exit))

        uxClients = self._ui.root.add_scroll_menu('Clients', 0, 0)
        uxClients.set_on_selection_change_event(self._onClientChanged)
        self._ui.add("uxClients", uxClients)

        uxCdpInterfaces = self._ui.root.add_scroll_menu('CDP Neighbors', 0, 1)
        uxCdpInterfaces.set_on_selection_change_event(self._onCdpInterfaceChanged)
        self._ui.add("uxCdpInterfaces", uxCdpInterfaces)

        uxCdpDetail = self._ui.root.add_scroll_menu('Neighbor', 1, 1, column_span=2, row_span=2)
        self._ui.add("uxCdpDetail", uxCdpDetail)

