"""
Persistencia académica de predicciones en archivo de texto (JSONL + reporte legible).
"""

from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from modelo_simulado import CATEGORIAS

RUTA_REGISTRO = Path(
    os.environ.get("REGISTRO_PREDICCIONES", "datos/predicciones.jsonl")
)
RUTA_REPORTE = Path(
    os.environ.get("REPORTE_ESTADISTICAS", "datos/reporte_estadisticas.txt")
)


def _asegurar_directorio() -> None:
    RUTA_REGISTRO.parent.mkdir(parents=True, exist_ok=True)


def leer_registros() -> list[dict[str, Any]]:
    if not RUTA_REGISTRO.exists():
        return []
    registros: list[dict[str, Any]] = []
    with RUTA_REGISTRO.open(encoding="utf-8") as archivo:
        for linea in archivo:
            linea = linea.strip()
            if linea:
                registros.append(json.loads(linea))
    return registros


def _escribir_reporte_texto(estadisticas: dict[str, Any]) -> None:
    lineas = [
        "=== Reporte de predicciones (simulado) ===",
        f"Generado: {datetime.now(timezone.utc).isoformat()}",
        f"Total de predicciones: {estadisticas['total_predicciones']}",
        f"Fecha última predicción: {estadisticas['fecha_ultima_prediccion'] or '—'}",
        "",
        "Totales por categoría:",
    ]
    for categoria in CATEGORIAS:
        total = estadisticas["totales_por_categoria"][categoria]
        lineas.append(f"  - {categoria}: {total}")

    lineas.extend(["", "Últimas 5 predicciones:"])
    if not estadisticas["ultimas_5_predicciones"]:
        lineas.append("  (sin registros)")
    else:
        for i, registro in enumerate(estadisticas["ultimas_5_predicciones"], start=1):
            lineas.append(
                f"  {i}. [{registro['fecha']}] {registro['categoria']} | entrada={registro['entrada']}"
            )

    RUTA_REPORTE.write_text("\n".join(lineas) + "\n", encoding="utf-8")


def obtener_estadisticas() -> dict[str, Any]:
    registros = leer_registros()
    totales = {categoria: 0 for categoria in CATEGORIAS}
    for registro in registros:
        categoria = registro.get("categoria")
        if categoria in totales:
            totales[categoria] += 1

    ultimas_5 = registros[-5:]
    fecha_ultima = registros[-1]["fecha"] if registros else None

    return {
        "totales_por_categoria": totales,
        "ultimas_5_predicciones": ultimas_5,
        "fecha_ultima_prediccion": fecha_ultima,
        "total_predicciones": len(registros),
        "archivo_registro": str(RUTA_REGISTRO),
        "archivo_reporte": str(RUTA_REPORTE),
    }


def registrar_prediccion(categoria: str, entrada: dict[str, Any]) -> dict[str, Any]:
    _asegurar_directorio()
    registro = {
        "fecha": datetime.now(timezone.utc).isoformat(),
        "categoria": categoria,
        "entrada": entrada,
    }
    with RUTA_REGISTRO.open("a", encoding="utf-8") as archivo:
        archivo.write(json.dumps(registro, ensure_ascii=False) + "\n")

    estadisticas = obtener_estadisticas()
    _escribir_reporte_texto(estadisticas)
    return registro
