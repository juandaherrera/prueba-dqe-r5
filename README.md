# Prueba técnica Data Quality - R5
![Python 3.11.5](https://img.shields.io/badge/python-3.11.5-blue.svg)

Prueba técnica de Data Quality para R5. 

# Instalación

Sigue estos pasos para configurar el entorno de desarrollo y ejecutar el proyecto.

## Clonar el Repositorio

Primero, clona el repositorio en tu máquina local utilizando el siguiente comando:

```bash
git clone https://github.com/juandaherrera/prueba-dqe-r5.git
cd prueba-dqe-r5
```

## Configurar el Entorno Virtual
Es recomendable usar un entorno virtual para manejar las dependencias. Puedes crear uno utilizando venv:
```bash
python -m venv venv
```

Activar el entorno virtual:

En Windows:

```bash
venv\Scripts\activate
```
En macOS y Linux:

```bash
source venv/bin/activate
```

## Instalar Dependencias
Instala todas las dependencias necesarias con pip:

```bash
pip install -r requirements.txt
```

# Uso
## Primera parte
Si deseas ejecutar el [script](primera_parte/main.py) puedes usar los siguientes comandos
```bash
cd primera_parte
python main.py
```
Este script te regresará un CSV llamado [```output.csv```](primera_parte/data/processed/output.csv) y se encontrará ubicado en:

```
primera_parte
└── data
    └── processed
        └── output.csv
```

## Segunda parte
Estructura de la sección:
```
segunda_parte
├── img
├── main.ipynb
├── summary.md
└── utils
    ├── __init__.py
    ├── data_quality.py
    └── pandas_api_ext.py
```
En este caso podras encontrar:
- El [**Reporte de Calidad de Datos**](segunda_parte/summary.md) como ```summary.md```. Este es el entregable de esta sección y contiene el reporte de calidad obtenido a partir del análisis del output de la [primera parte](#primera-parte) de la prueba.
- El [**Código del Reporte de Calidad**](segunda_parte/main.ipynb) como ```main.ipynb```. Si se desea puede ejecutarse o simplemente visualizar el notebook.