# CI/CD MLOps — Unidad 2

Repositorio para versionar y automatizar la solución de predicción de estado clínico desarrollada en la unidad anterior.

## Problema

Los médicos necesitan apoyarse en un modelo que, a partir de signos y datos del paciente, estime el **estado de enfermedad** y oriente la atención. En la unidad 1 se expuso un servicio local con Docker que devolvía una de cuatro categorías. En esta unidad el mismo escenario se mantiene, pero el foco pasa a **organizar el código en GitHub**, incorporar **nuevos requerimientos funcionales** y definir un **pipeline de CI/CD** con GitHub Actions.

## Propósito de este repositorio

- Centralizar la solución de predicción clínica simulada bajo control de versiones.
- Documentar el proyecto y su evolución mediante ramas y pull requests.
- Ampliar el modelo simulado (quinta categoría y reporte de estadísticas).
- Automatizar pruebas, comentarios en PRs y publicación de la imagen Docker en GitHub Packages.


## Estado actual del repositorio

En la rama `main` solo existe este archivo `README.md`. Aún no se ha integrado el código de la unidad 1 ni la configuración de CI/CD; eso se hará en ramas y PRs según la guía del curso.

## Estructura prevista

La siguiente organización es la **propuesta** para desarrollar la solución. No implica que todos los archivos existan ya en `main` pero eso es lo que tengo planeado de base para realizar si llego a tener alguna modificacion se estaria sustentando por que fue la necesidad teniendo encuenta que este es un proceso que se debe de mejorar en su ciclo de vida:

```
CI-CD-mlops-U2/
├── README.md                 # Documentación del proyecto
├── app.py                    # Servicio Flask (predicción y reportes)
├── modelo_simulado.py        # Lógica determinista de predicción
├── requirements.txt          # Dependencias Python
├── Dockerfile                # Imagen para despliegue
├── datos/                    # Archivo(s) de registro de predicciones (estadísticas)
├── tests/                    # Pruebas unitarias (pytest)
└── .github/
    └── workflows/
        └── workflow.yaml     # Pipeline CI/CD (PR y push a main)
```

### Flujo de ramas (resumen)

| Rama / etapa | Contenido esperado |
|--------------|-------------------|
| `main` | Documentación y, tras los merges, código estable |
| `solución-inicial` | Archivos de la unidad 1 (sin el MD del pipeline general) |
| `segunda-versión` | Ajustes opcionales según retroalimentación |
| Ramas de features | Quinta categoría `ENFERMEDAD TERMINAL` y reporte de estadísticas |
| `añadir-github-actions` | Workflow: tests en PR, build y push de imagen en `main` |

### Categorías de predicción (objetivo final)

1. `NO ENFERMO`
2. `ENFERMEDAD LEVE`
3. `ENFERMEDAD AGUDA`
4. `ENFERMEDAD CRÓNICA`
5. `ENFERMEDAD TERMINAL` *(nuevo requerimiento)*

### Reporte para médicos (objetivo final)

- Total de predicciones por categoría.
- Últimas 5 predicciones.
- Fecha de la última predicción.

Los resultados se persistirán en archivo de texto y se consultarán desde el servicio desplegado con Docker.
