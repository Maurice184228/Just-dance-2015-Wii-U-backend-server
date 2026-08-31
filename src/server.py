from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from src.ubiservices.configuration import build_configuration
from src.ubiservices.sessions import SessionStore

app = FastAPI(title="Just Dance 2015 Wii U Backend")

sessions = SessionStore()


def log_request(
    method: str,
    path: str,
    query: str,
    headers: dict[str, str],
    body: bytes,
) -> None:
    print("\n==============================")
    print("JD2015 REQUEST")
    print("==============================")
    print(f"Method : {method}")
    print(f"Path   : {path}")
    print(f"Query  : {query}")

    print("Headers:")
    for name, value in headers.items():
        print(f"  {name}: {value}")

    if body:
        print("Body:")
        print(body[:4096])
    else:
        print("Body   : <empty>")

    print("==============================\n")


@app.get("/applications/{application_id}/configuration")
async def application_configuration(application_id: str, request: Request):
    body = await request.body()

    log_request(
        request.method,
        str(request.url.path),
        request.url.query,
        dict(request.headers),
        body,
    )

    return JSONResponse(build_configuration(application_id))


@app.api_route(
    "/profiles/sessions",
    methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
)
async def profile_sessions(request: Request):
    body = await request.body()

    log_request(
        request.method,
        str(request.url.path),
        request.url.query,
        dict(request.headers),
        body,
    )

    return JSONResponse(
        {
            "sessionId": "",
            "profileId": "",
            "spaceId": "",
            "environment": "",
            "platformType": "WiiU",
        }
    )


@app.api_route(
    "/{path:path}",
    methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
)
async def catch_all(path: str, request: Request):
    body = await request.body()

    log_request(
        request.method,
        "/" + path,
        request.url.query,
        dict(request.headers),
        body,
    )

    return JSONResponse(
        {
            "status": "received",
            "path": "/" + path,
        }
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "src.server:app",
        host="0.0.0.0",
        port=8080,
        reload=False,
    )