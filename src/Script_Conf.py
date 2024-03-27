from selenium.webdriver.common.by import By
from twocaptcha import TwoCaptcha
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
import time
import psycopg2
from telegram import bot
import pandas as pd
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from aiogram import Bot
import asyncio
import yaml
from selenium.webdriver.common.keys import Keys


TELEGRAM_TOKEN = '7004343270:AAFT_1nYs4ra_Yxc6YdiCjdEG1WMRhgpn-U'
DB_USER = 'postgres'
DB_PASSWORD = 'postgres'
DB_HOST = '10.211.55.5'
DB_PORT ='5433'
DB_NAME = 'telegram'
captcha_page_url = "https://onlineservices.mpi.mb.ca/drivertesting/identity/verify"
bot = Bot(TELEGRAM_TOKEN)

# Options
chrome_options = Options()
chrome_options.add_argument("--headless")  # Запуск в безголовом режиме
chrome_options.add_argument("--no-sandbox")


# chrome_options.add_argument("--headless")

# Instantiate the WebDriver

with open('/Users/astonuser/Documents/Docs/PAFALL23/Applied Statistics/Test/MPI/cofig.yaml', 'r') as file:
    config = yaml.safe_load(file)

def get_latest_user_data():
    # Подключение к базе данных
    conn = psycopg2.connect(user=DB_USER, password=DB_PASSWORD, database=DB_NAME, host=DB_HOST, port=DB_PORT)
    try:
        # Создание курсора для выполнения SQL-запросов
        cursor = conn.cursor()

        # Выполнение запроса для получения последних данных пользователя
        cursor.execute('SELECT id, user_id, document_number, postal_code, birth_date FROM People ORDER BY id DESC LIMIT 1')
        # Получение результатов запроса
        result = cursor.fetchone()
        return result
    finally:
        # Закрытие курсора и соединения с базой данных
        cursor.close()
        conn.close()

async def send_message_to_user(user_id, message):
    await bot.send_message(chat_id=user_id, text=message)
    
def format_df_data(df):
    messages = []
    for index, row in df.iterrows():
        message = f"Date: {row.loc['Date']}, Start Time: {row.loc['Start Time']}, End Time: {row.loc['End Time']}"
        messages.append(message)
    return messages

def solve_recaptcha(local_driver):
    start_time = time.time()
    print("Solving Captcha")
    solver = TwoCaptcha("ebac4aff88bbb5ca462e9b55d271f3d7")
    code = solver.solve_captcha(site_key='6Lccu0sUAAAAAKG0hGhC0KgEVfdIHLwm2OY-rP12', page_url=captcha_page_url)
    print(f"Successfully solved the Captcha")
    end_time = time.time() 
    execution_time = end_time - start_time 
    print("Время выполнения функции:", execution_time, "секунд")
    # Set the solved Captcha
    recaptcha_response_element = local_driver.find_element(By.ID, 'RecaptchaResponse')
    local_driver.execute_script(f'arguments[0].value = "{code}";', recaptcha_response_element)

def send_message_to_user(user_id, message):
        bot.send_message(chat_id=user_id, text=message)

def execute_scenario(scenario_name, local_driver):
    if scenario_name in config['scenarios']:
        for step in config['scenarios'][scenario_name]['steps']:
            action = step['action']
            if action in ['waitclick', 'click']:
                if 'locator' in step:
                    parts = step['locator'].split(', ', 1)
                    locator_type, locator_value = parts[0].strip(), parts[1].strip()
                    locator_type = getattr(By, locator_type)

                    if action == 'waitclick':
                        WebDriverWait(local_driver, 10).until(EC.element_to_be_clickable((locator_type, locator_value))).click()
                    elif action == 'click':
                        local_driver.find_element(locator_type, locator_value).click()
            elif action == 'sleep':
                time.sleep(step['value'])
    else:
        print(f"Scenario {scenario_name} not found in configuration.")

async def main():
    local_driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)
    local_driver.set_window_size(1920, 1080)
    
    start_time = time.time()
    latest_user_data = get_latest_user_data()
    user_id = latest_user_data[1]
    print(user_id)
    
    if user_id is None:
        print("No user data found.")
        return

    user_data = {
        'document_number': latest_user_data[2],
        'postal_code': latest_user_data[3],
        'birth_date': latest_user_data[4],
    }
    
    local_driver.get(captcha_page_url)
    WebDriverWait(local_driver, 10).until(EC.element_to_be_clickable((By.ID, 'authenticate-with-ddref-container'))).click()
    local_driver.find_element(By.ID, 'DateOfBirth').send_keys(user_data['birth_date'])
    local_driver.find_element(By.ID, 'DocumentNumber').send_keys(user_data['document_number'])
    local_driver.find_element(By.ID, 'Code').send_keys(user_data['postal_code'])
    local_driver.execute_script("window.scrollBy(0, 150);")
    local_driver.find_element(By.CLASS_NAME, 'iCheck-helper').click()
    
    solve_recaptcha(local_driver)
    local_driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click() 

    # Submit the form
    execute_scenario('NEW_APPOINTMENT', local_driver)

    
    
        # Предполагаем, что у вас есть список центров или вы можете получить его программно
    service_centers = ["Gateway Service Centre", "Bison Service Centre", "St. Mary's Service Centre", "Main Street Service Centre", "King Edward Service Centre"]
    final_message = ""

    for center in service_centers:
        # Кликнуть, чтобы открыть выпадающий список
        local_driver.find_element(By.CSS_SELECTOR, "span.select2-selection--single").click()
        
        # Ожидаем, пока не станет кликабельным и кликаем на нужный элемент
        if "'" in center:
            parts = center.split("'")
            xpath_expression = f"//li[contains(., concat('{parts[0]}', \"'\", '{parts[1]}'))]"
        else:
            xpath_expression = f"//li[contains(., '{center}')]"

        WebDriverWait(local_driver, 10).until(EC.element_to_be_clickable((By.XPATH, xpath_expression))).click()
        # time.sleep(1)


        date = local_driver.find_element(By.ID, 'AppointmentDate').text
        local_driver.find_element(By.ID, 'AppointmentDate').send_keys(Keys.CONTROL, 'A')
        local_driver.find_element(By.ID, 'AppointmentDate').send_keys({date})
        
        # Нажимаем на кнопку поиска
        WebDriverWait(local_driver, 10).until(EC.element_to_be_clickable((By.ID, "search-submit"))).click()

        # Проверяем наличие данных и формируем сообщение
        try:
            WebDriverWait(local_driver, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "#appointment-table td:not(.dataTables_empty)"))
            )
            html = local_driver.page_source
            soup = BeautifulSoup(html, 'html.parser')
            table = soup.find('table', id='appointment-table')
            df = pd.read_html(str(table), flavor='bs4')[0]
            df = df[['Date', 'Start Time', 'End Time']]
            final_message += f"{center}\n{df.to_string(index=False)}\n\n"
        except TimeoutException:
            final_message += f"{center}\nNo dates\n\n"
            
        print(final_message)    

# Здесь код для отправки final_message в Telegram
    user_id = '156837559'
    await bot.send_message(chat_id=user_id, text=final_message)
    local_driver.close()
    end_time = time.time()
    print(f"Функция main выполнена за {end_time - start_time} секунд")
    
async def other_tasks():
    # Ваша другая логика
    print("Другие задачи")

async def periodic_main():
    while True:
        await main()
        await asyncio.sleep(1800)

async def main_coroutine():
    task1 = asyncio.create_task(periodic_main())

    # Ждем выполнения обеих задач
    await task1

asyncio.run(main_coroutine())
# Pause the execution so you can see the screen after submission before closing the driver
input("Press enter to continue")
