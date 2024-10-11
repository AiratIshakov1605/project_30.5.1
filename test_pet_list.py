from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging
import time

logging.basicConfig(level=logging.INFO)

def test_pet_list():
    # Инициализация драйвера (предполагается, что у вас установлен ChromeDriver)
    driver = webdriver.Chrome()
    driver.implicitly_wait(10)  # Неявные ожидания для всех элементов
    driver.get("https://petfriends.skillfactory.ru/my_pets")

    try:
        # Ожидание загрузки страницы и элементов
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "pet-list")))

        # Увеличиваем время, сколько будет открыта страница
        time.sleep(3600000)

        # Получение статистики пользователя (количество питомцев)
        user_stats = driver.find_element(By.CLASS_NAME, "user-stats")
        total_pets = int(user_stats.text.split()[0])  # Предполагается, что статистика находится в тексте
        logging.info(f"Total pets: {total_pets}")

        # Получение списка питомцев
        pet_list = driver.find_elements(By.CLASS_NAME, "pet-item")

        # Проверка 1: Присутствуют все питомцы
        assert len(pet_list) == total_pets, "Количество питомцев не совпадает с количеством в статистике"
        logging.info(f"Found {len(pet_list)} pets, expected {total_pets}")

        # Проверка 2: Хотя бы у половины питомцев есть фото
        pets_with_photo = 0
        for pet in pet_list:
            img = pet.find_element(By.TAG_NAME, "img")
            if img.get_attribute("src") and img.get_attribute("src") != "":
                pets_with_photo += 1
        assert pets_with_photo >= total_pets / 2, "Меньше половины питомцев имеют фото"
        logging.info(f"Pets with photo: {pets_with_photo}, expected at least {total_pets / 2}")

        # Проверка 3: У всех питомцев есть имя, возраст и порода
        for pet in pet_list:
            name = pet.find_element(By.CLASS_NAME, "pet-name").text
            age = pet.find_element(By.CLASS_NAME, "pet-age").text
            breed = pet.find_element(By.CLASS_NAME, "pet-breed").text
            assert name and age and breed, "У питомца отсутствует имя, возраст или порода"
        logging.info("All pets have name, age, and breed")

        # Проверка 4: У всех питомцев разные имена
        pet_names = [pet.find_element(By.CLASS_NAME, "pet-name").text for pet in pet_list]
        assert len(pet_names) == len(set(pet_names)), "Есть повторяющиеся имена питомцев"
        logging.info("All pets have unique names")

        # Проверка 5: В списке нет повторяющихся питомцев
        unique_pets = set()
        for pet in pet_list:
            name = pet.find_element(By.CLASS_NAME, "pet-name").text
            age = pet.find_element(By.CLASS_NAME, "pet-age").text
            breed = pet.find_element(By.CLASS_NAME, "pet-breed").text
            pet_info = (name, age, breed)
            assert pet_info not in unique_pets, "Найден повторяющийся питомец"
            unique_pets.add(pet_info)
        logging.info("All pets are unique")

    except Exception as e:
        logging.error(f"Test failed: {e}")
        raise

    finally:
        driver.quit()

# Запуск теста
test_pet_list()