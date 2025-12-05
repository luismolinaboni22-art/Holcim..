from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime

app = Flask(__name__)

# ------------------------
#   USUARIOS
# ------------------------
USERS = {
    "CoordinadorHolcim": "123"
}

# ------------------------
#   MEMORIAS TEMPORALES
# ------------------------
VISITORS = []
CONTRACTORS = []
PROVIDERS = []

# ------------------------
#       LOGIN
# ------------------------
@app.route("/")
def login():
    return render_template("login.html")


@app.route("/auth", methods=["POST"])
def auth():
    username = request.form.get("username")
    password = request.form.get("password")

    if username in USERS and USERS[username] == password:
        return redirect(url_for("home"))

    return render_template("login.html", error="Credenciales incorrectas")


# ------------------------
#   PÁGINA PRINCIPAL
# ------------------------
@app.route("/home")
def home():
    visitantes_dentro = sum(1 for v in VISITORS if v["hora_salida"] is None)
    contratistas_dentro = sum(1 for c in CONTRACTORS if c["hora_salida"] is None)
    proveedores_dentro = sum(1 for p in PROVIDERS if p["hora_salida"] is None)

    return render_template(
        "home.html",
        visitantes_dentro=visitantes_dentro,
        contratistas_dentro=contratistas_dentro,
        proveedores_dentro=proveedores_dentro
    )


# ------------------------
#   REGISTRO DE VISITANTES
# ------------------------
@app.route("/registro", methods=["GET", "POST"])
def registro():

    if request.method == "POST":
        visitante = {
            "nombre": request.form["nombre"],
            "cedula": request.form["cedula"],
            "empresa": request.form["empresa"],
            "responsable": request.form["responsable"],
            "placa": request.form["placa"],
            "motivo": request.form["motivo"],
            "hora_ingreso": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "hora_salida": None
        }

        VISITORS.append(visitante)

        return render_template("visitor_success.html", visitante=visitante)

    return render_template("visitor_form.html", visitors=VISITORS)


@app.route("/salida/<int:index>")
def salida(index):
    VISITORS[index]["hora_salida"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return redirect(url_for("registro"))


# ------------------------
#   REGISTRO DE CONTRATISTAS
# ------------------------
@app.route("/contratistas", methods=["GET", "POST"])
def contratistas():

    if request.method == "POST":
        contratista = {
            "nombre": request.form["nombre"],
            "cedula": request.form["cedula"],
            "empresa": request.form["empresa"],
            "responsable": request.form["responsable"],
            "hora_ingreso": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "hora_salida": None
        }

        CONTRACTORS.append(contratista)

        return render_template("contractor_success.html", contratista=contratista)

    return render_template("contractor_form.html", contractors=CONTRACTORS)


@app.route("/salida_contratista/<int:index>")
def salida_contratista(index):
    CONTRACTORS[index]["hora_salida"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return redirect(url_for("contratistas"))


# ------------------------
#   REGISTRO DE PROVEEDORES
# ------------------------
@app.route("/proveedores", methods=["GET", "POST"])
def proveedores():

    if request.method == "POST":
        proveedor = {
            "nombre": request.form["nombre"],
            "cedula": request.form["cedula"],
            "empresa": request.form["empresa"],
            "responsable": request.form["responsable"],
            "motivo": request.form["motivo"],
            "hora_ingreso": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "hora_salida": None
        }

        PROVIDERS.append(proveedor)

        return render_template("provider_success.html", proveedor=proveedor)

    return render_template("provider_form.html", providers=PROVIDERS)


@app.route("/salida_proveedor/<int:index>")
def salida_proveedor(index):
    PROVIDERS[index]["hora_salida"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return redirect(url_for("proveedores"))
# ------------------------
#       REPORTES
# ------------------------
@app.route("/reportes", methods=["GET"])
def reportes():
    return render_template(
        "reportes.html",
        visitantes=VISITORS,
        contratistas=CONTRACTORS,
        proveedores=PROVIDERS
    )
# ------------------------
#   CREAR USUARIO
# ------------------------
@app.route("/crear_usuario", methods=["GET", "POST"])
def crear_usuario():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        role = request.form["role"]

        for u in USERS:
            if u["username"] == username:
                return render_template("crear_usuario.html", error="Usuario ya existe")

        hashed = bcrypt.generate_password_hash(password).decode("utf-8")
        USERS.append({"username": username, "password": hashed, "role": role})
        return render_template("crear_usuario.html", success="Usuario creado exitosamente")

    return render_template("crear_usuario.html")

# ------------------------
#   CAMBIAR CONTRASEÑA
# ------------------------
@app.route("/cambiar_password", methods=["GET", "POST"])
def cambiar_password():
    if request.method == "POST":
        username = request.form["username"]
        old_pass = request.form["old_password"]
        new_pass = request.form["new_password"]

        for u in USERS:
            if u["username"] == username and bcrypt.check_password_hash(u["password"], old_pass):
                u["password"] = bcrypt.generate_password_hash(new_pass).decode("utf-8")
                return render_template("cambiar_password.html", success="Contraseña actualizada correctamente")
        return render_template("cambiar_password.html", error="Usuario o contraseña incorrecta")
    
    return render_template("cambiar_password.html")


# ------------------------
#       RUN LOCAL
# ------------------------
if __name__ == "__main__":
    app.run(debug=True)



