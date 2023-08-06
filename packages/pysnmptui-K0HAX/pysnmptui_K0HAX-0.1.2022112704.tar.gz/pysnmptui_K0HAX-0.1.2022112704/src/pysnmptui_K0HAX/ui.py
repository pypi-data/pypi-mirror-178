import py_cui
import sys
import json

from .Client import Client

class UiWidgetSetDoesNotExistError(Exception):
    pass

class UiObjectExistsError(Exception):
    pass

class UI:
    _ui_objects = {}
    _ui_widget_sets = {}

    @property
    def root(self):
        return self._root

    def add(self, name, widget):
        if name in self._ui_objects.keys():
            raise UiObjectExistsError
        self._ui_objects[name] = widget

    def get(self, name):
        return self._ui_objects[name]

    def add_screen(self, name, x=2, y=2):
        newScreen = UIScreen(self._root.create_new_widget_set(y, x), x, y)
        self._ui_widget_sets[name] = newScreen
        return self._ui_widget_sets[name]

    def activate_screen(self, name):
        if name not in self._ui_widget_sets.keys():
            raise UiWidgetSetDoesNotExistError
        self._root.apply_widget_set(self._ui_widget_sets[name]._root)

    def start(self):
        self._root.start()

    def __init__(self,
            x=2,
            y=2):
        self._root = py_cui.PyCUI(x, y)
        self._root.set_title(sys.argv[0])

class UIScreen(UI):
    def update_grid_height_width(self, height, width):
        self._root._grid.set_num_rows(height)
        self._root._grid.set_num_cols(width)

    def __init__(self,
                 uiScreen,
                 x=2,
                 y=2):
        self._root = uiScreen
        self.update_grid_height_width(y, x)

class UiWindow:
    clientType = Client
    clients = {}
    snmp_data = {}

    def __exit(self):
        sys.exit(0)

    def _printDict(self, data):
        strData = json.dumps(data, indent=2, default=str)
        retval = strData.splitlines()
        return retval

    def _setSNMP(self, clientType, host, version, userName, authPass, privPass, extraMibs):
        return self.clientType(
            host=host,
            version=3,
            userName=userName,
            authPass=authPass,
            privPass=privPass,
            extraMibs=extraMibs
            )

    def setSNMP(self, host, version, userName, authPass, privPass, extraMibs):
        self.clients[host] = self._setSNMP(
            clientType,
            host=host,
            version=3,
            userName=userName,
            authPass=authPass,
            privPass=privPass,
            extraMibs=extraMibs
            )

    def __init__(self):
        self._ui = UI(x=4, y=3)

class MenuValue:
    def __init__(self, key, val):
        self._key = key
        self._val = val

    def get(self):
        return self._val

    def __str__(self):
        return self._key
