#!/usr/bin/env python3
from .snmp import SnmpUI, Client
import argparse
import sys

def Exit():
    sys.exit(0)

def main(
        host,
        userName,
        authPass,
        privPass,
        version=3
        ):
    myUI = SnmpUI()
    myUI.setSNMP(
            host=host,
            version=version,
            userName=userName,
            authPass=authPass,
            privPass=privPass
            )
    myUI.run()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
            prog = "snmpui",
            description = "Python SNMP TUI (Terminal User Interface)"
            )
    parser.add_argument('-H', '--host', required=True, help="SNMP Host")
    parser.add_argument('-u', '--user', required=True, help="SNMP Username")
    parser.add_argument('-p', '--authpass', required=True, help="SNMP Auth Password")
    parser.add_argument('-x', '--privpass', required=True, help="SNMP Encryption (priv) Password")
    parser.add_argument('-v', '--version', choices=["3"], default="3", help="SNMP Version")
    args = parser.parse_args()
    host = args.host
    userName = args.user
    authPass = args.authpass
    privPass = args.privpass
    version = args.version
    if version == "3":
        version = 3
    main(
            host,
            userName,
            authPass,
            privPass,
            version
            )
