# Extractor de Títulos de libros

## 1. Introducción

Este módulo  es una herramienta que permite extraer un listado de libros a partir de la información de una base de datos.


## 2.- Requisitos


Para ejecutar este script necesitamos las siguientes herramientas


1. Python 3.9 o superior
2. pip
3. Ambiente virtual
4. Base de datos SQLite
5. Python dot-env
6. Selenium


## 3. Instalación


1. Clonar repositorio


```bash
git clone https://github.com/isa-bos-dev/extractor_titulos_libros.git
````


2. Crear un ambiente virtual


```bash
python -m venv nombre_ambiente
```


3. Activar el ambiente virtual


3.1 Linux/MacOs


```bash
source nombre_ambiente/bin/activate
```


3.2 Windows


```bash
nombre_ambiente\Scripts\activate.bat
```

4. Instalar las dependencias


```bash
pip install -r requirements.txt
```


4. Crear un archivo `.env` con la siguiente información


```bash
EMAIL = # Correo electrónico de la cuenta de ChatGPT
PASSWORD = # Contraseña de la cuenta de ChatGPT
```

## 4. Ejecución


Para ejecutar el script, debemos ejecutar el siguiente comando:


```bash
python main.py
```


## 5. Resultados


La información de libros quedará almacenada en la base de datos


El Script nos generará un archivo `libros.txt` con el siguiente formato:


## 6. A tener en cuenta


- Antes de ejecutar el script se debe tener en cuenta el nombre de la base de datos en SQLite.

- La extracción de datos es semiautomática, el navegador podría mostrar un captcha que hay que resolver manualmente.
