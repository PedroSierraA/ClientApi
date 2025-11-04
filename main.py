from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
from zoneinfo import ZoneInfo
from datetime import datetime

app = FastAPI()

# Cargar CSV al iniciar
df = pd.read_csv("creditos_dummy.csv", dtype=str)
df["nombre_norm"] = df["nombre persona"].str.strip().str.lower()
df["id_norm"] = df["id"].astype(str).str.strip()

def hoy_bogota_iso():
    return datetime.now(ZoneInfo("America/Bogota")).date().isoformat()  # 'YYYY-MM-DD'


class ClienteRequest(BaseModel):
    nombre: str
    identificacion: str


class ClienteResponse(BaseModel):
    found: bool
    cliente: dict = None
    

class ClienteDetalleResponse(BaseModel):
    nombre: str
    id: str
    credit_amount: float
    credit_date: str
    credit_interest: float

@app.get("/")
def root():
    return {"status": "ok", "message": "DummyClient API está corriendo"}

@app.get("/now")
def now_endpoint():
    return {"today": hoy_bogota_iso(), "tz": "America/Bogota"}


@app.post("/buscar_cliente")
def buscar_cliente(req: ClienteRequest):
    nombre = req.nombre.strip().lower()

    identificacion = str(req.identificacion).strip()

    cliente = df[(df["nombre_norm"] == nombre) & (df["id_norm"] == identificacion)]

    if cliente.empty:
        return {"found": False, "cliente": None}

    row = cliente.iloc[0]
    credit_amount = row.get("credit amount")
    credit_interest = row.get("credit interest")
    mora = row.get("dias_mora")
    monto_final = row.get("monto_final")
    

    return {
        "found": True,
        "cliente": {
            "nombre": row["nombre persona"],
            "id": str(row["id"]),
            "credit_amount": float(credit_amount) if credit_amount not in (None, "") else None,
            "credit_date": row["credit date"],  # string M/D/YYYY
            "credit_interest": float(credit_interest) if credit_interest not in (None, "") else None,
            "dias_mora": int(mora) if mora not in (None, "") else None,
            "monto_final": str(monto_final) if monto_final not in (None, "") else None
        }
    }

