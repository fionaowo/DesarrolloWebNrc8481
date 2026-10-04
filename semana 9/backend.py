import os
import secrets
from itertools import count

from fastapi import Depends, FastAPI, Header, HTTPException
from pydantic import BaseModel

BACKEND_SHARED_SECRET = os.getenv("BACKEND_SHARED_SECRET")
if not BACKEND_SHARED_SECRET:
    raise RuntimeError("BACKEND_SHARED_SECRET no está configurado")


async def only_from_gateway(
    x_gateway_secret: str = Header(default=""),
    x_authenticated_user: str = Header(default=""),
    x_authenticated_roles: str = Header(default=""),
) -> dict:
    ok = secrets.compare_digest(x_gateway_secret.encode(), BACKEND_SHARED_SECRET.encode())
    if not ok or not x_authenticated_user:
        raise HTTPException(status_code=403, detail="Acceso directo no permitido")
    return {"user": x_authenticated_user, "roles": x_authenticated_roles.split(",")}


async def solo_admin(auth: dict = Depends(only_from_gateway)) -> dict:
    if "admin" not in auth["roles"]:
        raise HTTPException(status_code=403, detail="Se requiere rol admin")
    return auth


app = FastAPI(title="Backend Doggys", dependencies=[Depends(only_from_gateway)])

products = {
    1: {"id": 1, "name": "Completo Italiano", "category": "Italianos", "price": 2500},
    2: {"id": 2, "name": "Completo Dinámico", "category": "Dinámicos", "price": 2600},
    3: {"id": 3, "name": "Hot Dog Americano", "category": "Americanos", "price": 2800},
}
orders: dict[int, dict] = {}
_product_ids = count(4)
_order_ids = count(1)


class ProductIn(BaseModel):
    name: str
    category: str
    price: float


class OrderIn(BaseModel):
    product_id: int
    quantity: int = 1


@app.get("/health")
async def health():
    return {"status": "ok", "service": "backend"}


@app.get("/products")
async def list_products():
    return list(products.values())


@app.post("/products", status_code=201)
async def create_product(item: ProductIn, auth: dict = Depends(solo_admin)):
    pid = next(_product_ids)
    products[pid] = {"id": pid, **item.model_dump()}
    return products[pid]


@app.get("/products/{product_id}")
async def get_product(product_id: int):
    if product_id not in products:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return products[product_id]


@app.put("/products/{product_id}")
async def update_product(product_id: int, item: ProductIn, auth: dict = Depends(solo_admin)):
    if product_id not in products:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    products[product_id] = {"id": product_id, **item.model_dump()}
    return products[product_id]


@app.delete("/products/{product_id}", status_code=204)
async def delete_product(product_id: int, auth: dict = Depends(solo_admin)):
    if products.pop(product_id, None) is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")


@app.get("/orders")
async def list_orders(auth: dict = Depends(only_from_gateway)):
    return [o for o in orders.values() if o["user"] == auth["user"]]


@app.post("/orders", status_code=201)
async def create_order(item: OrderIn, auth: dict = Depends(only_from_gateway)):
    if item.product_id not in products:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    oid = next(_order_ids)
    orders[oid] = {"id": oid, "user": auth["user"], **item.model_dump()}
    return orders[oid]