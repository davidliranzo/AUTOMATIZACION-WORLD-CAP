from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time
import os


def generate_report(success, message, screenshots):
    with open("registro_report.html", "w") as f:
        f.write(f"""
        <!DOCTYPE html>
        <html lang="es">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Reporte de Registro</title>
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
                <h1>Reporte de Registro</h1>
                <div class="result">
                    <h2>Proceso Exitoso</h2>
                    <p>{message}</p>
                </div>
                {''.join([f'<img src="{screenshot}" alt="Captura de pantalla de {screenshot}">' for screenshot in screenshots])}
            </div>

        </body>
        </html>
        """)


service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)


if not os.path.exists('screenshots/registro'):
    os.makedirs('screenshots/registro')

def take_screenshot(step_name, folder):
    screenshot_path = f'screenshots/{folder}/{step_name}.png'
    driver.save_screenshot(screenshot_path)
    print(f"Captura de pantalla tomada: {screenshot_path}")
    return screenshot_path


registration_success = True 
message = "El registro se realizó exitosamente."  
screenshots = []


driver.get('https://tiendadegorra.netlify.app/registro.html')
time.sleep(2)

try:
    
    screenshots.append(take_screenshot('pagina_registro_cargada', 'registro'))

   
    name_field = driver.find_element(By.ID, 'name') 
    name_field.send_keys('david liranzo')

    screenshots.append(take_screenshot('nombre_ingresado', 'registro'))

    email_field = driver.find_element(By.ID, 'email')  
    email_field.send_keys('davidliranzo0@correo.com')

    screenshots.append(take_screenshot('correo_ingresado', 'registro'))

    password_field = driver.find_element(By.ID, 'password')  
    password_field.send_keys('itla1127')

    screenshots.append(take_screenshot('contraseña_ingresada', 'registro'))

    confirm_password_field = driver.find_element(By.ID, 'confirmPassword') 
    confirm_password_field.send_keys('nueva_contraseña')

    screenshots.append(take_screenshot('confirmacion_contraseña_ingresada', 'registro'))

    register_button = driver.find_element(By.XPATH, '//button[text()="Registrarse"]')
    register_button.click()

    screenshots.append(take_screenshot('boton_registro_click', 'registro'))

    time.sleep(5)

   
    try:
        welcome_message = driver.find_element(By.XPATH, '//h1[text()="Bienvenido"]') 
        message = "El registro fue exitoso. Bienvenido a tu cuenta."
    except:
        message = "No se pudo verificar el registro. El registro ha fallado."

    screenshots.append(take_screenshot('resultado_registro', 'registro'))

except Exception as e:
    message = f"Error al intentar realizar el registro: {e}"
    screenshots.append(take_screenshot('error_registro', 'registro'))


generate_report(registration_success, message, screenshots)


driver.quit()

print("Reporte generado como registro_report.html")
