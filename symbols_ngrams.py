import os
import nltk
import re

signs = ["'", " ", "(", ")", ","]
alphabet = ["а", "б", "в", "г", "д", "е", "ё", "ж", "з", "и", "й",
            "к", "л", "м", "н", "о", "п", "р", "с", "т", "у", "ф",
            "х", "ц", "ч", "ш", "щ", "ъ", "ы", "ь", "э", "ю", "я",
            "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k",
            "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v",
            "w", "x", "y", "z"]


class SymbolsNgrams(object):
    ngrams_list = []  # Список n-грамм
    count_ngrams_list = []  # Частоты n-грамм
    """Конструктор, n - размер n-граммы"""
    def __init__(self, n):
        self.n = n
        self.calculation_ngrams_list()

    """Очищение списка частот"""
    def clear_counts(self):
        for i in range(len(self.count_ngrams_list)):
            self.count_ngrams_list[i] = 0.0

    """Формируем список n-грамм"""
    def calculation_ngrams_list(self):
        if self.n == 2:
            for symb1 in alphabet:
                for symb2 in alphabet:
                    self.ngrams_list.append(symb1 + symb2)
                    self.count_ngrams_list.append(0.0)
        elif self.n == 3:
            for symb1 in alphabet:
                for symb2 in alphabet:
                    for symb3 in alphabet:
                        self.ngrams_list.append(symb1 + symb2 + symb3)
                        self.count_ngrams_list.append(0.0)
        elif self.n == 4:
            for symb1 in alphabet:
                for symb2 in alphabet:
                    for symb3 in alphabet:
                        for symb4 in alphabet:
                            self.ngrams_list.append(symb1 + symb2 + symb3 + symb4)
                            self.count_ngrams_list.append(0.0)

    """Изменить размер n-граммы символов на n"""
    def change_n(self, n):
        self.n = n
        self.count_ngrams_list.clear()
        self.ngrams_list.clear()
        self.calculation_ngrams_list()

    """Формирование частот n-грамм символов для text"""
    def list_building_ngrams(self, text):
        n = self.n
        # Число слов в тексте
        count_words = len([word for word in nltk.wordpunct_tokenize(text) if word.isalpha() or word == " "])
        # Очищаем текст
        text = [word for word in text if word.isalpha() or word == " "]
        # Создаем n-граммы
        if n == 2:
            grams = nltk.collocations.BigramCollocationFinder.from_words(text)
        elif n == 3:
            grams = nltk.collocations.TrigramCollocationFinder.from_words(text)
        # Подсчитываем частоты
        for gram, freq in grams.ngram_fd.items():
            # Отбрасываем лишние n-граммы
            if ' ' not in gram:
                # Очищаем строку
                st = re.sub(r"[( ),']", "", str(gram))
                # Вычисляем частоту
                if st in self.ngrams_list:
                    self.count_ngrams_list[self.ngrams_list.index(st)] = float("{0:.6f}".format(freq / count_words))

    """Удаление автора из модели"""
    def delete_author(self, author_name):
        for n in range(2, 4):
            directory = "{}-gramsOfSymbols".format(n)
            if not os.path.exists(directory):
                return

            directory = directory + "/" + author_name + ".txt"
            try:
                fp = open(directory)
                fp.close()
                # Удаляем все данные для автора
                os.remove(directory)
            except IOError:
                print("  Автора {} не существует для метода ПФР {}-грамм".format(author_name, n))
                return
        print("  Автор {} успешно удален для метода ПФР n-грамм символов".format(author_name))

    """Добавление эталонного text с названием text_name к автору author_name"""
    def add_reference_text(self, text, author_name):
        n = self.n
        # Формируем n-граммы символов и их частоты для text
        self.list_building_ngrams(text)
        directory = str(n) + "-gramsOfSymbols"  # Каталог со средними ПФР для author_name
        # Если нет папки, то создаем
        if not os.path.exists(directory):
            os.makedirs(directory)
        # Записываем n-граммы и их значения в файл
        file_path = directory + "/" + author_name + ".txt"
        try:
            fp = open(file_path, encoding='utf-8')
            # Считываем средние значения для автора и пересчитываем их
            average_counts = []
            i = 0
            for line in fp.readlines():
                average_counts.append(float("{0:.6f}".format((float(line) + self.count_ngrams_list[i]) / 2)))
                self.count_ngrams_list[i] = 0.0
                i += 1
            fp.close()
            # Перезаписываем средневзвешенную ПФР в файл
            fp = open(file_path, 'w', encoding='utf-8')
            for average_count in average_counts:
                fp.write(str(average_count) + "\n")
        except IOError:
            # Если нет автора, создаем файл для него
            fp = open(file_path, 'w+', encoding='utf-8')
            # Записываем частоты n-грамм
            for i in range(len(self.count_ngrams_list)):
                fp.write(str(self.count_ngrams_list[i]) + "\n")
                self.count_ngrams_list[i] = 0.0

        fp.close()
        print("  Метод, основанный на {}-граммах символов успешно выполнен".format(str(n)))

    """Предсказание автора для text"""
    def identify_author(self, text):
        n = self.n
        min_deviation = 1000.0  # Наименьшее отклонение
        probable_author = ""  # Наиболее вероятный автор
        self.list_building_ngrams(text)  # Формируем n-граммы слов для text
        directory = str(n) + "-gramsOfSymbols"  # Каталог с эталонными текстами
        # Проверяем есть ли эталонные тексты
        if not os.path.exists(directory):
            print("Модель не обучена, предсказание невозможно")
            return ""
        else:
            # Проходим по всем авторам и ищем наименьшее расстояние со средневзвешенной ПФР
            for author in os.listdir(directory):
                i = 0  # Счетчик
                deviation = 0  # Среднее отклонение для автора
                file_path = directory + "/" + author
                fp = open(file_path, encoding='utf-8')
                for count_ngram in fp.readlines():
                    deviation += abs(float(count_ngram) - self.count_ngrams_list[i])
                    i += 1
                # Обновляем наиболее вероятного автора, если необоходимо
                if min_deviation > deviation:
                    min_deviation = deviation
                    probable_author = author.replace(".txt", "")
            self.clear_counts()
            return probable_author

    """Предсказание автора, считывая частоты из файла"""
    def identify_author_by_ngrams_from_file(self, text, path):
        n = self.n
        min_deviation = 1000.0  # Наименьшее отклонение
        probable_author = ""  # Наиболее вероятный автор
        i = 0
        # Формируем n-граммы слов для text, считывая из файла
        fp = open(path, encoding='utf-8')
        for count_ngram in fp.readlines():
            self.count_ngrams_list[i] = float(count_ngram)
            i += 1
        fp.close()
        directory = str(n) + "-gramsOfSymbols"  # Каталог с эталонными текстами
        # Проверяем есть ли эталонные тексты
        if not os.path.exists(directory):
            print("Модель не обучена, предсказание невозможно")
            return ""
        else:
            # Проходим по всем авторам и ищем наименьшее расстояние со средневзвешенной ПФР
            for author in os.listdir(directory):
                i = 0  # Счетчик
                deviation = 0  # Среднее отклонение для автора
                file_path = directory + "/" + author
                fp = open(file_path, encoding='utf-8')
                for count_ngram in fp.readlines():
                    deviation += abs(float(count_ngram) - self.count_ngrams_list[i])
                    i += 1
                # Обновляем наиболее вероятного автора, если необоходимо
                if min_deviation > deviation:
                    min_deviation = deviation
                    probable_author = author.replace(".txt", "")
            self.clear_counts()
            return probable_author

    """Добавление эталонного text с названием text_name к автору author_name, считывая частоты из файла"""
    def add_reference_text_by_ngrams_from_file(self, author_name, path):
        n = self.n
        i = 0
        # Формируем n-граммы символов и их частоты для text, считывая из файла
        fp = open(path, encoding='utf-8')
        for count_ngram in fp.readlines():
            self.count_ngrams_list[i] = float(count_ngram)
            i += 1
        fp.close()
        directory = str(n) + "-gramsOfSymbols"  # Каталог со средними ПФР для author_name
        # Если нет папки, то создаем
        if not os.path.exists(directory):
            os.makedirs(directory)
        # Записываем n-граммы и их значения в файл
        file_path = directory + "/" + author_name + ".txt"
        try:
            fp = open(file_path, encoding='utf-8')
            # Считываем средние значения для автора и пересчитываем их
            average_counts = []
            i = 0
            for line in fp.readlines():
                average_counts.append(float("{0:.6f}".format((float(line) + self.count_ngrams_list[i]) / 2)))
                self.count_ngrams_list[i] = 0.0
                i += 1
            fp.close()
            # Перезаписываем средневзвешенную ПФР в файл
            fp = open(file_path, 'w', encoding='utf-8')
            for average_count in average_counts:
                fp.write(str(average_count) + "\n")
        except IOError:
            # Если нет автора, создаем файл для него
            fp = open(file_path, 'w+', encoding='utf-8')
            # Записываем частоты n-грамм
            for i in range(len(self.count_ngrams_list)):
                fp.write(str(self.count_ngrams_list[i]) + "\n")
                self.count_ngrams_list[i] = 0.0

        fp.close()
        print("  Метод, основанный на {}-граммах символов успешно выполнен".format(str(n)))