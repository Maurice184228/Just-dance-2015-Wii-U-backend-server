from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class UbisoftConfig:
    app_id: str = "3133a1ba-bf7b-443b-9e8a-f1d5f3b2ac7b"
    app_build_id: str = "JD2015WIIU_E163180"

    # Keep this value consistent in SessionInfo and configuration.
    environment: str = "production"

    # Use the same space ID everywhere.
    space_id: str = "e137c118-3e14-553c-aa55-93282e686408"

    base_host: str = "api-ubiservices.ubi.com"

    configuration_path: str = (
        "/applications/{application_id}/configuration"
    )

    sessions_path: str = "/profiles/sessions"
    users_path: str = "/users"
    policies_path: str = "/policies"


UBISOFT = UbisoftConfig()


def build_configuration(application_id: str) -> dict[str, Any]:
    return {
        "applicationId": application_id,
        "applicationBuildId": UBISOFT.app_build_id,
        "environment": UBISOFT.environment,

        "configuration": {
            "custom": {
                "resources": [],
                "featuresSwitches": [],
            },

            "featuresSwitches": [
                {
                    "name": "Connection",
                    "value": True,
                },
                {
                    "name": "Everything",
                    "value": True,
                },
            ],

            "gatewayResources": [
                {
                    "url": (
                        "https://api-ubiservices.ubi.com/"
                        "{version}/profiles/connections"
                    ),
                    "name": "all_connections",
                    "version": 1,
                },
                {
                    "url": (
                        "https://api-ubiservices.ubi.com/"
                        "{version}/profiles/{profileId}/connections"
                    ),
                    "name": "connections",
                    "version": 1,
                },
                {
                    "url": (
                        "wss://api-ubiservices.ubi.com/"
                        "{version}/websocket"
                    ),
                    "name": "websocket/server",
                    "version": 2,
                },
            ],

            "storm": {},

            "sdkConfig": {
                "remoteLogs": {
                    "ubiservicesLogLevel": "None",
                    "prodLogLevel": "None",
                },
                "httpSafetySleepTime": 0,
                "keepAliveTimeoutMin": 10,
                "timeoutSec": 30,
                "httpParam": {
                    "timeoutParam": {
                        "initialDelayMsec": 30000,
                    },
                },
                "websocketParam": {
                    "timeoutParam": {
                        "initialDelayMsec": 30000,
                    },
                },
            },

            "platformConfig": {
                "platform": "WiiU",
                "applicationId": application_id,
                "spaceId": UBISOFT.space_id,
                "environment": UBISOFT.environment,
                "applicationBuildId": UBISOFT.app_build_id,
            },

            "resources": [],
            "uplayServices": [],
            "legacyUrls": [],
        },
    }