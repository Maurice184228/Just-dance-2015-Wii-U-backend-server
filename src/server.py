from __future__ import annotations


from typing import Any
from uuid import uuid4
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from src.ubiservices.configuration import build_configuration


from pathlib import Path
from datetime import datetime, timezone


PROJECT_DIR = Path(__file__).resolve().parent.parent

LOG_DIR = PROJECT_DIR / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)

REQUEST_LOG = LOG_DIR / "ubiservices_requests.log"


def save_request_log(
    request: Request,
    body: bytes,
) -> None:
    timestamp = datetime.now(timezone.utc).isoformat()

    with REQUEST_LOG.open("a", encoding="utf-8") as f:
        f.write("\n" + "=" * 70 + "\n")
        f.write(f"Timestamp: {timestamp}\n")
        f.write(f"Method: {request.method}\n")
        f.write(f"Path: {request.url.path}\n")
        f.write(f"Query: {request.url.query}\n")
        f.write("Headers:\n")

        for name, value in request.headers.items():
            f.write(f"  {name}: {value}\n")

        f.write("Body:\n")
        if body:
            f.write(body[:16384].decode("utf-8", errors="replace"))
            f.write("\n")
        else:
            f.write("<empty>\n")


app = FastAPI(title="Just Dance 2015 Wii U Backend")


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

# We will fill these with the real JD2015 values once we recover them from
# the RPX / traffic analysis.

APP_ID = "3133a1ba-bf7b-443b-9e8a-f1d5f3b2ac7b"
APP_BUILD_ID = "JD2015WIIU_E163180"
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
    save_request_log(request, body)

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

# ---------------------------------------------------------------------------
# UbiServices: profile session creation
# ---------------------------------------------------------------------------

@app.post("/v2/profiles/sessions")
async def create_profile_session(request: Request):
    body = await request.body()
    log_request(request, body)

    try:
        data: dict[str, Any] = await request.json()
    except Exception:
        return json_error(
            "Invalid JSON body",
            status_code=400,
        )

    genome_id = data.get("genomeId")
    name_on_platform = data.get("nameOnPlatform")
    id_on_platform = data.get("idOnPlatform")

    if not genome_id or not name_on_platform or not id_on_platform:
        return json_error(
            "Missing CreateSession fields",
            status_code=400,
        )

    print("[JobCreateSession]")
    print(f"  genomeId       : {genome_id}")
    print(f"  nameOnPlatform : {name_on_platform}")
    print(f"  idOnPlatform   : {id_on_platform}")

    session_id = str(uuid4())
    profile_id = str(uuid4())
    user_id = str(uuid4())

    response = {
        "sessionId": session_id,
        "profileId": profile_id,
        "userId": user_id,
        "productId": "BJDE41",
        "spaceId": SPACE_ID,
        "environment": ENVIRONMENT,
        "nameOnPlatform": name_on_platform,
        "platformType": "WiiU",
        "accountIssues": [],
        "hasAcceptedLegalOptins": True,
    }

    print("[JobCreateSession] Returning development SessionInfo:")
    print(response)

    return JSONResponse(response)


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

    print(f"[UbiServices] Session lookup requested: {session_id}")

    return json_error(
        "Session lookup not implemented yet",
        status_code=501,
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
    import ssl
    import uvicorn

    tls_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)

    tls_context.minimum_version = ssl.TLSVersion.TLSv1
    tls_context.maximum_version = ssl.TLSVersion.TLSv1_2
    
    tls_context.set_ciphers("DEFAULT:@SECLEVEL=0")

    tls_context.load_cert_chain(
        certfile="config/tls/api-ubiservices.crt",
        keyfile="config/tls/api-ubiservices.key",
    )

    def make_ssl_context(config, default_factory):
        return tls_context

    uvicorn.run(
        "src.server:app",
        host="0.0.0.0",
        port=443,
        reload=False,
        ssl_context_factory=make_ssl_context,
    )