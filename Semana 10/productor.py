import stomp
import argparse
import json
from decimal import Decimal, InvalidOperation
import xml.etree.ElementTree as ET

DESTINO = "/queue/pedidos"

def construir_mensaje(formato: str, pedido: dict, texto: str) -> tuple[str, str]:
    if formato == "texto":
        return texto, "text/plain; charset=utf-8"
    # Aquí se pueden agregar otros formatos (fijo, xml, json)

def main():
    parser = argparse.ArgumentParser(description="Productor STOMP")
    parser.add_argument("--formato", choices=["texto", "fijo", "xml", "json"], required=True)
    parser.add_argument("--mensaje", default="Hola desde el productor STOMP")
    parser.add_argument("--id", default="123")
    parser.add_argument("--cliente", default="Edward Norton")
    parser.add_argument("--monto", default="123.45")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=61613)
    parser.add_argument("--usuario", default="demo")
    parser.add_argument("--clave", default="demo123")

    args = parser.parse_args()

    try:
        monto = Decimal(args.monto)
        if not monto.is_finite():
            raise ValueError("El monto debe ser número finito")
    except InvalidOperation as exc:
        parser.error(f"Monto no válido: {args.monto}")

    pedido = {
        "id": args.id,
        "cliente": args.cliente,
        "monto": str(monto)
    }

    cuerpo, mime = construir_mensaje(args.formato, pedido, args.mensaje)

    # Enviar mensaje al broker STOMP
    try:
        conexion = stomp.Connection12([(args.host, args.port)])
        conexion.connect(args.usuario, args.clave, wait=True)
        conexion.send(
            destination=DESTINO,
            body=cuerpo,
            headers={
                "content-type": mime,
                "x-formato": args.formato,
                "persistent": "true"
            }
        )
        print(f"Mensaje enviado a {DESTINO} (formato={args.formato}): {cuerpo}")
    finally:
        if conexion.is_connected():
            conexion.disconnect()

if __name__ == "__main__":
    main()