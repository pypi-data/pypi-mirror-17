# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

from traitlets import Integer, Unicode # Used to declare attributes of our widget
from IPython.core.getipython import get_ipython

from .util.serializer import Serializer
from .util.functions import apply_with_conversion, signature_spec
from .urth_widget import UrthWidget
from .urth_exception import UrthException

from functools import reduce


class Function(UrthWidget):
    """
    A Widget for invoking a function on the kernel.
    """
    function_name = Unicode('', sync=True)
    limit = Integer(100, sync=True)

    def __init__(self, **kwargs):
        self.log.info("Created a new Function widget.")

        self.on_msg(self._handle_custom_event_msg)
        self.shell = get_ipython()
        self.serializer = Serializer()
        super(Function, self).__init__(**kwargs)

    def _function_name_changed(self, old, new):
        try:
            self.log.info("Binding to function name {}...".format(new))
            self._sync_state()
            self.ok()
        except Exception as e:
            self.error(e)

    def _handle_custom_event_msg(self, wid, content, buffers):
        event = content.get('event', '')
        if event == 'invoke':
            self._invoke(content.get('args', {}))
        elif event == 'sync':
            self._sync_state()

    def _the_function(self):
        try:
            name = self.function_name.split('.')
            return reduce(lambda x, y: getattr(x, y), [self.shell.user_ns[name.pop(0)]] + name)
        except (KeyError, AttributeError):
            raise UrthException("Invalid function name {}".format(
                self.function_name))

    def _invoke(self, args):
        self.log.info("Invoking function {} with args {}...".format(
            self.function_name, args))
        try:
            result = apply_with_conversion(self._the_function(), args)
            serialized_result = self.serializer.serialize(
                result, limit=self.limit)
            self._send_update("result", serialized_result)
            self.ok()
        except Exception as e:
            self.error("Error while invoking function: {}".format(str(e)))

    def _sync_state(self):
        try:
            signature = signature_spec(self._the_function())
            self._send_update("signature", signature)
        except Exception as e:
            self.error("Error while getting function signature: {}".format(str(e)))
