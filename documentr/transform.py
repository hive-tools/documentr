from abc import ABCMeta, abstractmethod


class Transform:
    __metaclass__ = ABCMeta

    def __init__(self, table):
        self._table = table

    @abstractmethod
    def transform(self):
        raise Exception("Method not implemented")


class JSONTransform(Transform):
    def transform(self):
        print "Hello"
        exit()