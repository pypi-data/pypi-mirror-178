# pysnmptui

Python SNMP TUI (Terminal User Interface)

## Configuration

You can use a configuration file instead of command line flags.

Invoke pysnmptui with `pysnmptui -c config.yaml` if your config file is named "config.yaml" and in the current directory.

Below is an example config.yaml.

```
Host: 127.0.0.1
Username: v3user
AuthProto: SHA
AuthPassword: password
PrivProto: AES
PrivPassword: password
Version: 3
ExtraMibs:
  - IF-MIB
  - ENTITY-MIB
  - ./mibs/CISCO-SMI
  - ./mibs/CISCO-TC
  - ./mibs/CISCO-IF-EXTENSION-MIB
  - ./mibs/CISCO-VTP-MIB
  - ./mibs/CISCO-CDP-MIB
```
