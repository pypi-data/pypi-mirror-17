import logging

from tornado import gen, concurrent

from zoonado import exc

from .data_watcher import DataWatcher
from .recipe import Recipe


log = logging.getLogger(__name__)


class Counter(Recipe):

    sub_recipes = {
        "watcher": DataWatcher
    }

    def __init__(self, base_path, use_float=False):
        super(Counter, self).__init__(base_path)

        self.value = None

        if use_float:
            self.numeric_type = float
        else:
            self.numeric_type = int

        self.value_sync = concurrent.Future()

    @gen.coroutine
    def start(self):
        self.watcher.add_callback(self.base_path, self.data_callback)
        yield gen.moment

        yield self.ensure_path()

        raw_value = yield self.client.get_data(self.base_path)
        self.value = self.numeric_type(raw_value or 0)

    def data_callback(self, new_value):
        self.value = self.numeric_type(new_value)
        if not self.value_sync.done():
            self.value_sync.set_result(None)
            self.value_sync = concurrent.Future()

    @gen.coroutine
    def set_value(self, value, force=True):
        data = str(value)
        yield self.client.set_data(self.base_path, data, force=force)
        log.debug("Set value to '%s': successful", data)
        yield self.value_sync

    @gen.coroutine
    def apply_operation(self, operation):
        success = False
        while not success:
            data = str(operation(self.value))
            try:
                yield self.client.set_data(self.base_path, data, force=False)
                log.debug("Operation '%s': successful", operation.__name__)
                yield self.value_sync
                success = True
            except exc.BadVersion:
                log.debug(
                    "Operation '%s': version mismatch, retrying",
                    operation.__name__
                )
                yield self.value_sync

    @gen.coroutine
    def incr(self):

        def increment(value):
            return value + 1

        yield self.apply_operation(increment)

    @gen.coroutine
    def decr(self):

        def decrement(value):
            return value - 1

        yield self.apply_operation(decrement)

    @gen.coroutine
    def stop(self):
        self.watcher.remove_callback(self.base_path, self.data_callback)
