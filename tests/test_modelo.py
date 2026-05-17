"""Pruebas unitarias del modelo simulado y del registro de predicciones."""

from __future__ import annotations

import pytest

from modelo_simulado import CATEGORIAS, clasificar_estado
from registro_predicciones import (
    obtener_estadisticas,
    registrar_prediccion,
)


@pytest.fixture(autouse=True)
def registros_aislados(tmp_path, monkeypatch):
    """Estadísticas vacías por prueba usando archivos temporales."""
    registro = tmp_path / "predicciones.jsonl"
    reporte = tmp_path / "reporte_estadisticas.txt"
    monkeypatch.setattr("registro_predicciones.RUTA_REGISTRO", registro)
    monkeypatch.setattr("registro_predicciones.RUTA_REPORTE", reporte)
    yield


def test_clasificacion_enfermedad_leve():
    entrada = {
        "presion_sistolica": 140,
        "presion_diastolica": 90,
        "nivel_colesterol": 2,
        "nivel_glucosa": 2,
        "presencia_enfermedad": 0,
        "fumador": False,
    }
    assert clasificar_estado(entrada) == "ENFERMEDAD LEVE"


def test_estadisticas_vacias_al_inicio():
    stats = obtener_estadisticas()
    assert stats["total_predicciones"] == 0
    assert stats["fecha_ultima_prediccion"] is None
    assert stats["ultimas_5_predicciones"] == []
    for categoria in CATEGORIAS:
        assert stats["totales_por_categoria"][categoria] == 0


def test_registro_y_ultima_prediccion_coincide():
    entrada = {
        "presion_sistolica": 118,
        "presion_diastolica": 76,
        "nivel_colesterol": 1,
        "nivel_glucosa": 1,
        "presencia_enfermedad": 0,
        "fumador": False,
    }
    esperado = clasificar_estado(entrada)
    registrar_prediccion(esperado, entrada)

    stats = obtener_estadisticas()
    assert stats["total_predicciones"] == 1
    assert stats["totales_por_categoria"][esperado] == 1
    assert stats["ultimas_5_predicciones"][-1]["categoria"] == esperado
    assert stats["fecha_ultima_prediccion"] is not None


def test_las_cinco_categorias_son_alcanzables():
    casos = {
        "NO ENFERMO": {
            "presion_sistolica": 118,
            "presion_diastolica": 76,
            "nivel_colesterol": 1,
            "nivel_glucosa": 1,
            "presencia_enfermedad": 0,
            "fumador": False,
        },
        "ENFERMEDAD LEVE": {
            "presion_sistolica": 140,
            "presion_diastolica": 90,
            "nivel_colesterol": 2,
            "nivel_glucosa": 2,
            "presencia_enfermedad": 0,
            "fumador": False,
        },
        "ENFERMEDAD AGUDA": {
            "presion_sistolica": 180,
            "presion_diastolica": 80,
            "nivel_colesterol": 2,
            "nivel_glucosa": 1,
            "presencia_enfermedad": 0,
            "fumador": False,
        },
        "ENFERMEDAD CRÓNICA": {
            "presion_sistolica": 130,
            "presion_diastolica": 80,
            "nivel_colesterol": 2,
            "nivel_glucosa": 2,
            "presencia_enfermedad": 1,
            "fumador": False,
        },
        "ENFERMEDAD TERMINAL": {
            "presion_sistolica": 195,
            "presion_diastolica": 115,
            "nivel_colesterol": 3,
            "nivel_glucosa": 3,
            "presencia_enfermedad": 1,
            "fumador": True,
        },
    }
    obtenidas = {clasificar_estado(entrada) for entrada in casos.values()}
    assert obtenidas == set(CATEGORIAS)
