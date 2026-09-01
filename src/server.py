from __future__ import annotations

from dataclasses import asdict
from typing import Any
from uuid import uuid4

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from src.ubiservices.configuration import build_configuration
from src.ubiservices.models import SessionInfo
from src.ubiservices.sessions import SessionStore


app = FastAPI(title="Just Dance 2015 Wii U Backend")

sessions = SessionStore()


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

# We will fill these with the real JD2015 values once we recover them from
# the RPX / traffic analysis.
APP_ID = "UNKNOWN"
APP_BUILD_ID = "UNKNOWN"
ENVIRONMENT = "production"

# Used only by our development backend for now.
SPACE_ID = "jd2015"


# ---------------------------------------------------------------------------
# Debug logging
# ---------------------------------------------------------------------------

def log_request(
    request: Request,
    body: bytes,
) -> None:
    print("\n==============================")
    print("JD2015 / UbiServices REQUEST")
    print("==============================")
    print(f"Method : {request.method}")
    print(f"Path   : {request.url.path}")
    print(f"Query  : {request.url.query}")

    print("Headers:")
    for name, value in request.headers.items():
        print(f"  {name}: {value}")

    if body:
        print("Body:")
        print(body[:4096])
    else:
        print("Body   : <empty>")

    print("==============================\n")


def json_error(message: str, status_code: int = 400) -> JSONResponse:
    return JSONResponse(
        status_code=status_code,
        content={
            "error": message,
        },
    )


# ---------------------------------------------------------------------------
# UbiServices: application configuration
# ---------------------------------------------------------------------------

@app.api_route(
    "/applications/{application_id}/configuration",
    methods=["GET", "POST"],
)
async def application_configuration(
    application_id: str,
    request: Request,
):
    body = await request.body()
    log_request(request, body)

    print(f"[UbiServices] Configuration requested for application: {application_id}")

    # Keep the real application ID supplied by the client in the response for
    # now. We will replace the empty configuration with recovered JD2015 data.
    response = build_configuration(application_id)

    response.update(
        {
            "applicationId": application_id,
            "applicationBuildId": APP_BUILD_ID,
            "environment": ENVIRONMENT,
        }
    )

    return JSONResponse(response)


# ---------------------------------------------------------------------------
# UbiServices: profile session creation
# ---------------------------------------------------------------------------

@app.post("/profiles/sessions")
async def create_profile_session(request: Request):
    body = await request.body()
    log_request(request, body)

    # We are intentionally not pretending that we know the production
    # CreateSession JSON yet.
    #
    # For now we create an internal development session so that the server has
    # the same conceptual state that the RPX's UbiServices SDK expects.

    profile_id = str(uuid4())

    session = sessions.create(
        profile_id=profile_id,
        space_id=SPACE_ID,
        environment=ENVIRONMENT,
        platform_type="WiiU",
    )

    print("[UbiServices] Created development session:")
    print(asdict(session))

    # Placeholder response. The exact Ubisoft wire format still needs to be
    # recovered from the RPX/runtime behavior.
    return JSONResponse(
        {
            "sessionId": session.session_id,
            "profileId": session.profile_id,
            "spaceId": session.space_id,
            "environment": session.environment,
            "platformType": session.platform_type,
        }
    )


# ---------------------------------------------------------------------------
# UbiServices: session lookup / extension
# ---------------------------------------------------------------------------

@app.api_route(
    "/profiles/sessions/{session_id}",
    methods=["GET", "POST", "PUT", "PATCH"],
)
async def profile_session(
    session_id: str,
    request: Request,
):
    body = await request.body()
    log_request(request, body)

    session = sessions.get(session_id)

    if session is None:
        return json_error(
            "Unknown JD2015 session",
            status_code=404,
        )

    # Extend the session conceptually. We will implement Ubisoft's exact
    # session-extension semantics later.
    return JSONResponse(
        {
            "sessionId": session.session_id,
            "profileId": session.profile_id,
            "spaceId": session.space_id,
            "environment": session.environment,
            "platformType": session.platform_type,
        }
    )


# ---------------------------------------------------------------------------
# UbiServices: diagnostic endpoints for related requests
# ---------------------------------------------------------------------------

@app.api_route(
    "/users",
    methods=["GET", "POST", "PUT", "PATCH", "DELETE"],
)
async def users(request: Request):
    body = await request.body()
    log_request(request, body)

    return JSONResponse(
        {
            "status": "not_implemented",
            "service": "users",
        },
        status_code=501,
    )


@app.api_route(
    "/policies",
    methods=["GET", "POST", "PUT", "PATCH", "DELETE"],
)
async def policies(request: Request):
    body = await request.body()
    log_request(request, body)

    return JSONResponse(
        {
            "status": "not_implemented",
            "service": "policies",
        },
        status_code=501,
    )


# ---------------------------------------------------------------------------
# Catch-all
# ---------------------------------------------------------------------------

@app.api_route(
    "/{path:path}",
    methods=[
        "GET",
        "POST",
        "PUT",
        "PATCH",
        "DELETE",
        "OPTIONS",
        "HEAD",
    ],
)
async def catch_all(path: str, request: Request):
    body = await request.body()
    log_request(request, body)

    return JSONResponse(
        {
            "status": "received",
            "path": f"/{path}",
        }
    )


# ---------------------------------------------------------------------------
# Local development entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "src.server:app",
        host="0.0.0.0",
        port=8080,
        reload=False,
    )