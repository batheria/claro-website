import requests





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

# --- Prueba del código ---
# Usamos una API pública de prueba que devuelve un JSON
