# api_rest
api_rest2

## crear la base de datos
'''sql
sqlite3 clientes.sqlite < clientes.sql
'''

## correr el servidor
''' bash
uvicorn main:app --reload
'''

## ejecutar la prueba
''' bash
pytest -v
'''

usar -vv para mostrar completos los errores

## crear un contenedor

## servidor de python3 en el puerto 8080
python3 -m  http.server 8080
