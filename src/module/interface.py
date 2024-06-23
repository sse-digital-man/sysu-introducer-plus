from abc import ABCMeta
from framework import BasicModule as ModuleInterface


class BasicModule(ModuleInterface, metaclass=ABCMeta):
    pass
