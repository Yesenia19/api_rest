import web
urls=(
    "/",  "Index",
    "/get_clientes/", "get_clientes",
    "/clientes/get/(.*)",       "GetCliente",
    "/clientes/post/(.*)",     "PostCliente",
    "/clientes/put/(.*)",      "PutCliente",
    "/clientes/delete/(.*)",   "DeleteCliente",
)

app = web.application(urls, globals())
render = web.template.render("templates/")


class getclientes:
    def GET(self):
        return render.get_clientes()

           
if __name__ == "__main__":
    app.run()