from __future__ import annotations


from typing import Any
from uuid import uuid4
from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect
from fastapi.responses import JSONResponse

from src.ubiservices.configuration import build_configuration


from pathlib import Path
from datetime import datetime, timezone, timedelta


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

session_cache: dict[str, dict[str, Any]] = {}

connection_cache: dict[str, dict[str, Any]] = {}


# configuration for the ubiservices endpoints for testing and developing

APP_ID = "3133a1ba-bf7b-443b-9e8a-f1d5f3b2ac7b"
APP_BUILD_ID = "JD2015WIIU_E163180"
ENVIRONMENT = "production"

# Used for the backend development.
SPACE_ID = "jd2015"


# Debug logging 


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


# UbiServices: profile session creation


@app.post("/v2/profiles/sessions")
async def create_profile_session(request: Request):
    body = await request.body()
    log_request(request, body)

    try:
        data: dict[str, Any] = await request.json()
    except Exception:
        return json_error("Invalid JSON body", 400)

    genome_id = data.get("genomeId")
    name_on_platform = data.get("nameOnPlatform")
    id_on_platform = data.get("idOnPlatform")

    if not genome_id or not name_on_platform or not id_on_platform:
        return json_error("Missing CreateSession fields", 400)

    auth_key = request.headers.get("authorization", "")

    now_dt = datetime.now(timezone.utc)

    if auth_key not in session_cache:
        expiration_dt = now_dt + timedelta(days=1)

        session_cache[auth_key] = {
            "sessionId": str(uuid4()),
            "profileId": str(uuid4()),
            "userId": str(uuid4()),
            "productId": "BJDE41",
            "spaceId": SPACE_ID,
            "environment": "Prod",
            "token": "",
            "ticket": "",
            "accountIssues": None,
            "nameOnPlatform": name_on_platform,
            "hasAcceptedLegalOptins": True,
            "expiration": expiration_dt.isoformat().replace("+00:00", "Z"),
            "serverTime": now_dt.isoformat().replace("+00:00", "Z"),
            "clientIp": request.client.host if request.client else None,
            "initializeUser": True,
            "platformType": "WiiU",
        }

    response = session_cache[auth_key]

    print("[JobCreateSession]")
    print(f"  genomeId       : {genome_id}")
    print(f"  nameOnPlatform : {name_on_platform}")
    print(f"  idOnPlatform   : {id_on_platform}")

    print("[JobCreateSession] Returning development SessionInfo:")
    print(response)

    return JSONResponse(response)

# UbiServices: application configuration

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

    print(
        f"[JobRequestConfig] Configuration requested for application: "
        f"{application_id}"
    )

    response = {
        "applicationId": application_id,
        "applicationBuildId": APP_BUILD_ID,
        "environment": "Prod",
        "configuration": {},
        "resources": {},
        "sandboxes": {},
        "uplayServices": {},
        "sdkConfig": {},
        "platformConfig": {
            "platform": "WiiU",
        },
        "legacyUrls": {},
        "featuresSwitches": {},
    }

    print("[JobRequestConfig] Returning development configuration:")
    print(response)

    return JSONResponse(response)

# UbiServices: session lookup / extension


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

    print(f"[JobLogin] Session lookup requested: {session_id}")

    for session_data in session_cache.values():
        if session_data.get("sessionId") == session_id:
            print(f"[JobLogin] Session found: {session_id}")
            return JSONResponse(session_data)

    print(f"[JobLogin] Unknown session: {session_id}")

    return json_error(
        "Unknown JD2015 session",
        status_code=404,
    )

# Development connection service

@app.api_route(
    "/v2/connections",
    methods=["GET", "POST"],
)
async def connections(request: Request):
    body = await request.body()
    log_request(request, body)

    print("[JobInitiateConnection] Connection request received")

    connection_id = str(uuid4())

    connection_cache[connection_id] = {
        "connectionId": connection_id,
        "status": "ready",
        "environment": "Prod",
        "platformType": "WiiU",
    }

    response = connection_cache[connection_id]

    print("[JobInitiateConnection] Returning development connection:")
    print(response)

    return JSONResponse(response)

# UbiServices: diagnostic endpoints for related requests

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

# Catch-all info

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

    print(
        f"[UbiServices] UNIMPLEMENTED ENDPOINT: "
        f"{request.method} /{path}"
    )

    return JSONResponse(
        {
            "status": "not_implemented",
            "path": f"/{path}",
        },
        status_code=501,
    )
    
# Development WebSocket diagnostic endpoint

@app.websocket("/{path:path}")
async def websocket_diagnostic(websocket: WebSocket, path: str):
    await websocket.accept()

    print("\n==============================")
    print("JD2015 / UbiServices WEBSOCKET")
    print("==============================")
    print(f"Path   : /{path}")
    print("Headers:")

    headers = dict(websocket.headers)

    for name, value in headers.items():
        print(f"  {name}: {value}")

    print("==============================\n")
    print("[WebSocket] Handshake accepted")

    try:
        while True:
            message = await websocket.receive()

            if message.get("text") is not None:
                print("[WebSocket] TEXT:")
                print(message["text"])

            elif message.get("bytes") is not None:
                print("[WebSocket] BINARY:")
                print(message["bytes"].hex())

            elif message.get("type") == "websocket.disconnect":
                break

    except WebSocketDisconnect:
        print("[WebSocket] Client disconnected")

# Local development entry point

if __name__ == "__main__":
    import ssl
    import uvicorn

    tls_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)

    tls_context.keylog_filename = str(
        PROJECT_DIR / "captures" / "jd2015_python_tls.keys"
    )

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