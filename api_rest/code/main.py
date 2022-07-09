import hashlib  # importa la libreria hashlib permite generar un hash
import os # trabajar con rutas permitiendo que las ajuste de acuerdo al sistema operativo que se utilice 
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials # solicita automaticamente usuario y contraseña
from fastapi.middleware.cors import CORSMiddleware
DATABASE_URL = os.path.join("sql/usuarios.sqlite")
security = HTTPBasic() # se encarga de solicitar a la api usuario y contraseña
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

class Usuarios(BaseModel): 
    username: str
    level: int

app = FastAPI()
#valida el formato sea igual a de respuesta

origins = [
    "https://8080-yesenia19-apirest-6xk2vh2kwcd.ws-us53.gitpod.io",
    "https://8080-yesenia19-apirest-6xk2vh2kwcd.ws-us53.gitpod.io/get_cliente.html",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins= origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_current_level(credentials: HTTPBasicCredentials = Depends(security)): # recibe los user y password y nos indica si las contraseñas son correcta
    password_b = hashlib.md5(credentials.password.encode()) #lo convierte en md5
    password = password_b.hexdigest() #lo convierte a bits
    with sqlite3.connect(DATABASE_URL) as connection:
        cursor = connection.cursor()
        cursor.execute(
            "SELECT level FROM usuarios WHERE username = ? and password = ?",
            (credentials.username, password),
        )
        user = cursor.fetchone()
        if not user:
            raise HTTPException( #raise es lanza
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Basic"},
            )
    return user[0]

@app.get("/", response_model=Respuesta) #endpoint
async def index(): # creamos una clase de manera asincrona
    return  {"mensaje":"API REST"}


@app.get(
    "/clientes/",
    response_model=List[Cliente],
    status_code=status.HTTP_202_ACCEPTED,
    summary="Regresa una lista de clientes", # aparece en la documentacion de la api
    description="Regresa una lista de clientes",
)
async def get_clientes(level: int = Depends(get_current_level)):
    if level == 1:  # Administrador
        with sqlite3.connect('sql/clientes.sqlite') as connection:
            connection.row_factory=sqlite3.Row
            #cursor para realizar las operaciones en la BD
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM clientes")
            #ordena los formatos en json
            response = cursor.fetchall()
            return response
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Don't have permission to access this resource",
            headers={"WWW-Authenticate": "Basic"},
        )

@app.get(
    "/clientes/{id}",
    response_model=List[Cliente],
    status_code=status.HTTP_202_ACCEPTED,
    summary="Regresa un cliente", # aparece en la documentacion de la api
    description="Regresa un cliente",
)
async def get_cliente(id: int,level: int = Depends(get_current_level)):
    if level == 0:  # Administrador
        with sqlite3.connect('sql/clientes.sqlite') as connection:
            connection.row_factory=sqlite3.Row
            #cursor para realizar las operaciones en la BD
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM clientes where id_cliente={}".format(id))
            #ordena los formatos en json
            response = cursor.fetchall()
            return response
            if response is None:
                raise HTTPException(
                    status_code = status.HTTP_404_NOT_FOUND,
                    detail="ID no encontrado",
                    headers={"WWW-Authenticate": "Basic"},
                )
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Don't have permission to access this resource",
            headers={"WWW-Authenticate": "Basic"},
        )

@app.post(  
    "/POST/{nombre}&{email}",
    response_model=Respuesta,
    status_code=status.HTTP_202_ACCEPTED,
    summary="Inserta un cliente", # aparece en la documentacion de la api
    description="Inserta un cliente",
)
async def post_cliente(nombre: str, email:str,level: int = Depends(get_current_level)):
    if level == 0:  # Administrador
        with sqlite3.connect('sql/clientes.sqlite') as connection:
            connection.row_factory=sqlite3.Row
            #cursor para realizar las operaciones en la BD
            cursor = connection.cursor()
            cursor.execute("INSERT INTO clientes (nombre, email) values ('{}','{}');".format(nombre,email))
            #ordena los formatos en json
            response = {"mensaje":"Cliente agregado"}
            return  response
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Don't have permission to access this resource",
            headers={"WWW-Authenticate": "Basic"},
        )

@app.put(  
    "/PUT/{id}&{nombre}&{email}",
    response_model=Respuesta,
    status_code=status.HTTP_202_ACCEPTED,
    summary="Actualiza un cliente", # aparece en la documentacion de la api
    description="Actualiza un cliente",
)
async def put_cliente(id:int, nombre: str, email:str,level: int = Depends(get_current_level)):
    if level == 0:  # Administrador
        #conexion a una bd cierra automaticamente el archivo que se utilice
        with sqlite3.connect('sql/clientes.sqlite') as connection:
            connection.row_factory=sqlite3.Row
            #cursor para realizar las operaciones en la BD
            cursor = connection.cursor()
            cursor.execute("UPDATE clientes SET nombre='{}', email='{}' WHERE id_cliente={} ;".format(nombre,email,id))
            #ordena los formatos en json
            response = {"mensaje":"Cliente actualizado"}
            return  response
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Don't have permission to access this resource",
            headers={"WWW-Authenticate": "Basic"},
        )

@app.delete(  
    "/DELETE/{id}",
    response_model=Respuesta,
    status_code=status.HTTP_202_ACCEPTED,
    summary="Elimina un cliente", # aparece en la documentacion de la api
    description="Elimina un cliente",
)
async def delete_cliente(id:int,level: int = Depends(get_current_level)):
    if level == 0:  # Administrador
        #conexion a una bd cierra automaticamente el archivo que se utilice
        with sqlite3.connect('sql/clientes.sqlite') as connection:
            connection.row_factory=sqlite3.Row
            #cursor para realizar las operaciones en la BD
            cursor = connection.cursor()
            cursor.execute("DELETE FROM clientes WHERE id_cliente={};".format(id))
            #ordena los formatos en json
            response = {"mensaje":"Cliente borrado"}
            return  response
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Don't have permission to access this resource",
            headers={"WWW-Authenticate": "Basic"},
        )