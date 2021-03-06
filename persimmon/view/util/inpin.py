from persimmon.view.util import Pin, Connection
from kivy.properties import ObjectProperty
import logging


logger = logging.getLogger(__name__)

class InputPin(Pin):
    origin = ObjectProperty(allownone=True)

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos) and touch.button == 'left':
            logger.info('Creating connection')
            touch.ud['cur_line'] = Connection(start=self,
                                              color=self.color)
            self.origin = touch.ud['cur_line']
            # Add to blackboard
            self.block.parent.parent.parent.add_widget(touch.ud['cur_line'])
            return True
        else:
            return False

    def on_touch_up(self, touch):
        if ('cur_line' in touch.ud.keys() and touch.button == 'left' and
                self.collide_point(*touch.pos)):
            if touch.ud['cur_line'].end and self.typesafe(touch.ud['cur_line'].end):
                logger.info('Establishing connection')
                touch.ud['cur_line'].finish_connection(self)
                self.origin = touch.ud['cur_line']
            else:
                logger.info('Deleting connection')
                touch.ud['cur_line'].delete_connection(self.block.parent.parent)
            return True
        else:
            return False

    def on_connection_delete(self, connection: Connection):
        self.origin = None

    def typesafe(self, other: Pin) -> bool:
        return super().typesafe(other) and self.origin == None
