import yaml
import json

class Configuration:
    _filename = None
    ExtraMibs = []
    Host = None
    Version = None
    SecName = None
    AuthProto = None
    AuthPassword = None
    PrivProto = None
    PrivPassword = None

    def __str__(self):
        data = {
            'Host': self.Host,
            'Version': self.Version,
            'Username': self.SecName,
            'AuthProto': self.AuthProto,
            'AuthPassword': self.AuthPassword,
            'PrivProto': self.PrivProto,
            'PrivPassword': self.PrivPassword,
            'ExtraMibs': self.ExtraMibs
            }
        return json.dumps(data)

    def save(self):
        data = {
            'Host': self.Host,
            'Version': self.Version,
            'Username': self.SecName,
            'AuthProto': self.AuthProto,
            'AuthPassword': self.AuthPassword,
            'PrivProto': self.PrivProto,
            'PrivPassword': self.PrivPassword,
            'ExtraMibs': self.ExtraMibs
            }
        with open(filename, 'w') as f:
            yaml.dump(data, f)

    def _parseconfig(self, data):
        self.ExtraMibs = data.get('ExtraMibs')
        self.Host = data.get('Host')
        self.Version = data.get('Version')
        self.SecName = data.get('Username')
        self.AuthProto = data.get('AuthProto')
        self.AuthPassword = data.get('AuthPassword')
        self.PrivProto = data.get('PrivProto')
        self.PrivPassword = data.get('PrivPassword')

    def __init__(self, filename):
        data = None
        self._filename = filename
        with open(filename, 'r') as f:
            data = yaml.safe_load(f)
            self._parseconfig(data)
