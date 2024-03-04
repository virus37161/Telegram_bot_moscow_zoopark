import aiohttp
import asyncio
from aiogram import F
from aiogram.filters import Command, CommandObject
from aiogram.types import Message
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from aiogram.utils.formatting import (
   Bold, as_list, as_marked_section
)
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram import  Router, types
from aiogram.filters import Command
import random
from Victorina import questions
import re
class Order(StatesGroup):
    start_victorina = State()
    Question_next = State()
    result= State()
    otziv_set = State()
router = Router()
Otzivi=[]

def set_otziv(ot, name):
    global Otzivi
    lis_ot = ot.split(" ")
    lis_ot_filter = f"{name}"    #данная функция фильтрует отзыв от всяких смайликов и так далее. Чтобы без проблем записывать отзыв в отдельный файл
    for i in lis_ot:
        i = re.findall(r"\w", i)
        i = ''.join(i)
        lis_ot_filter = f"{lis_ot_filter} { i}"
    Otzivi.append(lis_ot_filter)
    return None

def print_otziv():
    return Otzivi

def clear():
    global Otzivi
    Otzivi = []

@router.message(Command("victorina"))# Начало викторины
async def start(message: Message, state: FSMContext):

    kb = [[types.KeyboardButton(text="Ураа!Поехали!")]]
    keybord = (types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True, one_time_keyboard= True,))
    await message.answer(f"Добро пожаловать в викторину. Любой человек хотел бы узнать каким бы животным он был. И я вас поздравляю!!! "
                         f"Пройдя тест вы сможете узнать кто вы есть. Правила игры просты, честно отвечайте на вопросы)", reply_markup=keybord)
    await state.set_state(Order.start_victorina.state)



@router.message(Order.start_victorina)#на данном этапе задается первый вопрос,создаются все необходимые переменные
async def victorina(message: Message, state: FSMContext):
    Q = questions.copy()
    Res = Q.copy()
    result=[]
    Q_1= random.choice(Q)
    Q.remove(Q_1)
    kb = []
    answers = []
    for i in list((list(Q_1.values())[0]).keys()):
        kb.append([types.KeyboardButton(text=i)])
    keybord = (types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True, one_time_keyboard= True,))
    await message.answer(f"{list(Q_1.keys())[0]}", reply_markup=keybord)

    await state.set_data([Q, Res, result, Q_1, answers])
    await state.set_state(Order.Question_next.state)


async def result_victorina (message: Message, result,answers):#выводит результат викторины
    kb = [[types.KeyboardButton(text="Связаться со специалистом")], [types.KeyboardButton(text="Узнать, как взять под опеку вашего нового друга")],
           [types.KeyboardButton(text="Перезапуск викторины /victorina")]]
    keybord = (types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True, one_time_keyboard=True, ))
    res_volk = set(result).intersection({'1_1', '2_1', '3_2', "5_2", "6_1","7_1"})               #в данных присвоениях определяется количество совпадений
    res_Rosom = set(result).intersection({"1_1", "2_1", "3_2", "5_2", "6_2", "4_1", "8_1"})                 #а также присваивается значение животного
    res_mart = set(result).intersection({"1_1", "2_2", "3_2", "5_1", "6_1"})
    res_jaguar = set(result).intersection({"1_1", "2_1", "3_2", "4_2", "5_2", "6_2", "7_2"})
    res_orel = set(result).intersection({"1_2", "2_1", "4_2", "5_2", "6_2", "9_1"})
    res_dikdik = set(result).intersection({"1_1", "2_2", "4_1", "5_1", "10_1"})
    res_cherepaha = set(result).intersection({"1_1", "2_2", "3_1", "4_2", "5_1", "10_2"})        #
    result_list = [res_volk, res_Rosom, res_mart, res_cherepaha, res_dikdik, res_orel,res_jaguar]                                             #создали список с совпадениями
    result_list2 = sorted(result_list, key = lambda x:len(x), reverse=True)                 #сортируем по убыванию.
    if result_list2[0] == res_volk:                                                        #То есть первый элемент будет с самым большим количеством совпадений
        await message.answer("Смелость и храбрость это про вас. Вы настоящий волк", reply_markup=keybord)
        await message.answer_photo(photo = 'https://moscowzoo.ru/upload/iblock/5fe/1.jpg')
        await message.answer("Поближе с данным животным вы можете познакомиться здесь: https://moscowzoo.ru/animals/khishchnye/polyarnyy-volk/")
                                                                                   #а соответственно первый элемент списка будет нашим результатом викторины
    elif result_list2[0] == res_Rosom:                                                                   #Но результат викторины в списке пока в виде множества, надо найти равенство с переменными с нашими животными
        await message.answer("Да вы росомаха. Милое и одновременно опасное животное",reply_markup=keybord)
        await message.answer_photo(photo="https://moscowzoo.ru/upload/iblock/e80/e804e2d3618197eefef705ffcd1bd2c4.jpg")
        await message.answer("Поближе с данным животным вы можете познакомиться здесь: https://moscowzoo.ru/animals/khishchnye/rosomakha/")
                                                                  #В ИТОГЕ мы получили алгоритм, который наибольше сходство ответов пользователя
    elif result_list2[0] == res_mart:                                                 #c признаками животного и выдает нам результат.
        await message.answer("Любите бананы? Тогда вы мартышка)",reply_markup=keybord)
        await message.answer_photo(photo="https://moscowzoo.ru/upload/iblock/cf7/2.jpg")   # чтобы добавлять новых животных надо просто создать переменные с признаками и добавить их в писок result_list
        await message.answer("Поближе с данным животным вы можете познакомиться здесь: https://moscowzoo.ru/animals/primaty/martyshka-diana/")

    elif result_list2[0] == res_orel:                                                   # и еще надо дополнительный elif добавить по аналогии
        await message.answer("Высоты, видимо, вы не боитесь. Вы вольный орел ", reply_markup=keybord)
        await message.answer_photo(photo="https://moscowzoo.ru/upload/iblock/f82/610.4.jpg")
        await message.answer("Поближе с данным животным вы можете познакомиться здесь: https://moscowzoo.ru/animals/sokoloobraznye/stepnoy-orel/")

    elif result_list2[0] == res_dikdik:
        await message.answer("Смотрите какие классные обыкновенные дикдики. Вы один из них)", reply_markup=keybord)
        await message.answer_photo(photo="https://moscowzoo.ru/upload/iblock/96e/96e105e6bd95cb3091db0e393acf924b.jpg")
        await message.answer("Поближе с данным животным вы можете познакомиться здесь: https://moscowzoo.ru/animals/parnokopytnye/obyknovennyy-dikdik/")

    elif result_list2[0] == res_cherepaha:
        await message.answer("Слоновая черепаха", reply_markup=keybord)
        await message.answer_photo(photo="https://moscowzoo.ru/upload/resize_cache/iblock/5fc/350_350_1/5fc23d18660bb25ab23237d55151be1e.jpg")
        await message.answer("Поближе с данным животным вы можете познакомиться здесь: https://moscowzoo.ru/animals/cherepakhi/slonovaya-cherepakha/")

    elif result_list2[0] == res_jaguar:
        await message.answer("Ягуарунди.А вы в жизни тоже такие красивые? ", reply_markup=keybord)
        await message.answer_photo(photo="https://moscowzoo.ru/upload/iblock/a95/a95c0e1c18f051933644368bb2bc2350.jpg")
        await message.answer("Поближе с данным животным вы можете познакомиться здесь: https://moscowzoo.ru/animals/khishchnye/yaguarundi/")


@router.message(Order.Question_next)  # данный обработчик задает все остальные вопросы,
async def second_question(message: Message, state: FSMContext):   #а также сохраняет 2 вида результатов викторины
    Take = await state.get_data()    #(1- индексы ответов,которые в дальнейшем передаются в функцию result_victorina, где на основании даных индексов происходит определение животного
    Q = Take[0]    # 2- сохраняются вопрос - ответ для дальнейшей передачи специалисту, в случае возникновения необходимости)
    Res = Take[1]
    result = Take[2]
    answer = Take[3]
    answers = Take[4]
    if message.text not in list(list(answer.values())[0].keys()):
        await message.answer ("Что-то не могу найти подобный ответ \n Попробуйте, пожалуйста, запустить викторину заного")
        await state.clear()
        return None
    result.append(list(answer.values())[0].get(message.text))
    answers.append({list(answer.keys())[0]:message.text})
    if Q!= []:
        Q_1 = random.choice(Q)
    else:
        await result_victorina(message, result,answers)
        await state.clear()
        return None
    Q.remove(Q_1)
    kb = []
    for i in list((list(Q_1.values())[0]).keys()):
        kb.append([types.KeyboardButton(text=i)])
    keybord = (types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True, one_time_keyboard= True,))
    await message.answer(f"{list(Q_1.keys())[0]}", reply_markup=keybord)
    await state.set_data([Q, Res,result, Q_1, answers])
    await state.set_state(Order.Question_next.state)


@router.message(Command("otziv"))
async def otziv (message: Message, state: FSMContext):
    await message.answer("Оставьте, пожалуйста, свой честный отзыв ")
    await state.set_data([f"{message.chat.first_name} - {message.from_user.id}"])
    await state.set_state(Order.otziv_set.state)

@router.message(Order.otziv_set)
async def oziv_set_(message:Message, state:FSMContext):
    sved = await state.get_data()
    mess_otziv = f"{message.text}"
    name = f"{sved} \n Отзыв: \n"
    set_otziv(mess_otziv, name)
    await message.answer("Спасибо за вашу обратную связь\n"
                         )
    await state.clear()

@router.message(Command("otziv_take"))
async def otziv_take(message: Message):
    if message.from_user.id == 6433843865: # команду может запустить только человек с таким id
        with open("otzivi.txt", 'a') as f:
            for i in print_otziv():
                f.write(f"{i} \n")  #Сохраняет все отзывы в отдельный файл
                await message.answer(i)     #отправляет НОВЫЕ отзывы специалисту. Старые отзывы специалисту направлены не будут. Но все можно будет найти в файле
        clear()
    else:
        await message.answer("Извините, но вы ошиблись командой")

@router.message(Command("opeka"))
async def victori(message: Message, state: FSMContext):
    await message.answer("По этой ссылке можно узнать информацию об опеке \nhttps://moscowzoo.ru/my-zoo/become-a-guardian/ \n"
                         "А еще там очень много классных животных. Одного себе точно возьмете")


@router.message(Command("support"))
async def victor(message: Message):
    await message.answer(f"Данный сотрудник готов вам помочь решить все ваши вопросы. \nЕсли он не отвечает, значит ухаживает за вашим будущим животным. \n@Aleks14242")


