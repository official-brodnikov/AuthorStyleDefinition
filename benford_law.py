import os
import shutil
import nltk
import pymorphy2
import scipy.stats as stats

benford_values = [0.301, 0.176, 0.125, 0.097, 0.079, 0.067, 0.058, 0.051, 0.046]  # Распределение по закону Бенфорда
signs = ["!", ".", "..", "...", "?", ",", ";", ":",
                 "/", "(", ")", "[", "]", "#", "№", "*", "{", "}", "'"]

# Проанализировав с помощью pymorphy тексты был получен слудующий список начальных форм числительных
one = ["один", "единица", "полтора", "одиннадцать", "двенадцать", "тринадцать", "четырнадцать",
       "пятнадцать", "шестнадцать", "семнадцать", "восемнадцать", "девятнадцать",
       "сто", "тысяча", "миллион", "миллиард"]
two = ["два", "двадцать", "двести"]
three = ["три", "тридцать", "триста"]
four = ["четыре", "сорок", "четыреста"]
five = ["пять", "пятьдесят", "пятьсот"]
six = ["шесть", "шестьдесят", "шестьсот"]
seven = ["семь", "семьдесят", "семьсот"]
eight = ["восемь", "восемьдесят", "восемьсот"]
nine = ["девять", "девяносто", "девятьсот"]
numbers = ["один", "единица", "полтора", "одиннадцать", "двенадцать", "тринадцать", "четырнадцать",
           "пятнадцать", "шестнадцать", "семнадцать", "восемнадцать", "девятнадцать",
           "сто", "тысяча", "миллион", "миллиард", "два", "двадцать", "двести", "три",
           "тридцать", "триста", "четыре", "сорок", "четыреста",
           "пять", "пятьдесят", "пятьсот", "шесть", "шестьдесят",
           "шестьсот", "семь", "семьдесят", "семьсот",
           "восемь", "восемьдесят", "восемьсот", "девять", "девяносто", "девятьсот"]


class BenfordLaw(object):
    alpha = 0.05
    """Конструктор"""
    def __init__(self):
        return

    """Изменить значение alpha"""
    def change_alpha(self, alpha):
        self.alpha = alpha

    """Определение цифры из word, возвращаем индекс в списке частот"""
    def number_definition(self, word):
        if word in one:
            return 0
        elif word in two:
            return 1
        elif word in three:
            return 2
        elif word in four:
            return 3
        elif word in five:
            return 4
        elif word in six:
            return 5
        elif word in seven:
            return 6
        elif word in eight:
            return 7
        elif word in nine:
            return 8

    """Формирование отклонений 1-ых значащих цифр для text"""
    def list_building_deviations(self, text):
        wtokens = nltk.word_tokenize(text)  # Токенизируем текст
        tfreq = nltk.FreqDist(wtokens)  # Создаем словарь для токенов
        morph = pymorphy2.MorphAnalyzer()
        wtokens_nosym = [t for t in wtokens if t.isalnum() or t in signs]  # Удаляем ненужные символы
        is_numb = False  # Метка для составных числительных
        count_numbers = 0  # Количество чисел в тексте
        freq_numbers = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]  # Список частот первой значащей цифры в тексте
        # Проверяем каждое слово на принадлежность к словарю
        for wtoken in wtokens_nosym:
            morph_word = morph.parse(wtoken)[0].normal_form
            if morph_word in numbers:
                # Проверяем, что первая значащая цифра
                if not is_numb:
                    is_numb = True
                    count_numbers += 1
                    freq_numbers[self.number_definition(morph_word)] += 1
            else:
                # Меняем метку, т.к. не составное числительное
                is_numb = False
                # Если цифра, то тоже добавляем
                if wtoken.isdigit():
                    count_numbers += 1
                    index =  wtoken[0]
                    freq_numbers[int(index) - 1] += 1

        # Вычисляем отклонения для каждой цифры
        for i in range(len(freq_numbers)):
            if count_numbers > 0:
                freq_numbers[i] = abs((freq_numbers[i] / count_numbers) - benford_values[i])
        return  freq_numbers

    """Удаление автора модели"""
    def delete_author(self, author_name):
        directory = "Benford"
        # Если нет папки, то создаем
        if not os.path.exists(directory):
            print("  Автора {} не существует для метода Бенфорда".format(author_name))
            return

        directory = directory + "/" + author_name
        # Если нет папки, то создаем
        if not os.path.exists(directory):
            print("  Автора {} не существует для метода Бенфорда".format(author_name))
            return
        # Рекурсивно удаляем все эталонные тексты для автора
        shutil.rmtree(directory)

        print("  Автор {} успешно удален для метода Бенфорда".format(author_name))

    """Добавление эталонного text к автору author_name"""
    def add_reference_text(self, text, author_name, text_name):
        freq_numbers = self.list_building_deviations(text)  # Формируем отклонения для text
        directory = "Benford"
        # Если нет папки, то создаем
        if not os.path.exists(directory):
            os.makedirs(directory)

        directory = directory + "/" + author_name
        # Если нет папки, то создаем
        if not os.path.exists(directory):
            os.makedirs(directory)
        file_path = directory + "/" + text_name + ".txt"
        # Записываем отклонения в файл
        fp = open(file_path, 'w+', encoding='utf-8')
        for freq_number in freq_numbers:
            fp.write(str(freq_number) + "\n")
        fp.close()
        print("  Метод, основанный на законе Бенфорда успешно выполнен")

    """Вычисление значения критерия Манна-Уитни"""
    def calculating_mannwhitney(self, a, b):
        stat, p = stats.mannwhitneyu(a, b)
        return p

    """Предсказание автора для text"""
    def identify_author(self, text):
        min_mannwhitney  = 0.0  # Наибольшее значение критерия Манна-Уитни
        probable_author = ""  # Наиболее вероятный автор
        freq_numbers = self.list_building_deviations(text)  # Формируем отклонения для text
        directory = "Benford"  # Каталог с отклонениями
        # Проверяем есть ли эталонные тексты
        if not os.path.exists(directory):
            print("Модель не обучена, предсказание невозможно")
            return ""
        else:
            for author in os.listdir(directory):
                mannwhitney = 1.0  # Максимальный коэффициент Манна-Уитни для автора
                i = 0  # Счетчик текстов для автора
                for reference_text in os.listdir(directory + "/" + author):
                    reference_freq_numbers = []  # Список n-грамм эталонного текста
                    file_path = directory + "/" + author + "/" + reference_text
                    fp = open(file_path, encoding='utf-8')
                    for freq_number in fp.readlines():
                        reference_freq_numbers.append(float(freq_number))
                    mannwhitney *= self.calculating_mannwhitney(freq_numbers, reference_freq_numbers) - self.alpha
                    i += 1
                # Обновляем наиболее вероятного автора, если необходимо
                if min_mannwhitney < mannwhitney:
                    min_mannwhitney = mannwhitney
                    probable_author = author
        return probable_author

    """Предсказание автора, с помощью считывания отклонений из файла"""
    def identify_author_by_ngrams_from_file(self, text_name, author_name, reference_texts_list, authors_list):
        min_mannwhitney = 0.0  # Наибольшее значение критерия Манна-Уитни
        probable_author = ""  # Наиболее вероятный автор
        # Формируем отклонения для text, считывая из файла
        directory = "BankBenford"  # Каталог с эталонными текстами
        file_path = directory + "/" + author_name + "/" + text_name
        fp = open(file_path, encoding='utf-8')
        freq_numbers = []
        for count_ngram in fp.readlines():
            freq_numbers.append(float(count_ngram))
        fp.close()
        for author in os.listdir(directory):
            if author in authors_list:
                mannwhitney = 1.0  # Максимальный коэффициент Манна-Уитни для автора
                lis_deviations = []
                i = 0  # Счетчик текстов для автора
                for reference_text in os.listdir(directory + "/" + author):
                    if reference_text in reference_texts_list:
                        reference_freq_numbers = []  # Список n-грамм эталонного текста
                        file_path = directory + "/" + author + "/" + reference_text
                        fp = open(file_path, encoding='utf-8')
                        for freq_number in fp.readlines():
                            reference_freq_numbers.append(float(freq_number))
                        mannwhitney *= self.calculating_mannwhitney(freq_numbers, reference_freq_numbers) - self.alpha
                        lis_deviations.append(mannwhitney)
                # Обновляем наиболее вероятного автора, если необходимо
                if min_mannwhitney < mannwhitney:
                    min_mannwhitney = mannwhitney
                    probable_author = author
                i += 1

        return probable_author