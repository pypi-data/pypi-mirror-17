"""Abstract class for various clients"""

import json
import pkgutil
import logging
from abc import ABCMeta, abstractmethod
from past.builtins import basestring # pylint: disable=redefined-builtin

import jsonschema
from future.utils import with_metaclass

from jsonrpcclient import config, exceptions
from jsonrpcclient.request import Notification, Request
from jsonrpcclient.log import _log


class Client(with_metaclass(ABCMeta, object)):
    """Protocol-agnostic base class the clients. Subclasses should inherit and
    override ``_send_message``.

    :param endpoint: The server address.
    """

    # Request and response logs
    __request_log = logging.getLogger(__name__+'.request')
    __response_log = logging.getLogger(__name__+'.response')

    #: Validate the response message
    __validator = jsonschema.Draft4Validator(json.loads(pkgutil.get_data(
        __name__, 'response-schema.json').decode('utf-8')))

    def __init__(self, endpoint):
        #: Holds the server address
        self.endpoint = endpoint

    def _log_request(self, request, extra=None):
        """Log the JSON-RPC request before sending. Should be called by
        subclasses in :meth:`_send_message`, before sending.

        :param request: The JSON-RPC request string.
        :param extra: A dict of extra fields that may be logged.
        """
        if extra is None:
            extra = {}
        # Add endpoint to list of info to include in log message
        extra.update({'endpoint': self.endpoint})
        _log(self.__request_log, 'info', request, fmt='--> %(message)s',
             extra=extra)

    def _log_response(self, response, extra=None):
        """Log the JSON-RPC response after sending. Should be called by
        subclasses in :meth:`_send_message`, after receiving the response.

        :param response: The JSON-RPC response string.
        :param extra: A dict of extra fields that may be logged.
        """
        if extra is None:
            extra = {}
        # Add the endpoint to the log entry
        extra.update({'endpoint': self.endpoint})
        # Clean up the response for logging
        response = response.replace("\n", '').replace('  ', ' ') \
                .replace('{ ', '{')
        _log(self.__response_log, 'info', response, fmt='<-- %(message)s',
             extra=extra)

    def _process_response(self, response):
        """Processes the response and returns the 'result' portion if present.

        :param response: The JSON-RPC response string to process.
        :return: The response string, or None
        """
        if response:
            if isinstance(response, basestring):
                # Attempt to parse the response
                try:
                    response = json.loads(response)
                except ValueError:
                    raise exceptions.ParseResponseError()
            # Validate the response against the Response schema (raises
            # jsonschema.ValidationError if invalid)
            if config.validate:
                self.__validator.validate(response)
            if isinstance(response, list):
                # For now, just return the whole response
                return response
            else:
                # If the response was "error", raise to ensure it's handled
                if 'error' in response:
                    raise exceptions.ReceivedErrorResponse(
                        response['error'].get('code'),
                        response['error'].get('message'),
                        response['error'].get('data'))
                # else
                return response.get('result')
        # No response was given
        return None

    @abstractmethod
    def _send_message(self, request, **kwargs):
        """Used internally - send the request to the server. Override this
        method in the protocol-specific subclasses. Be sure to log both the
        request and response, and return the response.

        :param request: A JSON-RPC request, in dict format.
        :returns: The response (a string for requests, None for notifications).
        """

    def send(self, request, **kwargs):
        """Send a request, passing the whole JSON-RPC `request object
        <http://www.jsonrpc.org/specification#request_object>`_.


            >>> client.send({'jsonrpc': '2.0', 'method': 'ping', 'id': 1})
            --> {"jsonrpc": "2.0", "method": "ping", "id": 1}
            <-- {"jsonrpc": "2.0", "result": "pong", "id": 1}
            'pong'

        :param request: The JSON-RPC request.
        :type request: string or a JSON serializable object
        :param kwargs: For HTTPClient, these are passed on to
            `requests.Session.send()
            <http://docs.python-requests.org/en/master/api/#requests.Session.send>`_.
        :returns: The payload (i.e. the ``result`` part of the response, or
            ``None`` in the case of a Notification).
        :rtype: A `JSON-decoded object
            <https://docs.python.org/library/json.html#json-to-py-table>`_.
        :raises ParseResponseError:
            The response was not valid JSON.
        :raises ValidationError:
            The response was valid JSON, but not valid JSON-RPC.
        :raises ReceivedErrorResponse:
            The server responded with a JSON-RPC `error object
            <http://www.jsonrpc.org/specification#error_object>`_.
        """
        # Convert request to a string
        if not isinstance(request, basestring):
            request = json.dumps(request)
        # Call internal method to transport the message
        response = self._send_message(request, **kwargs)
        return self._process_response(response)

    # Alternate ways to send a request -----------

    def notify(self, method_name, *args, **kwargs):
        """Send a JSON-RPC request, without expecting a response.

        :param method_name: The remote procedure's method name.
        :param args: Positional arguments passed to the remote procedure.
        :param kwargs: Keyword arguments passed to the remote procedure.
        :return: The payload (i.e. the ``result`` part of the response).
        """
        return self.send(Notification(method_name, *args, **kwargs))

    def request(self, method_name, *args, **kwargs):
        """Send a request, by passing the method and arguments. This is the main
        public method.

            >>> client.request('cat', name='Mittens')
            --> {"jsonrpc": "2.0", "method": "cat", "params": {"name": "Mittens"}, "id": 1}
            <-- {"jsonrpc": "2.0", "result": "meow", "id": 1}
            'meow'

        :param method_name: The remote procedure's method name.
        :param args: Positional arguments passed to the remote procedure.
        :param kwargs: Keyword arguments passed to the remote procedure.
        :return: The payload (i.e. the ``result`` part of the response).
        """
        return self.send(Request(method_name, *args, **kwargs))

    def __getattr__(self, name):
        """This gives us an alternate way to make a request::

            >>> client.cube(3)
            27

        That's the same as saying ``client.request('cube', 3)``.

        Technique is explained here: http://code.activestate.com/recipes/307618/
        """
        def attr_handler(*args, **kwargs):
            """Call self.request from here"""
            return self.request(name, *args, **kwargs)
        return attr_handler
