import os
import sqlite3
import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv

class Episodio:
    """
    Representa un episodio de un podcast.
    """
    def __init__(self, item_id, duration_ms, release_date, name, description):
        """
        Inicializa un episodio.

        Args:
            item_id (str): ID del episodio
            duduration_ms (int): Duración del episodio en milisegundos
            relrelease_date (str): Fecha de lanzamiento del episodio.
            name (str): Nombre del episodio.
            dedescription (str): Descripción del episodio.

        """
        self.item_id = item_id
        self.duration_ms = duration_ms
        self.release_date = release_date
        self.name = name
        self.description = description
        self.resultado = None
        self.libros = None

    def __str__(self):
        """
        Devuelve una representación en string del episodio.

        Returns:
            str: Representación en string del episodio.
        """
        return f"Episodio(Id: {self.item_id}\nDuration (ms): {self.duration_ms}\nRelease Date: {self.release_date}\nName: {self.name}\nDescription: {self.description})"
    
    def __repr__(self):
        """
        Devuelve una representación en string del episodio.

        Returns:
            str: Representación en string del episodio.
        """
        return self.__str__()

def obtener_credenciales():
    """
    Obtiene las credenciales de un archivo .env

    Returns:
        EMAIL (str): Email de la cuenta de OpenAI
        PASSWORD (str): Contraseña de la cuenta de OpenAI
    """
    load_dotenv()

    EMAIL = os.environ.get('EMAIL')
    PASSWORD = os.environ.get('PASSWORD')

    return EMAIL, PASSWORD

def generar_driver():
    """
    Genera un driver de Selenium.

    Returns:
        driver (selenium.webdriver.chrome.webdriver.WebDriver): Driver de Selenium para Google
        driver (selenium.webdriver.firefox.webdriver.WebDriver): Driver de Selenium para Firefox
    """
    # driver = webdriver.Chrome()
    driver = webdriver.Firefox()
    return driver

def login (driver, email, password):
    """
    Inicia sesión conOpenAI

    Args:
        driver (selenium.webdriver.chrome.webdriver.Webdriver): Driver Selenium.
        email (str): Email de la cuenta OpenAI
        password (str): Contraseña de la cuenta OpenAI
    """
    driver.get('https://platform.openai.com/login?launch')
    
    time.sleep(3)
    
    try:
        login_button = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, "//button[contains(@class, 'relative flex h-12 items-center justify-center rounded-md text-center text-base font-medium bg-[#3C46FF] text-[#fff] hover:bg-[#0000FF]')]"))
        )
        login_button.click()
    except Exception as e:
        print('No se pudo encontrar el botón de login:', str(e))

    time.sleep(1)

    username_field = driver.find_element(By.NAME, 'username')
    username_field.send_keys(email)


    submit_button = driver.find_element(By.XPATH, "//button[@type='submit' and text() ='Continue']")
    submit_button.click()

    time.sleep(1)
    
    password_field = driver.find_element(By.NAME, 'password')
    password_field.send_keys(password)

    password_field.send_keys(Keys.RETURN)

    time.sleep(30)

    btn_okay = driver.find_element(By.CSS_SELECTOR, "button.btn.relative.btn-primary")
    btn_okay[1].click()

    time.sleep(1)

    btn_dismiss = driver.find_element(By.CSS_SELECTOR, "button.btn.relative.btn-neutral.btn-small")
    btn_dismiss.click()

    time.sleep(1)

    btn_next = driver.find_element(By.CSS_SELECTOR, "button.-my-1")
    btn_next.click()

def hacer_prompt(driver, descripcion):
    """
    Hace un prompt en OpenAI

    Args:
        driver (selenium.webdriver.chrome.webdriver.Webdriver): Driver Selenium.
        descripcion (str): Descripción del prompt.
    """
    prompt_textarea = driver.find_element(By.ID, "prompt-textarea")

    prompt = f"""En el siguiente texto encuentra los títulos de los libros: $$$ {descripcion} $$$ El formato de la salida debe ser el siguiente: Autor - Título del libro. Por ejemplo: 1. Immanuel Kant - Crítica de la razón pura
    """

    prompt_textarea.send_keys(prompt)

    prompt_textarea.send_keys(Keys.RETURN)

    time.sleep(5)

    while "Stop generating" in driver.page_source:
        print('Stop generating...')
        time.sleep(1)

    try:
        output = driver.find_elements(By.CSS_SELECTOR, "div.markdown.prose.w-full.break-words.dark\:prose-invert.light")[-1]
        libros = []
        if output:
            libros = []
            for li in output.find_elements(By.TAG_NAME, "li"):
                print('libro: ', li.text)
                libros.append(li.text)

            resultado = output.text
        
        return resultado, libros
    
    except Exception as e:
        print('Error: ', e)
        return None, []

def conectar_db(nombre_archivo):
    """
    Conecta a la base de datos.

    Args:
        nombre_archivo (str): Nombre del archivo de la base de datos.

    Returns:
        conn (sqlite3.Connection): Conexión a la base de datos
    """
    conexion = sqlite3.connect(nombre_archivo)

    return conexion

def obtener_episodios(conexion):
    """
    Obtiene los episodios de la base de datos

    Args:
        conexion (sqlite3.Connection): Conexión a la base de datos

    Returns: 
        episodios
    """

    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM episodio")
    registros = cursor.fetchall()

    episodios = []

    for r in registros:
        episodio = Episodio(r[0], r[1], r[2], r[3], r[4])
        episodios.append(episodio)

    return episodios

def actualizar_episodio(conexion, episodio):
    """
    Actualiza un episodio en la base de datos.

    Args:
        conexion (sqlite3.Connection): Conexión a la base de datos
        episodio (Episodio): Episodio a actualizar
    """
    cursor = conexion.cursor()

    cursor.execute("UPDATE episodio SET resultado = ?, libros = ? WHERE item_id = ?", (episodio.resultado, episodio.libros, episodio.item_id))

    conexion.commit()

def main():
    
    conexion = conectar_db('filosofia_bolsillo_episodios.db')
    episodios = obtener_episodios(conexion)

    print ('episodios: ', len(episodios))

    EMAIL, PASSWORD = obtener_credenciales()
    driver = generar_driver()

    time.sleep(1)

    login(driver, EMAIL, PASSWORD)

    for episodio in episodios:
        print ('ID del episodio: ', episodio.item_id)
        descripcion = episodio.decription

        resultado = hacer_prompt(driver, descripcion)

        if len(resultado):
            print('Resultado: ', resultado)   

            episodio.resultado = resultado
        
        time.sleep(5) 

    time.sleep(1000)

if __name__ == '__main__':
    main()