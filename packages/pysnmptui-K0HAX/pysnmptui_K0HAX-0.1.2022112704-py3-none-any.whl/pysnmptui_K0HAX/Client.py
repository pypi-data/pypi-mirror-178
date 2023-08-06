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
