import json
import pandas as pd

# Rutas
archivo_json = "ine.mx-20250725T132007.json"
archivo_csv = "lighthouse_completo_formateado.csv"

# Cargar JSON
with open(archivo_json, 'r', encoding='utf-8-sig') as f:
    data = json.load(f)

# Mapear ID de auditoría a categoría (accessibility, performance, etc.)
id_to_categoria = {}
for cat_name, categoria in data['categories'].items():
    for audit in categoria.get('auditRefs', []):
        id_to_categoria[audit['id']] = cat_name

# Preparar lista de auditorías completas
auditorias = []
for audit_id, audit in data['audits'].items():
    auditorias.append({
        "Categoría": id_to_categoria.get(audit_id, "N/A"),
        "ID": audit_id,
        "Título": audit.get('title', ''),
        "Descripción": audit.get('description', ''),
        "Puntaje": audit.get('score'),
        "Explicación": audit.get('explanation', ''),
        "Ayuda URL": audit.get('helpUrl', '')
    })

# Crear y exportar DataFrame
df = pd.DataFrame(auditorias)
df.to_csv(archivo_csv, index=False)
print(f"✅ Exportado a {archivo_csv}")
