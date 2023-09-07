from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time

# Si ChromeDriver no esta en tu PATH, especifica su ubicación directamente
# driver = webdriver.Vhrome(executable_path='/ruta/del/chromedriver')
# Inicializar el controlador de Selenium (asegúrate de tener el controlador de Chrome descargado y en tu PATH)

driver = webdriver.Chrome()


# Navegar a la https://www.bing.compágina de inicio de Google
driver.get("https://www.google.com")

# Encontrar el campo de búsqueda y escribir las palabras clave
search_box = driver.find_element(By.NAME, "q")
search_box.send_keys("¿Es Google hoy día, después de la aparición de ChatGPT, las nuevas páginas amarillas?")

# Enviar la búsqueda
search_box.send_keys(Keys.RETURN)

time.sleep(5)

# La ventana maximizada
driver.maximize_window()

# Esperar unos segundos para ver los resultados (ajusta este tiempo según sea necesario)
time.sleep(25)


