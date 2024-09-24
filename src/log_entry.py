import json
from typing import Any, Dict, Optional
from datetime import datetime
import uuid

class LogEntry:
    def __init__(self):
        self.basic = BasicInfo()
        self.event = EventInfo()
        self.error = ErrorInfo()
        self.http = HttpInfo()
        self.trace = TraceInfo()
        self.additional_properties = {}

    def to_json(self) -> str:
        data = {}
        self._add_properties_to_dict(data, self.basic)
        self._add_properties_to_dict(data, self.event)
        self._add_properties_to_dict(data, self.error)
        self._add_properties_to_dict(data, self.http)
        self._add_properties_to_dict(data, self.trace)
        self._add_properties_to_dict(data, self.additional_properties)
        return json.dumps(data)

    def _add_properties_to_dict(self, data: Dict[str, Any], obj: Any):
        if obj is None:
            return

        if isinstance(obj, dict):
            for key, value in obj.items():
                if value is not None and str(value).strip():
                    data[key.lower()] = value
        else:
            for key, value in obj.__dict__.items():
                if value is not None and str(value).strip():
                    data[key.lower()] = value

    def add_property(self, key: str, value: Any):
        self.additional_properties[key] = value

class BasicInfo:
    def __init__(self):
        self.summary = None
        self.log_level_number = 0
        self.timestamp = datetime.utcnow()
        self.log_level = None
        self.message = None
        self.host_name = None
        self.service_name = None
        self.service_menu = None
        self.service_obj = None
        self.service_fun = None
        self.user_id = None
        self.user_name = None
        self.log_index = None

class EventInfo:
    def __init__(self):
        self.event_id = str(uuid.uuid4())
        self.event_kind = None
        self.event_category = None
        self.event_action = None
        self.event_outcome = None
        self.event_duration = None
        self.transaction_id = None

class ErrorInfo:
    def __init__(self):
        self.error_type = None
        self.error_message = None
        self.error_stack_trace = None

class HttpInfo:
    def __init__(self):
        self.http_request_method = None
        self.http_request_body_content = None
        self.http_response_status_code = None
        self.url_original = None

class TraceInfo:
    def __init__(self):
        self.trace_id = None
        self.span_id = None