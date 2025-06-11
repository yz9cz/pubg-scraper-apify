# scraper.py

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PUBGScraper:
    def __init__(self):
        self.chromedriver_path = "chromedriver"  # تأكد أن Appify يستخدم Chrome Headless مثبت مسبقًا

    def setup_driver(self):
        try:
            chrome_options = Options()
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--window-size=1920,1080")
            
            service = Service(executable_path=self.chromedriver_path)
            driver = webdriver.Chrome(service=service, options=chrome_options)
            return driver
        except Exception as e:
            logger.error(f"خطأ في إعداد WebDriver: {e}")
            return None

    def get_player_name(self, player_id: str):
        driver = self.setup_driver()
        if not driver:
            return None
        
        try:
            wait = WebDriverWait(driver, 20)
            driver.get("https://www.midasbuy.com/midasbuy/buy/pubgm")
            time.sleep(3)

            # إغلاق النوافذ المنبثقة
            try:
                popup_close = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div/div[14]/div[3]"))
                )
                popup_close.click()
            except:
                pass

            # النقر على المنطقة
            region_button = wait.until(EC.element_to_be_clickable(
                (By.XPATH, "/html/body/div[2]/div/div[2]/div[2]/div/div[2]/div[2]/div/div/div")
            ))
            region_button.click()
            time.sleep(2)

            # إدخال معرف اللاعب
            id_input = wait.until(EC.presence_of_element_located(
                (By.XPATH, "/html/body/div[2]/div/div[5]/div[2]/div[1]/div[2]/div/div[2]/div/input")
            ))
            id_input.clear()
            id_input.send_keys(player_id)
            time.sleep(2)

            # التحقق
            verify_button = wait.until(EC.element_to_be_clickable(
                (By.XPATH, "/html/body/div[2]/div/div[5]/div[2]/div[1]/div[3]/div/div")
            ))
            verify_button.click()
            time.sleep(5)

            player_name_element = wait.until(EC.presence_of_element_located(
                (By.XPATH, "/html/body/div[2]/div/div[2]/div[2]/div/div[2]/div[2]/div/div/div[1]/div/span[1]")
            ))
            return player_name_element.text.strip()
        except Exception as e:
            logger.error(f"فشل في جلب اسم اللاعب: {e}")
            return None
        finally:
            driver.quit()
