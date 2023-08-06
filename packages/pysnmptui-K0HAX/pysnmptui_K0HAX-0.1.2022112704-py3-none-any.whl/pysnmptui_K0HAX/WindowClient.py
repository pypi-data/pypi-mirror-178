from snimpy import manager
import sys
import json

class WindowClient:
    # M will become the SNMP Manager provided by snimpy
    M = None

    host = None
    community = None
    version = None
    port = 161

    def _doTryGet(self, func, i):
        m = self.M
        try:
            return m.__getattribute__(func)[i]
        except Exception as e:
            print(e)
            return None

    def __init__(self,
                 host,
                 version,
                 community=None,
                 userName=None,
                 authPass=None,
                 privPass=None,
                 authProtocol="SHA",
                 privProtocol="AES",
                 port=161,
                 extraMibs=[]
                 ):
        self.host = host
        self.community = community
        self.version = version
        self.port = port
        print(f"Extra MIBs: {json.dumps(extraMibs)}", file=sys.stderr)
        for mib in extraMibs:
            print(f"Loading: {mib}", file=sys.stderr)
            manager.load(mib)
        self.M = manager.Manager(
            host=host,
            version=version,
            secname=userName,
            authprotocol=authProtocol,
            authpassword=authPass,
            privprotocol=privProtocol,
            privpassword=privPass
            )
