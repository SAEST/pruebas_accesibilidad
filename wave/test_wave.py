import requests
import csv
import json

# --- Configuración ---
# Sustituye 'TU_CLAVE_API_WAVE' con tu clave de API real de WAVE
WAVE_API_KEY = 'g91g92e45627'
# URL de la página que quieres analizar
URL_A_ANALIZAR = 'https://ine.mx' # Puedes cambiar esta URL

# Archivo de salida CSV
NOMBRE_ARCHIVO_CSV = 'informe_accesibilidad_wave.csv'

# --- Función para obtener datos de la API de WAVE ---
def obtener_datos_wave(url, api_key):
    api_endpoint = f"https://wave.webaim.org/api/request?key={api_key}&url={url}&reporttype=2"
    try:
        response = requests.get(api_endpoint)
        response.raise_for_status()  # Lanza un error para códigos de estado HTTP 4xx/5xx
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error al conectar con la API de WAVE: {e}")
        return None

# --- Función para procesar y exportar a CSV ---
def exportar_a_csv(datos_wave, nombre_archivo):
    if not datos_wave:
        print("No hay datos para exportar.")
        return

    # Definir los encabezados del CSV
    encabezados = [
        'Tipo de Problema',
        'ID del Problema',
        'Descripción (WCAG)',
        'Contexto (fragmento de código)',
        'WCAG Nivel',
        'Principios WCAG',
        'Elemento Selector (XPath/CSS)'
    ]

    # Crear una lista para almacenar las filas de datos
    filas_datos = []

    # Procesar errores (categories.error)
    if 'categories' in datos_wave and isinstance(datos_wave['categories'], dict) and 'error' in datos_wave['categories']:
        errors = datos_wave['categories']['error']
        if isinstance(errors, list):
            for error in errors:
                filas_datos.append([
                    'Error',
                    error.get('id', 'N/A'),
                    error.get('description', 'N/A'),
                    error.get('context', 'N/A'),
                    error.get('level', 'N/A'),
                    error.get('principles', 'N/A'),
                    error.get('selector', 'N/A')
                ])

    # Procesar alertas (categories.alert)
    if 'categories' in datos_wave and isinstance(datos_wave['categories'], dict) and 'alert' in datos_wave['categories']:
        alerts_dict = datos_wave['categories']['alert']
        if isinstance(alerts_dict, dict):
            for alert_type, alerts in alerts_dict.items():
                if isinstance(alerts, dict) and 'items' in alerts and isinstance(alerts['items'], list):
                    for alert_item in alerts['items']:
                        filas_datos.append([
                            'Alerta',
                            alert_item.get('id', 'N/A'),
                            alert_item.get('description', 'N/A'),
                            alert_item.get('context', 'N/A'),
                            alert_item.get('level', 'N/A'),
                            alert_item.get('principles', 'N/A'),
                            alert_item.get('selector', 'N/A')
                        ])

    # Abrir y escribir en el archivo CSV
    try:
        with open(nombre_archivo, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(encabezados) # Escribir los encabezados
            writer.writerows(filas_datos) # Escribir las filas de datos
        print(f"Datos exportados exitosamente a '{nombre_archivo}'")
    except IOError as e:
        print(f"Error al escribir en el archivo CSV: {e}")

# --- Ejecución principal ---
if __name__ == "__main__":
    print(f"Analizando la URL: {URL_A_ANALIZAR}...")
    datos_analisis = obtener_datos_wave(URL_A_ANALIZAR, WAVE_API_KEY)

    if datos_analisis:
        print(json.dumps(datos_analisis, indent=2))
        # Imprime la estructura de categorías para depuración
        print("Estructura de 'categories':")
        print(json.dumps(datos_analisis.get('categories', {}), indent=2))

        # Guardar el JSON en un archivo
        with open('informe_accesibilidad_wave.json', 'w', encoding='utf-8') as jsonfile:
            json.dump(datos_analisis, jsonfile, ensure_ascii=False, indent=2)

        exportar_a_csv(datos_analisis, NOMBRE_ARCHIVO_CSV)
    else:
        print("No se pudieron obtener los datos de la API de WAVE.")