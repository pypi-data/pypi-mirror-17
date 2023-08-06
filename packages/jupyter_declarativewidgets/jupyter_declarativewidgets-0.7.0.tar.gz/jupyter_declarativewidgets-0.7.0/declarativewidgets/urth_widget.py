# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
import time
import logging

from ipywidgets import widgets  # Widget definitions
import traceback

class UrthWidget(widgets.Widget):
    """ A base class for Urth widgets. """

    def __init__(self, **kwargs):
        super(UrthWidget, self).__init__(**kwargs)

    def get_state(self, key=None):
        """
        In general, urth widgets don't have initial state
        """
        return {}

    def _send_update(self, attribute, value):
        """
        Sends a message to update the front-end state of the given attribute.
        """
        msg = {
            "method": "update",
            "state": {
                attribute: value
            }
        }
        self._send(msg)

    def send_status(self, status, msg=""):
        """
        Sends a message to inform the front-end of the execution status.

        Parameters
        ----------
        status : string
            "ok" for success, "error" for failure.
        msg : string
            Message accompanying the status, e.g. an error message.
        """
        self._send({
            "method": "update",
            "state": {
                "__status__": {
                    "status": status,
                    "msg": msg,
                    "timestamp": round(time.time() * 1000)
                }
            }
        })

    def error(self, error):
        """
        Inform the front-end that an error occurred, with the given error msg.
        Parameters
        ----------
        error: string or exception
        """
        self.send_status("error", str(error))
        self.log.error(traceback.format_exc())

    def ok(self, msg=""):
        """
        Inform the front-end that processing succeeded.
        Parameters
        ----------
        msg : string
            An optional message.
        """
        self.send_status("ok", msg)