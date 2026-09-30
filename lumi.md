# Lumi: aprende a tu ritmo

**Demo en vivo:** https://jmarcosloeza-jpg.github.io/lumi.html

Aplicación educativa para celular dirigida a niños de 4 a 12 años con TDAH, acompañada por Lumi, una luciérnaga animada original.

## Qué incluye

- **Cinco mundos:** Números (contar, sumar y restar, series, multiplicar), Letras (reconocer letras, primeras letras, completar palabras y frases), Atención (memorama, Simón dice, "toca solo las estrellas" y encontrar el diferente), Emociones (reconocer emociones, estrategias para manejarlas y ordenar rutinas) y Música (agudo o grave, contar aplausos, repetir melodías y un xilófono libre).
- **Tres niveles de edad:** el contenido de cada actividad cambia según la edad configurada.
- **Rincón de calma** con un globo que guía la respiración y **Mi rutina** con pasos visuales para la mañana y la noche.
- **Álbum de stickers** que se ganan al completar misiones con tres estrellas.
- **Área para padres** protegida (mantener presionado 3 segundos) con nombre, edad, tiempo diario de juego, voz, pausas y avance por mundo.

## Decisiones de diseño para el TDAH

- **Misiones cortas** de cinco preguntas, con indicador visible de cuánto falta.
- **Una instrucción a la vez**, leída en voz alta con síntesis de voz, para que también sirva a quien aún no lee.
- **Recompensa inmediata** con sonido, animación y estrellas.
- **Aprendizaje sin frustración:** después de dos errores, la respuesta correcta se ilumina.
- **Pausas de movimiento** de 15 segundos entre misiones y **límite de tiempo diario** que configuran los padres.
- **Actividades de control inhibitorio**, como tocar solo las estrellas e ignorar los distractores.

## Validación

Probé automáticamente todas las actividades de opción múltiple en los tres niveles de edad y los juegos especiales (memorama, Simón dice, ordenar la rutina, pausas, respiración y área de padres) sin errores.

## Limitaciones

Es un apoyo para practicar en casa y no sustituye la orientación de profesionales de la salud o de la educación. La voz depende del dispositivo, y las imágenes son emojis, por lo que se ven distintas en cada sistema.

## Tecnologías

JavaScript sin dependencias, Web Audio API para sonidos y xilófono, Web Speech API para la voz, SVG y Canvas para la mascota y las animaciones.
