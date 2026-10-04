import os

import httpx
from fastapi import Depends, FastAPI, HTTPException, Request, Response
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

VAULT_ADDR = os.getenv("VAULT_ADDR", "http://localhost:8200")
VAULT_TOKEN = os.getenv("VAULT_TOKEN")
if not VAULT_TOKEN:
    raise RuntimeError("VAULT_TOKEN no está configurado")

BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:9000")
AUTH_URL = os.getenv("AUTH_URL", "http://localhost:8100")

app = FastAPI(title="API Gateway Doggys")
security = HTTPBearer(auto_error=False)


async def get_backend_secret() -> str:
    url = f"{VAULT_ADDR}/v1/secret/data/gateway"
    headers = {"X-Vault-Token": VAULT_TOKEN}
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get(url, headers=headers)
    except httpx.RequestError as exc:
        raise HTTPException(status_code=500, detail=f"No fue posible conectar con Vault: {exc}")

    if response.status_code != 200:
        raise HTTPException(status_code=500, detail=f"No fue posible acceder a Vault: {response.status_code}")

    return response.json()["data"]["data"]["backend_shared_secret"]


async def llamar_auth(ruta: str, datos: dict):
    secreto = await get_backend_secret()
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            return await client.post(
                f"{AUTH_URL}{ruta}",
                json=datos,
                headers={"X-Gateway-Secret": secreto},
            )
    except httpx.RequestError:
        raise HTTPException(status_code=502, detail="El servicio de autenticación no responde")


async def authenticate_client(credentials: HTTPAuthorizationCredentials = Depends(security)):
    if credentials is None:
        raise HTTPException(status_code=401, detail="Bearer token requerido")

    res = await llamar_auth("/introspect", {"token": credentials.credentials})
    if res.status_code != 200:
        raise HTTPException(status_code=502, detail="Error al validar el token")

    info = res.json()
    if not info.get("active"):
        raise HTTPException(status_code=401, detail="Token inválido o expirado")

    return {"username": info["username"], "roles": ",".join(info["roles"])}


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.post("/auth/login")
async def login(request: Request):
    datos = await request.json()
    res = await llamar_auth("/login", datos)
    return Response(content=res.content, status_code=res.status_code, media_type="application/json")


@app.post("/auth/logout")
async def logout(credentials: HTTPAuthorizationCredentials = Depends(security)):
    if credentials is None:
        raise HTTPException(status_code=401, detail="Bearer token requerido")
    res = await llamar_auth("/logout", {"token": credentials.credentials})
    return Response(content=res.content, status_code=res.status_code, media_type="application/json")


_SKIP_REQUEST_HEADERS = {
    "host", "content-length", "authorization", "connection",
    "x-gateway-secret", "x-authenticated-user", "x-authenticated-roles",
}


@app.api_route("/api/{path:path}", methods=["GET", "POST", "PUT", "PATCH", "DELETE"])
async def proxy(path: str, request: Request, auth=Depends(authenticate_client)):
    secreto = await get_backend_secret()
    target_url = f"{BACKEND_URL}/{path}"
    body = await request.body()

    headers = {k: v for k, v in request.headers.items() if k.lower() not in _SKIP_REQUEST_HEADERS}
    headers["X-Gateway-Secret"] = secreto
    headers["X-Authenticated-User"] = auth["username"]
    headers["X-Authenticated-Roles"] = auth["roles"]

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            upstream = await client.request(
                request.method,
                target_url,
                params=request.query_params,
                content=body,
                headers=headers,
            )
    except httpx.RequestError:
        raise HTTPException(status_code=502, detail="El backend no responde")

    return Response(
        content=upstream.content,
        status_code=upstream.status_code,
        media_type=upstream.headers.get("content-type"),
    )