# Reprocesar el archivo JSON subido, revisando más profundamente si hay datos válidos en la categoría de accesibilidad

import json
import pandas as pd

# Ruta del archivo
json_path = "ine.mx-20250725T132007.json"
with open(json_path, 'r', encoding='utf-8-sig') as f:
    data = json.load(f)

# Revisar contenido de auditorías específicamente de accesibilidad
accesibilidad_auditorias = [
    audit for audit in data['audits'].values()
    if audit.get('score') is not None and audit['score'] < 1 and 'accessibility' in audit.get('tags', [])
]

# Si no hay etiquetas de accesibilidad, intentar con la categoría específica
if not accesibilidad_auditorias and 'categories' in data:
    accesibilidad_auditorias = []
    for audit_id in data['categories']['accessibility'].get('auditRefs', []):
        ref = data['audits'].get(audit_id['id'], {})
        if ref.get('score') is not None and ref['score'] < 1:
            accesibilidad_auditorias.append({
                "ID": audit_id['id'],
                "Título": ref.get('title', ''),
                "Descripción": ref.get('description', ''),
                "Puntaje": ref.get('score'),
                "Explicación": ref.get('explanation', ''),
                "Ayuda URL": ref.get('helpUrl', '')
            })

# Convertir a DataFrame y exportar si hay datos
df = pd.DataFrame(accesibilidad_auditorias)
csv_path = "lighthouse_accesibilidad.csv"
df.to_csv(csv_path, index=False)

csv_path if not df.empty else "⚠️ No se encontraron auditorías de accesibilidad con score < 1."
