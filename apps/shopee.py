from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
import logging
from urllib3.exceptions import MaxRetryError

# Atur logging untuk debugging
logging.basicConfig(level=logging.DEBUG)

def start_driver():
    try:
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Jalankan browser tanpa UI
        chrome_options.add_argument("--disable-gpu")  # Untuk menghindari error di beberapa sistem
        chrome_options.add_argument("--no-sandbox")  # Mengatasi error di beberapa OS
        service = Service('path_to_chromedriver')  # Sesuaikan dengan path ke chromedriver Anda
        driver = webdriver.Chrome(service=service, options=chrome_options)
        return driver
    except Exception as e:
        logging.error("Error saat menginisialisasi WebDriver: %s", str(e))
        return None

def flash_sale_checkout(product_url):
    driver = start_driver()
    if not driver:
        logging.error("WebDriver gagal dijalankan.")
        return

    try:
        driver.get(product_url)
        logging.info("Mengunjungi halaman: %s", product_url)
        
        # Tunggu beberapa detik untuk memastikan halaman sudah dimuat
        time.sleep(3)  # Sesuaikan durasi sesuai dengan kecepatan loading halaman

        # Coba mengambil screenshot jika terjadi error
        try:
            driver.save_screenshot('checkout_error.png')  # Menyimpan screenshot untuk analisis
            logging.info("Screenshot berhasil disimpan.")
        except Exception as e:
            logging.error("Gagal mengambil screenshot: %s", str(e))
        
        # Lakukan operasi checkout di sini, misalnya menekan tombol checkout
        # driver.find_element(By.ID, "checkout_button").click()  # Contoh
        # Tunggu untuk melihat apakah proses checkout berhasil
        time.sleep(5)  # Sesuaikan jika perlu

    except MaxRetryError as e:
        logging.error("Gagal koneksi ke server: %s", str(e))
    except Exception as e:
        logging.error("Error saat melakukan checkout: %s", str(e))
    finally:
        driver.quit()  # Pastikan untuk menutup driver setelah selesai

if __name__ == "__main__":
    product_url = "https://www.shopee.com.my/product_url"  # Ganti dengan URL produk yang valid
    flash_sale_checkout(product_url)
