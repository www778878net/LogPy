import json
from typing import Any, Dict, Optional
from datetime import datetime, timezone
import uuid
from dataclasses import dataclass, field

@dataclass
class BasicInfo:
    summary: str = ""
    message: Optional[str] = None
    log_level: str = "INFO"
    log_level_number: int = 30
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    service_name: Optional[str] = None
    service_obj: Optional[str] = None
    service_fun: Optional[str] = None
    user_id: Optional[str] = None
    user_name: Optional[str] = None

@dataclass
class EventInfo:
    event_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    event_kind: Optional[str] = None
    event_category: Optional[str] = None
    event_action: Optional[str] = None
    event_outcome: Optional[str] = None
    event_duration: Optional[float] = None
    transaction_id: Optional[str] = None

@dataclass
class ErrorInfo:
    error_type: Optional[str] = None
    error_message: Optional[str] = None
    error_stack_trace: Optional[str] = None

@dataclass
class HttpInfo:
    http_request_method: Optional[str] = None
    http_request_body_content: Optional[str] = None
    http_response_status_code: Optional[int] = None
    url_original: Optional[str] = None

@dataclass
class TraceInfo:
    trace_id: Optional[str] = None
    span_id: Optional[str] = None

class LogEntry:
    def __init__(self, basic: BasicInfo = None, event: EventInfo = None, error: ErrorInfo = None, http: HttpInfo = None, trace: TraceInfo = None):
        self.basic = basic if basic is not None else BasicInfo()
        self.event = event if event is not None else EventInfo()
        self.error = error if error is not None else ErrorInfo()
        self.http = http if http is not None else HttpInfo()
        self.trace = trace if trace is not None else TraceInfo()
        self.additional_properties: Dict[str, Any] = {}

    def to_json(self) -> str:
        data = {}
        self._add_properties_to_dict(data, self)
        data = {key.replace('_', ''): value for key, value in data.items()}
    
        if 'additional_properties' in data and not data['additional_properties']:
            del data['additional_properties']
        return json.dumps(data, ensure_ascii=False, default=str)  # 添加 default=str

    def _add_properties_to_dict(self, data: Dict[str, Any], obj: Any):
        if isinstance(obj, dict):
            for key, value in obj.items():
                self._add_value_to_dict(data, key, value)
        elif hasattr(obj, '__dict__'):
            for key, value in obj.__dict__.items():
                if not key.startswith('_'):
                    self._add_value_to_dict(data, key, value)

    def _add_value_to_dict(self, data: Dict[str, Any], key: str, value: Any):
        if value is not None and str(value).strip():
            if isinstance(value, (BasicInfo, EventInfo, ErrorInfo, HttpInfo, TraceInfo)):
                self._add_properties_to_dict(data, value)
            elif isinstance(value, datetime):
                data[key.lower()] = value.isoformat()
            else:
                data[key.lower()] = value

    def add_property(self, key: str, value: Any):
        self.additional_properties[key] = value