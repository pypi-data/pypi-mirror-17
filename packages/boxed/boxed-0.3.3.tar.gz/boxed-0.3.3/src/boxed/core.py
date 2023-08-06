import io
import os
import pwd
import sys
import builtins
import importlib
import contextlib
import collections
import traceback
import base64


def _sendpickle_factory(pickler):
    def sendpickle(self, data):
        lib = importlib.import_module(pickler)
        data = lib.dumps(data)
        self.sendsafe(data)
    sendpickle.__name__ = 'send' + pickler

    return sendpickle


def _recvpickle_factory(pickler):
    def recvpickle(self):
        try:
            lib = self.picklers[pickler]
        except KeyError:
            lib = self.picklers[pickler] = importlib.import_module(pickler)
        data = self.recvsafe()
        return lib.loads(data)
    recvpickle.__name__ = 'recv' + pickler

    return recvpickle

# We store these here in case someone messes with the system's builtins
# This happens with the ejudge engine since it messes with these functions in
# order to capture inputs and outputs from a program.
_python_input_function = input
_python_print_function = print


class CommunicationPipe:
    """
    A simple communication link between two programs based on sending and
    receiving messages in the stdin and stdout streams.
    """

    def __init__(self, stdout=None, stdin=None, serializer='pickle',
                 encoding='utf8'):
        self.serializer = serializer
        self.stdout = stdout
        self.stdin = stdin
        self.encoding = encoding
        self.picklers = {}

    @property
    def serializer(self):
        return self._default

    @serializer.setter
    def serializer(self, value):
        try:
            self._default_sender = getattr(self, 'send%s' % value)
            self._default_receiver = getattr(self, 'recv%s' % value)
            self._default = value
        except AttributeError:
            raise ValueError('invalid method')

    def senderror(self, ex):
        """Sends an exception"""

        if self.serializer == 'json':
            self.send({
                '@error': type(ex).__name__,
                '@message': str(ex),
            })
        else:
            self.send(ex)

    def recvcheck(self):
        """Receive and check if some error were raised."""

        data = self.recv()
        if self.serializer == 'json' and data and isinstance(data, dict):
            if '@error' in data:
                exception = getattr(builtins, data['@error'])
                if (isinstance(exception, type) and
                        issubclass(exception, Exception)):
                    raise exception(data['@message'])
        else:
            if isinstance(data, Exception):
                raise data
        return data

    def sendraw(self, st):
        """Send a raw string of text. The other end must read it using
        the recvraw() function."""

        st = self.as_str(st)

        if '\n' in st or '\r\f' in st:
            raise ValueError('cannot send strings with newline characters')
        _python_print_function(st, file=self.stdout or sys.stdout)

    def recvraw(self):
        """Receives a raw stream sent by sendraw()."""

        if self.stdin is None:
            return _python_input_function()
        else:
            return self.stdin.readline().rstrip('\n')

    def sendnumber(self, number):
        """Sends numeric data. The other end must read it with recvnumber()"""

        import numbers

        if not isinstance(number, numbers.Number):
            raise ValueError('not a number: %r' % number)

        self.sendraw(str(number))

    def recvnumber(self):
        """Receives a number sent by sendnumber()"""

        data = self.recvraw()
        try:
            return int(data)
        except ValueError:
            try:
                return float(data)
            except ValueError:
                return complex(data)

    def sendjson(self, data):
        """Sends data by converting it to JSON stream."""

        import json

        self.sendraw(json.dumps(data))

    def recvjson(self):
        """Receive data sent by sendjson."""

        import json

        data = self.recvraw()
        return json.loads(data)

    def sendsafe(self, data):
        """Encode an arbitrary string into a safe form to pass to print()"""

        import base64

        data = base64.b85encode(self.as_bytes(data))
        return self.sendraw(data)

    def recvsafe(self):
        """Receive stream from sendsafe()"""

        import base64

        data = self.as_bytes(self.recvraw())
        return base64.b85decode(data)

    # Pickle support
    sendpickle = _sendpickle_factory('pickle')
    sendcloudpickle = _sendpickle_factory('cloudpickle')
    senddill = _sendpickle_factory('dill')
    recvpickle = _recvpickle_factory('pickle')
    recvcloudpickle = _recvpickle_factory('cloudpickle')
    recvdill = _recvpickle_factory('dill')

    def as_bytes(self, x):
        if isinstance(x, bytes):
            return x
        else:
            return x.encode(self.encoding)

    def as_str(self, x):
        if isinstance(x, str):
            return x
        else:
            return x.decode(self.encoding)

    def send(self, data):
        """Sends an arbitrary python data over the default stream."""

        self._default_sender(data)

    def recv(self):
        """Receives data sent by ty send(data) function."""

        return self._default_receiver()

    def prepare(self, data):
        """Prepare some data with the default send method that can later be
        sent using sendraw(). The other side of the connection should receive
        data using the recv() method normally"""

        buffer = []
        try:
            self.sendraw = buffer.append
            self.send(data)
        finally:
            del self.sendraw
        return buffer[0]


#
# Specialized error classes
#
class SerializationError(ValueError):
    """Triggered when pickle or other serializer fails."""


#
# Utility functions
#
real_stdout = sys.stdout
global_serializer = None
global_deserializer = None


# Maps exception names to their corresponding classes
exceptions = {
    k: v
    for k, v in vars(builtins).items()
    if isinstance(v, type) and issubclass(v, Exception)
}
exceptions['SerializationError'] = SerializationError


def indent(msg, indent):
    """Indent message"""

    prefix = ' ' * indent
    return '\n'.join(prefix + line for line in msg.splitlines())


def real_print(*args, **kwargs):
    """
    Prints to the real stdout, ignoring the value in sys.stdout.
    """

    kwargs.setdefault('file', real_stdout)
    print(*args, **kwargs)


def set_serializer(func):
    """
    Sets the default serializer function.

    This function should only be used by a __main__.py script running a sandbox.
    """

    global global_serializer

    global_serializer = func


def set_deserializer(func):
    """
    Sets the default de-serializer function.

    This function should only be used by a __main__.py script running a sandbox.
    """

    global global_deserializer

    global_deserializer = func


def set_protocol(name):
    """
    Sets the global serializer and de-serializer functions.


    This function should only be used by a __main__.py script running a sandbox.
    """

    global global_serializer, global_deserializer
    global_serializer = get_serializer(name)
    global_deserializer = get_deserializer(name)


def load_data():
    """
    Loads data using the global de-serializer.

    This function should only be used by a __main__.py script running a sandbox.
    """

    if global_deserializer is None:
        raise SystemExit('global de-serializer was not set')

    return global_deserializer(input())


def send_data(data):
    """
    Sends data using the global serializer.

    This function should only be used by a __main__.py script running a sandbox.
    """

    if global_serializer is None:
        raise SystemExit('global serializer was not set')

    try:
        serialized = global_serializer(data)
    except Exception as ex:
        raise SerializationError(ex)
    real_print(serialized)


def END_POINT(data):
    """Sends data using the global serializer and finish execution with a
    success exit code."""

    send_data(data)
    raise SystemExit(0)


def comment(*args, symbol='# ', **kwargs):
    """Sends a paragraph prepended by the comment symbol."""

    with capture_print() as st:
        data = '\n'.join(symbol + x for x in st.splitlines())
    real_print(symbol, *args, **kwargs)


# noinspection PyMissingConstructor
class FileString(collections.UserString):
    """
    A string-like object that is initialized with the contents of a file object
    inside a context manager.
    """

    def __init__(self, file):
        self.file = file
        self._data = None

    @property
    def data(self):
        if self._data is None:
            self._data = self.file.getvalue()
        return self._data


@contextlib.contextmanager
def capture_print():
    """Context manager that captures data printed to stdout into a
    string-like object."""

    old_stdout = sys.stdout
    try:
        sys.stdout = io.StringIO()
        yield FileString(sys.stdout)
    finally:
        sys.stdout = old_stdout


def validate_target(data, handshake):
    """
    Returns a validated target function.

    If handshake is invalid, terminate execution with an invalid-handshake
    status.

    Import all requested modules if data contains an "import" clause.
    """

    if data['header'] != handshake:
        END_POINT({
            'status': 'invalid-handshake',
            'handshake': handshake,
        })
    comment('handshake: %r' % data['header'])

    # Import all requested modules
    for mod in data.get('imports', ()):
        try:
            importlib.import_module(mod)
        except ImportError:
            END_POINT({
                'status': 'invalid-import',
                'module': mod,
            })
    comment('all modules successfully imported')

    # If the target attribute is a callable, simply return it
    target = data['target']
    if callable(target):
        return target

    # If it is a path string, we load the proper target function in the given
    # location.
    mod, _, func = data['target'].rpartition('.')
    try:
        mod = importlib.import_module(mod)
        target = getattr(mod, func)
    except ImportError as ex:
        END_POINT({
            'status': 'invalid-target',
            'message':
                'could not import module %r. Maybe it must be passed it to '
                'the "imports" argument.' % mod,
        })
    except AttributeError:
        END_POINT({
            'status': 'invalid-target',
            'message':
                'could not find function "%s" in module %s' % (func, mod),
        })
    comment('target function loaded as %s' % target)
    return target


def lower_privileges(username):
    """
    Sets the UID of the current process to the uid of the given username.
    """

    try:
        if username == 'root':
            raise PermissionError
        userinfo = pwd.getpwnam(username)
    except (KeyError, PermissionError):
        END_POINT({
            'status': 'invalid-user',
            'user': username,
        })
    else:
        os.setuid(userinfo.pw_uid)
        comment('changed to user %s, (uid=%s)' % (username, userinfo.pw_uid))


def execute_target(target, args, kwargs, send_exception=False):
    """
    Executes target function with the given args and kwargs.

    If target raise an exception, it executes an END_POINT that sends a
    dictionary with exception data. If send_exception = True, it includes the
    actual exception in the 'exception' key of this dictionary.
    """

    output = None

    with capture_print() as stdout:
        try:
            output = target(*args, **kwargs)
            comment('target function %s successfully executed' % target)
        except Exception as ex:
            tb_data = io.StringIO()
            traceback.print_tb(ex.__traceback__, limit=-3, file=tb_data)
            exc_data = {
                'status': 'exception',
                'type': ex.__class__.__name__,
                'message': str(ex),
                'traceback': tb_data.getvalue(),
                'target': '%s.%s' % (target.__module__, target.__name__),
            }
            if send_exception:
                exc_data['exception'] = ex
            END_POINT(exc_data)

    return {
        'status': 'success',
        'stdout': str(stdout),
        'output': output,
    }


def return_from_status_data(data):
    """Interpret status data sent from the __main__.py script and return the
    correct value or raise the corresponding exception."""

    if 'status' not in data:
        raise RuntimeError('subprocess returned an invalid message')
    status = data['status']

    if status == 'success':
        print(data.get('stdout', ''), end='')
        return data['output']

    elif status == 'invalid-handshake':
        raise RuntimeError(
            'the version of boxed installed in the subprocess is invalid.\n'
            'Handshake message: %s' % data['handshake']
        )

    elif status == 'invalid-user':
        if data['user'] == 'root':
            raise PermissionError('cannot run as superuser')
        else:
            raise PermissionError('user does not exist: %s' % data['user'])

    elif status == 'invalid-target':
        raise RuntimeError(data['message'])

    elif status == 'exception':
        print('Error while running sandboxed function %s(...)' %
              data['target'])
        print(data['traceback'], end='')

        try:
            exc = exceptions[data['type']]
            msg = data['message']
            raise exc(msg)
        except KeyError:
            data = '%s(%r)' % (data['type'], data['message'])
            raise RuntimeError('failed with unknown exception: %s' % data)

    elif status == 'serialization-error':
        raise SerializationError(
            'output could not be converted to JSON: %s' % data['output']
        )

    elif status == 'invalid-import':
        raise ImportError(
            'could not import module %r' % data['module']
        )

    else:
        raise RuntimeError('invalid status: %s' % status)


def execute_subprocess(command, inputs, *, timeout, target, args, kwargs):
    """Assure that subprocess did not raised any errors."""

    from subprocess import Popen, PIPE

    proc = Popen(command,
                 stdin=PIPE, stdout=PIPE, stderr=PIPE,
                 universal_newlines=True)
    out, err = proc.communicate(input=inputs, timeout=timeout)

    if err:
        raise RuntimeError(
            'error running function %s with:\n'
            '    args=%r\n'
            '    kwargs=%r\n\n'
            'Process returned code %s.\n'
            'Stdout:\n%s\n'
            'Error message:\n%s' % (
                target, args, kwargs, proc.poll(),
                indent(out or '<empty>', 4),
                indent(err or '<empty>', 4)
            )
        )

    # We remove all comments and send a separate comments and data sections
    data = '\n'.join(
        line for line in out.splitlines() if not line.startswith('#')
    ).strip()
    comments = '\n'.join(
        line for line in out.splitlines() if line.startswith('#')
    ).strip()

    # A data section must always be present
    if not data:
        raise RuntimeError('subprocess returned an empty response:\n%s' %
                           indent(out, 4))
    return data, comments


def get_serializer(name):
    """Return the serialization function from name."""

    dumps = importlib.import_module(name).dumps

    # Serializers that handle unicode streams and a are safe against comments
    # can be used directly
    if name == 'json':
        import json
        return json.dumps

    def serializer(x):
        # Serialize
        try:
            data = dumps(x)
        except Exception as ex:
            raise SerializationError(ex)

        # Transmit with b85 encode: safe characters and no newlines
        return (b'+' + base64.b85encode(data)).decode('ascii')

    return serializer


def get_deserializer(name):
    """Return the de-serialization function from name."""

    loads = importlib.import_module(name).loads

    # Serializers that handle unicode streams and a are safe against comments
    # can be used directly
    if name == 'json':
        import json
        return json.loads

    def deserializer(x):
        # Load base85 bytes data
        x = x[1:].encode('ascii')
        x = base64.b85decode(x)
        try:
            return loads(x)
        except Exception as ex:
            raise SerializationError(ex)

    return deserializer
