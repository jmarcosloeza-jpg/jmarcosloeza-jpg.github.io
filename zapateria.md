# Sistema de taller, ventas y marketing para una zapatería

**Demo en vivo:** https://jmarcosloeza-jpg.github.io/zapateria.html (usa "Probar con datos de ejemplo")

Sistema web que diseñé y desarrollé para la zapatería de mi familia, un negocio que vende y repara calzado. Está pensado para que el dueño y sus empleados lo usen desde el celular.

## El problema

Un taller de reparación necesita saber en todo momento qué trabajos están pendientes o atrasados, cuánto se ha cobrado en el día y qué clientes han dejado de venir, y todo eso compartido entre varias personas que atienden el mostrador.

## La solución

- **Taller:** cada reparación es una nota con folio consecutivo, trabajos, fecha de entrega y saldo. Avanza por estados (recibido, en reparación, listo, entregado) y marca en rojo lo atrasado.
- **Notas imprimibles** en media carta o ticket térmico de 80 y 58 mm, con talón recortable para el calzado, y envío por WhatsApp.
- **Ventas, inventario y corte de caja** con separación por forma de pago y cálculo de diferencias.
- **Clientes:** historial, visitas y total gastado, con autocompletado al crear notas.
- **Marketing:** segmentación automática (sin recoger, inactivos, frecuentes, recientes), campañas por WhatsApp con registro de envíos y medición de cuántos clientes regresan. Programa de lealtad por sellos.
- **Resumen del negocio:** ingresos, ganancia, tiempo promedio de reparación, porcentaje entregado a tiempo, trabajos más pedidos y alertas.

## Retos técnicos

- **Varios usuarios a la vez:** en la versión de producción los datos se sincronizan en tiempo real. Para evitar folios duplicados cuando dos empleados registran al mismo tiempo, el contador se protege con un bloqueo temporal (lease) antes de incrementarse.
- **Permisos por rol:** los empleados registran; solo el administrador borra, ve costos y ganancias y exporta respaldos.
- **Diseño para el mostrador:** botones grandes, pocas pantallas y acciones de un toque, porque se usa con prisa y desde el celular.

## Proceso

El sistema se construyó por iteraciones: primero el control de reparaciones, ventas e inventario; después permisos, folios consecutivos, notas imprimibles, clientes y corte de caja; al final el módulo de marketing. Cada versión se probó en celular y computadora antes de la siguiente.

## Sobre esta versión

Esta demo guarda los datos solo en el navegador de quien la abre y no contiene información de clientes reales. La versión en producción usa una base de datos compartida.

## Tecnologías

JavaScript, HTML, CSS, SVG, jsPDF para las notas, base de datos documental en tiempo real (versión de producción).

## Proyecto relacionado

[Ciencia de datos para el taller](ciencia-de-datos.md): modelo de abandono de clientes, segmentación y pronóstico de demanda con los datos que exporta este sistema.
