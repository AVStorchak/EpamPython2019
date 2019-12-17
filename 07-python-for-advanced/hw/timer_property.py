import time
import uuid


def timer_property(t):
    reset_interval = t

    class TimedProperty(object):
        def __init__(self, fget=None, fset=None, fdel=None, doc=None):
            self.fget = fget
            self.fset = fset
            self.fdel = fdel
            self.__doc__ = doc
            self.time = 0
            self.result = 0

        def __get__(self, obj, objtype=None):
            if obj is None:
                return self
            if self.fget is None:
                raise AttributeError("Unable to read attribute")
            if self.time == 0 or time.time() - self.time > reset_interval:
                self.result = self.fget(obj)
                self.time = time.time()
            return self.result

        def __set__(self, obj, value):
            if self.fset is None:
                raise AttributeError("Unable to set attribute")
            self.time = time.time()
            self.result = value

        def __delete__(self, obj):
            if self.fdel is None:
                raise AttributeError("Unable to delete attribute")
            self.fdel(obj)

        def getter(self, fget):
            return type(self)(fget, self.fset, self.fdel, self.__doc__)

        def setter(self, fset):
            return type(self)(self.fget, fset, self.fdel, self.__doc__)

        def deleter(self, fdel):
            return type(self)(self.fget, self.fset, fdel, self.__doc__)

    return TimedProperty


class Message:

    @timer_property(t=10)
    def msg(self):
        self._msg = self.get_message()
        return self._msg

    @msg.setter
    def msg(self, param):
        self._msg = param

    def get_message(self):
        """
        Return random string
        """
        return uuid.uuid4().hex
