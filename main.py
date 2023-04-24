import time
from aiogram import Bot, Dispatcher, executor, types
import logging
import openai
from googletrans import Translator
import sqlite3


logging.basicConfig(level=logging.INFO)
chat_api = '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'
bot = Bot(token="6051099724:AAGNVP-IbMm-5AAkJQ8_QJEXdhCHBdThoCw")
dp = Dispatcher(bot)

help_com = """
ЗАПРОСЫ И ПРИМЕРЫ:


/bill - Запрос для AI  (/bill + ваш запрос)

Пример: /bill Напиши доклад на тему курение вредит 
(В ответ получите сгенерированный ответ AI)


/ttr - Перевести на Русский 

Пример: /ttr Hello, how are you? 
(В ответ получите переведенный текст)


/tte - Перевести на Английский

Пример: /tte Привет, как дела? 
(В ответ получите переведенный текст)
"""
hello_com = """
Привет я Искуственный интелект, чем могу помочь?
Нажмите /help для списка команд
"""
en_com = "You entered an empty request!"
ru_com = "Вы ввели пустой запрос!"
checks = ""
jdi = """
Ваш запрос принят, ожидайте ответ.
"""
jdisuka = """
Секундочку хозяин, ваш запрос в приоритете
"""

vips = """
Секундочку, вы постаянный пользователь и мой создатель добавил вас в список приоритета, вы получите ответ одним из первых!
"""



@dp.message_handler(commands=['help'])
async def help_command(message: types.Message):
    await message.reply(text=help_com)


@dp.message_handler(commands=['start'])
async def help_command(message: types.Message):
    await message.answer(text=hello_com)
    await message.delete()


@dp.message_handler(commands=['ttr'])
async def chat_cmd(message: types.Message):
    gruf = message.get_args()
    translator = Translator()
    arg = message.get_args()
    checks = ""
    lin = [arg]
    ids = message.from_user.id
    name = message.from_user.username
    idds = str(ids)
    print(ids)
    print(name)
    if arg == checks:
        await message.reply(text=en_com)

    try:
        result = translator.translate(gruf, src='en', dest='ru')
        args =  result.text
        print(args)

    except:
        print("Пусто")

@dp.message_handler(commands=['tte'])
async def chat_cmd(message: types.Message):
    gruf = message.get_args()
    translator = Translator()
    arg = message.get_args()
    lin = [arg]
    ids = message.from_user.id
    name = message.from_user.username
    idds = str(ids)
    print(ids)
    print(name)
    if arg == checks:
        await message.reply(text=ru_com)

    try:
        result = translator.translate(gruf, src='ru', dest='en')
        args =  result.text
        print(args)
    except:
        print("Пусто")


@dp.message_handler(commands=['bill'])
async def chat_cmd(message: types.Message):
    arg = message.get_args()

    print(arg)
    lin = [arg]
    checks = ""
    zero = """
Вы ввели пустой запрос
You entered an empty request!
"""
    check = str(zero)
    ids = message.from_user.id
    name = message.from_user.username
    idds = str(ids)
    print(ids)
    print(name)
    suka = str('gervnotfound')
    vip1 = str('lyuda_s_h')
    vip2 = str('mariupolchanin1')
    vip3 = str('madarauchihaoriginal')
    vip4 = str('billsaidkhanov')
    vip5 = str('ilo02')

    if name == suka:
        await message.reply(text=jdisuka)
    if name == vip1:
        await message.reply(text=vips)
    if name == vip2:
        await message.reply(text=vips)
    if name == vip3:
        await message.reply(text=vips)
    if name == vip4:
        await message.reply(text=jdisuka)
    if name == vip5:
        await message.reply(text=vips)

    else:
        await message.reply(text=jdi)


    if arg == checks:
        await message.reply(text=check + help_com)

    else:
        with open(fr"ss.txt", "a") as file:
            file.writelines("%s\n" % line for line in lin)
            file.close()
        openai.api_key = chat_api
        model_engine = "text-davinci-003"
        prompt = f"{arg}"
        completation = openai.Completion.create(
            engine = model_engine,
            prompt = prompt,
            max_tokens = 2048,
            n = 1,
            stop = None,
            temperature = 0.5
        )
        response = completation.choices[0].text
        await message.reply(f"{response}")


if __name__ == "__main__":
    try:
        executor.start_polling(dp, skip_updates=True)

    except:
        time.sleep(10)
        executor.start_polling(dp, skip_updates=True)
