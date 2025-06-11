from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def setup_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    
    driver = webdriver.Chrome(options=chrome_options)
    return driver

def get_pubg_name(player_id: str):
    driver = None
    try:
        driver = setup_driver()
        wait = WebDriverWait(driver, 20)

        driver.get("https://www.midasbuy.com/midasbuy/buy/pubgm")
        time.sleep(3)

        try:
            popup_close = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div/div[14]/div[3]"))
            )
            popup_close.click()
        except:
            pass

        region_button = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "/html/body/div[2]/div/div[2]/div[2]/div/div[2]/div[2]/div/div/div")
        ))
        region_button.click()
        time.sleep(2)

        id_input = wait.until(EC.presence_of_element_located(
            (By.XPATH, "/html/body/div[2]/div/div[5]/div[2]/div[1]/div[2]/div/div[2]/div/input")
        ))
        id_input.clear()
        id_input.send_keys(player_id)
        time.sleep(2)

        verify_button = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "/html/body/div[2]/div/div[5]/div[2]/div[1]/div[3]/div/div")
        ))
        verify_button.click()
        time.sleep(5)

        player_name_element = wait.until(EC.presence_of_element_located(
            (By.XPATH, "/html/body/div[2]/div/div[2]/div[2]/div/div[2]/div[2]/div/div/div[1]/div/span[1]")
        ))

        player_name = player_name_element.text.strip()
        return player_name if player_name else None

    except Exception as e:
        logger.error(f"Error getting player name: {e}")
        return None
    finally:
        if driver:
            driver.quit()
