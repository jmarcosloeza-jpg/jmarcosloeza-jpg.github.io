# Prepárate: plataforma de preparación para entrevistas técnicas

**Demo en vivo:** https://jmarcosloeza-jpg.github.io/preparate.html

Aplicación web para prepararse para entrevistas de **Scrum Master**, **ingeniería de datos** y **cloud y DevOps**. Nació al prepararme para vacantes que pedían Scrum, Jira, Confluence, Azure DevOps, Scala y fundamentos de nube.

## Qué incluye

- **Tres rutas de estudio** con 25 lecciones, tarjetas de memoria, exámenes con explicación de cada respuesta y preguntas de entrevista con respuestas modelo.
- **Plan de 14 días** con seguimiento de avance e indicador de preparación por ruta.
- **Laboratorio práctico:**
  - **Simulador de Sprint:** Sprint Planning con velocidad histórica y capacidad reducida, elección del Sprint Goal, historias que no cumplen la Definition of Ready, tablero con límite de trabajo en curso, burndown diario y tres imprevistos (cambio de alcance, impedimento con otro equipo e incidente en producción) con retroalimentación sobre cada decisión.
  - **Práctica de JQL:** 11 retos contra 17 incidencias de ejemplo, con validación de resultados.
  - **Ejercicios de Scala:** 17 preguntas de "¿qué imprime?" y "completa el código", de lo básico a Spark.
- **Simulador de entrevista con IA** (en la versión alojada en Claude): califica respuestas del 0 al 10, señala fortalezas y áreas de mejora y propone una versión mejorada.

## Retos técnicos

### Intérprete de JQL
Escribí un intérprete para un subconjunto real del lenguaje de consultas de Jira:

1. **Tokenizador:** separa campos, operadores, valores entre comillas, funciones como `currentUser()` y palabras reservadas.
2. **Analizador sintáctico descendente:** respeta la precedencia de `AND` sobre `OR`, los paréntesis y `NOT`.
3. **Evaluación con la semántica de Jira:** `is EMPTY`, `in (...)`, comparaciones de prioridad, fechas relativas como `-7d`, y la regla de que `assignee != luis` no devuelve incidencias sin responsable.

Cada reto compara el conjunto de resultados del usuario con el de la consulta de referencia y muestra qué incidencias faltan o sobran.

### Simulador de Sprint
El avance diario depende de la capacidad del equipo y del trabajo en curso: con más de tres tarjetas activas la eficiencia baja, y las historias que no estaban listas tardan más. Verifiqué que jugando con buenas prácticas se cumple el Sprint Goal y con malas decisiones no.

### Control de calidad del contenido
Validé automáticamente que cada pregunta tenga una respuesta válida. Al revisar los ejercicios de Scala detecté que `100.0 * 1.16` no da `116.0` sino `115.99999999999999` por la aritmética de punto flotante; corregí el ejercicio y agregué la explicación.

## Sobre esta versión
En GitHub Pages funcionan todas las secciones excepto el simulador de entrevista con IA, que requiere el entorno de Claude. El avance se guarda en el navegador.

## Tecnologías
JavaScript sin dependencias, HTML, CSS y SVG.
