from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import os


def generate_report(success, message, screenshots):
    with open("carrito_report.html", "w") as f:
        f.write(f"""
        <!DOCTYPE html>
        <html lang="es">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Reporte del Carrito de Compras</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    background-color: #f4f4f9;
                    margin: 0;
                    padding: 20px;
                }}
                .container {{
                    width: 80%;
                    margin: 0 auto;
                    background-color: white;
                    padding: 20px;
                    border-radius: 8px;
                    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                }}
                h1 {{
                    color: #333;
                }}
                .result {{
                    padding: 15px;
                    margin-top: 20px;
                    border-radius: 5px;
                    background-color: #4CAF50; /* Verde para éxito */
                    color: white;
                }}
                img {{
                    max-width: 100%;
                    border: 2px solid #ddd;
                    margin-top: 20px;
                    border-radius: 5px;
                }}
            </style>
        </head>
        <body>

            <div class="container">
                <h1>Reporte del Carrito de Compras</h1>
                <div class="result">
                    <h2>Proceso Exitoso</h2>
                    <p>{message}</p>
                </div>
                {''.join([f'<img src="{screenshot}" alt="Captura de pantalla de {screenshot}">' for screenshot in screenshots])}
            </div>

        </body>
        </html>
        """)


def take_screenshot(step_name, folder):
    screenshot_path = f'screenshots/{folder}/{step_name}.png'
    driver.save_screenshot(screenshot_path)
    print(f"Captura de pantalla tomada: {screenshot_path}")
    return screenshot_path


service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)


if not os.path.exists('screenshots'):
    os.makedirs('screenshots')
if not os.path.exists('screenshots/carrito'):
    os.makedirs('screenshots/carrito')


carrito_success = True  
message = "Los productos se agregaron correctamente al carrito y el proceso fue exitoso."
screenshots = []


try:
    
    url = "https://tiendadegorra.netlify.app/principal.html?email=davidliranzo0%40gmail.com&password=12223"
    driver.get(url)
    time.sleep(2)

    
    page_title = driver.title
    if "Carrito" not in page_title:
        raise Exception("No se cargó la página correcta. El título es: " + page_title)

    
    screenshots.append(take_screenshot('login_exitoso', 'carrito'))

   
    product_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//a[@class="u-full-width button-primary button input agregar-carrito"][1]'))
    )

   
    driver.execute_script("arguments[0].scrollIntoView(true);", product_button)
    time.sleep(1) 
    product_button.click()
    time.sleep(2)

   
    screenshots.append(take_screenshot('producto_agregado', 'carrito'))

    
    carrito_icon = driver.find_element(By.ID, 'img-carrito')
    WebDriverWait(driver, 10).until(EC.visibility_of(carrito_icon))  
    carrito_icon.click()
    time.sleep(2)
    screenshots.append(take_screenshot('carrito_abierto', 'carrito'))

   
    vaciar_button = driver.find_element(By.ID, 'vaciar-carrito')
    vaciar_button.click()
    time.sleep(2)
    screenshots.append(take_screenshot('carrito_vaciado', 'carrito'))


    carrito_empty_message = driver.find_element(By.XPATH, '//*[text()="El carrito está vacío."]') 
    if carrito_empty_message:
        message = "El carrito ha sido vaciado correctamente."

    
    checkout_button = driver.find_element(By.XPATH, '//*[text()="Pagar"]')  
    checkout_button.click()
    screenshots.append(take_screenshot('proceder_pago', 'carrito'))

except Exception as e:
    message = f"Error en el proceso del carrito: {e}"
    screenshots.append(take_screenshot('error_carrito', 'carrito'))


generate_report(carrito_success, message, screenshots)


driver.quit()

print("Reporte generado como carrito_report.html")
