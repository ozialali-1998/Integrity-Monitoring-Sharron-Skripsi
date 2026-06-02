def severity_for_event(event_type: str) -> str:
    return {
        "UNCHANGED": "INFO",
        "ADDED": "MEDIUM",
        "MODIFIED": "HIGH",
        "DELETED": "HIGH",
        "ERROR": "MEDIUM",
    }.get(event_type, "INFO")
