import os
import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from dotenv import load_dotenv

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
        driver (selenium.webdriver.chrome.webdriver.WebDriver): Driver de Selenium
    """
    driver = webdriver.Chrome()
    return driver

def login (driver, email, password):
    """
    Inicia sesión conOpenAI

    Args:
        driver (selenium.webdriver.chrome.webdriver.Webdriver): Driver Selenium.
        email (str): Email de la cuenta OpenAI
        password (str): Contraseña de la cuenta OpenAI
    """
    driver.get('https://chat.openai.com/auth/login')
    
    time.sleep(3)
    
    try:
        login_button = driver.find_element(By.XPATH, "//button[div[contains(@class, 'fex w-full gap-2 itmes-center justify-center') and text()='Log in']]")   
        login_button.click()

    except:
        print('No se pudo encontrar el botón de login')
        login_button = driver.find_element(By.XPATH, "//button[contains(@class, 'relative flex h-12 items-center justify-center rounded-md text-center text-base font-medium bg-[#3C46FF] text-[#fff] hover:bg-[#0000FF]')]")
        login_button.click()

    time.sleep(3)

    username_field = driver.find_element(By.NAME, 'username')
    username_field.send_keys(email)


    submit_button = driver.find_element(By.XPATH, "//button[@type='submit' and text() ='Continue']")
    submit_button.click()

    time.sleep(1)
    
    password_field = driver.find_element(By.NAME, 'password')
    password_field.send_keys(password)

    password_field.send_keys(Keys.RETURN)

    time.sleep(1)

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

    while True:
        try:
            driver.find_element(By.CLASS_NAME, "text-2x1")
        except:
            break

    try:
        output = driver.find_elements(By.CSS_SELECTOR, "div.markdown.prose.w-full.break-words.dark\:prose-invert.light")[-1]

        if output:
            libros = []
            for li in output.find_elements(By.TAG_NAME, "li"):
                print('libro: ', li.text)
                libros.append(li.text)
        else:
            return []
    
    except Exception as e:
        print('Error: ', e)
        return []

EMAIL, PASSWORD = obtener_credenciales()

driver = generar_driver()

time.sleep(1)

login(driver, EMAIL, PASSWORD)


time.sleep(1000)