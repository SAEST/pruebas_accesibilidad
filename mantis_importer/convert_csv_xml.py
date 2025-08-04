import csv
import xml.etree.ElementTree as ET

CSV_FILE = 'incidencias.csv'
XML_FILE = 'incidencia_import3.xml'

def csv_to_mantis_xml(csv_file, xml_file):
    mantis = ET.Element('mantis', {
        'version': '2.22.1',
        'urlbase': 'http://localhost:8989/',
        'issuelink': '#',
        'notelink': '~',
        'format': '1'
    })

    with open(csv_file, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            issue = ET.SubElement(mantis, 'issue')
            ET.SubElement(issue, 'project', id=row.get('project_id', '1')).text = row.get('project', 'TEST')
            ET.SubElement(issue, 'reporter', id=row.get('reporter_id', '1')).text = row.get('reporter', 'administrator')
            ET.SubElement(issue, 'handler', id=row.get('handler_id', '2')).text = row.get('handler', 'eric.ruiz')
            ET.SubElement(issue, 'priority', id=row.get('priority_id', '30')).text = row.get('priority', 'normal')
            ET.SubElement(issue, 'severity', id=row.get('severity_id', '50')).text = row.get('severity', 'menor')
            ET.SubElement(issue, 'reproducibility', id=row.get('reproducibility_id', '70')).text = row.get('reproducibility', 'no se ha intentado')
            ET.SubElement(issue, 'status', id=row.get('status_id', '50')).text = row.get('status', 'asignada')
            ET.SubElement(issue, 'resolution', id=row.get('resolution_id', '10')).text = row.get('resolution', 'abierta')
            ET.SubElement(issue, 'projection', id=row.get('projection_id', '10')).text = row.get('projection', 'ninguna')
            ET.SubElement(issue, 'category', id=row.get('category_id', '1')).text = row.get('category', 'General')
            ET.SubElement(issue, 'date_submitted').text = row.get('date_submitted', '1754091208')
            ET.SubElement(issue, 'last_updated').text = row.get('last_updated', '1754091208')
            ET.SubElement(issue, 'eta', id=row.get('eta_id', '10')).text = row.get('eta', 'ninguno')
            ET.SubElement(issue, 'os').text = row.get('os', 'Windows')
            ET.SubElement(issue, 'os_build').text = row.get('os_build', 'Enterprise')
            ET.SubElement(issue, 'platform').text = row.get('platform', '1')
            ET.SubElement(issue, 'view_state', id=row.get('view_state_id', '10')).text = row.get('view_state', 'público')
            ET.SubElement(issue, 'summary').text = row.get('summary', '[TEST] Crear incidencia importada')
            ET.SubElement(issue, 'due_date').text = row.get('due_date', '1')
            ET.SubElement(issue, 'description').text = row.get('description', 'Descripcion de la incidencia importada')
            ET.SubElement(issue, 'steps_to_reproduce').text = row.get('steps_to_reproduce', 'Pasos para reproducir la incidencia importada')
            ET.SubElement(issue, 'additional_information').text = row.get('additional_information', 'Informacion adicional de la incidencia importada')

    tree = ET.ElementTree(mantis)
    tree.write(xml_file, encoding='utf-8', xml_declaration=True)

if __name__ == "__main__":
    csv_to_mantis_xml(CSV_FILE, XML_FILE)