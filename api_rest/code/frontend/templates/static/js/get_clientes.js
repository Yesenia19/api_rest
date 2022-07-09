function getClientes() {
    var request = new XMLHttpRequest();
    //Accede a la session de la pagina
    //username= sessionStorage.getItem("username");
    //password= sessionStorage.getItem("password");
    username ="user";
    password ="user";
   
    request.open('GET', 'https://8000-yesenia19-apirest-6xk2vh2kwcd.ws-us53.gitpod.io/clientes/');
    request.setRequestHeader("Accept", "application/json");
    request.setRequestHeader("Authorization", "Basic " + btoa(username + ":" + password))
    request.setRequestHeader("Content-Type", "application/json");
    const  tabla   = document.getElementById("tabla_Clientes");
   
    var tblBody = document.createElement("tbody");
    var tblHead = document.createElement("thead");
    
    tblHead.innerHTML = `
        <a href='/post_cliente.html?'>Cliente nuevo</a>
        <tr>
            <th>ID</th>
            <th>Nombre</th>
            <th>Email</th>
            <th>Detalle</th>
            <th>Actualizar</th>
            <th>Borrar</th>
        </tr>`;
   
    request.onload = () => {
            // Almacena la respuesta en una variable, si es 202 es que se obtuvo correctamente
            const response = request.responseText;
            const json = JSON.parse(response);
            
            if (request.status === 401 || request.status === 403) {
                alert(json.detail);
            }
            else if (request.status == 202){
                const response = request.responseText;
                const json = JSON.parse(response);
                for (let a = 0; a < json.length; a++) {
                    var tr = document.createElement('tr');
                    var id_cliente = document.createElement('td');
                    var nombre = document.createElement('td');
                    var email = document.createElement('td');
                    var detalle = document.createElement('td');
                    var actualizar = document.createElement('td');
                    var eliminar = document.createElement('td');

                    id_cliente.innerHTML = json[a].id_cliente;
                    nombre.innerHTML = json[a].nombre;
                    email.innerHTML = json[a].email;
                    detalle.innerHTML = "<a href='/get_cliente.html?" + json[a].id_cliente + "'>Ver</a>";
                    actualizar.innerHTML = "<a href='/put_cliente.html?" + json[a].id_cliente + "'>Actualizar</a>";
                    eliminar.innerHTML = "<a href='/delete_cliente.html?" + json[a].id_cliente +  "'>Eliminar</a>";

                    tr.appendChild(id_cliente);
                    tr.appendChild(nombre);
                    tr.appendChild(email);
                    tr.appendChild(detalle);
                    tr.appendChild(actualizar);
                    tr.appendChild(eliminar);

                    tblBody.appendChild(tr);
                }
                tabla.appendChild(tblHead);
                tabla.appendChild(tblBody);
        }    
    };
    request.send();
};