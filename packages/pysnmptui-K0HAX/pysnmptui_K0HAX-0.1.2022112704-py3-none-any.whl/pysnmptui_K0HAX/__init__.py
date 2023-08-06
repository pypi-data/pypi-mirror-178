#!/usr/bin/env python3
from .snmp import SnmpUI
import argparse
import sys

def NotApplicationError(Exception):
    pass

def Exit():
    sys.exit(0)

def main(
        host,
        userName,
        authPass,
        privPass,
        version=3,
        extraMibs=[]
        ):
    myUI = SnmpUI(
        host,
        version,
        userName,
        authPass,
        privPass,
        extraMibs)
    myUI.run()

if __name__ == "__main__":
    raise NotApplicationError
