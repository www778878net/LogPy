import sys
import os
import json
from datetime import datetime


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src'))))

from log_entry import LogEntry, BasicInfo, EventInfo, ErrorInfo, HttpInfo, TraceInfo

class CustomLogEntry(LogEntry):
    def __init__(self):
        super().__init__()
        self.custom_field1 = "Custom Value"
        self.custom_field2 = 42

def test_custom_log_entry_to_json():
    log_entry = CustomLogEntry()
    log_entry.basic.summary = "Custom log entry test"
    log_entry.basic.log_level_number = 30
    log_entry.basic.timestamp = datetime(2023, 5, 10, 8, 30)
    log_entry.basic.log_level = "INFO"
    log_entry.basic.message = "This is a custom log entry"
    log_entry.basic.host_name = "web-server-01"
    log_entry.basic.service_name = "AuthService"
    log_entry.basic.user_id = "user123"
    log_entry.basic.user_name = "johndoe"
    log_entry.basic.log_index = "index1"

    log_entry.event.event_id = "550e8400-e29b-41d4-a716-446655440000"
    log_entry.event.event_kind = "event"
    log_entry.event.event_category = "authentication"
    log_entry.event.event_action = "login"
    log_entry.event.event_outcome = "success"
    log_entry.event.event_duration = 150
    log_entry.event.transaction_id = "tx-12345"

    log_entry.error.error_type = None
    log_entry.error.error_message = None
    log_entry.error.error_stack_trace = None

    log_entry.http.http_request_method = None
    log_entry.http.http_request_body_content = None
    log_entry.http.http_response_status_code = None
    log_entry.http.url_original = None

    log_entry.trace.trace_id = "trace-6789"
    log_entry.trace.span_id = "span-9876"

    # Convert datetime to string for JSON serialization
    log_entry.basic.timestamp = log_entry.basic.timestamp.isoformat()

    json_output = log_entry.to_json()
    print(json_output)

    expected_output = {
        "summary": "Custom log entry test",
        "log_level_number": 30,
        "timestamp": "2023-05-10T08:30:00",
        "log_level": "INFO",
        "message": "This is a custom log entry",
        "host_name": "web-server-01",
        "service_name": "AuthService",
        "user_id": "user123",
        "user_name": "johndoe",
        "log_index": "index1",
        "event_id": "550e8400-e29b-41d4-a716-446655440000",
        "event_kind": "event",
        "event_category": "authentication",
        "event_action": "login",
        "event_outcome": "success",
        "event_duration": 150,
        "transaction_id": "tx-12345",
        "trace_id": "trace-6789",
        "span_id": "span-9876",
        "custom_field1": "Custom Value",
        "custom_field2": 42
    }

    assert json.loads(json_output) == expected_output

if __name__ == "__main__":
    test_custom_log_entry_to_json()