import abc
import copy
import inspect
import json
import uuid

from .exceptions import CantParseLine, ExitContext
from .handlers import LineHandler, EmptyLineHandler, EchoLineHandler, ExitLineHandler, \
    ExactLineHandler, ArgparseLineHandler, RegexLineHandler


__all__ = (
    'CommandContext', 'MultiLineContext', 'JsonContext', 'StandardPrompt', 'PrebuiltCommandContext'
)


class CommandContext(metaclass=abc.ABCMeta):
    force_handlers = []

    def __init__(self, handlers=None, name='', ignore_force_handlers=False):
        # construct handler list
        self.handlers = copy.copy(handlers or [])
        if not ignore_force_handlers:
            self.handlers += [handler_class() for handler_class in self.force_handlers]

        self.name = name
        self.out_stream = None

        for handler in self.handlers:
            handler.set_context(self)

    def set_out_stream(self, out_stream):
        self.out_stream = out_stream

    def execute(self, line):
        """
        Try to interpret a line by applying every handler in the list until one succeeds.
        If none do, then execute the error handler self.on_cant_execute
        """
        for handler in self.handlers:
            try:
                return handler.try_execute(line)

            except CantParseLine:
                pass

        self.on_cant_execute(line)

    def write(self, text):
        """Write to the current output stream."""
        if self.out_stream:
            self.out_stream.write(text)
            self.out_stream.flush()

    def exit(self):
        raise ExitContext(self)

    def clone(self, *args, **kwargs):
        kwargs['ignore_force_handlers'] = True
        return self.__class__([handler.clone() for handler in self.handlers], *args, **kwargs)

    @abc.abstractmethod
    def prompt(self):
        raise NotImplementedError

    @abc.abstractmethod
    def on_cant_execute(self, line):
        raise NotImplementedError


class MultiLineContext(CommandContext):
    class FinishedHandler(LineHandler):
        @abc.abstractmethod
        def is_finished(self, line):
            raise NotImplementedError

        def try_execute(self, line):
            if self.is_finished(line):
                self.context.on_finished()

            else:
                self.context.to_buffer(line)

    class OverOn2EmptyLines(FinishedHandler):
        def __init__(self):
            super().__init__()
            self.empty_line_count = 0

        def is_finished(self, line):
            if not line.strip():
                self.empty_line_count += 1
                if self.empty_line_count > 1:
                    return True

            else:
                self.empty_line_count = 0

            return False

    def __init__(self, *args, **kwargs):
        self.force_handlers = [self.FinishedHandler]
        super().__init__(*args, **kwargs)
        self.buffer = ''

    def execute(self, line):
        super().execute(line)

    def to_buffer(self, line):
        self.buffer += line

    @abc.abstractmethod
    def on_finished(self):
        raise NotImplementedError


class JsonContext(MultiLineContext):
    FinishedHandler = MultiLineContext.OverOn2EmptyLines

    def __init__(self, *args, **kwargs):
        self.callback = kwargs.pop('callback', lambda data: None)
        self.error = kwargs.pop('error', lambda err: self.write('{0}\n'.format(str(err))))
        super().__init__(*args, **kwargs)

    def on_finished(self):
        try:
            data = json.loads(self.buffer)

        except ValueError as err:
            self.error(err)
            self.exit()
            return

        self.callback(data)
        self.exit()

    def prompt(self):
        self.write('... ')

    def on_cant_execute(self, line):
        pass


class StandardPrompt(CommandContext):
    force_handlers = [EmptyLineHandler, EchoLineHandler, ExitLineHandler]

    def prompt(self):
        if self.out_stream:
            if self.name:
                self.out_stream.write('{0} > '.format(self.name))
            else:
                self.out_stream.write('>>> ')
            self.out_stream.flush()

    def on_cant_execute(self, line):
        self.write('Invalid command: {0}'.format(line))


class PrebuiltCommandContext(CommandContext):

    def __init__(self, handlers=None, name=''):
        self._handler_class_arg_sets = {}
        methods = inspect.getmembers(self.__class__, predicate=inspect.isfunction)
        for method_tuple in methods:
            method = method_tuple[1]
            if getattr(method, '_bound_command', False):
                handler_class = method._handler_class
                handler_class_name = handler_class.__name__
                if handler_class_name not in self._handler_class_arg_sets:
                    self._handler_class_arg_sets[handler_class_name] = [
                        '{0}.{1}'.format(self.__class__, handler_class_name), (handler_class,), {}
                    ]

                redirect_method = (
                    lambda local_method: lambda handler_self, *args, **kwargs:
                    local_method(handler_self.context, *args, **kwargs)
                )(method)
                redirect_method._bound_command = True
                redirect_method._args = method._args
                redirect_method._kwargs = method._kwargs

                handler_method_name = 'generated_method_{}'.format(uuid.uuid4().hex)
                self._handler_class_arg_sets[handler_class_name][2][handler_method_name] = redirect_method

        handlers = copy.copy(handlers) or [] + [
            type(*handler_class_args)() for handler_class_args in self._handler_class_arg_sets.values()
        ]

        super().__init__(handlers=handlers, name=name)
