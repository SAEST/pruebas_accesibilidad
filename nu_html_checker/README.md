# pruebas_accesibilidad/nu_html_checker

CMD:
java -jar ./jar/vnu.jar --format json https://ine.mx > informe_web.json 2>&1

java -jar ./jar/vnu.jar --format json https://ine.mx > informe.json 2> informe_errores_vnu.txt