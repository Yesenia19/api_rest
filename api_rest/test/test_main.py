from fastapi.testclient import TestClient
from code.pruebas import app

#verificar que se conecta a la tabla 
clientes = TestClient(app)

def test_index():
    response = clientes.get("/") #requests
    data={"mensaje":"API REST"}
    #la respuesta que se reciba debe ser 200
    assert response.status_code == 200
    #el response debe dar lo que se indica
    assert response.json() == data

def test_clientes():
    response = clientes.get("/clientes/") #requests
    data=[
        {"id_cliente":1,"nombre":"Yesenia","email":"yesenia@email.com"},
        {"id_cliente":2,"nombre":"Lizbeth","email":"lizbeth@email.com"},
        {"id_cliente":3,"nombre":"Veronica","email":"veronica@email.com"}
        ]
    #la respuesta que se reciba debe ser 200
    assert response.status_code == 200
    #el response debe dar lo que se indica
    assert response.json() == data


def test_cliente_1():
    response = clientes.get("/clientes/1") #requests
    data=[{"id_cliente":1,"nombre":"Yesenia","email":"yesenia@email.com"}]
    #la respuesta que se reciba debe ser 200
    assert response.status_code == 200
    #el response debe dar lo que se indica
    assert response.json() == data

def test_cliente_2():
    response = clientes.get("/clientes/2") #requests
    data=[{"id_cliente":2,"nombre":"Lizbeth","email":"lizbeth@email.com"}]
    #la respuesta que se reciba debe ser 200
    assert response.status_code == 200
    #el response debe dar lo que se indica
    assert response.json() == data

def test_cliente_3():
    response = clientes.get("/clientes/3") #requests
    data=[{"id_cliente":3,"nombre":"Veronica","email":"veronica@email.com"}]
    #la respuesta que se reciba debe ser 200
    assert response.status_code == 200
    #el response debe dar lo que se indica
    assert response.json() == data

def test_insertar_cliente():
    response = clientes.post("/POST/Cliente1&cliente1@email.com") #requests
    data = {"mensaje":"Cliente agregado"}
    #la respuesta que se reciba debe ser 200
    assert response.status_code == 200
    #el response debe dar lo que se indica
    assert response.json() == data

def test_actualizar_cliente():
    response = clientes.put("/PUT/5&Clienteactualizado&actualizado@email.com")  #requests
    data = {"mensaje":"Cliente actualizado"}
    #la respuesta que se reciba debe ser 200
    assert response.status_code == 200
    #el response debe dar lo que se indica
    assert response.json() == data

def test_borrar_cliente():
    response = clientes.delete("/DELETE/5" ) #requests
    data = {"mensaje":"Cliente borrado"}
    #la respuesta que se reciba debe ser 200
    assert response.status_code == 200
    #el response debe dar lo que se indica
    assert response.json() == data

