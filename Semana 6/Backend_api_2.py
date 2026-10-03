import os

from bson import ObjectId
from bson.errors import InvalidId
from fastapi import FastAPI, HTTPException
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel, Field

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
client = AsyncIOMotorClient(MONGO_URI)
db = client["doggys"]

app = FastAPI(title="Backend Pedidos Doggys")


class ItemPedido(BaseModel):
    nombre: str
    precio: int = Field(gt=0)
    cantidad: int = Field(gt=0)


class PedidoIn(BaseModel):
    cliente: str = Field(min_length=1)
    telefono: str
    items: list[ItemPedido]


class EstadoIn(BaseModel):
    estado: str


def a_pedido(doc):
    return {
        "id": str(doc["_id"]),
        "cliente": doc["cliente"],
        "telefono": doc["telefono"],
        "items": doc["items"],
        "total": doc["total"],
        "estado": doc["estado"],
    }


def validar_id(id: str):
    try:
        return ObjectId(id)
    except InvalidId:
        raise HTTPException(status_code=400, detail="ID inválido")


@app.get("/health")
async def health():
    return {"status": "ok", "service": "pedidos"}


@app.get("/pedidos")
async def listar_pedidos(estado: str | None = None):
    filtro = {}
    if estado:
        filtro["estado"] = estado
    pedidos = []
    async for doc in db.pedidos.find(filtro):
        pedidos.append(a_pedido(doc))
    return pedidos


@app.post("/pedidos", status_code=201)
async def crear_pedido(pedido: PedidoIn):
    datos = pedido.model_dump()
    datos["total"] = sum(i["precio"] * i["cantidad"] for i in datos["items"])
    datos["estado"] = "pendiente"
    res = await db.pedidos.insert_one(datos)
    doc = await db.pedidos.find_one({"_id": res.inserted_id})
    return a_pedido(doc)


@app.get("/pedidos/{id}")
async def obtener_pedido(id: str):
    doc = await db.pedidos.find_one({"_id": validar_id(id)})
    if doc is None:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    return a_pedido(doc)


@app.put("/pedidos/{id}")
async def cambiar_estado(id: str, datos: EstadoIn):
    res = await db.pedidos.update_one({"_id": validar_id(id)}, {"$set": {"estado": datos.estado}})
    if res.matched_count == 0:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    doc = await db.pedidos.find_one({"_id": validar_id(id)})
    return a_pedido(doc)


@app.delete("/pedidos/{id}", status_code=204)
async def eliminar_pedido(id: str):
    res = await db.pedidos.delete_one({"_id": validar_id(id)})
    if res.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")