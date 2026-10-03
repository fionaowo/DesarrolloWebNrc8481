import httpx
from fastapi import FastAPI, HTTPException, Request, Response

BACKEND_PRODUCTOS = "http://localhost:9000"
BACKEND_PEDIDOS = "http://localhost:9100"

app = FastAPI(title="API Gateway Doggys")


async def reenviar(request: Request, url: str):
    body = await request.body()
    headers = {"content-type": request.headers.get("content-type", "application/json")}
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            res = await client.request(
                request.method,
                url,
                params=request.query_params,
                content=body,
                headers=headers,
            )
    except httpx.RequestError:
        raise HTTPException(status_code=502, detail="El backend no responde")

    return Response(
        content=res.content,
        status_code=res.status_code,
        media_type=res.headers.get("content-type"),
    )


@app.get("/health")
async def health():
    return {"status": "ok", "service": "gateway"}


@app.api_route("/api/productos", methods=["GET", "POST"])
@app.api_route("/api/productos/{path:path}", methods=["GET", "PUT", "DELETE"])
async def productos(request: Request, path: str = ""):
    url = f"{BACKEND_PRODUCTOS}/productos"
    if path:
        url = url + "/" + path
    return await reenviar(request, url)


@app.api_route("/api/pedidos", methods=["GET", "POST"])
@app.api_route("/api/pedidos/{path:path}", methods=["GET", "PUT", "DELETE"])
async def pedidos(request: Request, path: str = ""):
    url = f"{BACKEND_PEDIDOS}/pedidos"
    if path:
        url = url + "/" + path
    return await reenviar(request, url)