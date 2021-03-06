from persimmon.view.util import CircularButton, Connection
#from persimmon.backend import Test
from kivy.properties import ObjectProperty
from kivy.lang import Builder
from kivy.graphics import Color, Ellipse, Line
from persimmon.view.util import Type, AbstractWidget
from abc import abstractmethod


Builder.load_file('view/util/pin.kv')

class Pin(CircularButton, metaclass=AbstractWidget):
    val = ObjectProperty(None, force_dispatch=True)
    block = ObjectProperty()
    ellipse = ObjectProperty()
    line = ObjectProperty()
    _type = ObjectProperty(Type.ANY) 

    def on__type(self, instance, value):
        """ If the kv lang was a bit smarted this would not be needed
        """
        self.color = value.value
    
    @abstractmethod
    def on_touch_down(self, touch):
        raise NotImplementedError
    
    @abstractmethod
    def on_touch_up(self, touch):
        raise NotImplementedError
    
    @abstractmethod
    def on_connection_delete(self, connection: Connection):
        raise NotImplementedError

    def typesafe(self, other: 'Pin') -> bool:
        if ((self._type == Type.ANY or other._type == Type.ANY) and
                self.block != other.block and self.__class__ != other.__class__):
            return True  # Anything is possible with ANY
        else:
            return self._type == other._type and self.block != other.block and self.__class__ != other.__class__
