# Bit: gimnasio de programación

**Demo en vivo:** https://jmarcosloeza-jpg.github.io/bit.html

Aplicación para practicar JavaScript un poco cada día, con retroalimentación inmediata y elementos de juego que ayudan a mantener la constancia.

## Qué incluye

- **30 retos** en cinco rutas: Fundamentos, Texto y cadenas, Arreglos y objetos, Datos con JavaScript (map, filter, reduce, estadística) y Algoritmos (búsqueda binaria, pilas, criba de Eratóstenes).
- **Editor de código** con resaltado de sintaxis, números de línea, sangría automática y atajo Ctrl + Enter.
- **Pruebas automáticas aisladas:** el código del usuario corre en un Web Worker con límite de 3 segundos, así un ciclo infinito no congela la página. Cada prueba muestra el valor esperado y el obtenido.
- **Progreso con juego:** experiencia, siete niveles, racha diaria, reto del día con experiencia doble y bono por resolver a la primera sin pistas.
- **Bit, una mascota animada original** en SVG que cambia de expresión según el resultado.
- **Tutor con IA** (en la versión alojada en Claude): da pistas sin revelar la solución y revisa el estilo del código. En esta versión de GitHub se reemplaza por consejos según el tipo de error y la solución se desbloquea tras 3 intentos.

## Decisiones de diseño

- **Retroalimentación antes que castigo:** los mensajes explican qué revisar según el error (sintaxis, variable inexistente, tipo, ciclo infinito).
- **Ver la solución tiene costo** (la mitad de la experiencia) para que sea el último recurso y no el primero.
- **Las 30 soluciones de referencia se validan** contra sus pruebas antes de publicar, para garantizar que cada reto es correcto.

## Tecnologías

JavaScript, Web Workers, HTML, CSS (animaciones), SVG y Canvas (confeti). Sin dependencias.
