import hashlib
import os
import secrets
import time

from fastapi import Depends, FastAPI, Header, HTTPException
from pydantic import BaseModel

AUTH_SHARED_SECRET = os.getenv("AUTH_SHARED_SECRET")
if not AUTH_SHARED_SECRET:
    raise RuntimeError("AUTH_SHARED_SECRET no está configurado")

TOKEN_DURATION = 15 * 60


def hash_clave(clave: str) -> str:
    return hashlib.sha256(clave.encode()).hexdigest()


USERS = {
    "darien": {"password": hash_clave("darien123"), "roles": ["admin"]},
    "fiona": {"password": hash_clave("fiona123"), "roles": ["cliente"]},
}

sessions: dict[str, dict] = {}


async def verify_caller(x_gateway_secret: str = Header(default="")):
    ok = secrets.compare_digest(x_gateway_secret.encode(), AUTH_SHARED_SECRET.encode())
    if not ok:
        raise HTTPException(status_code=403, detail="Acceso no permitido")


app = FastAPI(title="Auth Service Doggys", dependencies=[Depends(verify_caller)])


class LoginIn(BaseModel):
    username: str
    password: str


class TokenIn(BaseModel):
    token: str


@app.post("/login")
async def login(datos: LoginIn):
    user = USERS.get(datos.username)
    if user is None or user["password"] != hash_clave(datos.password):
        raise HTTPException(status_code=401, detail="Usuario o contraseña incorrectos")

    token = secrets.token_urlsafe(32)
    sessions[token] = {
        "username": datos.username,
        "roles": user["roles"],
        "exp": time.time() + TOKEN_DURATION,
    }
    return {"access_token": token, "token_type": "Bearer", "expires_in": TOKEN_DURATION}


@app.post("/introspect")
async def introspect(datos: TokenIn):
    session = sessions.get(datos.token)
    if session is None:
        return {"active": False}

    if session["exp"] < time.time():
        del sessions[datos.token]
        return {"active": False}

    return {
        "active": True,
        "username": session["username"],
        "roles": session["roles"],
        "exp": int(session["exp"]),
    }


@app.post("/logout")
async def logout(datos: TokenIn):
    sessions.pop(datos.token, None)
    return {"message": "Sesión cerrada"}