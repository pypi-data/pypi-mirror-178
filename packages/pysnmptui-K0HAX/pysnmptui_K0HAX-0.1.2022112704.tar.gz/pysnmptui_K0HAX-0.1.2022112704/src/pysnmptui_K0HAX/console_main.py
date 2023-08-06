#!/usr/bin/env python3
from . import main
from .Configuration import Configuration
import argparse

class ArgumentError(Exception):
    pass

def console_main():
    parser = argparse.ArgumentParser(
            description = "Python SNMP TUI (Terminal User Interface)"
            )
    parser.add_argument('-H', '--host', help="SNMP Host")
    parser.add_argument('-u', '--user', help="SNMP Username")
    parser.add_argument('-p', '--authpass', help="SNMP Auth Password")
    parser.add_argument('-x', '--privpass', help="SNMP Encryption (priv) Password")
    parser.add_argument('-v', '--version', choices=["3"], default="3", help="SNMP Version")
    parser.add_argument('-c', '--config', help="Configuration file")
    args = parser.parse_args()
    config = None
    host = None
    version = None
    userName = None
    authPass = None
    privPass = None
    extraMibs = []

    if args.config != None:
        config = Configuration(args.config)
        host = config.Host
        version = config.Version
        userName = config.SecName
        authPass = config.AuthPassword
        privPass = config.PrivPassword
        extraMibs = config.ExtraMibs

    print(args.config)
    print(config)
    print(host)
    print(version)

    if (host == None) and (args.host != None):
        host = args.host
    elif (host == None) and (args.host == None):
        raise ArgumentError
    else:
        pass

    if (host == None) and (args.user != None):
        userName = args.SecName
    elif (userName == None) and (args.SecName == None):
        raise ArgumentError
    else:
        pass

    if (authPass == None) and (args.authpass != None):
        authPass = args.authpass
    elif (authPass == None) and (args.authpass == None):
        raise ArgumentError
    else:
        pass

    if (privPass == None) and (args.privpass != None):
        privPass = args.privpass
    elif (privPass == None) and (args.privpass == None):
        raise ArgumentError
    else:
        pass

    if (version == None):
        version = args.version

    if version == "3":
        version = 3
    main(
        host,
        userName,
        authPass,
        privPass,
        version,
        extraMibs)

if __name__ == "__main__":
    console_main()

