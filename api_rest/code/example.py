import hashlib  # importa la libreria hashlib permite generar un hash
import sqlite3
import os # trabajar con rutas permitiendo que las ajuste de acuerdo al sistema operativo que se utilice
from typing import List 

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials # solicita automaticamente usuario y contraseña
from pydantic import BaseModel

app = FastAPI()

DATABASE_URL = os.path.join("sql/usuarios.sqlite")

security = HTTPBasic() # se encarga de solicitar a la api usuario y contraseña

"""
DROP TABLE IF EXISTS usuarios;

CREATE TABLE usuarios(
    username TEXT,
    password varchar(32),
    level INTEGER
);

CREATE UNIQUE INDEX index_usuario ON usuarios(username);

INSERT INTO usuarios(username, password, level) VALUES('admin','21232f297a57a5a743894a0e4a801fc3',0);
INSERT INTO usuarios(username, password, level) VALUES('user','ee11cbb19052e40b07aac0ca060c23ee',1);

SELECT * FROM usuarios;
"""


class Usuarios(BaseModel): 
    username: str
    level: int


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

@app.get(
    "/usuarios/",
    response_model=List[Usuarios],
    status_code=status.HTTP_202_ACCEPTED,
    summary="Regresa una lista de usuarios", # aparece en la documentacion de la api
    description="Regresa una lista de usuarios",
)
async def get_usuarios(level: int = Depends(get_current_level)):
    if level == 0:  # Administrador
        with sqlite3.connect(DATABASE_URL) as connection:
            connection.row_factory = sqlite3.Row
            cursor = connection.cursor()
            cursor.execute("SELECT username, level FROM usuarios")
            usuarios = cursor.fetchall()
            return usuarios
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Don't have permission to access this resource",
            headers={"WWW-Authenticate": "Basic"},
        )