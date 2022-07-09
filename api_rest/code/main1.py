from fastapi import FastAPI
import sqlite3
#nos lo muestre en una lista
from typing import List
#valida el formato
from pydantic import BaseModel

class Respuesta(BaseModel):
    mensaje:str

class Cliente(BaseModel):
    id_cliente:int 
    nombre:str 
    email:str


app = FastAPI()
#valida el formato sea igual a de respuesta
@app.get("/", response_model=Respuesta) #endpoint
async def index(): # creamos una clase de manera asincrona
    return  {"mensaje":"API REST"}

@app.get("/clientes/", response_model=List[Cliente])
async def clientes():
    #conexion a una bd cierra automaticamente el archivo que se utilice
    with sqlite3.connect('sql/clientes.sqlite') as connection:
        connection.row_factory=sqlite3.Row
        #cursor para realizar las operaciones en la BD
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM clientes")
        #ordena los formatos en json
        response = cursor.fetchall()
        return response

@app.get("/clientes/{id}", response_model=List[Cliente])
async def clientes(id: int):
    #conexion a una bd cierra automaticamente el archivo que se utilice
    with sqlite3.connect('sql/clientes.sqlite') as connection:
        connection.row_factory=sqlite3.Row
        #cursor para realizar las operaciones en la BD
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM clientes where id_cliente={}".format(id))
        #ordena los formatos en json
        response = cursor.fetchall()
        return response

@app.post("/POST/{nombre}&{email}", response_model=Respuesta) #insertar
async def clientes(nombre: str, email:str):
    #conexion a una bd cierra automaticamente el archivo que se utilice
    with sqlite3.connect('sql/clientes.sqlite') as connection:
        connection.row_factory=sqlite3.Row
        #cursor para realizar las operaciones en la BD
        cursor = connection.cursor()
        cursor.execute("INSERT INTO clientes (nombre, email) values ('{}','{}');".format(nombre,email))
        #ordena los formatos en json
        response = {"mensaje":"Cliente agregado"}
        return  response

@app.put("/PUT/{id}&{nombre}&{email}", response_model=Respuesta) #actualizar
async def clientes(id:int, nombre: str, email:str):
    #conexion a una bd cierra automaticamente el archivo que se utilice
    with sqlite3.connect('sql/clientes.sqlite') as connection:
        connection.row_factory=sqlite3.Row
        #cursor para realizar las operaciones en la BD
        cursor = connection.cursor()
        cursor.execute("UPDATE clientes SET nombre='{}', email='{}' WHERE id_cliente={} ;".format(nombre,email,id))
        #ordena los formatos en json
        response = {"mensaje":"Cliente actualizado"}
        return  response

@app.delete("/DELETE/{id}", response_model=Respuesta) #eliminar
async def clientes(id:int):
    #conexion a una bd cierra automaticamente el archivo que se utilice
    with sqlite3.connect('sql/clientes.sqlite') as connection:
        connection.row_factory=sqlite3.Row
        #cursor para realizar las operaciones en la BD
        cursor = connection.cursor()
        cursor.execute("DELETE FROM clientes WHERE id_cliente={};".format(id))
        #ordena los formatos en json
        response = {"mensaje":"Cliente borrado"}
        return  response