from dataclasses import dataclass


@dataclass
class CallbackData:
    event_handler: str
    event_type: str
    value: str | None = None
