from telegram import Bot, Update, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup, ParseMode
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, CallbackQueryHandler
from bd.connect2 import *
from bd.connect import *
from get_rasp import get_rasp

TOKEN = "1017501436:AAFu6rvpQFrXNdXQXSMWTDlteJmc_ft6hf4"

NAME, SURNAME, OTCHESTVO, GROUP = range(4)
LESSON, TEACHER = range(2)
VAR = range(1)


def start(bot: Bot, update: Update):
    chat_id = update.message.chat_id
    auth_user = check_user(chat_id)
    if auth_user:
        auth_user_name = auth_user[0][1]
        auth_user_surname = auth_user[0][2]
        auth_user_otchestvo = auth_user[0][3]
        auth_fullname = auth_user_surname + " " + auth_user_name + " " + auth_user_otchestvo
        bot.send_message(
            chat_id=update.message.chat_id,
            text="Здравствуй! \n" + auth_fullname
        )
    else:
        bot.send_message(
            chat_id=update.message.chat_id,
            text="Привет! Здесь ты сможешь узнать о своих задолжностях по учебе. "
                 "Для того чтобы начать, нажми /registration"
        )


def registration(bot: Bot, update: Update):
    chat_id = update.message.chat_id
    auth_user = check_user(chat_id)
    if not auth_user:
        # Спросить имя
        update.message.reply_text(
            "Введи свою фамилию",
            reply_markup=ReplyKeyboardRemove()
        )
        return NAME
    else:
        auth_user_name = auth_user[0][1]
        auth_user_surname = auth_user[0][2]
        auth_user_otchestvo = auth_user[0][3]
        auth_fullname = auth_user_surname + " " + auth_user_name + " " + auth_user_otchestvo
        update.message.reply_text(
            f'Вы уже зарегестрированны! \n Вы:{auth_fullname}'
        )
        return ConversationHandler.END


def name_handler(bot: Bot, update: Update, user_data: dict):
    # Получить имя
    user_data[NAME] = update.message.text
    update.message.reply_text(
        "Введи своё имя"
    )
    return SURNAME


def surname_handler(bot: Bot, update: Update, user_data: dict):
    user_data[SURNAME] = update.message.text
    print(user_data)

    update.message.reply_text(
        "Введи свою отчество"
    )
    return OTCHESTVO


def otchestvo_handler(bot: Bot, update: Update, user_data: dict):
    user_data[OTCHESTVO] = update.message.text
    update.message.reply_text(
        "Введи свою группу"
    )

    return GROUP


def finish_handler(bot: Bot, update: Update, user_data: dict):
    user_data[GROUP] = update.message.text

    chat_id = update.message.chat_id
    inp_name = user_data[NAME]
    inp_surname = user_data[SURNAME]
    inp_otchestvo = user_data[OTCHESTVO]
    inp_group = user_data[GROUP]
    add_user(chat_id, inp_name, inp_surname, inp_otchestvo, inp_group)

    update.message.reply_text(
        f'Вы успешно зарегестрированны! \n Вы:{user_data[SURNAME]} {user_data[NAME]} {user_data[OTCHESTVO]} '
        f'из группы {inp_group} '
    )

    return ConversationHandler.END


def cancel_handler(bot: Bot, update: Update):
    update.message.reply_text(
        "Отмена.Для того чтобы начать сначала нажмите /start")
    return ConversationHandler.END


def see_debts_in_paras(bot: Bot, update: Update):  # проверить сданные работы
    chat_id = update.message.chat_id
    auth_user = check_user(chat_id)
    if auth_user:  # Если пользователь найден
        user_group = auth_user[0][4]
        user_group_id = get_group_by_text(user_group)
        if user_group_id:
            user_id = get_student_id(auth_user[0][2], auth_user[0][1], auth_user[0][3], user_group_id)
            print(auth_user)
            print(auth_user[0][1] + " " + auth_user[0][2] + " " + auth_user[0][3] + " " + user_group)
            print("id student: " + str(user_id))
            if user_id:  # Если пользователь найден в студентах
                keyboard = []
                lessons = []
                for para in get_id_paras_by_group(user_group_id):
                    lesson = get_lesson_by_id_lesson(id_lesson_by_id_para(para))
                    print(lesson)
                    if lesson not in lessons and lesson is not None:
                        lessons.append(lesson)
                print(lessons)

                for i in lessons:
                    keyboard.append([InlineKeyboardButton(str(i), callback_data=str(i))])

                update.message.reply_text("Выберите предмет", reply_markup=InlineKeyboardMarkup(keyboard))
                return LESSON
            else:
                bot.send_message(
                    chat_id=chat_id,
                    text="Вы не найдены в списках студентов "
                )
                return ConversationHandler.END
        else:
            bot.send_message(
                chat_id=chat_id,
                text="Вы не найдены в списках студентов "
            )
            return ConversationHandler.END
    else:
        bot.send_message(
            chat_id=chat_id,
            text="Для начала зарегистрируйтесь! /registration"
        )
        return ConversationHandler.END


def lesson_handler(bot: Bot, update: Update, user_data: dict):
    chat_id = update.callback_query.message.chat.id
    auth_user = check_user(chat_id)

    query = update.callback_query
    selection = query.data

    bot.send_message(
        chat_id=chat_id,
        text="Предмет:" + selection
    )

    user_data['LESSON'] = get_lesson_by_text(selection)

    keyboard = []
    teachers = []

    user_group = auth_user[0][4]
    user_group_id = get_group_by_text(user_group)
    group_paras = get_id_paras_by_group(user_group_id)

    for teacher in get_teachers_by_lesson(user_data['LESSON']):  # все преподы по предмету
        teacher_paras = get_id_para_by_teacher(teacher, user_data['LESSON'])
        if teacher_paras in group_paras:  # если у препода есть пары в группе
            teachers.append(get_teacher_by_teacher_id(teacher))

    for i in teachers:
        keyboard.append([InlineKeyboardButton(str(i), callback_data=str(i))])

    update.effective_message.edit_text("Выберите преподавателя", reply_markup=InlineKeyboardMarkup(keyboard))
    return TEACHER


def teacher_handler(bot: Bot, update: Update, user_data: dict):
    query = update.callback_query
    selection = query.data
    teacher_FIO = selection.split(" ")

    bot.send_message(
        chat_id=update.callback_query.message.chat.id,
        text="Преподаватель:" + selection
    )

    print(teacher_FIO[0], teacher_FIO[1], teacher_FIO[2])
    print(get_teacher_id(teacher_FIO[0], teacher_FIO[1], teacher_FIO[2]))
    user_data['TEACHER'] = get_teacher_id(teacher_FIO[0], teacher_FIO[1], teacher_FIO[2])

    bot.delete_message(chat_id=update.callback_query.message.chat.id,
                       message_id=update.callback_query.message.message_id)

    chat_id = update.callback_query.message.chat.id
    auth_user = check_user(chat_id)
    user_name = auth_user[0][1]
    user_surname = auth_user[0][2]
    user_otchestvo = auth_user[0][3]
    user_group = auth_user[0][4]
    user_group_id = get_group_by_text(user_group)
    student_id = get_student_id(user_surname, user_name, user_otchestvo, user_group_id)
    print(user_data)
    changed_para = get_para(user_data['TEACHER'], user_data['LESSON'])  # Выбранная пара
    print(123)
    works_by_para = get_works_for_para_id(changed_para)  # Работы по выбранной паре
    works_id_by_para = get_works_id_for_para_id(changed_para)  # id работ по выбранной паре

    works = '<b style="text-align:center;">❗Работы❗</b>\n❗Название Работы | Тип работы❗\n'
    submitted_work = get_work_id_in_submitted_works(student_id)  # сданные работы
    print(submitted_work)
    for work, work_id in zip(works_by_para, works_id_by_para):
        if work_id in submitted_work:
            works = works + '\n✔' + str(work)
        else:
            works = works + '\n❌' + str(work)
    bot.send_message(
        chat_id=update.callback_query.message.chat.id,
        text=str(works),
        parse_mode='HTML'
    )

    return ConversationHandler.END


def rasp(bot: Bot, update: Update):
    print(1)
    chat_id = update.message.chat_id
    auth_user = check_user(chat_id)
    if auth_user:
        user_group = auth_user[0][4]
        print(user_group)
        rasp = get_rasp(user_group)
        print(rasp)
        if rasp:
            msg = ""
            j = {}
            for i in rasp:
                if j != {}:
                    if j['date'] != i['date']:
                        msg = msg + "\n\n" + "<b>Дата:</b>" + i['date'] + "\n" \
                              + "Пара:" + i['para'] + "\n" \
                              + "Преподаватель:" + i['teacher'] + "\n" \
                              + "Аудитория:" + i['auditory'] + "\n" \
                              + "Тип:" + i['para_type'] + "\n" \
                              + "№ Пары:" + str(i['num'])
                    else:
                        if j['para'] == i['para'] and j['teacher'] == i['teacher'] and j['para_type'] == i['para_type']:
                            msg = msg + " " + str(i['num'])
                        else:
                            msg = msg + "\n" \
                                  + "Пара:" + i['para'] + "\n" \
                                  + "Преподаватель:" + i['teacher'] + "\n" \
                                  + "Аудитория:" + i['auditory'] + "\n" \
                                  + "Тип:" + i['para_type'] + "\n" \
                                  + "№ Пары:" + str(i['num'])
                j = i

            bot.send_message(
                chat_id=chat_id,
                text=str(msg),
                parse_mode="HTML"

            )
        else:
            bot.send_message(
                chat_id=chat_id,
                text="Не найдено расписание",
            )
    else:
        bot.send_message(
            chat_id=chat_id,
            text="Для начала зарегистрируйтесь! /registration",
        )


def delete_profile(bot: Bot, update: Update):
    chat_id = update.message.chat_id
    print(chat_id)
    auth_user = check_user(chat_id)
    if auth_user:
        keyboard = [
            [InlineKeyboardButton("Да", callback_data="yes"), InlineKeyboardButton("Нет", callback_data="no")]
        ]

        update.message.reply_text("Действительно хотите удалить профиль?", reply_markup=InlineKeyboardMarkup(keyboard))
        return VAR
    else:
        update.message.reply_text("Для начала зарегистрируйтесь! /registration")
        return ConversationHandler.END


def var_handler(bot: Bot, update: Update, user_data: dict):
    user_data['VAR'] = update.callback_query.data
    if user_data['VAR'] == "yes":
        delete_user_by_user_id(update.callback_query.message.chat.id)
        update.effective_message.edit_text("Профиль удален!")
    else:
        update.effective_message.edit_text("Отменено!")
    return ConversationHandler.END


def main():
    bot = Bot(
        token=TOKEN,
        base_url="https://telegg.ru/orig/bot"
    )
    updater = Updater(
        bot=bot
    )

    conv_handler = ConversationHandler(
        entry_points=[
            CommandHandler("registration", callback=registration),
        ],
        states={
            NAME: [
                MessageHandler(Filters.all, callback=name_handler, pass_user_data=True)
            ],
            SURNAME: [
                MessageHandler(Filters.all, surname_handler, pass_user_data=True)
            ],
            OTCHESTVO: [
                MessageHandler(Filters.all, otchestvo_handler, pass_user_data=True)
            ],
            GROUP: [
                MessageHandler(Filters.all, finish_handler, pass_user_data=True)
            ]
        },
        fallbacks=[
            CommandHandler('cancel', cancel_handler)
        ]
    )

    see_debs = ConversationHandler(
        entry_points=[
            CommandHandler("see_debs", callback=see_debts_in_paras),
        ],
        states={
            LESSON: [
                CallbackQueryHandler(lesson_handler, pass_user_data=True)
            ],
            TEACHER: [
                CallbackQueryHandler(teacher_handler, pass_user_data=True)
            ]
        },
        fallbacks=[
            CommandHandler('cancel', cancel_handler)
        ]
    )

    dlt_profile = ConversationHandler(
        entry_points=[
            CommandHandler("delete_profile", callback=delete_profile),
        ],
        states={
            VAR: [
                CallbackQueryHandler(var_handler, pass_user_data=True)
            ]
        },
        fallbacks=[
            CommandHandler('cancel', cancel_handler)
        ]
    )
    start_handler = CommandHandler("start", start)
    rasp_handler = CommandHandler("get_rasp", rasp)

    updater.dispatcher.add_handler(start_handler)
    updater.dispatcher.add_handler(dlt_profile)
    updater.dispatcher.add_handler(see_debs)
    updater.dispatcher.add_handler(conv_handler)
    updater.dispatcher.add_handler(rasp_handler)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
