import logging
import json

from taskqueue.workitem import Workitem as BaseWorkitem
from taskqueue.workitem import WorkitemError as BaseWorkitemError

LOG = logging.getLogger(__name__)

class WorkitemError(BaseWorkitemError):
    pass

class Workitem(BaseWorkitem):
    """Workitem specific to Bureaucrat."""

    mime_type = 'application/x-bureaucrat-workitem'

    @staticmethod
    def create(process_id, event_name):
        self = Workitem()
        self._body = {
            "fei": {
                "origin": '',
                "pid": process_id,
                "event_name": event_name,
                "target": '',
                "worker_type": None
            },
            "fields": {
            }
        }
        return self

    def _assert_body(self):
        """Make sure body is loaded."""
        if self._body is None:
            raise WorkitemError("Workitem hasn't been loaded")

    def loads(self, blob):
        try:
            self._body = json.loads(blob)
            assert self._body["fei"]["origin"] is not None
            assert self._body["fei"]["pid"] is not None
            assert self._body["fields"] is not None
        except (ValueError, KeyError, TypeError, AssertionError):
            raise WorkitemError("Can't parse workitem body")

    def dumps(self):
        self._assert_body()
        return json.dumps(self._body)

    def set_error(self, error):
        self._assert_body()
        self._body["error"] = error

    def set_trace(self, trace):
        self._assert_body()
        self._body["trace"] = trace

    @property
    def pid(self):
        """Return process Id this workitem belongs to.

        This is a read only property.
        """

        self._assert_body()
        return self._body["fei"]["pid"]

    @property
    def origin(self):
        """Return flow expression ID this workitem originates from."""

        self._assert_body()
        return self._body["fei"]["origin"]

    @origin.setter
    def origin(self, new_origin):
        self._assert_body()
        self._body["fei"]["origin"] = new_origin

    @property
    def target(self):
        """Return flow expression ID this workitem targets to."""

        self._assert_body()
        return self._body["fei"]["target"]

    @target.setter
    def target(self, new_target):
        """Update workitem's target."""

        self._assert_body()
        self._body["fei"]["target"] = new_target

    @property
    def fields(self):
        """Return workitem's fields accessible by workers."""

        self._assert_body()
        return self._body["fields"]

    @property
    def event_name(self):
        """Return workitem's event name."""

        self._assert_body()
        return self._body["fei"]["event_name"]

    @event_name.setter
    def event_name(self, new_name):
        """Setter for event_name."""
        self._assert_body()
        self._body["fei"]["event_name"] = new_name

    @property
    def worker_type(self):
        """Return type of worker this workitem was sent to."""

        self._assert_body()
        return self._body["fei"]["worker_type"]

    @worker_type.setter
    def worker_type(self, wtype):
        """Setter for worker_type."""

        self._assert_body()
        self._body["fei"]["worker_type"] = wtype
