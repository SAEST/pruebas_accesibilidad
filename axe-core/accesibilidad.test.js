const { Builder } = require('selenium-webdriver');
const AxeBuilder = require('@axe-core/webdriverjs');
const fs = require('fs');
const { Parser } = require('json2csv');

(async function pruebaAccesibilidad() {
  // Inicializa el navegador
  let driver = await new Builder().forBrowser('chrome').build();

  try {
    // Cargar la página pública que deseas probar
    await driver.get('https://ine.mx');

    // Ejecutar prueba de accesibilidad
    const resultados = await new AxeBuilder(driver).analyze();

    // Mostrar resultados en consola
    if (resultados.violations.length > 0) {
      console.log('⚠️ Problemas de accesibilidad encontrados:');
      resultados.violations.forEach((violation, index) => {
        console.log(`\n${index + 1}. ${violation.help}`);
        console.log(`Descripción: ${violation.description}`);
        console.log(`Impacto: ${violation.impact}`);
        console.log('Nodos afectados:');
        violation.nodes.forEach(node => {
          console.log(`- ${node.html}`);
          // Guardar resultados en archivo JSON
        fs.writeFileSync('resultados-accesibilidad.json', JSON.stringify(resultados, null, 2));
        console.log('✅ Resultados exportados a resultados-accesibilidad.json');
        // Extraer los datos que nos interesan
        const data = resultados.violations.flatMap(v =>
        v.nodes.map(n => ({
            pagina: 'https://ine.mx', // Puedes parametrizarlo
            severidad: v.impact,
            codigo: v.id,
            problema: v.help,
            descripcion: v.description,
            elemento: n.html,
            sugerencia: v.helpUrl
        }))
        );

        const campos = ['pagina', 'severidad', 'codigo', 'problema', 'descripcion', 'elemento', 'sugerencia'];
        const csvParser = new Parser({ fields: campos });
        const csv = csvParser.parse(data);

        fs.writeFileSync('resultados-accesibilidad.csv', csv);
        console.log('✅ Archivo CSV con formato mejorado generado');
        });
      });
    } else {
      console.log('✅ No se encontraron problemas de accesibilidad.');
    }
  } catch (error) {
    console.error('Error en la prueba:', error);
  } finally {
    await driver.quit();
  }
})();
