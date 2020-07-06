import os
import io
import nltk
import shutil
from basic_methods import BasicMethods
from words_ngrams import WordsNgrams
from symbols_ngrams import SymbolsNgrams
from benford_law import BenfordLaw

bigrams_errors_list = []
trigrams_errors_list = []
w3grams_errors_list = []
w4grams_errors_list = []
complex_errors_list = []

bm = BasicMethods()
wngrams = WordsNgrams(2)
sngrams = SymbolsNgrams(2)
benford = BenfordLaw()

class CrossValidation(object):
    # Точности методов
    accuracy = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    # Число тестов для оценки точности
    tests_number = 0

    """ Конструктор, block_size - размер блока, k - количество блоков"""
    def __init__(self, block_size, k):
        self.block_size = block_size
        self.k = k

    """ Изменение количества блоков"""
    def change_k(self, k):
        self.k = k

    """ Изменение размера блока"""
    def change_block_size(self, block_size):
       self.block_size = block_size

    """Чтение файла"""
    def read_text_from_dir(self, path, filename):
        path = path + '/' + filename
        text = io.open(path, encoding='utf-8').read()
        text = text.lower()
        # Число знаков препинания в выбранных методах не играет роли
        # Поэтому заменяем знак ?!, для простоты разделения по предложениям
        return text.replace("?!", "?"), filename.replace(".txt", "")

    """Очищение всей обученной модели, т.е. удаление данных о всех авторах"""
    def delete_all_authors(self):
        directory = "BasicMethods"
        # Проверяем существует ли папка для данного метода и удаляем
        if os.path.exists(directory):
            shutil.rmtree(directory)
        directory = "Benford"
        # Проверяем существует ли папка для данного метода и удаляем
        if os.path.exists(directory):
            shutil.rmtree(directory)
        for i in range(2, 7):
           directory = str(i) + "-grams"
        # Проверяем существует ли папка для данного метода и удаляем
           if os.path.exists(directory):
               shutil.rmtree(directory)
        for i in range(2, 4):
            directory = str(i) + "-gramsOfSymbols"
            # Проверяем существует ли папка для данного метода и удаляем
            if os.path.exists(directory):
                shutil.rmtree(directory)
        print("Очищение обученной модели прошло успешно\n")

    """Добавление эталонного текста """
    def add_reference_text(self, text, author_name, text_name):
        bm.add_reference_text(text, author_name)
        benford.add_reference_text(text, author_name, text_name)
        # Быстрое вычисление средневзвешенной ПФР, с помощью n0грамм из файлов
        sngrams.change_n(2)
        sngrams.add_reference_text_by_ngrams_from_file(author_name, "BankNgramsOfSymbols/2-gramsOfSymbols/" + author_name + "/" + text_name + ".txt")
        sngrams.change_n(3)
        sngrams.add_reference_text_by_ngrams_from_file(author_name, "BankNgramsOfSymbols/3-gramsOfSymbols/" + author_name + "/" + text_name + ".txt")
        #Обычное вычисление средневзвешенной ПФР
        #sngrams.change_n(2)
        #sngrams.add_reference_text(text, author_name)
        #sngrams.change_n(3)
        #sngrams.add_reference_text(text, author_name)

        # Добавление текста к модели
        # Не используется, если используется быстрый метод,
        # где сформирован каталог с наборами n-грамм слов
        # для каждого автора и каждого его текста
        #wngrams.change_n(2)
        #wngrams.add_reference_text(text, author_name, text_name)
        #wngrams.change_n(3)
        #wngrams.add_reference_text(text, author_name, text_name)
        #wngrams.change_n(4)
        #wngrams.add_reference_text(text, author_name, text_name)
        #wngrams.change_n(5)
        #wngrams.add_reference_text(text, author_name, text_name)
        #wngrams.change_n(6)
        #wngrams.add_reference_text(text, author_name, text_name)

    """Определение автора text всеми доступными методами"""
    def analyze_by_all_methods(self, text, text_name, author_name, reference_texts_list, authors_list):
        # Инициализируем экемпляры классов
        self.tests_number += 1
        print(" Наиболее вероятные авторы по характеристикам:")
        # Список вероятных авторов по методам с низкой точностью
        not_probable_authors = bm.identify_author(text)
        print("  Средняя длина предложения в тексте (в словах) : {}\n".format(not_probable_authors[0]),
              " Удельный словарный запас автора текста : {}\n".format(not_probable_authors[1]),
              " Процент служебных слов в тексте : {}".format(not_probable_authors[2])
              )
        # Быстрое опредение автора, с помощью считывания отклонений из файла
        #probable_author_benford = benford.identify_author_by_ngrams_from_file(text_name + ".txt", author_name, reference_texts_list, authors_list)
        # Обычное определение
        probable_author_benford = benford.identify_author(text)
        print("  Отклонения от закона Бенфорда: {}".format(probable_author_benford))
        not_probable_authors.append(probable_author_benford)
        # Считаем точность
        for c in range(len(not_probable_authors)):
            if not_probable_authors[c] == author_name:
                self.accuracy[c] += 1

        # Список вероятных авторов по методам с высокой точностью
        probable_authors = []


        path = author_name + "/" + text_name + ".txt"
        sngrams.change_n(2)

        #probable_author_symbols_bigrams = sngrams.identify_author_by_ngrams_from_file(text, "BankNgramsOfSymbols/2-gramsOfSymbols/" + path)
        # Обычное определение автора
        probable_author_symbols_bigrams = sngrams.identify_author(text)
        sngrams.change_n(3)
        # Быстрое определение автора, с помощью чтения n-грамм из файла
        #probable_author_symbols_trigrams = sngrams.identify_author_by_ngrams_from_file(text, "BankNgramsOfSymbols/3-gramsOfSymbols/" + path)
        # Обычное определение автора
        probable_author_symbols_trigrams = sngrams.identify_author(text)

        print("  Биграммы символов:",
              "{}".format(probable_author_symbols_bigrams))
        print("  Триграммы символов:",
              "{}".format(probable_author_symbols_trigrams))
        probable_authors.append(probable_author_symbols_bigrams)
        probable_authors.append(probable_author_symbols_trigrams)

        for n in range(2, 7):
            wngrams.change_n(n)
            # Определение автора с помощью n-грамм из файлов
            #author = wngrams.identify_author_by_ngrams_from_file(text, text_name + ".txt", author_name, reference_texts_list, authors_list)
            # Обычное определение
            wngrams.change_n(n)
            author = wngrams.identify_author(text)
            probable_authors.append(author)
            print("  {}-граммы слов:".format(n),
                  "{}".format(author))

        # Подсчитываем точность, добавляем тексты с обшибками к списку
        for c in range(len(probable_authors)):
            if probable_authors[c] == author_name:
                self.accuracy[c + 4] += 1
            elif c == 0:
                bigrams_errors_list.append(text_name + " - " + probable_authors[c])
            elif c == 1:
                trigrams_errors_list.append(text_name + " - " + probable_authors[c])
            elif c == 3:
                w3grams_errors_list.append(text_name + " - " + probable_authors[c])
            elif c == 4:
                w4grams_errors_list.append(author_name + " - " + probable_authors[c])
        # Принцип мажоритарного голосования
        wfreq = nltk.FreqDist(probable_authors)
        most_popular_words = wfreq.most_common(2)
        author = most_popular_words[0].__getitem__(0)
        if len(most_popular_words) > 1:
            # При одинаковых результатах у 2-ух авторов, смотрим менее точные методы
            if most_popular_words[0].__getitem__(1) == most_popular_words[1].__getitem__(1):
                if str(most_popular_words[0].__getitem__(0)) == str(not_probable_authors[3]):
                    author = most_popular_words[0].__getitem__(0)
                elif str(most_popular_words[1].__getitem__(0)) == str(not_probable_authors[3]):
                    author = most_popular_words[1].__getitem__(0)
                elif str(most_popular_words[0].__getitem__(0)) == str(not_probable_authors[2]):
                    author = most_popular_words[0].__getitem__(0)
                elif str(most_popular_words[1].__getitem__(0)) == str(not_probable_authors[2]):
                    author = most_popular_words[1].__getitem__(0)
                elif str(most_popular_words[0].__getitem__(0)) == str(not_probable_authors[1]):
                    author = most_popular_words[0].__getitem__(0)
                elif str(most_popular_words[1].__getitem__(0)) == str(not_probable_authors[1]):
                    author = most_popular_words[1].__getitem__(0)
                elif str(most_popular_words[0].__getitem__(0)) == str(not_probable_authors[0]):
                    author = most_popular_words[0].__getitem__(0)
                elif str(most_popular_words[1].__getitem__(0)) == str(not_probable_authors[0]):
                    author = most_popular_words[1].__getitem__(0)
        print(" Наиболее вероятный автор по комбинированному методу: ", author, "\n")
        # Подсчитываем точность, добавляем текст к списку ошибочных
        if author == author_name:
            self.accuracy[len(self.accuracy) - 1] += 1
        else:
            complex_errors_list.append(text_name + " - " + author)

    """ Обучение модели методом k-fold-validation"""
    def fold_cross_validation(self, authors_list, authors_directory):
        print(" Модель обучена на текстах: ")
        i = 0
        while i <= (self.k - 1) * self.block_size:
            # Список текстов для тестирования
            analyze_texts = []
            # Список текстов для обучения
            reference_texts_list = []
            for author in authors_list:
                print(" ", author, ":")

                # Получаем список текстов для автора
                texts_directory = authors_directory + "/" + author
                texts_list = os.listdir(texts_directory)

                # Осуществляем k-fold-validation для блока = block_size
                # Не забываем переобучать, а не дообучать модель, для этого используем метод delete_all_authors
                iteration_texts_list = texts_list.copy()
                for j in range(i, self.block_size + i):
                    # Убираем из обучающего множества block_size текстов для тестирования
                    iteration_texts_list.remove(texts_list[j])
                    # Добавляем block_size текстов в множество тестирования
                    analyze_texts.append(texts_list[j])

                # Обучаем модель на данном множестве текстов автора
                for reference_text in iteration_texts_list:
                    text, text_name = self.read_text_from_dir(texts_directory, reference_text)
                    self.add_reference_text(text, author, text_name)
                    print("  ", reference_text.replace(".txt", ""))
                    # Список обучающих текстов
                    reference_texts_list.append(reference_text)
                # очищаем список для текстов другого автора
                iteration_texts_list.clear()
            p = 0
            # Тестируем по одному тексту для каждого автора
            for j in range(len(analyze_texts)):
                text, text_name = self.read_text_from_dir(authors_directory + "/" + authors_list[p], analyze_texts[j])
                print(" {} - {}".format(text_name, authors_list[p]))
                # Анализируем текст всеми методами
                self.analyze_by_all_methods(text, text_name, authors_list[p], reference_texts_list, authors_list)
                # В списке для тестирования block_size текстов для каждого автора
                if (j + 1) % self.block_size == 0:
                    p += 1

            # Очищаем модель
            self.delete_all_authors()

            # Выбираем следующий блок для тестирования
            i += self.block_size

    """ Кросс-валидация для тестирования метода для выборки с 3-емя авторами"""
    def texts_authors_3_cross_validation(self):
        # Задаем папку, содержащую подпапки для эталонных текстов каждого автора
        authors_directory = "TextsByAuthors"
        # Формируем список авторов
        authors_list = os.listdir(authors_directory)
        authors_list_for_iteration = []
        # Формируем списки из разных авторов с длиной равной количеству различных авторов для данной обучающей выборки
        # То есть может быть или 3 или 10
        # Каждый новый список - новое множество авторов для тестирования
        for i in range(len(authors_list)):
            for j in range(i + 1, len(authors_list)):
                for k in range(j + 1, len(authors_list)):
                    authors_list_for_iteration.append(authors_list[i])
                    authors_list_for_iteration.append(authors_list[j])
                    authors_list_for_iteration.append(authors_list[k])
        authors_list_for_iteration.append(authors_list[0])
        authors_list_for_iteration.append(authors_list[1])
        authors_list_for_iteration.append(authors_list[2])
        # Отправляем данную итерацию авторов для обучения и тестирования
        self.fold_cross_validation(authors_list_for_iteration, authors_directory)
        authors_list_for_iteration.clear()
        # Промежуточные результаты средней точности
        self.print_accuracy()
        # Выводим среднюю точность для данной обучающей выборки
        self.print_accuracy()
        # Очищаем точности
        self.tests_number = 0
        for k in range(len(self.accuracy)):
            self.accuracy[k] = 0

    # Вывод средней точности для каждого метода
    def print_accuracy(self):
        print(" Средняя точность для методов:\n",
              "  Средняя длина предложения {}\n".format(self.accuracy[0] / self.tests_number),
              "  Удельный словарный запас {}\n".format(self.accuracy[1] / self.tests_number),
              "  Доля служебных слов {}\n".format(self.accuracy[2] / self.tests_number),
              "  Закон Бенфорда {}\n".format(self.accuracy[3] / self.tests_number),
              "  Биграммы символов {}\n".format(self.accuracy[4] / self.tests_number),
              "  Триграммы символов {}\n".format(self.accuracy[5] / self.tests_number),
              "  2-граммы слов {}\n".format(self.accuracy[6] / self.tests_number),
              "  3-граммы слов {}\n".format(self.accuracy[7] / self.tests_number),
              "  4-граммы слов {}\n".format(self.accuracy[8] / self.tests_number),
              "  5-граммы слов {}\n".format(self.accuracy[9] / self.tests_number),
              "  6-граммы слов {}\n".format(self.accuracy[10] / self.tests_number),
              "  Комбинированный метод {}\n".format(self.accuracy[11] / self.tests_number),
              " Общее число протестированных текстов = {}\n".format(self.tests_number),
              " Список текстов с ошибками:\n",
              "  Метод, основанный на биграммах символов: ")
        for error_text in bigrams_errors_list:
            print("    " + error_text)
        print("   Метод, основанный на триграммах символов: ")
        for error_text in trigrams_errors_list:
            print("    " + error_text)
        print("   Метод, основанный на 3-граммах слов: ")
        for error_text in w3grams_errors_list:
            print("    " + error_text)
        print("   Метод, основанный на 4-граммах слов: ")
        for error_text in w4grams_errors_list:
            print("    " + error_text)
        print("   Комбинированный метод: ")
        for error_text in complex_errors_list:
            print("    " + error_text)
