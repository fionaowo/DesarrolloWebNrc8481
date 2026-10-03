import os

from bson import ObjectId
from bson.errors import InvalidId
from fastapi import FastAPI, HTTPException
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel, Field

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
client = AsyncIOMotorClient(MONGO_URI)
db = client["doggys"]

app = FastAPI(title="Backend Productos Doggys")


class ProductoBase(BaseModel):
    nombre: str = Field(min_length=1)
    categoria: str
    precio: int = Field(gt=0)
    disponible: bool = True


class ProductoIn(ProductoBase):
    pass


class ProductoOut(ProductoBase):
    id: str


def a_producto(doc):
    return {
        "id": str(doc["_id"]),
        "nombre": doc["nombre"],
        "categoria": doc["categoria"],
        "precio": doc["precio"],
        "disponible": doc["disponible"],
    }


def validar_id(id: str):
    try:
        return ObjectId(id)
    except InvalidId:
        raise HTTPException(status_code=400, detail="ID inválido")


@app.get("/health")
async def health():
    return {"status": "ok", "service": "productos"}


@app.get("/productos", response_model=list[ProductoOut])
async def listar_productos(categoria: str | None = None, skip: int = 0, limit: int = 20):
    filtro = {}
    if categoria:
        filtro["categoria"] = categoria
    productos = []
    async for doc in db.productos.find(filtro).skip(skip).limit(limit):
        productos.append(a_producto(doc))
    return productos


@app.post("/productos", response_model=ProductoOut, status_code=201)
async def crear_producto(item: ProductoIn):
    res = await db.productos.insert_one(item.model_dump())
    doc = await db.productos.find_one({"_id": res.inserted_id})
    return a_producto(doc)


@app.get("/productos/{id}", response_model=ProductoOut)
async def obtener_producto(id: str):
    doc = await db.productos.find_one({"_id": validar_id(id)})
    if doc is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return a_producto(doc)


@app.put("/productos/{id}", response_model=ProductoOut)
async def actualizar_producto(id: str, item: ProductoIn):
    res = await db.productos.update_one({"_id": validar_id(id)}, {"$set": item.model_dump()})
    if res.matched_count == 0:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    doc = await db.productos.find_one({"_id": validar_id(id)})
    return a_producto(doc)


@app.delete("/productos/{id}", status_code=204)
async def eliminar_producto(id: str):
    res = await db.productos.delete_one({"_id": validar_id(id)})
    if res.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Producto no encontrado")