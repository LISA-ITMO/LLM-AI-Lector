from aiogram import F, Router
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.types import BotCommand, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, PollAnswer
from aiogram.methods.send_poll import SendPoll
import json
import utils
from bot import bot

router = Router()
POS = {904273633 : "Студент", 370925655 : "Студент", 170805003 : "Студент", 802016788 : "Студент"}
FLAG = {}
DISC = {}
THEME = {}
NUM = {}
POLLS = {}
SCORE = {}

class Form(StatesGroup):
    isu = State()
    position = State()
    discipline = State()
    theme = State()

async def set_commands_student(bot):
    commands = [
        BotCommand(command="/menu", description="Вернуться в меню"),
        BotCommand(command="/ask", description="Задать вопрос ИИ"),
        BotCommand(command="/test", description="Пройти тестирование"),
        BotCommand(command="/read", description="Изучить конспект"),
    ]
    await bot.set_my_commands(commands)

async def set_commands_teacher(bot):
    commands = [
        BotCommand(command="/menu", description="Вернуться в меню"),
        BotCommand(command="/statistics", description="Просмотреть статистику"),
        BotCommand(command="/docs", description="Загрузить матриалы"),
    ]
    await bot.set_my_commands(commands)

async def set_commands_noone(bot):
    commands = [
        BotCommand(command="/menu", description="Вернуться в меню"),
    ]
    await bot.set_my_commands(commands)

@router.message(Command("menu"))
async def start_handler(msg: Message):
    print(msg.chat.id)
    FLAG[msg.chat.id] = 0
    DISC[msg.chat.id] = 0
    THEME[msg.chat.id] = 0

    pos = POS[msg.chat.id]
    if pos == 'Преподаватель':
        await set_commands_teacher(bot)
        await msg.reply(text="Ознакомтесь с доступными вам командами. Если вам кажется, что в наборе команд ошибка, свяжитесь с администратором.")
    elif pos == 'Студент':
        await set_commands_student(bot)
        await msg.reply(text="Ознакомтесь с доступными вам командами. Если вам кажется, что в наборе команд ошибка, свяжитесь с администратором.")
    else:
        await set_commands_noone(bot)
        keyboard = InlineKeyboardMarkup(inline_keyboard=[[
                InlineKeyboardButton(text="✅ Хочу!", callback_data="register_yes"),
                InlineKeyboardButton(text="❌ Нет.", callback_data="register_no"),]])
        await msg.answer(text="Вашего ID не обнаружено в базе данных. Хотите зарегестрироваться?", reply_markup=keyboard)

@router.callback_query(F.data == 'register_yes')
async def yes_reg(call: CallbackQuery, state: FSMContext):
    await state.set_state(Form.isu)
    await call.message.answer("Ведите ваш ИСУ")

@router.message(Form.isu)
async def isu_get(message: Message, state: FSMContext):
    await state.update_data(isu=message.text)
    await state.set_state(Form.position)
    await message.answer("Введите вашу должность: преподаватель или студент")

@router.message(Form.position)
async def isu_get(message: Message, state: FSMContext):
    await state.update_data(position=message.text)
    date = await state.get_data()
    isu, pos = date["isu"], date["position"]
    await message.answer(text="Ваши данные отправлены на проверку администратору:\n" + str(message.chat.id) + ' ' + str(isu) + ' ' + str(pos) + "\nОжидайте ответа!")
    await state.clear()
    await start_handler(message)

@router.callback_query(F.data == 'register_no')
async def no_reg(call: CallbackQuery):
    await call.answer("Регистрация отменена.", show_alert=True)
    return

@router.message(F.text.in_ ({"/test", "/read"}))
async def test(Message, state: FSMContext):

    if Message.text == '/read' :
        await Message.answer(text="В разработке!")
        return

    if DISC[Message.chat.id] == 0 or THEME[Message.chat.id] == 0 :
        NUM[Message.chat.id] = 0
        SCORE[Message.chat.id] = 0
        kb = []
        with open(f'diciplines.txt', 'r') as file:
            for line in file:
                line = line.replace('_', ' ')
                kb.append([KeyboardButton(text=f'{line}')])
        keyboard = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True, one_time_keyboard=True)
        await state.set_state(Form.discipline)
        await Message.answer(text="Выберите дисциплину", reply_markup=keyboard)

    if DISC[Message.chat.id] != 0 and THEME[Message.chat.id] != 0:
        NUM[Message.chat.id] += 1
        if NUM[Message.chat.id] > 3:
            await Message.answer(f"Тест завершен! Ваш результат: {SCORE[Message.chat.id]}/3")
            await start_handler(Message)
            return
        d = DISC[Message.chat.id]
        t = THEME[Message.chat.id]
        with open(f'{d}/{t}/test_{NUM[Message.chat.id]}.json', 'r') as json_file:
            data = json.load(json_file)
        quest = str(data["вопрос"])
        opt = data["ответы"]
        correct = int(data["верный ответ"])
        explan = str(data["объяснение"])

        keyboard = InlineKeyboardMarkup(inline_keyboard=[[
                InlineKeyboardButton(text="Ещё!", callback_data="another_quest"),]])
        quiz = await bot.send_poll(Message.chat.id, quest, options=opt, is_anonymous=False, type='quiz', correct_option_id=correct, explanation=explan, reply_markup=keyboard)
        POLLS[quiz.poll.id] = quiz.poll.correct_option_id

@router.poll_answer()
async def poll_answer(poll_answer: PollAnswer):

    answer_ids = poll_answer.option_ids
    user_id = poll_answer.user.id
    poll_id = poll_answer.poll_id
    if POLLS[poll_id] == answer_ids[0]:
        SCORE[user_id] += 1
        print("good", SCORE[user_id])
    else:
        print("bad")

@router.message(Form.discipline)
async def isu_get(message: Message, state: FSMContext):
    await state.update_data(discipline=message.text)
    await state.set_state(Form.theme)
    kb = []
    with open(f'themes.txt', 'r') as file:
        for line in file:
            a, b = line.split()
            a = a.replace('_', ' ')
            if a == message.text:
                kb.append([KeyboardButton(text=f'{b}')])
    keyboard = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True, one_time_keyboard=True)
    await message.answer(text="Выберите тему", reply_markup=keyboard)

@router.message(Form.theme)
async def isu_get(message: Message, state: FSMContext):
    await state.update_data(theme=message.text)
    date = await state.get_data()
    isu, pos = date["discipline"], date["theme"]
    DISC[message.chat.id] = isu
    THEME[message.chat.id] = pos
    await message.answer(text=f"Опрос по дисциплине {isu} по теме {pos}")
    await state.clear()
    await test(message, state)

@router.callback_query(F.data == 'another_quest')
async def quest(call: CallbackQuery):
    await test(call.message, FSMContext)
    return

@router.message(Command("docs"))
async def docs(Message):
    await Message.reply("В разработке!")

@router.message(Command("statistics"))
async def stats(Message):
    await Message.reply("В разработке!")

@router.message(Command("ask"))
async def side_ask(Message):
    global FLAG
    FLAG[Message.chat.id] = 1
    await Message.reply(text="Для выхода из режима общения воспользуйтесь командой /menu. Внимательно формулируйте вопросы, общаясь с ИИ. Помните, что он совершает ошибки!\nПродуктивного общения!")

@router.message(F.text)
async def ask(Message):
    global FLAG

    if (Message.chat.id in FLAG) and (FLAG[Message.chat.id] == 1):
        await Message.reply(text=str(utils.get_answer(Message)))
    else:
        await start_handler(Message)
    return


