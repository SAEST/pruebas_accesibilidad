import json
import csv

# Nombre del archivo JSON generado por vnu.jar
json_file = 'informe_web.json'
# Nombre del archivo CSV de salida
csv_file = 'informe_html_checker.csv'

def json_to_csv_html_checker(json_filename, csv_filename):
    try:
        with open(json_filename, 'r', encoding='utf-8-sig') as f:
            data = json.load(f)

        messages = data.get('messages', []) # 'messages' es la clave principal para errores/advertencias

        if not messages:
            print("No se encontraron mensajes (errores/advertencias) en el archivo JSON.")
            return

        # Definir los encabezados del CSV
        headers = ['Tipo', 'Subtipo', 'Mensaje', 'Última Línea', 'Última Columna', 'Extracto de Código']

        with open(csv_filename, 'w', newline='', encoding='utf-8') as outfile:
            writer = csv.writer(outfile)
            writer.writerow(headers) # Escribir los encabezados

            for msg in messages:
                # Cada mensaje es un diccionario. Extraemos los campos relevantes.
                row = [
                    msg.get('type', 'N/A'),
                    msg.get('subtype', 'N/A'), # A veces hay un subtipo (e.g., "warning")
                    msg.get('message', 'N/A'),
                    msg.get('lastLine', 'N/A'),
                    msg.get('lastColumn', 'N/A'),
                    msg.get('extract', 'N/A') # Fragmento de código relevante
                ]
                writer.writerow(row)
        print(f"Informe exportado exitosamente a '{csv_filename}'")

    except FileNotFoundError:
        print(f"Error: El archivo '{json_filename}' no fue encontrado.")
    except json.JSONDecodeError:
        print(f"Error: No se pudo decodificar el JSON del archivo '{json_filename}'. Asegúrate de que es un JSON válido.")
    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")

if __name__ == "__main__":
    json_to_csv_html_checker(json_file, csv_file)