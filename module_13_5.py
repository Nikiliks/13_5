from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import  ReplyKeyboardMarkup, KeyboardButton
import asyncio


api = '1'
bot = Bot(token = api)
dp = Dispatcher(bot, storage = MemoryStorage())

kb = ReplyKeyboardMarkup(resize_keyboard=True)
button_1 = KeyboardButton(text = 'Расчитать')
button_2 = KeyboardButton(text = 'Информация')
kb.add(button_1)
kb.add(button_2)



# Определяем класс UserState, наследуемый от StatesGroup
class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()
    gender = State()

@dp.message_handler(commands = 'start')
async def start(message: types.Message):
    await message.answer('Привет!', reply_markup = kb)

@dp.message_handler(text = 'Информация')
async def start(message: types.Message):
    await message.answer('Я бот помогающий твоему здоровью!')

# Функция для получения возраста
@dp.message_handler(lambda message: message.text == 'Рассчитать')
async def set_age(message: types.Message):
    await message.answer('Введите свой возраст:')
    await UserState.age.set()

# Функция для получения роста
@dp.message_handler(state = UserState.age)
async def set_growth(message: types.Message, state: FSMContext):
    try:
        await state.update_data(age = message.text)
        await message.answer('Введите свой рост:')
        await UserState.growth.set()
    except Exception as e:
        await message.answer("Произошла ошибка. Пожалуйста, попробуйте снова.")
        print(f"Ошибка при вводе возраста: {e}")

# Функция для получения веса
@dp.message_handler(state = UserState.growth)
async def set_weight(message: types.Message, state: FSMContext):
    try:
        await state.update_data(growth = message.text)
        await message.answer('Введите свой вес:')
        await UserState.weight.set()
    except Exception as e:
        await message.answer("Произошла ошибка. Пожалуйста, попробуйте снова.")
        print(f"Ошибка при вводе роста: {e}")

# Функция для получения пола
@dp.message_handler(state = UserState.weight)
async def set_gender(message: types.Message, state: FSMContext):
    try:
        await state.update_data(weight = message.text)
        await message.answer('Введите ваш пол (м/ж):')
        await UserState.gender.set()
    except Exception as e:
        await message.answer("Произошла ошибка. Пожалуйста, попробуйте снова.")
        print(f"Ошибка при вводе веса: {e}")

# Функция для вычисления норм калорий
@dp.message_handler(state = UserState.gender)
async def calculate_calories(message: types.Message, state: FSMContext):
    try:
        gender = message.text.lower()
        data = await state.get_data()
        age = int(data['age'])
        growth = float(data['growth'])
        weight = float(data['weight'])

        # Определяем формулу для подсчета калорий
        if gender == 'м':
            calories = 10 * weight + 6.25 * growth - 5 * age + 5
        else:
            calories = 10 * weight + 6.25 * growth - 5 * age - 161

        await message.answer(f"Ваша норма калорий: {calories:.2f} ккал.")
        await state.finish()  # Завершение состояний
    except Exception as e:
        await message.answer("Произошла ошибка при расчете калорий. Пожалуйста, попробуйте снова.")
        print(f"Ошибка при расчете калорий: {e}")

@dp.message_handler()
async def all_message(message: types.Message):
    await message.answer('Введите команду /start, чтобы начать общение.')

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates = True)


