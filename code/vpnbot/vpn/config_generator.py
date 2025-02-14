from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

def generate_config(email, password, wireguard_name):
    """
    Генерирует WireGuard-конфигурацию через личный кабинет Mullvad.
    :param email: Email от аккаунта Mullvad
    :param password: Пароль от аккаунта Mullvad
    :param wireguard_name: Имя устройства (например, MyDevice)
    :return: Строка с содержимым конфигурации WireGuard
    """
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Без отображения окна браузера
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=options)

    try:
        # Заходим на сайт Mullvad
        driver.get("https://mullvad.net/en/account/")
        time.sleep(3)

        # Авторизация
        driver.find_element(By.NAME, "email").send_keys(email)
        driver.find_element(By.NAME, "password").send_keys(password + Keys.RETURN)
        time.sleep(5)

        # Переход в раздел WireGuard
        driver.find_element(By.LINK_TEXT, "WireGuard").click()
        time.sleep(3)

        # Создаем новую конфигурацию
        driver.find_element(By.ID, "create-config-button").click()
        time.sleep(2)
        driver.find_element(By.ID, "config-name").send_keys(wireguard_name)
        driver.find_element(By.ID, "save-button").click()
        time.sleep(3)

        # Скачиваем конфигурацию
        config_content = driver.find_element(By.XPATH, "//textarea").get_attribute("value")
        return config_content

    finally:
        driver.quit()
