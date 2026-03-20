import requests
from datetime import datetime

def esta_vencida(fecha_texto):
    """
    Verifica si una fecha en formato 'MM/AA' está vencida.
    Devuelve True si está vencida, False si aún es válida.
    """
    try:
        # 1. Separar el texto por la barra "/"
        # Ej: "12/32" -> mes_str = "12", anio_str = "32"
        mes_str, anio_str = fecha_texto.split('/')
        
        # 2. Convertir a números enteros
        mes_exp = int(mes_str)
        anio_exp = int(anio_str)
        
        # 3. Convertir el año de 2 dígitos a 4 dígitos (ej: 32 -> 2032)
        # Esto evita problemas al comparar con el año actual
        if anio_exp < 100:
            anio_exp += 2000
            
        # Validar que el mes tenga sentido (entre 1 y 12)
        if mes_exp < 1 or mes_exp > 12:
            return True # Consideramos vencida/inválida si el mes es irreal
            
        # 4. Obtener la fecha y año actuales
        hoy = datetime.now()
        mes_actual = hoy.month
        anio_actual = hoy.year
        
        # 5. Lógica de comparación
        if anio_exp < anio_actual:
            # Si el año de expiración es menor al actual, ya venció
            return True
        elif anio_exp == anio_actual and mes_exp < mes_actual:
            # Si es el mismo año, pero el mes de expiración ya pasó, ya venció
            return True
        else:
            # Si el año es mayor, o es el mismo año y el mes es igual o mayor, es válida
            return False
            
    except (ValueError, AttributeError):
        # Si el usuario ingresa algo raro como "Hola/Mundo" o no pone la barra
        return True # La marcamos como inválida/vencida por seguridad



def customer_date(dni):
    try:
        url = f'https://clientes.credicuotas.com.ar/v1/onboarding/resolvecustomers/{dni}'
        # 1. Hacemos la petición GET (si necesitas enviar datos, usarías requests.post)
        # Agregamos un 'timeout' de 5 segundos para que tu app no se quede congelada si el otro sitio falla
        print(url)
        respuesta = requests.get(url, timeout=5)
        print(respuesta)  
        # 2. Esto es clave: Lanza un error automáticamente si el sitio responde con un error (ej: 404 No Encontrado o 500 Error de Servidor)
        respuesta.raise_for_status()

        # 3. Convertimos la respuesta directamente a un diccionario de Python
        datos_json = respuesta.json()

        print("¡Petición exitosa!")
        return datos_json

    except requests.exceptions.Timeout:
        print("Error: El sitio tardó demasiado en responder.")
        return None
    except requests.exceptions.HTTPError as errHTTP:
        print(f"Error HTTP: {errHTTP}")
        return None
    except requests.exceptions.RequestException as e:
        # Captura cualquier otro error de conexión (no hay internet, URL mal escrita, etc.)
        print(f"Error de conexión: {e}")
        return None
    except ValueError:
        # Se ejecuta si el sitio respondió, pero el contenido NO era un JSON válido
        print("Error: El sitio no devolvió un JSON válido.")
        return None
