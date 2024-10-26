from selenium.webdriver.common.by import By
from twocaptcha import TwoCaptcha
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
import time
import psycopg2
from telegram import Bot
import pandas as pd
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from aiogram import Bot
import asyncio
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Telegram token and database credentials from the .env file
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
DB2_USER = os.getenv('DB2_USER')
DB2_PASSWORD = os.getenv('DB2_PASSWORD')
DB2_HOST = os.getenv('DB2_HOST')
DB2_PORT = os.getenv('DB2_PORT')
DB2_NAME = os.getenv('DB2_NAME')
CAPTCHA_PAGE_URL = os.getenv('CAPTCHA_PAGE_URL')
SITE_KEY = os.getenv('SITE_KEY')
CAPTCHA_API_KEY = os.getenv('CAPTCHA_API_KEY')

# Initialize Telegram Bot with the token
bot = Bot(TELEGRAM_TOKEN)

# Options for Chrome WebDriver
chrome_options = Options()
# chrome_options.add_argument("--headless")

# Instantiate the WebDriver
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)
driver.maximize_window()

def get_latest_user_data():
    # Connect to the database
    conn = psycopg2.connect(user=DB2_USER, password=DB2_PASSWORD, database=DB2_NAME, host=DB2_HOST, port=DB2_PORT)
    try:
        # Create a cursor to execute SQL queries
        cursor = conn.cursor()

        # Execute query to get the latest user data
        cursor.execute('SELECT id, user_id, document_number, postal_code, birth_date FROM People ORDER BY id DESC LIMIT 1')
        result = cursor.fetchone()
        return result
    finally:
        # Close cursor and connection
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

def solve_recaptcha():
    start_time = time.time()
    print("Solving Captcha")
    # Initialize 2Captcha solver with API key from .env file
    solver = TwoCaptcha(os.getenv('2CAPTCHA_API_KEY'))
    # Solve the captcha using the site key from .env file
    code = solver.solve_captcha(site_key=SITE_KEY, page_url=CAPTCHA_PAGE_URL)
    print(f"Successfully solved the Captcha")
    end_time = time.time() 
    execution_time = end_time - start_time 
    print("Function execution time:", execution_time, "seconds")
    # Set the solved Captcha
    recaptcha_response_element = driver.find_element(By.ID, 'RecaptchaResponse')
    driver.execute_script(f'arguments[0].value = "{code}";', recaptcha_response_element)

def send_message_to_user(user_id, message):
    bot.send_message(chat_id=user_id, text=message)

async def main():
    latest_user_data = get_latest_user_data()
    user_id = latest_user_data[1]
    print(user_id)
    
    if user_id is None:
        print("No user data found.")
        return

    # Fill in user data for the form
    user_data = {
        'document_number': latest_user_data[2],
        'postal_code': latest_user_data[3],
        'birth_date': latest_user_data[4],
    }
    
    driver.get(CAPTCHA_PAGE_URL)
    driver.execute_script("window.scrollBy(0, 150);")
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'authenticate-with-ddref-container'))).click()
    driver.find_element(By.ID, 'DateOfBirth').send_keys(user_data['birth_date'])
    driver.find_element(By.ID, 'DocumentNumber').send_keys(user_data['document_number'])
    driver.find_element(By.ID, 'Code').send_keys(user_data['postal_code'])
    driver.execute_script("window.scrollBy(0, 150);")
    driver.find_element(By.CLASS_NAME, 'iCheck-helper').click()
    
    solve_recaptcha()
    driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click() 

    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#link-container > span:nth-child(2) > a'))).click()
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'span[aria-labelledby="select2-SelectedServiceId-container"]'))).click()
    time.sleep(2)
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//li[contains(., '5 - Passenger Vehicle')]"))).click()
    time.sleep(2)
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'span[aria-labelledby="select2-SelectedLanguageCode-container"]'))).click()
    time.sleep(2)
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//li[contains(., 'English')]"))).click()
    time.sleep(2)
    driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click() 

    # Assuming you have a list of centers or can obtain it programmatically
    service_centers = ["Gateway Service Centre", "Bison Service Centre", "St. Mary's Service Centre", "Main Street Service Centre", "King Edward Service Centre"]
    final_message = ""

    for center in service_centers:
        # Click to open the dropdown menu
        driver.find_element(By.CSS_SELECTOR, "span.select2-selection--single").click()
        
        # Wait until clickable and click the desired element
        if "'" in center:
            parts = center.split("'")
            xpath_expression = f"//li[contains(., concat('{parts[0]}', \"'\", '{parts[1]}'))]"
        else:
            xpath_expression = f"//li[contains(., '{center}')]"

        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, xpath_expression))).click()

        # Click the search button
        driver.find_element(By.ID, "search-submit").click()

        # Check if data is present and format the message
        try:
            WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "#appointment-table td:not(.dataTables_empty)"))
            )
            html = driver.page_source
            soup = BeautifulSoup(html, 'html.parser')
            table = soup.find('table', id='appointment-table')
            df = pd.read_html(str(table), flavor='bs4')[0]
            df = df[['Date', 'Start Time', 'End Time']]
            final_message += f"{center}\n{df.to_string(index=False)}\n\n"
        except TimeoutException:
            final_message += f"{center}\nNo dates\n\n"
            
        print(final_message)    

    # Send final message to Telegram
    user_id = '156837559'
    await bot.send_message(chat_id=user_id, text=final_message)
    print("Main function completed")

 
async def other_tasks():
    print("Other tasks")

async def periodic_main():
    while True:
        await main()
        await asyncio.sleep(1800)

async def main_coroutine():
    task1 = asyncio.create_task(periodic_main())

    # Wait for tasks to complete
    await task1

asyncio.run(main_coroutine())
input("Press enter to continue")
driver.close()
