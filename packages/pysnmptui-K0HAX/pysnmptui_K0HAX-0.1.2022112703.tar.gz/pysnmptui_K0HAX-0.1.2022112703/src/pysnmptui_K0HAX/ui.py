import py_cui

class UiObjectExistsError(Exception):
    pass

class UI:
    _ui_objects = {}

    @property
    def root(self):
        return self._root

    def add(self, name, widget):
        if name in self._ui_objects.keys():
            raise UiObjectExistsError
        self._ui_objects[name] = widget

    def get(self, name):
        return self._ui_objects[name]

    def start(self):
        self._root.start()

    def __init__(self,
            x=2,
            y=2):
        self._root = py_cui.PyCUI(x, y)
