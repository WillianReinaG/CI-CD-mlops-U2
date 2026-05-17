"""
Servicio web de demostración (trabajo académico).
"""

from __future__ import annotations

from flask import Flask, jsonify, render_template, request

from modelo_simulado import CAMPOS_PERMITIDOS, CATEGORIAS, clasificar_estado, validar_entrada_minima
from registro_predicciones import obtener_estadisticas, registrar_prediccion

app = Flask(__name__)


def _extraer_cuerpo_json():
    if not request.is_json:
        return None
    return request.get_json(silent=True)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/predecir", methods=["POST"])
def predecir():
    payload = _extraer_cuerpo_json()
    if payload is None:
        return (
            jsonify(
                {
                    "ok": False,
                    "error": "Enviar JSON (Content-Type: application/json) con los campos permitidos.",
                    "campos_permitidos": sorted(CAMPOS_PERMITIDOS),
                }
            ),
            400,
        )

    if not isinstance(payload, dict):
        return jsonify({"ok": False, "error": "El cuerpo debe ser un objeto JSON."}), 400

    ok, msg = validar_entrada_minima(payload)
    if not ok:
        return jsonify({"ok": False, "error": msg}), 400

    try:
        estado = clasificar_estado(payload)
    except (KeyError, TypeError, ValueError) as exc:
        return jsonify({"ok": False, "error": f"Dato inválido: {exc}"}), 400

    registro = registrar_prediccion(estado, payload)
    return jsonify(
        {
            "ok": True,
            "estado": estado,
            "entrada": payload,
            "registrado_en": registro["fecha"],
        }
    )


@app.route("/estadisticas", methods=["GET"])
def estadisticas():
    """Reporte de predicciones para médicos (lee el archivo de registro)."""
    datos = obtener_estadisticas()
    return jsonify(
        {
            "ok": True,
            "categorias_validas": list(CATEGORIAS),
            **datos,
        }
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
