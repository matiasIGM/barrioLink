# Guía para instalar y ejecutar un proyecto Django (BarrioLink)

Esta guía te mostrará cómo crear un entorno virtual, instalar Django y ejecutar un proyecto Django en tu máquina a través de la línea de comandos.

## Requisitos previos

Antes de comenzar, asegúrate de tener lo siguiente instalado en tu sistema:

- Python (3.6 o superior)
- pip (un administrador de paquetes de Python)
- virtualenv https://help.dreamhost.com/hc/es/articles/115000695551-Instalar-y-usar-virtualenv-con-Python-3

## Paso 1: Clonar el proyecto desde GitHub

Clona el repositorio  desde GitHub en la ubicación deseada en tu sistema:

```bash
git https://github.com/matiasIGM/barrioLink.git
cd tu-proyecto

## Paso 2: Activar el entorno virtual

En Windows:
```bash
venv\Scripts\activate
Luego, activa el entorno virtual:

En Windows:
```bash
venv\Scripts\activate

En macOS y Linux:

```bash
source venv/bin/activate

## Paso 3: Instalar las dependencias
Dentro del entorno virtual, instala las dependencias del proyecto utilizando pip y el archivo requirements.txt:

```bash
pip install -r requirements.txt

## Paso 4: Aplicar las migraciones
Aplica las migraciones para crear la estructura de la base de datos:

```bash
python manage.py migrate

## Paso 5: Ejecutar el servidor de desarrollo
Finalmente, inicia el servidor de desarrollo de Django:

```bash
python manage.py runserver

Ahora, puedes acceder al proyecto en  Django en tu navegador visitando http://localhost:8000/.


Recuerda desactivar el entorno virtual cuando hayas terminado:

En Windows:

```bash
deactivate