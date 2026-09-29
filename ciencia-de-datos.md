# Ciencia de datos para un taller de calzado

Análisis predictivo construido sobre los datos del sistema de taller y ventas que diseñé y desarrollé para la zapatería de mi familia. Responde tres preguntas de negocio:

1. **¿Qué clientes no van a regresar?** Modelo de abandono con validación temporal (regresión logística y gradient boosting contra una regla base).
2. **¿Cuánto vale cada cliente?** Segmentación RFM y valor esperado a 12 meses, con una lista priorizada de clientes para campañas.
3. **¿Cuánto trabajo viene?** Pronóstico de demanda semanal evaluado a 1, 4 y 8 semanas contra el límite teórico por azar.

## Hallazgos principales

- El modelo de abandono **empata con la regla simple "días sin venir"** para ordenar clientes. En un servicio de uso ocasional, gran parte del abandono es impredecible (el cliente simplemente no necesitó una reparación). El valor del modelo está en dar probabilidades calibradas y en medir factores controlables.
- **Entregar tarde se asocia con más abandono**, y los retrasos se disparan cuando el taller se satura. Esto conecta operación y retención.
- El pronóstico semana a semana está cerca del límite por azar; su utilidad real es anticipar la temporada alta con semanas de anticipación.

## Sobre los datos

El sistema empezó a usarse recientemente, así que el análisis corre sobre **dos años de datos simulados** con el formato exacto que exporta el sistema. El simulador (`simular_datos.py`) sigue un modelo BG/NBD de comportamiento de clientes con efectos conocidos (estacionalidad, saturación, impacto de los retrasos), lo que permite verificar que el método detecta patrones que sabemos que existen. Con datos reales, solo se reemplazan los CSV.

## Cómo ejecutarlo

```bash
pip install -r requirements.txt
python simular_datos.py          # genera datos/Reparaciones.csv y datos/Ventas y cobros.csv
jupyter notebook analisis_taller.ipynb
```

Para usar datos reales: exporta los CSV desde el sistema (Ajustes → Respaldos), colócalos en `datos/` y cambia `HOY` a la fecha de exportación.

## Estructura

| Archivo | Contenido |
|---|---|
| `analisis_taller.ipynb` | Análisis completo con resultados y gráficas |
| `simular_datos.py` | Generador de datos con el formato del sistema |
| `lista_para_campana.csv` | Clientes prioritarios (alto valor y alto riesgo) |
| `datos/` | CSV de entrada (se generan con `simular_datos.py`) |

**Herramientas:** Python, pandas, scikit-learn, SciPy, matplotlib.
