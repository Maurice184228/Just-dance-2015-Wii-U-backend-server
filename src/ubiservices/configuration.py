from typing import Any


def build_configuration(application_id: str) -> dict[str, Any]:
    return {
        "applicationId": application_id,
        "configuration": {},
    }