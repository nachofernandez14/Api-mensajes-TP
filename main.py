##LIBRERIAS
from typing import Optional
from pydantic import BaseModel
#MODELO MENSAJE
class Mensaje(BaseModel):
    id: Optional[int] = None
    user: str
    mensaje: str

#API
from fastapi import FastAPI, HTTPException
#INICIALAMOS LA API
app = FastAPI()

#Base de datos simulada
mensajes_db = []

#Crear mensaje
@app.post("/mensajes/", response_model=Mensaje)
def crear_mensaje(mensaje: Mensaje):
    mensaje.id = len(mensajes_db) + 1
    mensajes_db.append(mensaje)
    return mensaje

#Ver mensaje por id
@app.get("/mensajes/{mensaje_id}", response_model=Mensaje)
def ver_mensaje(mensaje_id: int):
    for mensaje in mensajes_db:
        if mensaje.id == mensaje_id:
            return mensaje
        raise HTTPException(status_code=404, detail="Mensajes no encontrado")
    
#Listar mensaje
@app.get("/mensajes/", response_model = list[Mensaje])
def listar_mensajes():
    return mensajes_db

#Actualizar mensaje
@app.put("/mensajes/{mensaje_id}", response_model=Mensaje)
def actualizar_mensaje(mensaje_id: int, mensaje_actualizado: Mensaje):
    for index, mensaje in enumerate(mensajes_db):
        if mensaje.id == mensaje_id:
            mensajes_db[index] = mensaje_actualizado
            return mensaje_actualizado
    raise HTTPException(status_code=404, detail="Mensaje no encontrado")


#Eliminar mensaje
@app.delete("/mensajes/{mensaje_id}", response_model=Mensaje)
def eliminar_mensaje(mensaje_id: int):
    for index, mensaje in enumerate(mensajes_db):
        if mensaje.id == mensaje_id:
            mensaje_eliminado = mensajes_db[index]
            del mensajes_db[index]
            return mensaje_eliminado
    raise HTTPException(status_code=404, detail="Mensaje no encontrado")
    