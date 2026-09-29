"""
Simulador de datos para el taller de calzado.

Genera dos años de historia con el MISMO formato que exporta el sistema
(Ajustes > Respaldos): "Reparaciones.csv" y "Ventas y cobros.csv".

El comportamiento de los clientes sigue un modelo BG/NBD (Fader, Hardie y Lee, 2005):
cada cliente tiene su propia frecuencia de visitas (Gamma) y una probabilidad de
dejar de venir después de cada visita (Beta). Sobre esa base se agregan efectos
conocidos para verificar que el análisis los detecta:

  * Estacionalidad: más trabajo en agosto (regreso a clases), temporada de lluvias
    y diciembre; los sábados son el día más fuerte y el domingo se cierra.
  * Carga de trabajo: en semanas saturadas aumentan los retrasos.
  * Retrasos: si a un cliente se le entrega tarde, es más probable que no regrese.

Se simulan tres años previos que se descartan, para que la clientela ya esté
formada al inicio del periodo (como en un negocio establecido).

Uso:  python simular_datos.py  [--semilla 7] [--salida datos]
"""
import argparse
from datetime import date, timedelta
from pathlib import Path

import numpy as np
import pandas as pd

INICIO = date(2024, 10, 1)
CALENTAMIENTO = date(2021, 10, 1)  # el negocio ya existía: se simulan 3 años previos y se descartan
FIN = date(2026, 9, 27)

NOMBRES = ("José María Juan Guadalupe Francisco Ana Luis Rosa Carlos Patricia Jorge Elena Miguel Laura "
           "Antonio Carmen Alejandro Sofía Ricardo Gabriela Fernando Verónica Arturo Leticia Eduardo Adriana "
           "Roberto Mónica Javier Claudia Manuel Alejandra Raúl Teresa Sergio Silvia Pedro Diana Héctor Lucía "
           "Daniel Martha Óscar Isabel Rafael Norma Enrique Beatriz Alberto Yolanda").split()
APELLIDOS = ("Hernández García Martínez López González Pérez Rodríguez Sánchez Ramírez Cruz Flores Gómez "
             "Morales Vázquez Reyes Jiménez Torres Díaz Gutiérrez Ruiz Mendoza Aguilar Ortiz Moreno Castillo "
             "Romero Álvarez Méndez Chávez Rivera Juárez Ramos Domínguez Herrera Medina Castro Vargas Guzmán").split()
CALZADO = ["Botas de piel", "Zapatos de vestir", "Zapatillas", "Botines", "Mocasines", "Tenis",
           "Zapatos escolares", "Sandalias", "Botas de trabajo", "Botas vaqueras", "Bolsa de piel", "Cinturón"]
COLORES = ["negros", "café", "miel", "blancos", "rojos", "grises", "azul marino", "vino"]
# trabajo: (probabilidad relativa, precio mínimo, precio máximo, días de trabajo)
TRABAJOS = {
    "Tapas": (26, 60, 120, 1), "Media suela": (16, 180, 320, 2), "Suela completa": (7, 350, 650, 3),
    "Tacón": (8, 90, 180, 1), "Costura": (14, 60, 180, 1), "Pegado": (14, 50, 120, 1),
    "Cambio de cierre": (6, 150, 260, 2), "Tinte": (6, 150, 300, 2), "Limpieza y lustrado": (10, 70, 150, 1),
    "Estirar": (4, 80, 150, 1), "Plantilla": (5, 60, 150, 1),
}
PRODUCTOS = [  # nombre, precio, costo, peso relativo, meses fuertes
    ("Zapato escolar", 640, 340, 5, {7, 8}), ("Tenis escolar", 590, 310, 4, {7, 8}),
    ("Bota vaquera", 2450, 1400, 1.5, {11, 12}), ("Zapato de vestir", 1290, 720, 3, {11, 12}),
    ("Zapatilla", 890, 450, 3, {5, 12}), ("Botín", 1350, 760, 2, {10, 11, 12, 1}),
    ("Mocasín", 1150, 640, 2, set()), ("Sandalia", 520, 260, 2, {3, 4, 5}),
    ("Crema para calzado", 95, 45, 8, set()), ("Agujetas", 35, 12, 7, set()), ("Plantilla de gel", 189, 95, 3, set()),
]
ESTACION_MES = {1: .85, 2: .85, 3: .95, 4: 1.0, 5: 1.0, 6: 1.15, 7: 1.2, 8: 1.35, 9: 1.15, 10: 1.0, 11: 1.05, 12: 1.3}
DIA_SEMANA = [0.8, 0.9, 0.95, 1.0, 1.1, 1.45, 0.0]  # lunes..domingo (domingo cerrado)
MAX_EST = max(ESTACION_MES.values()) * max(DIA_SEMANA)


def fecha_str(d):
    return d.isoformat() if d else ""


def simular(semilla=7):
    rng = np.random.default_rng(semilla)
    dias = (FIN - CALENTAMIENTO).days + 1

    # 1) Llegada de clientes nuevos (proceso de Poisson con estacionalidad)
    clientes, nuevos_por_dia = [], []
    for i in range(dias):
        d = CALENTAMIENTO + timedelta(days=i)
        lam = 1.05 * ESTACION_MES[d.month] * DIA_SEMANA[d.weekday()]
        nuevos_por_dia.append((d, rng.poisson(lam)))
    usados = set()
    for d, n in nuevos_por_dia:
        for _ in range(n):
            while True:
                nombre = f"{rng.choice(NOMBRES)} {rng.choice(APELLIDOS)} {rng.choice(APELLIDOS)}"
                if nombre not in usados:
                    usados.add(nombre)
                    break
            tel = f"55{rng.integers(10_000_000, 99_999_999)}" if rng.random() < 0.85 else ""
            clientes.append({
                "nombre": nombre, "tel": tel, "primera": d,
                "tasa": rng.gamma(1.6, 1.9),          # visitas por año mientras está activo
                "p_abandono": rng.beta(2.2, 7.5),      # prob. de no volver tras cada visita
            })

    # 2) Visitas de cada cliente (BG/NBD con adelgazamiento estacional)
    visitas = []
    for c in clientes:
        t = c["primera"]
        visitas.append((t, c))
        while True:
            # tiempo hasta la siguiente visita candidata, con thinning por estacionalidad
            while True:
                t = t + timedelta(days=max(1, int(rng.exponential(365 / (c["tasa"] * MAX_EST)))))
                if t > FIN:
                    break
                if rng.random() < ESTACION_MES[t.month] * DIA_SEMANA[t.weekday()] / MAX_EST:
                    break
            if t > FIN:
                break
            visitas.append((t, c))
            c.setdefault("proximas", []).append(t)

    # Ordenar y procesar en el tiempo para poder aplicar el abandono con retrasos reales
    visitas.sort(key=lambda x: x[0])
    CAPACIDAD = 27  # trabajos por semana que el taller saca sin presión
    from collections import deque
    recientes = deque()  # fechas de trabajos aceptados en los últimos 7 días (carga del taller)

    nombres_trab = list(TRABAJOS)
    pesos_trab = np.array([TRABAJOS[k][0] for k in nombres_trab], float)
    pesos_trab /= pesos_trab.sum()

    filas, movs = [], []
    activo = {id(c): True for c in clientes}
    folio = 0
    for d, c in visitas:
        if d.weekday() == 6:
            d = d + timedelta(days=1)
        if d > FIN or not activo[id(c)]:
            continue
        registrar = d >= INICIO
        if registrar:
            folio += 1
        k = rng.choice([1, 2, 3], p=[0.62, 0.3, 0.08])
        trabajos = list(rng.choice(nombres_trab, size=k, replace=False, p=pesos_trab))
        precio = int(sum(rng.integers(TRABAJOS[j][1], TRABAJOS[j][2] + 1) for j in trabajos) // 10 * 10)
        anticipo = int(round(precio * rng.choice([0, 0.3, 0.5, 1.0], p=[0.35, 0.2, 0.35, 0.1]) / 10) * 10)
        dias_trab = max(TRABAJOS[j][3] for j in trabajos)
        prometido = d + timedelta(days=int(dias_trab + rng.integers(1, 4)))
        while recientes and (d - recientes[0]).days >= 7:
            recientes.popleft()
        recientes.append(d)
        saturacion = len(recientes) / CAPACIDAD
        # Retraso: más probable cuando el taller está saturado
        p_tarde = min(0.85, 0.12 * saturacion ** 3)
        atraso = int(rng.integers(1, 6)) if rng.random() < p_tarde else -int(rng.integers(0, 2))
        listo = prometido + timedelta(days=atraso)
        if listo < d:
            listo = d
        recoge = listo + timedelta(days=int(rng.choice([0, 1, 2, 3, 5, 8, 15, 30], p=[.25, .2, .15, .12, .1, .08, .06, .04])))
        tarde = listo > prometido

        estado = "Entregado"
        if listo > FIN:
            estado, listo_s, entregado = ("En reparación" if d < FIN - timedelta(days=1) else "Recibido"), None, None
        elif recoge > FIN:
            estado, listo_s, entregado = "Listo para entregar", listo, None
        else:
            listo_s, entregado = listo, recoge
        pagado = precio - anticipo if entregado else 0
        calzado = f"{rng.choice(CALZADO)} {rng.choice(COLORES)}"
        if registrar:
          filas.append({
            "Folio": f"R-{folio:04d}", "Cliente": c["nombre"], "Teléfono": c["tel"], "Calzado": calzado,
            "Trabajos": "; ".join(trabajos), "Observaciones": "", "Precio": precio, "Anticipo": anticipo,
            "Pagado al entregar": pagado, "Resta": precio - anticipo - pagado, "Estado": estado,
            "Recibido": fecha_str(d), "Entrega prometida": fecha_str(prometido),
            "Listo": fecha_str(listo_s), "Entregado": fecha_str(entregado),
        })
        if registrar and anticipo:
            movs.append((d, "Taller", f"Anticipo R-{folio:04d}, {c['nombre']}", anticipo, "", ""))
        if registrar and entregado and pagado:
            movs.append((entregado, "Taller", f"Saldo R-{folio:04d}, {c['nombre']}", pagado, "", ""))

        # ¿Vuelve? Abandono base del cliente + efecto de haberle entregado tarde
        p = c["p_abandono"] + (0.22 if tarde else 0.0)
        if rng.random() < p:
            activo[id(c)] = False

    # 3) Ventas de calzado y accesorios
    pesos = np.array([p[3] for p in PRODUCTOS], float)
    for i in range((FIN - INICIO).days + 1):
        d = INICIO + timedelta(days=i)
        if d.weekday() == 6:
            continue
        n = rng.poisson(2.1 * ESTACION_MES[d.month] * DIA_SEMANA[d.weekday()])
        for _ in range(n):
            w = pesos * np.array([2.5 if d.month in p[4] else 1 for p in PRODUCTOS])
            prod = PRODUCTOS[rng.choice(len(PRODUCTOS), p=w / w.sum())]
            movs.append((d, "Venta", prod[0], prod[1], prod[2], prod[1] - prod[2]))

    rep = pd.DataFrame(filas)
    metodos = ["Efectivo", "Tarjeta", "Transferencia"]
    ven = pd.DataFrame([{
        "Fecha": fecha_str(m[0]), "Hora": f"{rng.integers(10, 19)}:{rng.integers(0, 60):02d}",
        "Tipo": m[1], "Descripción": m[2], "Forma de pago": rng.choice(metodos, p=[.62, .25, .13]),
        "Monto": m[3], "Costo": m[4], "Ganancia": m[5]} for m in movs]).sort_values(["Fecha", "Hora"])
    return rep, ven


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--semilla", type=int, default=7)
    ap.add_argument("--salida", default="datos")
    a = ap.parse_args()
    rep, ven = simular(a.semilla)
    out = Path(a.salida); out.mkdir(exist_ok=True)
    rep.to_csv(out / "Reparaciones.csv", index=False, encoding="utf-8-sig")
    ven.to_csv(out / "Ventas y cobros.csv", index=False, encoding="utf-8-sig")
    print(f"{len(rep):,} reparaciones de {rep['Cliente'].nunique():,} clientes; {len(ven):,} movimientos de caja.")
