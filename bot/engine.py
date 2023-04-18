import sys

sys.path.append('/home/vanek/mark/config')
sys.path.append('/home/vanek/mark/database')


from aiogram.dispatcher import FSMContext
from aiogram import Bot, Dispatcher, types, executor
from config import BOT_TOKEN, ADMIN_ID
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from keyboard import keyboard_admin_sender, keyboard_language, keyboard_response_user_cn, keyboard_response_user_en, keyboard_response_user_ru
from aiogram.dispatcher.filters.state import State, StatesGroup
from db import db

bot = Bot(token=BOT_TOKEN)

dp = Dispatcher(bot=bot, storage=MemoryStorage())


class UserAnketa(StatesGroup):
    address = State()
    username = State()
    photo_logo = State()

class AdminAnswer(StatesGroup):
    id_user = State()
    text = State()
    photo = State()

@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    id_user = message.from_user.id
    user_in_db = db.check_user_db_users(id_user=id_user)
    if user_in_db == []:
        await message.answer('Choose language', reply_markup=keyboard_language)
    else:
        status = db.get_user_status(id_user=id_user)
        if status[0][0] == 'member':
            check_db = db.check_user_wait(id_user=id_user)
            user_language = db.get_user_language(id_user=id_user)[0][0]
            if check_db == []:
                if user_language == 'ru':
                    await message.answer("""USDTSCAN Star Bot приветствует Вас!
Заполните анкетные данные для получения Лидерского Аватара с текущим звездным рангом.
Для перехода к заполнению нажмите на кнопку Заполнить!""",
                         reply_markup=keyboard_response_user_ru)
                    
                elif user_language == 'en':
                    await message.answer("""USDTSCAN Star Bot welcomes you!
Fill out the personal data to receive a Leader Avatar with the current star rank.
To proceed to the filling, click on the Fill!""", reply_markup=keyboard_response_user_en)
                    
                elif user_language == 'cn':
                    await message.answer("""USDTSCAN Star Bot 歡迎您！
填寫個人資料，即可獲得當前星級的領袖頭像。
要繼續填充，請單擊填充！""", reply_markup=keyboard_response_user_cn)
                    
            else:
                if user_language == 'ru':
                    await message.answer("""Вы уже оставляли заявку, ожидайте ответа!""")
                elif user_language == 'en':
                    await message.answer("""You have already filled out your request, please respond again!""")
                elif user_language == 'cn':
                    await message.answer("""您已经填入了您的请求，请重新回答！""")
                    
        elif status[0][0] == 'admin':
            await message.answer('Вы находитесь в админ-панели!')
            
@dp.callback_query_handler(text='ru_lg')
async def ru_lg_func(call: types.CallbackQuery):
    await call.message.delete()
    await call.message.answer("""USDTSCAN Star Bot приветствует Вас!
Заполните анкетные данные для получения Лидерского Аватара с текущим звездным рангом.
Для перехода к заполнению нажмите на кнопку Заполнить!
""", reply_markup=keyboard_response_user_ru)
    
    db.correct_user(id_user=call.from_user.id, language='ru')            
            
@dp.callback_query_handler(text='en_lg')
async def en_lg_func(call: types.CallbackQuery):
    await call.message.delete()
    await call.message.answer("""USDTSCAN Star Bot welcomes you!
Fill out the personal data to receive a Leader Avatar with the current star rank.
To proceed to the filling, click on the Fill!
""", reply_markup=keyboard_response_user_en)
    
    db.correct_user(id_user=call.from_user.id, language='en')    
    
@dp.callback_query_handler(text='cn_lg')
async def cn_lg_func(call: types.CallbackQuery):
    await call.message.delete()
    await call.message.answer("""USDTSCAN Star Bot 歡迎您！
填寫個人資料，即可獲得當前星級的領袖頭像。
要繼續填充，請單擊填充！
""", reply_markup=keyboard_response_user_cn)
    
    db.correct_user(id_user=call.from_user.id, language='cn')           
             
             
@dp.callback_query_handler(text='start_response', state=None)
async def start_response_func(call: types.CallbackQuery):
    await call.message.delete()
    id_user = call.from_user.id
    user_language = db.get_user_language(id_user=id_user)[0][0]
    if user_language == 'ru':
        await call.message.answer("""Отправьте адрес кошелька USDTSCAN👇""")
        await UserAnketa.address.set()
    elif user_language == 'en':
        await call.message.answer("""Send USDTSCAN wallet address👇""")
        await UserAnketa.address.set()
    elif user_language == 'cn':
        await call.message.answer("""提交USDTSCAN錢包地址👇""")
        await UserAnketa.address.set()

@dp.message_handler(state=UserAnketa.address)
async def send_response_func_address(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['address'] = message.text
    id_user = message.from_user.id
    user_language = db.get_user_language(id_user=id_user)[0][0]
    if user_language == 'ru':
        await message.answer("""Отправьте Имя Фамилию/Никнейм, которое будет отображено на Лидерском Аватаре👇""")
        await UserAnketa.username.set()
    elif user_language == 'en':
        await message.answer("""Send First Name Last Name/Nickname, which will be displayed on the Leader Avatar👇""")
        await UserAnketa.username.set()
    elif user_language == 'cn':
        await message.answer("""發送 名字 姓氏/暱稱，會顯示在領袖頭像👇""")
        await UserAnketa.username.set()
    
@dp.message_handler(state=UserAnketa.username)
async def send_response_func_username(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['username'] = message.text
    id_user = message.from_user.id
    user_language = db.get_user_language(id_user=id_user)[0][0]
    
    if user_language == 'ru':
        await message.answer("""Отправьте Ваше Личное фото или Брендированный Логотип, который будет отображен на Лидерском Аватаре👇""")
        await UserAnketa.photo_logo.set()
    elif user_language == 'en':
        await message.answer("""Send your Personal Photo or Branded Logo to be displayed on the Leader Avatar👇""")
        await UserAnketa.photo_logo.set()
    elif user_language == 'cn':
        await message.answer("""提交您的個人照片或品牌標誌以顯示在領袖頭像👇""")
        await UserAnketa.photo_logo.set()

@dp.message_handler(state=UserAnketa.photo_logo, content_types=['document', 'photo'])
async def start_response_func_photo_logo(message: types.Message, state: FSMContext):
    try:
        if message['photo'] != []:
            async with state.proxy() as data:
                data['photo_logo'] = message.photo[0].file_id
            
            id_user = message.from_user.id
            user_language = db.get_user_language(id_user=id_user)[0][0]
                
            db.add_user_wait(id_user=message.from_user.id, address=data['address'], nickname=data['username'], 
                             image=data['photo_logo'])
            
            await bot.send_photo(chat_id=ADMIN_ID, photo=data['photo_logo'], caption=f'Запрос от пользователя {message.from_user.id} \nUSERNAME: {data["username"]}\nADDRESS: {data["address"]}\nЯзык пользователя: {user_language[0][0]}',
                                reply_markup=keyboard_admin_sender)
            
            if user_language == 'ru':  
                await message.answer("""Благодарим! Ваши данные приняты. Ожидайте обработки полученной информации. После завершения обработки, Вы получите сгенерированный Лидерский Аватар согласно Вашему Звездного Рангу.""")
            elif user_language == 'en':
                await message.answer("""Thank you! Your details have been accepted. Wait for the processing of the received information. Upon completion of processing, you will receive a generated Leader Avatar according to your Star Rank.""")
            elif user_language == 'cn':
                await message.answer("""謝謝你！ 您的詳細信息已被接受。 等待對接收到的信息進行處理。 處理完成後，您將根據您的星級獲得生成的領袖頭像。""")
    
            await state.finish()
    
    
        elif message['document']:
            async with state.proxy() as data:
                data['photo_logo'] = message.document.file_id
            
            id_user = message.from_user.id
            user_language = db.get_user_language(id_user=id_user)[0][0]
                
            db.add_user_wait(id_user=message.from_user.id, address=data['address'], nickname=data['username'], 
                             image=data['photo_logo'])
            
            await bot.send_document(chat_id=ADMIN_ID, document=data['photo_logo'], caption=f'Запрос от пользователя {message.from_user.id} \nUSERNAME: {data["username"]}\nADDRESS: {data["address"]}\nЯзык пользователя: {user_language[0][0]}',
                                reply_markup=keyboard_admin_sender)
            
            if user_language == 'ru':  
                await message.answer("""Благодарим! Ваши данные приняты. Ожидайте обработки полученной информации. После завершения обработки, Вы получите сгенерированный Лидерский Аватар согласно Вашему Звездного Рангу.""")
            elif user_language == 'en':
                await message.answer("""Thank you! Your details have been accepted. Wait for the processing of the received information. Upon completion of processing, you will receive a generated Leader Avatar according to your Star Rank.""")
            elif user_language == 'cn':
                await message.answer("""謝謝你！ 您的詳細信息已被接受。 等待對接收到的信息進行處理。 處理完成後，您將根據您的星級獲得生成的領袖頭像。""")
    
            await state.finish()
            
    except Exception as ex:
        id_user = message.from_user.id
        user_language = db.get_user_language(id_user=id_user)[0][0]
        
        if user_language == 'ru':
            await message.answer("""Ошибка! Пожалуйста, отправьте Ваше Личное фото или Брендированный Логотип, который будет отображен на Лидерском Аватаре👇""")
            await UserAnketa.photo_logo.set()
        elif user_language == 'en':
            await message.answer("""Error! Please, send your Personal Photo or Branded Logo to be displayed on the Leader Avatar👇""")
            await UserAnketa.photo_logo.set()
        elif user_language == 'cn':
            await message.answer("""提交您的個人照片或品牌標誌以顯示在領袖頭像👇""")
            await UserAnketa.photo_logo.set()


@dp.callback_query_handler(text='back_response')
async def back_response_func(call: types.CallbackQuery):
    await call.message.delete()
    id_user = int(call.message.caption.split('Запрос от пользователя ')[1].split(' \n')[0])
    await call.message.answer('Пользователь получил свой запрос обратно!')
    db.delete_user_wait(id_user=id_user)
    user_language = db.get_user_language(id_user=id_user)[0][0]
    if user_language == 'ru':
        await bot.send_message(chat_id=id_user, text='К сожалению мы не может принять такой лого!',
                               reply_markup=keyboard_response_user_ru)
    elif user_language == 'en':
        await bot.send_message(chat_id=id_user, text='Unfortunately, we cannot accept such a logo!',
                               reply_markup=keyboard_response_user_en)
    elif user_language == 'cn':
        await bot.send_message(chat_id=id_user, text='遗憾的是，我们不能接受这样的标识!',
                               reply_markup=keyboard_response_user_cn)


@dp.callback_query_handler(text='send_response')
async def send_response_func(call: types.CallbackQuery, state: FSMContext):
    id_user = int(call.message.caption.split('Запрос от пользователя ')[1].split(' \n')[0])
    async with state.proxy() as data:
        data['id_user'] = id_user
    await call.message.answer('Введите текст 👇')
    await AdminAnswer.text.set()

@dp.message_handler(state=AdminAnswer.text)
async def send_response_func_text(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['text'] = message.text
    await message.answer('Отправьте фотографию 👇')
    await AdminAnswer.photo.set()
    
@dp.message_handler(state=AdminAnswer.photo, content_types=['photo'])
async def send_response_func_photo(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['photo'] = message.photo[0].file_id 
        
        
    await bot.send_photo(chat_id=data['id_user'], photo=data['photo'],
                         caption=data['text'])
    await message.answer('Пользователь получил результат!')
    await state.finish()
    db.delete_user_wait(id_user=data['id_user'])

if __name__ == '__main__':
    executor.start_polling(dispatcher=dp, skip_updates=True)