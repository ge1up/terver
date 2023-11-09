import telebot
from telebot import types
import re

bot = telebot.TeleBot('6864893866:AAHIuEg9dIpG3vflatljRXouAu6iCFY6wBs')


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup()
    btn1 = types.KeyboardButton('Урновая модель')
    btn2 = types.KeyboardButton('Формулы комбинаторики')
    markup.add(btn1)
    markup.add(btn2)
    bot.send_message(message.chat.id, 'Здравствуйте! Что пожелаете?', reply_markup=markup)
    bot.register_next_step_handler(message, begin)


def begin(message):
    if message.text == 'Урновая модель':
        markup = types.ReplyKeyboardRemove()
        bot.send_message(message.chat.id,
                         'Имеются n предметов, среди которых m меченых. Необходимо умение решать два типа задач:',
                         reply_markup=markup)
        bot.send_message(message.chat.id,
                         'а) Наугад извлекаются k предметов (k < m). Найти вероятность того, что все '
                         'извлеченные предметы окажутся мечеными...',
                         reply_markup=markup)
        bot.send_message(message.chat.id,
                         'б) Наугад извлекаются k предметов (k < m). Найти вероятность того, что среди '
                         'извлеченных предметов окажутся r меченых',
                         reply_markup=markup)

        markup = types.ReplyKeyboardMarkup()
        btn1 = types.KeyboardButton('Задача а)')
        btn2 = types.KeyboardButton('Задача б)')
        markup.add(btn1)
        markup.add(btn2)
        bot.send_message(message.chat.id, 'Какая у вас задача?', reply_markup=markup)
        bot.register_next_step_handler(message, model)
    elif message.text == 'Формулы комбинаторики':
        markup = types.ReplyKeyboardMarkup()
        btn1 = types.KeyboardButton('C повторениями!')
        btn2 = types.KeyboardButton('Без повторений!')
        markup.add(btn1)
        markup.add(btn2)
        bot.send_message(message.chat.id, 'Все понял, а что насчет повторений?', reply_markup=markup)
        bot.register_next_step_handler(message, repeats)
    else:
        markup = types.ReplyKeyboardRemove()
        bot.send_message(message.chat.id, 'Ой, что-то пошло не так, давайте попробуем еще раз!', reply_markup=markup)
        start(message)


def model(message):
    if message.text == 'Задача а)':
        markup = types.ReplyKeyboardRemove()
        bot.send_message(message.chat.id, 'Введите число n...', reply_markup=markup)
        bot.register_next_step_handler(message, read_n, 'A')
    elif message.text == 'Задача б)':
        markup = types.ReplyKeyboardRemove()
        bot.send_message(message.chat.id, 'Введите число n...', reply_markup=markup)
        bot.register_next_step_handler(message, read_n, 'B')
    else:
        markup = types.ReplyKeyboardRemove()
        bot.send_message(message.chat.id, 'Ой, что-то пошло не так, давайте попробуем еще раз!', reply_markup=markup)
        start(message)


def read_n(message, c):
    if re.match(r'^[1-9]\d*$', message.text):
        bot.send_message(message.chat.id, 'Введите число m...')
        bot.register_next_step_handler(message, read_m, int(message.text), c)
    else:
        bot.send_message(message.chat.id, 'Ой, что-то пошло не так, давайте попробуем еще раз!')
        start(message)


def read_m(message, n, c):
    if re.match(r'^[1-9]\d*$', message.text):
        bot.send_message(message.chat.id, 'Введите число k...')
        bot.register_next_step_handler(message, read_k, n, int(message.text), c)
    else:
        bot.send_message(message.chat.id, 'Ой, что-то пошло не так, давайте попробуем еще раз!')
        start(message)


def read_k(message, n, m, c):
    if re.match(r'^[1-9]\d*$', message.text):
        if c == 'A':
            calculation_a(message, n, m, int(message.text))
        else:
            bot.send_message(message.chat.id, 'Введите число r...')
            bot.register_next_step_handler(message, read_r, n, m, int(message.text))
    else:
        bot.send_message(message.chat.id, 'Ой, что-то пошло не так, давайте попробуем еще раз!')
        start(message)


def read_r(message, n, m, k):
    if re.match(r'^[1-9]\d*$', message.text):
        calculation_b(message, n, m, k, int(message.text))
    else:
        bot.send_message(message.chat.id, 'Ой, что-то пошло не так, давайте попробуем еще раз!')
        start(message)


def calculation_a(message, n, m, k):
    markup = types.ReplyKeyboardMarkup()
    btn1 = types.KeyboardButton('/start')
    markup.add(btn1)
    try:
        c1 = factorial(m)
        c1 /= factorial(k)
        c1 /= factorial(m - k)
        c2 = factorial(n)
        c2 /= factorial(k)
        c2 /= factorial(n - k)
        ans = c1 / c2
        bot.send_message(message.chat.id, f'Ваш ответ: {round(ans, 6)}!', reply_markup=markup)
    except:
        markup = types.ReplyKeyboardRemove()
        bot.send_message(message.chat.id, 'Ой, что-то пошло не так, давайте попробуем еще раз!', reply_markup=markup)
        start(message)

def calculation_b(message, n, m, k, r):
    markup = types.ReplyKeyboardMarkup()
    btn1 = types.KeyboardButton('/start')
    markup.add(btn1)
    try:
        c1 = factorial(m)
        c1 /= factorial(r)
        c1 /= factorial(m - r)
        c2 = factorial(n - m)
        c2 /= factorial(k - r)
        c2 /= factorial(n - m - k + r)
        ans = c1 * c2
        c3 = factorial(n)
        c3 /= factorial(k)
        c3 /= factorial(n - k)
        ans /= c3
        bot.send_message(message.chat.id, f'Ваш ответ: {round(ans, 6)}!', reply_markup=markup)
    except:
        markup = types.ReplyKeyboardRemove()
        bot.send_message(message.chat.id, 'Ой, что-то пошло не так, давайте попробуем еще раз!', reply_markup=markup)
        start(message)




def repeats(message):
    if message.text == 'C повторениями!':
        markup = types.ReplyKeyboardMarkup()
        btn1 = types.KeyboardButton('Размещения!')
        btn2 = types.KeyboardButton('Перестановки!')
        btn3 = types.KeyboardButton('Сочетания!')
        markup.add(btn1)
        markup.add(btn2)
        markup.add(btn3)
        bot.send_message(message.chat.id, 'Отлично, теперь выберите формулу...', reply_markup=markup)
        bot.register_next_step_handler(message, comb_repetitions_reading)
    elif message.text == 'Без повторений!':
        markup = types.ReplyKeyboardMarkup()
        btn1 = types.KeyboardButton('Размещения!')
        btn2 = types.KeyboardButton('Перестановки!')
        btn3 = types.KeyboardButton('Сочетания!')
        markup.add(btn1)
        markup.add(btn2)
        markup.add(btn3)
        bot.send_message(message.chat.id, 'Отлично, теперь выберите формулу...', reply_markup=markup)
        bot.register_next_step_handler(message, comb_no_repetitions_reading)
    else:
        markup = types.ReplyKeyboardRemove()
        bot.send_message(message.chat.id, 'Ой, что-то пошло не так, давайте попробуем еще раз!', reply_markup=markup)
        start(message)


def comb_repetitions_reading(message):
    formula = message.text
    if formula != 'Размещения!' and formula != 'Перестановки!' and formula != 'Сочетания!':
        markup = types.ReplyKeyboardRemove()
        bot.send_message(message.chat.id, 'Ой, что-то пошло не так, давайте попробуем еще раз!', reply_markup=markup)
        start(message)
    markup = types.ReplyKeyboardRemove()
    if formula == 'Перестановки!':
        bot.send_message(message.chat.id, 'Введите число k...', reply_markup=markup)
        list = []
        bot.register_next_step_handler(message, k_set_reading, 0, list, 0, 0)
    else:
        flag = True
        bot.send_message(message.chat.id, 'Введите число n...', reply_markup=markup)
        bot.register_next_step_handler(message, n_reading, formula, flag)


def comb_no_repetitions_reading(message):
    formula = message.text
    if formula != 'Размещения!' and formula != 'Перестановки!' and formula != 'Сочетания!':
        markup = types.ReplyKeyboardRemove()
        bot.send_message(message.chat.id, 'Ой, что-то пошло не так, давайте попробуем еще раз!', reply_markup=markup)
        start(message)
    markup = types.ReplyKeyboardRemove()
    bot.send_message(message.chat.id, 'Введите число n...', reply_markup=markup)
    flag = False
    if formula == 'Перестановки!':
        bot.register_next_step_handler(message, only_n_reading, formula)
    else:
        bot.register_next_step_handler(message, n_reading, formula, flag)


def only_n_reading(message, formula):
    if re.match(r'^[1-9]\d*$', message.text):
        no_repetition_permutations(message, int(message.text))
    else:
        bot.send_message(message.chat.id, 'Ой, что-то пошло не так, давайте попробуем еще раз!')
        start(message)


def n_reading(message, formula, flag):
    if re.match(r'^[1-9]\d*$', message.text):
        bot.send_message(message.chat.id, 'Введите число k...')
        bot.register_next_step_handler(message, k_reading, formula, flag, int(message.text))
    else:
        bot.send_message(message.chat.id, 'Ой, что-то пошло не так, давайте попробуем еще раз!')
        start(message)


def k_reading(message, formula, flag, n):
    if re.match(r'^[1-9]\d*$', message.text):
        repetition_calculations(message, formula, flag, n, int(message.text))
    else:
        bot.send_message(message.chat.id, 'Ой, что-то пошло не так, давайте попробуем еще раз!')
        start(message)


def k_set_reading(message, k, list, i, n):
    if re.match(r'^[1-9]\d*$', message.text):
        if k == 0:
            k = int(message.text)
        else:
            n += int(message.text)
            list.append(int(message.text))
        if i < k:
            bot.send_message(message.chat.id, f'Введите число k{i + 1}...')
            bot.register_next_step_handler(message, k_set_reading, k, list, i + 1, n)
        else:
            repetition_permutations(message, list, n)
    else:
        bot.send_message(message.chat.id, 'Ой, что-то пошло не так, давайте попробуем еще раз!')
        start(message)


def repetition_calculations(message, formula, flag, n, k):
    if flag == False:
        if formula == 'Размещения!':
            no_repetition_placements(message, n, k)
        else:
            no_repetition_combinations(message, n, k)
    else:
        if formula == 'Размещения!':
            repetition_placements(message, n, k)
        else:
            no_repetition_combinations(message, n + k - 1, k);


def repetition_placements(message, n, k):
    markup = types.ReplyKeyboardMarkup()
    btn1 = types.KeyboardButton('/start')
    markup.add(btn1)
    ans = 1
    try:
        ans = pow(n, k)
        bot.send_message(message.chat.id, f'Ваш ответ: {ans}!', reply_markup=markup)
    except:
        markup = types.ReplyKeyboardRemove()
        bot.send_message(message.chat.id, 'Ой, что-то пошло не так, давайте попробуем еще раз!', reply_markup=markup)
        start(message)


def repetition_permutations(message, list, n):
    markup = types.ReplyKeyboardMarkup()
    btn1 = types.KeyboardButton('/start')
    markup.add(btn1)
    ans = 1
    try:
        ans = factorial(n)
        for i in list:
            ans /= factorial(i)
        bot.send_message(message.chat.id, f'Ваш ответ: {ans}!', reply_markup=markup)
    except:
        markup = types.ReplyKeyboardRemove()
        bot.send_message(message.chat.id, 'Ой, что-то пошло не так, давайте попробуем еще раз!', reply_markup=markup)
        start(message)


def repetition_combinations(message, n, k):
    markup = types.ReplyKeyboardMarkup()
    btn1 = types.KeyboardButton('/start')
    markup.add(btn1)
    ans = 1
    try:
        ans = factorial(n)

        bot.send_message(message.chat.id, f'Ваш ответ: {ans}', reply_markup=markup)
    except:
        markup = types.ReplyKeyboardRemove()
        bot.send_message(message.chat.id, 'Ой, что-то пошло не так, давайте попробуем еще раз!', reply_markup=markup)
        start(message)


def no_repetition_placements(message, n, k):
    markup = types.ReplyKeyboardMarkup()
    btn1 = types.KeyboardButton('/start')
    markup.add(btn1)
    ans = 1
    try:
        ans = factorial(n)
        nk_factorial = factorial(n - k)
        ans /= nk_factorial
        bot.send_message(message.chat.id, f'Ваш ответ: {int(ans)}', reply_markup=markup)
    except:
        markup = types.ReplyKeyboardRemove()
        bot.send_message(message.chat.id, 'Ой, что-то пошло не так, давайте попробуем еще раз!', reply_markup=markup)
        start(message)


def no_repetition_permutations(message, n):
    markup = types.ReplyKeyboardMarkup()
    btn1 = types.KeyboardButton('/start')
    markup.add(btn1)
    ans = 1
    try:
        ans = factorial(n)
        bot.send_message(message.chat.id, f'Ваш ответ: {ans}', reply_markup=markup)
    except:
        markup = types.ReplyKeyboardRemove()
        bot.send_message(message.chat.id, 'Ой, что-то пошло не так, давайте попробуем еще раз!', reply_markup=markup)
        start(message)


def no_repetition_combinations(message, n, k):
    markup = types.ReplyKeyboardMarkup()
    btn1 = types.KeyboardButton('/start')
    markup.add(btn1)
    ans = 1
    try:
        ans = factorial(n)
        nk_factorial = factorial(n - k)
        ans /= nk_factorial
        ans /= factorial(k)
        bot.send_message(message.chat.id, f'Ваш ответ: {int(ans)}', reply_markup=markup)
    except:
        markup = types.ReplyKeyboardRemove()
        bot.send_message(message.chat.id, 'Ой, что-то пошло не так, давайте попробуем еще раз!', reply_markup=markup)
        start(message)


def factorial(n):
    if n == 0:
        return 1
    else:
        result = 1
        for i in range(1, n + 1):
            result *= i
        return result


bot.polling(none_stop=True)
