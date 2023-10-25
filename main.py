## добавить изменение прогресса выполнения, и если 100, то добавить в изученое
## добавить пинки о повторении
## добавить счётчик времени когда пользователь закончит выполнение

import config
import Baze_Control
import telebot
import sys
from telebot import types

# какая то херня с забором из read_base, проверь какой индекс берёт в F()[][тут] РЕШЕНО
# import sqlite3

bot = telebot.TeleBot(config.TOKEN)
matereal = ''
type_mat = ''
progress_mat = ''

# когда будут проблеммы с тем что 2 пользователя долбятся, можно их обрабатывать путём просмотра предыдущих сообщений

# if input() == '':
#    sys.exit()
# Послане мне в будующее с интернетом, если что-то пойдёт что-то не так захерчь всё в int(), ну либо в тип данных. вероятно ошиька там, проверить не могу p.c. главное не забыть это прочитать РЕШЕНО
# РЕШЕНО

'''
@bot.message_handler(commands=['exit'])
def exit(message):
    print(f'Офнул: {message.chat.id}')
    sys.quit()
    #bot.polling(none_stop=False)
'''


@bot.message_handler(commands=['start'])
def start(message):
    Baze_Control.start()
    Baze_Control.add_user(message.chat.id)
    markup = types.InlineKeyboardMarkup()
    bot.send_message(message.chat.id,
                     f'Добро пожаловать в БоТиКа "Подсказочник"(над названием ведутся работы(как и над аватаркой)), этот бот позволяет во первых разработчику поковырять палкой Питухон, ТГ, БД, а также(что маловероятно) помочь вам в более удобном изучении информации, а именно вы можете попросить его запомнить какой-то материал, прогресс его изучения. А после его изучения будет напоминать о повотренни, тк для успешного и полного изучения стоит повторить материал(достаточно просто перечитать) через час, день, нделю, месяц(естественно разработчик не спорит о том что ты ГЕНИЙ и тебе это не надо, конечно не надо, поэтому можешь закрыть этого бота и забыть о нём) а всем омтавшимся остаётся терпеть кривого бота т.к. разработчику 17 лет и он ещё совсем маслёнок и ничего не понимает, но обязательно научится')
    bot.send_message(message.chat.id,
                     f'И да привет {message.from_user.first_name} {message.from_user.last_name} вся информация о тебе уже запомнена, но если ты не хочешь чтобы твои драгоценные данные были сохранены напиши мне: @Not_IvannZ, я удалю о тебе информацию')


@bot.message_handler(commands=['show'])
def inf(message):
    markup = types.ReplyKeyboardMarkup()
    btn1 = types.KeyboardButton("Посмотреть список записей которые в процессе изучения")
    btn2 = types.KeyboardButton("Посмотреть список изученого")
    btn3 = types.KeyboardButton("Посмотреть список Архива")
    markup.row(btn1)
    markup.row(btn2, btn3)
    bot.send_message(message.chat.id, f"выбери тип записей которые хочешь посмотерть\nЕсли хочешь выйти напиши /exit", reply_markup=markup)
    bot.register_next_step_handler(message, on_click)


@bot.message_handler(commands=['del'])
def inf(message):
    markup = types.ReplyKeyboardMarkup()
    btn1 = types.KeyboardButton("Удалить запись которая в процессе изучения")
    btn2 = types.KeyboardButton("Удалить запись из изученого")
    btn3 = types.KeyboardButton("Удалить запись из  Архива")
    markup.row(btn1)
    markup.row(btn2, btn3)
    bot.send_message(message.chat.id, f"выбери тип записи которую хочешь удалить\nЕсли хочешь выйти напиши /exit", reply_markup=markup)
    bot.register_next_step_handler(message, on_click)


@bot.message_handler(commands=['add'])
def inf(message):
    markup = types.ReplyKeyboardMarkup()
    btn1 = types.KeyboardButton("Добавить материал для изучения")
    markup.row(btn1)
    btn2 = types.KeyboardButton("Добавить материал в архив")
    btn3 = types.KeyboardButton("Добавить материал в повторение")
    markup.row(btn2, btn3)
    bot.send_message(message.chat.id, "ВЫберите то что хотите добавить\nЕсли хочешь выйти напиши /exit", reply_markup=markup)
    bot.register_next_step_handler(message, on_click)


def on_click(message):
    user_id = Baze_Control.read_base(message.chat.id, "users")[0][0]
    markup = types.ReplyKeyboardRemove()

    if message.text == "Удалить запись которая в процессе изучения":
        answ = ''
        c = 0
        lern_list = Baze_Control.read_base(user_id, 'lern')
        print(f"lern_list from Удалить запись которая в процессе изучения: {lern_list}")
        if len(lern_list) == 0:
            bot.send_message(message.chat.id, "ЙО лиьо ты ещё не создавал записей, либо у меня проблемма)",
                             reply_markup=markup)
            print(
                f"From Удалить запись которая в процессе изучения, user: {user_id} hasn`t mark")  # Ёпт, переведи это нормально
            return 0
        for i in lern_list:
            answ += f'id:{c} прогресс:{i[3]}, тип: {i[4]}\n материал: {i[5]}\n'
            c += 1
        bot.send_message(message.chat.id,
                         f"Вот твой список записей в процессе обучения:\n \n {answ}\n\n Напиши id записи которую хочешь удалить\nесли нажал случайно /exit",
                         reply_markup=markup)
        bot.register_next_step_handler(message, del_lern1)

    elif message.text == "Удалить запись из изученого":
        answ = ''
        c = 0

        lerned_list = Baze_Control.read_base(user_id, 'lerned')
        print(f"lerned_list from Удалить запись из изученого: {lerned_list}")
        if lerned_list == []:
            bot.send_message(message.chat.id, f"Упс, у тебя нет записей, либо у меня проблемма)", reply_markup=markup)
            print(f"From Удалить запись из изученого, user: {user_id} hasn`t mark")  # Ёпт, переведи это нормально
            return 0
        for i in lerned_list:
            answ += f'id:{c} тип: {i[3]}\n материал: {i[4]}\n'
            c += 1
        bot.send_message(message.chat.id,
                         f"Вот твой список записей, которые ты изучил:\n \n {answ}\n\n Напиши id записи которую хочешь удалить\nесли нажал случайно /exit",
                         reply_markup=markup)
        bot.register_next_step_handler(message, del_lerned1)

    elif message.text == "Удалить запись из  Архива":  # ТУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУт РЕШИИИИИИИИИИИИИИИИИИИИИИИИИИИИИИИИИИИИИ
        answ = ''
        c = 0
        lern_list = Baze_Control.read_base(user_id, 'archive')
        print(f"lern_list from Удалить запись из  Архива: {lern_list}")
        if lern_list == []:
            bot.send_message(message.chat.id, f"ЙОО либо у тебя ещё нет записей, либо у меня проблемма)",
                             reply_markup=markup)
            print(f"From Удалить запись из  Архива, user: {user_id} hasn`t mark")  # Ёпт, переведи это нормально
            return 0
        for i in lern_list:
            answ += f'id:{c}, тип: {i[2]}\n материал: {i[3]}\n'
            c += 1
        bot.send_message(message.chat.id,
                         f"Вот твой список записей из архиива:\n \n {answ} \n\n Напиши id записи которую хочешь удалить\nесли нажал случайно /exit",
                         reply_markup=markup)
        bot.register_next_step_handler(message, del_archive1)

    elif message.text == "Посмотреть список записей которые в процессе изучения":
        answ = ''
        c = 0
        lern_list = Baze_Control.read_base(user_id, 'lern')
        print(f"lern_list from Посмотреть список записей которые в процессе изучения: {lern_list}")
        if len(lern_list) == 0:
            bot.send_message(message.chat.id, "ЙО лиьо ты ещё не создавал записей, либо у меня проблемма)",
                             reply_markup=markup)
            print(
                f"From Посмотреть список записей которые в процессе изучения, user: {user_id} hasn`t mark")  # Ёпт, переведи это нормально
            return 0
        for i in lern_list:
            answ += f'id:{c} прогресс:{i[3]}, тип: {i[4]}\n материал: {i[5]}\n'
            c += 1
        bot.send_message(message.chat.id,
                         f"Вот твой список записей в процессе обучения:\n \n {answ}", reply_markup=markup)

    elif message.text == "Посмотреть список изученого":
        answ = ''
        c = 0

        lerned_list = Baze_Control.read_base(user_id, 'lerned')
        print(f"lerned_list from Посмотреть список изученого: {lerned_list}")
        if lerned_list == []:
            bot.send_message(message.chat.id, f"Упс, у тебя нет записей, либо у меня проблемма)", reply_markup=markup)
            print(f"From Посмотреть список изученого, user: {user_id} hasn`t mark")  # Ёпт, переведи это нормально
            return 0
        for i in lerned_list:
            answ += f'id:{c} тип: {i[3]}\n материал: {i[4]}\n'
            c += 1
        bot.send_message(message.chat.id,
                         f"Вот твой список записей, которые ты изучил:\n \n {answ}",
                         reply_markup=markup)

    elif message.text == "Посмотреть список Архива":  # ТУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУт РЕШИИИИИИИИИИИИИИИИИИИИИИИИИИИИИИИИИИИИИ
        answ = ''
        c = 0
        lern_list = Baze_Control.read_base(user_id, 'archive')
        print(f"lern_list from Посмотреть список Архива: {lern_list}")
        if lern_list == []:
            bot.send_message(message.chat.id, f"ЙОО либо у тебя ещё нет записей, либо у меня проблемма)",
                             reply_markup=markup)
            print(f"From Посмотреть список Архива, user: {user_id} hasn`t mark")  # Ёпт, переведи это нормально
            return 0
        for i in lern_list:
            answ += f'id:{c}, тип: {i[2]}\n материал: {i[3]}\n'
            c += 1
        bot.send_message(message.chat.id,
                         f"Вот твой список записей из архиива:\n \n {answ}",
                         reply_markup=markup)

    elif message.text == "Добавить материал для изучения":
        global matereal, type_mat, progress_mat
        matereal = type_mat = progress_mat = ''
        markup = types.ReplyKeyboardRemove()
        # Baze_Control.add_lern(message.chat.id, "A","B", 0)
        bot.send_message(message.chat.id,
                         "Введите 'материал', ну или как это назвать, в общем то что хотите повторить в будующем, а точнее изучить\nлибо если вы не хотите это делать напишите /exit",
                         reply_markup=markup)
        bot.register_next_step_handler(message, add_mat1)

    elif message.text == "Добавить материал в архив":
        answ = ''
        c = 0
        user_id = Baze_Control.read_base(message.chat.id, "users")[0][0]
        lern_list = Baze_Control.read_base(user_id, 'lern')
        print(f"lern_list from Добавить материал в архив: {lern_list}")
        if lern_list == []:
            bot.send_message(f"ЙО либо ты ещё не создавал записей, либо у меня проблемма)")
            print(f"From Добавить материал в архив, user: {user_id} hasn`t mark")  # Ёпт, переведи это нормально
            return 0
        print("Lern_list from Добавить материал в архив: ", lern_list)
        for i in lern_list:
            answ += f'id:{c}, тип: {i[4]}\n материал: {i[5]}\n'
            c += 1
        markup = types.ReplyKeyboardRemove()
        bot.send_message(message.chat.id,
                         f"Вот твой список записей, напишите id записи которую хотите перенести в архив:\n \n {answ} \n \nлибо если вы не хотите это делать напишите /exit",
                         reply_markup=markup)

        bot.send_message(message.chat.id,
                         f'Выше вы видети список своих записи, напишите число, id записи, которую хотите добавить в архив')
        bot.register_next_step_handler(message, add_archive1)

    elif message.text == "Добавить материал в повторение":
        markup = types.ReplyKeyboardRemove()

        answ = ''
        c = 0
        user_id = Baze_Control.read_base(message.chat.id, "users")[0][0]
        lern_list = Baze_Control.read_base(user_id, 'lern')

        print(f"lern_list from Добавить материал в повторение: {lern_list}")
        if len(lern_list) == 0:
            bot.send_message(f"ЙО лиьо ты ещё не создавал записей, либо у меня проблемма)")
            print(f"From Добавить материал в повторение, user: {user_id} hasn`t mark")  # Ёпт, переведи это нормально
            return 0

        for i in lern_list:
            answ += f'id:{c} прогресс:{i[3]}, тип: {i[4]}\n материал: {i[5]}\n'
            c += 1
        bot.send_message(message.chat.id,
                         f"Вот твой список записей, напишите id записи которую хотите перенести в изученое:\n \n {answ}. \n\nлибо если вы не хотите это делать напишите /exit",
                         reply_markup=markup)

        bot.send_message(message.chat.id,
                         f'Выше вы видети список своих записи, напишите число, id записи, которую хотите добавить в изученое, и чтобы бот надпомнил вам её повторить для лучшего запоминания(через час, деньБ нделю, месяц)',
                         reply_markup=markup)
        bot.register_next_step_handler(message, add_lerned1)

    elif message.text == "/exit":
        bot.send_message(message.chat.id, "Exit", reply_markup=markup)

    elif message.text[0] == '/':
        bot.register_next_step_handler(message, on_click)

    elif message.text == "":
        print("Main.py line 247")

    # markup = types.ReplyKeyboardRemove()
    # bot.send_message(message.chat.id, "", reply_markup=markup)


def del_lern1(message):  ## дообавить проверку на удаление
    user_answ = message.text
    if user_answ == "/exit":
        return 0
    try:
        user_answ = int(user_answ)
        markup = types.ReplyKeyboardRemove()

        user_list = Baze_Control.read_base(message.chat.id, "users")
        user_id = user_list[0][0]
        lern_list = Baze_Control.read_base(user_id, 'lern')

        if len(lern_list) < user_answ:
            bot.send_message(
                f"йо, либо у меня, либо у тебя проблеммы, скорее всего у меня, проверь не сильно ли большой айдишник ввёл?")
            print(lern_list, len(lern_list), user_answ)

        Baze_Control.remove(user_answ, "lern")

        bot.send_message(message.chat.id,
                         f'Запись:\n {lern_list[user_answ]} \n \n успешно удалена', reply_markup=markup)
    except:
        bot.send_message(message.chat.id,
                         "Упс, выпала ошибка, возможно вы ввели цифру а не букву, повторите ввод(не вводить нельзя, я ещё не прописал)")
        bot.register_next_step_handler(message, add_archive1)


def del_lerned1(message):
    user_answ = message.text
    if user_answ == "/exit":
        return 0
    try:
        user_answ = int(user_answ)
        markup = types.ReplyKeyboardRemove()

        user_list = Baze_Control.read_base(message.chat.id, "users")
        user_id = user_list[0][0]
        lerned_list = Baze_Control.read_base(user_id, 'lerned')

        if len(lerned_list) < user_answ:
            bot.send_message(
                f"йо, либо у меня, либо у тебя проблеммы, скорее всего у меня, проверь не сильно ли большой айдишник ввёл?")
            print(lerned_list, len(lerned_list), user_answ)

        Baze_Control.remove(user_answ, "lerned")

        bot.send_message(message.chat.id,
                         f'Запись:\n {lerned_list[user_answ]} \n \n успешно удалена', reply_markup=markup)
    except:
        bot.send_message(message.chat.id,
                         "Упс, выпала ошибка, возможно вы ввели цифру а не букву, повторите ввод(не вводить нельзя, я ещё не прописал)")
        bot.register_next_step_handler(message, add_archive1)


def del_archive1(message):
    user_answ = message.text
    if user_answ == "/exit":
        return 0
    try:
        user_answ = int(user_answ)
        markup = types.ReplyKeyboardRemove()

        user_list = Baze_Control.read_base(message.chat.id, "users")
        user_id = user_list[0][0]
        archive_list = Baze_Control.read_base(user_id, 'archive')

        if len(archive_list) < user_answ:
            bot.send_message(
                f"йо, либо у меня, либо у тебя проблеммы, скорее всего у меня, проверь не сильно ли большой айдишник ввёл?")
            print(archive_list, len(archive_list), user_answ)

        Baze_Control.remove(user_answ, "archive")

        bot.send_message(message.chat.id,
                         f'Запись:\n {archive_list[user_answ]} \n \n успешно удалена', reply_markup=markup)
    except:
        bot.send_message(message.chat.id,
                         "Упс, выпала ошибка, возможно вы ввели цифру а не букву, повторите ввод(не вводить нельзя, я ещё не прописал)")
        bot.register_next_step_handler(message, add_archive1)


def add_archive1(message):
    user_answ = message.text
    if user_answ == "/exit":
        return 0
    try:
        user_answ = int(user_answ)
        markup = types.ReplyKeyboardRemove()

        user_list = Baze_Control.read_base(message.chat.id, "users")
        user_id = user_list[0][0]
        lern_list = Baze_Control.read_base(user_id, 'lern')

        if len(lern_list) < user_answ:
            bot.send_message(
                f"йо, либо у меня, либо у тебя проблеммы, скорее всего у меня, проверь не сильно ли большой айдишник ввёл?")
            print(lern_list, len(lern_list), user_answ)

        Baze_Control.add_archive(message.chat.id, user_answ)
        bot.send_message(message.chat.id,
                         f'Запись:\n {lern_list[user_answ]} \n \n успешно добавлена(если что из списка изучения она ушла)\nЕсли хотите добавить любую запись(если хотите добавить эту же, то просто напишитет этот же id), в избраное нажмите на кнопку',
                         reply_markup=markup)
        # бля, хочу спать, не могу думать, потом додумай как побороться с проблемой передачи именно этой записи(аозможно стои боту читать чат, и тип смотреть на предыдущее предложение(да не мой вариант, потом обязательно поправишь)

    except:
        bot.send_message(message.chat.id,
                         "Упс, выпала ошибка, возможно вы ввели цифру а не букву, повторите ввод(не вводить нельзя, я ещё не прописал)")
        bot.register_next_step_handler(message, add_archive1)


def add_lerned1(message):
    user_answ = message.text
    if user_answ == "/exit":
        return 0
    try:
        user_answ = int(user_answ)
        markup = types.ReplyKeyboardRemove()

        '''
        user_list = Baze_Control.read_base(message.chat.id, 'users')
        print("User_list from:add_lerned1: ", user_list)
        if len(user_list) != 1:
            bot.send_message(message.chat.id,
                             "Сори, тут проблемка у на стороне базы, почему-то 2 человека имеют такой же id, я хз почему так, но поправлю когда увижу")
            return
        user_id = user_list[0][0]  # тут может быть ошибка
        '''

        user_list = Baze_Control.read_base(message.chat.id, "users")
        user_id = user_list[0][0]
        lern_list = Baze_Control.read_base(user_id, 'lern')

        if len(lern_list) < user_answ:
            bot.send_message(
                f"йо, либо у меня, либо у тебя проблеммы, скорее всего у меня, проверь не сильно ли большой айдишник ввёл?")
            print(lern_list, len(lern_list), user_answ)

        Baze_Control.add_lerned(message.chat.id, user_answ)
        # Baze_Control.remove(user_answ, "lern") ## именно отсюда не работает
        bot.send_message(message.chat.id,
                         f'Запись:\n {lern_list[user_answ]} \n \n успешно добавлена(если что из списка изучения она не ушла)',
                         reply_markup=markup)  # а теперь правда, НИХРЕНА там не ушло, я ещё ничего не написал чтобы убиралось
        # бля, хочу спать, не могу думать, потом додумай как побороться с проблемой передачи именно этой записи(аозможно стои боту читать чат, и тип смотреть на предыдущее предложение(да не мой вариант, потом обязательно поправишь)
    # добавь удаление
    # дать пользователю перенести запись в избраное
    except:
        bot.send_message(message.chat.id,
                         "Упс, выпала ошибка, возможно вы ввели цифру а не букву, повторите ввод(не вводить нельзя, я ещё не прописал)")
        bot.register_next_step_handler(message, add_lerned1)


def add_mat1(message):
    global matereal
    matereal = message.text
    if matereal == "/exit":
        return 0
    print(f'matereal: {matereal}')
    bot.send_message(message.chat.id,
                     "Введите тип материала к которому будет определён эта запись(впринципе не важно что напишите, но в будующем, а может и сейчас уже есть (а я забыл изменить этот текст🤡) сортировка по типам)")
    bot.register_next_step_handler(message, add_mat2)


def add_mat2(message):
    global type_mat
    type_mat = message.text
    if type_mat == "/exit":
        return 0
    print(f'type_mat: {type_mat}')
    bot.send_message(message.chat.id,
                     "И наконец введите так сказать прогресс вашего изучение(Число от 0 до 100, где 100 материал изучен, и должен запуститься тймер для напоминания вас о том что следует перечитать материал, а 0 это ещё не начатое изучение, и секундомер времени изучения ещё не запущен)")
    bot.register_next_step_handler(message, add_mat3)


def add_mat3(message):
    global matereal, type_mat, progress_mat
    progress_mat = message.text
    if progress_mat == "/exit":
        return 0
    print(f'progress_mat: {progress_mat}')
    try:
        int(progress_mat)
        if progress_mat == 0:
            bot.send_message(message.chat.id,
                             f"Прогресс = 0 означает то что вы ещё не начали изучение. и МиНуТоМеР ещё не запущен, если вы ошиблись написав (0), то пересоздайте запись путём /del удаалив запись, и /add (мне пока лень добавлять изменение через 1 команду))) )")
        if progress_mat == 100:
            bot.send_message(f"Проресс равный 100, означает что вы уже изучили материал, и он добавился в <Изученое>")

        Baze_Control.add_lern(message.chat.id, type_mat, matereal, progress_mat)
        bot.send_message(message.chat.id,
                         "ура, запись создана")  # , вы можете изменить её в ЛЮБОЙ МОМЕНТ, к слову если начнёте учить либо продвинитесь в изучении лучше измините(это можно сделать при помщи команды /change)") ## сделать изменение записи
    except:
        bot.send_message(message.chat.id,
                         "оу я вижу что вы ввели не только цифры(а может цифорок и нет), прогресс это ЦИФРА от 0 до 100")
        bot.register_next_step_handler(message, add_mat3)


bot.polling(none_stop=True)
