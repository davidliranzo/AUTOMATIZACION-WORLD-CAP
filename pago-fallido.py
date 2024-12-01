from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os

options = Options()

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

os.makedirs("screenshots", exist_ok=True)
os.makedirs("screenshots/pago-fallido", exist_ok=True)

driver.get("https://tiendadegorra.netlify.app/principal.html?email=davidliranzo0%40gmail.com&password=12223")

time.sleep(3)

driver.save_screenshot("screenshots/pago-fallido/pagina_inicial.png")

try:
    botones_agregar = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, "agregar-carrito"))
    )
    if botones_agregar:
        print(f"Se encontraron {len(botones_agregar)} botones 'Agregar al carrito'")

        producto = botones_agregar[0]
        producto.click()
        print("Producto agregado al carrito correctamente.")
        
        driver.save_screenshot("screenshots/pago-fallido/producto_agregado.png")
    else:
        print("No se encontraron botones 'Agregar al carrito'.")
except Exception as e:
    print(f"Error al agregar el producto al carrito: {e}")

driver.get("https://tiendadegorra.netlify.app/pagos")

time.sleep(3)

driver.save_screenshot("screenshots/pago-fallido/pagina_pago.png")

try:
    nombre = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "nombre"))
    )
    nombre.send_keys("David Liranzo")

    direccion = driver.find_element(By.ID, "direccion")
    direccion.send_keys("maximo gomez 5, Santo Domingo, RD")

    telefono = driver.find_element(By.ID, "telefono")
    telefono.send_keys("8091784567")

    tarjeta = driver.find_element(By.ID, "tarjeta")
    tarjeta.send_keys("12345678123456")

    select_mes = driver.find_element(By.ID, "fecha-mes")
    select_mes.send_keys("diciembre") 

    select_anio = driver.find_element(By.ID, "fecha-anio")
    select_anio.send_keys("25") 

    cvc = driver.find_element(By.ID, "cvc")
    cvc.send_keys("173")

    driver.save_screenshot("screenshots/pago-fallido/formulario_completado.png")

    confirmar_compra = driver.find_element(By.XPATH, "//button[contains(text(), 'Confirmar Compra')]")
    confirmar_compra.click()

    time.sleep(5)

    driver.save_screenshot("screenshots/pago-fallido/confirmacion_pago.png")

    print(driver.page_source)  

except Exception as e:
    print(f"Error al completar el formulario de pago: {e}")

driver.quit()

# Creación del reporte HTML
reporte_html = f"""
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Reporte de Pago Fallido - Tienda de Gorra</title>
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
            background-color: #f44336; /* Rojo para error */
            color: white;
        }}
        .details-list {{
            margin-top: 20px;
        }}
        .details-list li {{
            padding: 10px;
            font-size: 16px;
            border-bottom: 1px solid #ddd;
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
        <h1>Reporte de Pago Fallido - Tienda de Gorra</h1>
        <div class="result">
            <h2>Proceso Fallido</h2>
            <p>La compra no se ha completado correctamente.</p>
        </div>
        
        <h2>Detalles del Intento de Pago</h2>
        <ul class="details-list">
            <li><strong>Nombre:</strong> David Liranzo</li>
            <li><strong>Dirección:</strong> maximo gomez 5, Santo Domingo, RD</li>
            <li><strong>Teléfono:</strong> 8091234567</li>
            <li><strong>Tarjeta:</strong> 1234 5678 1234 5678</li>
            <li><strong>Mes de Expiración:</strong> Diciembre (12)</li>
            <li><strong>Año de Expiración:</strong> 2025</li>
            <li><strong>CVC:</strong> 173</li>
        </ul>
        
        <h2>Capturas de Pantalla</h2>
        <img src="screenshots/pago-fallido/pagina_inicial.png" alt="Captura de pantalla de la página inicial">
        <img src="screenshots/pago-fallido/producto_agregado.png" alt="Captura de pantalla de producto agregado al carrito">
        <img src="screenshots/pago-fallido/pagina_pago.png" alt="Captura de pantalla de la página de pago">
        <img src="screenshots/pago-fallido/formulario_completado.png" alt="Captura de pantalla del formulario de pago completado">
        <img src="screenshots/pago-fallido/confirmacion_pago.png" alt="Captura de pantalla de la confirmación del pago">
    </div>

</body>
</html>
"""

with open("reporte_pago_fallido.html", "w", encoding="utf-8") as file:
    file.write(reporte_html)

print("El reporte ha sido generado exitosamente en 'reporte_pago_fallido.html'.")

