#!/usr/bin/env python3
from . import main
import argparse

def console_main():
    parser = argparse.ArgumentParser(
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
    snmpui.main(
            host,
            userName,
            authPass,
            privPass,
            version)

if __name__ == "__main__":
    console_main()

