import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.filters.command import CommandStart
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.dispatcher.router import Router
import asyncpg
from dotenv import load_dotenv
import os

load_dotenv()

API_TOKEN = os.getenv('TELEGRAM_TOKEN')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME')

bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
router = Router()

class Form(StatesGroup):
    name = State()
    document_number = State()
    postal_code = State()
    birth_date = State()

async def create_db():
    conn = await asyncpg.connect(user=DB_USER, password=DB_PASSWORD, database=DB_NAME, host=DB_HOST, port=DB_PORT)
    try:
        await conn.execute(
            'CREATE TABLE IF NOT EXISTS People ('
            'id SERIAL PRIMARY KEY,'
            'user_id BIGINT,'
            'chat_id BIGINT,'
            'name VARCHAR(255),'
            'document_number VARCHAR(255),'
            'postal_code VARCHAR(255),'
            'birth_date VARCHAR(255),'
            'processed BOOLEAN DEFAULT FALSE'
            ')'
        )
        print("Table 'users' is created or already exists.")
    except Exception as e:
        print(f"An error occurred while creating the table: {e}")
    finally:
        await conn.close()

async def save_to_database(user_id,chat_id, data):
    conn = await asyncpg.connect(user=DB_USER, password=DB_PASSWORD, database=DB_NAME, host=DB_HOST, port=DB_PORT)
    try:
        await conn.execute(
            'INSERT INTO People (user_id, chat_id, name, document_number, postal_code, birth_date, processed) VALUES($1, $2, $3, $4, $5, $6, $7)',
            user_id, chat_id, data['name'], data['document_number'], data['postal_code'], data['birth_date'], False
        )
        print(f"Data saved successfully for user {user_id}: {data['name']}")
    except Exception as e:
        print(f"An error occurred while saving data for user {user_id}: {e}")
    finally:
        await conn.close()

@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await state.set_state(Form.name)
    await message.answer("Hello! What's your name?")

@router.message(Form.name)
async def process_name(message: Message, state: FSMContext):
    # Установка значения в контекст состояния
    await state.update_data(name=message.text)
    await state.set_state(Form.document_number)
    await message.answer("What's your Document Number (DD/REF)?")

@router.message(Form.document_number)
async def process_document_number(message: Message, state: FSMContext):
    # Получение данных из состояния и обновление их
    data = await state.get_data()
    data['document_number'] = message.text
    await state.set_data(data)
    await state.set_state(Form.postal_code)
    await message.answer("What's your Postal or Zip Code?")

@router.message(Form.postal_code)
async def process_postal_code(message: Message, state: FSMContext):
    data = await state.get_data()
    data['postal_code'] = message.text
    await state.set_data(data)
    await state.set_state(Form.birth_date)
    await message.answer("What's your Date of Birth?")

@router.message(Form.birth_date)
async def process_birth_date(message: Message, state: FSMContext):
    user_id = message.from_user.id
    chat_id = message.chat.id
    data = await state.get_data()
    data['birth_date'] = message.text
    await save_to_database(user_id, chat_id, data)
    await message.answer(f"Thank you, {data['name']}! Your data has been saved. We will notify you once we find an appointment.")
    await state.clear()

async def main():
    await create_db()
    dp = Dispatcher(storage=storage)
    dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())