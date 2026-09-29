# Dashboard de finanzas personales

**Demo en vivo:** https://jmarcosloeza-jpg.github.io/finanzas.html

Aplicación web que convierte el estado de cuenta del banco (CSV) en un tablero claro: a dónde se va el dinero, cómo cambia cada categoría y qué cargos son inusuales. Todo se procesa en el navegador; los datos no se envían a ningún servidor.

## Qué hace

- **Carga de CSV flexible:** reconoce columnas de fecha, concepto y monto (o cargo y abono), fechas en varios formatos y separador coma o punto y coma.
- **Categorización automática** con un diccionario de comercios comunes en México. Las reglas más específicas ganan ("Uber Eats" va a comida antes que "Uber" a transporte).
- **Aprende de las correcciones:** si cambias la categoría de un movimiento, se aplica a todos los de ese comercio.
- **Detección de anomalías** con puntaje z modificado: `z = 0.6745 · (x − mediana) / MAD`. Un cargo se marca si z > 3.5 y además es más del doble de la mediana de su comercio o categoría.
- **Comparación contra el promedio histórico** de cada categoría y cálculo del ahorro mensual.

## Decisiones de diseño

- **Mediana y MAD en lugar de media y desviación estándar:** un solo gasto enorme infla la desviación estándar y esconde otras anomalías; la MAD es robusta a esos valores.
- **Una barra proporcional como elemento principal:** responde de un vistazo la pregunta más común ("¿en qué se me va el dinero?") antes que cualquier gráfica detallada.
- **Privacidad por diseño:** al no haber servidor, el usuario puede usar sus datos bancarios reales sin riesgo.

## Tecnologías

JavaScript, HTML, CSS y gráficas SVG hechas a mano, sin dependencias.

## Cómo usarlo

Abre la demo: carga con datos de ejemplo. Para ver los tuyos, exporta el estado de cuenta de tu banco en CSV y usa "Cargar mi CSV".
