var id =window.location.search.substring(1);

let id_cliente = document.getElementById("id_cliente");

id_cliente.value = id;
function putCliente(){
    username= "admin";
    password= "admin";

    let id_cliente = document.getElementById("id_cliente");
    let nombre = document.getElementById("nombre");
    let email = document.getElementById("email");

    console.log(nombre.value);
    console.log(email.value);

    var request = new XMLHttpRequest();
    request.open('PUT', 'https://8000-yesenia19-apirest-6xk2vh2kwcd.ws-us53.gitpod.io/PUT/'+ id_cliente.value+'&'+nombre.value + '&' + email.value, true);
    request.setRequestHeader("Accept", "application/json");
    request.setRequestHeader("Authorization", "Basic " + btoa(username + ":" + password))
    request.setRequestHeader("Content-Type", "application/json");
    request.onload = () => {
            // Almacena la respuesta en una variable, si es 202 es que se obtuvo correctamente

            if (request.status === 401 || request.status === 403) {
                alert(json.detail);
            }
            else if (request.status == 202){
                const response = request.responseText;
                const json = JSON.parse(response);
                console.log(json);

                if (request.status == 202){
                    alert("Usuario actualizado")
                    window.location.replace("/get_clientes.html")
                }
            }      
    };
    request.send();
};