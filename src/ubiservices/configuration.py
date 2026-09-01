from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class UbisoftConfig:
    """
    JD2015 Wii U Ubisoft configuration recovered from the RPX.

    Some values are confirmed directly by the binary.
    Others are deliberately left unknown until we recover them from
    runtime behavior / additional binary analysis.
    """

    # Strong candidate from the embedded UbiServices application data.
    app_id: str = "3133a1ba-bf7b-443b-9e8a-f1d5f3b2ac7b"

    # The SDK expects this, the literal JD2015 value.
    app_build_id: str = "JD2015WIIU_E163180"

    # The client connects to the live Ubisoft endpoint.
    environment: str = "production"

    base_host: str = "api-ubiservices.ubi.com"

    configuration_path: str = (
        "/applications/{application_id}/configuration"
    )

    sessions_path: str = "/profiles/sessions"

    users_path: str = "/users"

    policies_path: str = "/policies"


UBISOFT = UbisoftConfig()


def build_configuration(application_id: str) -> dict:
    """
    Temporary development response.

    This is NOT yet the final JD2015 Ubisoft configuration.
    We will replace it after recovering the real configuration data.
    """

    return {
        "applicationId": application_id,
        "applicationBuildId": UBISOFT.app_build_id,
        "environment": UBISOFT.environment,
        "configuration": {},
        "resources": {},
        "sandboxes": {},
        "uplayServices": {},
        "sdkConfig": {},
        "platformConfig": {},
        "legacyUrls": {},
        "featuresSwitches": {},
        "gatewayResources": {},
    }