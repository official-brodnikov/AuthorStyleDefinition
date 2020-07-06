import io
import os
import nltk
import shutil
from basic_methods import BasicMethods
from words_ngrams import WordsNgrams
from symbols_ngrams import SymbolsNgrams
from benford_law import BenfordLaw
from cross_validation import CrossValidation


# Инициализируем экемпляры классов
bm = BasicMethods()
wngrams = WordsNgrams(2)
sngrams = SymbolsNgrams(2)
benford = BenfordLaw()

class AutorStyleDefinition(object):
    """Главное меню"""
    def main_menu(self):
        choice = 0
        while choice < 1 or choice > 6:
            print("Выберите действие:\n",
                  " 1. Проанализировать текст с помощью базовых методов",
                  "\n   (доля служебных слов, средняя длина предложения и др)\n",
                  " 2. Проанализировать текст, выбрав один из сложных методов\n",
                  " 3. Проанализировать текст всеми доступными методами\n",
                  " 4. Добавить эталонный текст\n",
                  " 5. Удалить из обученной модели одного или всех авторов\n",
                  " 6. Выход")
            choice = int(input())
        return choice

    """Выбор текста из банка доступных в каталоге directory"""
    def read_text_from_db(self):
        print("Выберите текст\n")
        # Каталог со всеми текстами
        directory = "Texts"
        texts_list = os.listdir(directory)  # Список файлов
        i = 0
        # Получаем список текстов
        for text in texts_list:
            print(" {}. {}\n".format(i + 1, text.replace(".txt", "")))
            i += 1
        filename = int(input())  # Выбираем текст по номеру
        text_name = texts_list.__getitem__(filename - 1).replace(".txt", "")  # Название текста
        print(text_name)
        path = 'Texts/' + text_name + '.txt'
        text = io.open(path, encoding='utf-8').read()  # Чтение файла
        text = text.lower()
        # Число знаков препинания в выбранных методах не играет роли
        # Поэтому заменяем знак ?!, для простоты разделения по предложениям
        return text.replace("?!", "?"), text_name

    """Чтение файла, путь указывает пользователь"""
    def read_text_from_dir(self, path, filename):
        path = path + '/' + filename
        text = io.open(path, encoding='utf-8').read()
        text = text.lower()
        # Число знаков препинания в выбранных методах не играет роли
        # Поэтому заменяем знак ?!, для простоты разделения по предложениям
        return text.replace("?!", "?"), filename.replace(".txt", "")

    """Меню чтения файла, путь указывает пользователь"""
    def menu_read_text_from_dir(self):
        print("Введите название файла (без разрешения)")
        filename = input() + ".txt"
        print("Введите путь к файлу")
        path = input()
        return self.read_text_from_dir(path, filename)

    """Меню чтения текста"""
    def menu_read_text(self):
        value = 0
        while value != 1 and value != 2:
            print("Откуда выбрать текст:\n",
              " 1. Из базы доступных\n",
              " 2. Указать путь")
            value = int(input())
        if value == 1:
            return self.read_text_from_db()
        else:
            return self.menu_read_text_from_dir()

    """Предсказание автора с помощью n-грамм слов"""
    def identify_author_using_words_ngrams(self, text, n):
        wngrams.change_n(n)
        author = wngrams.identify_author(text)
        return author

    """Меню для метода n-грамм слов"""
    def menu_words_ngrams(self, text):
        choice = 0
        while choice < 1 or choice > 6:
            print("Выберите используемую n-грамму:\n",
                  " 1. Вернуться в главное меню\n",
                  " 2. Биграмма\n",
                  " 3. Триграмма\n",
                  " 4. 4-грамма\n",
                  " 5. 5-грамма\n",
                  " 6. 6-грамма")
            choice = int(input())
        if choice == 1:
            return
        else:
            print("Наиболее вероятный автор по методу, основанном на {}-граммах слов:".format(choice),
                  "{}".format(self.identify_author_using_words_ngrams(text, choice)))

    """Предсказание автора с помощью ПФР n-грамм символов"""
    def identify_author_using_symbols_ngrams(self, text, n):
        sngrams.change_n(n)
        author = sngrams.identify_author(text)
        return author

    """Меню для метода ПФР n-грамм символов"""
    def menu_symbols_ngrams(self, text):
        choice = 0
        while choice < 1 or choice > 3:
            print("Выберите используемую n-грамму символов:\n",
                  " 1. Вернуться в главное меню\n",
                  " 2. Биграмма\n",
                  " 3. Триграмма")
            choice = int(input())
        if choice == 1:
            return
        else:
            print("Наиболее вероятный автор по методу {}-грамм слов:".format(choice),
                  "{}".format(self.identify_author_using_symbols_ngrams(text, choice)))

    """Вывод наболее вероятных авторов текста по бьазовым методам"""
    def print_authors_using_basic_methods(self, authors_list):
        print(" Наиболее вероятные авторы по методам:\n",
              "  Средняя длина предложения в тексте (в словах) : {}\n".format(authors_list[0]),
              "  Удельный словарный запас автора текста : {}\n".format(authors_list[1]),
              "  Процент служебных слов в тексте : {}\n".format(authors_list[2])
              )

    """Анализ текста text и предсказание автора по базовым методам"""
    def identify_author_using_basic_methods(self, text):
        authors_list = bm.identify_author(text)
        return authors_list

    """Предсказание автора с помощью метода, основанном на законе Бенфорда"""
    def identify_author_using_benford(self, text):
        return benford.identify_author(text)

    """Меню метода, основанном на законе Бенфорда"""
    def menu_benford(self, text):
        print(" Наиболее вероятный автор по методу, основанном на законе Бенфорда: {}".format(self.identify_author_using_benford(text)))

    """Меню выбора одного из списка доступных методов"""
    def hard_methods_menu(self):
        choice = 0
        while choice != 1 and choice != 2 and choice != 3 and choice != 4:
            print("Выберите метод:\n",
                  " 1. Метод отклонений ПФР (n-граммы символов)\n",
                  " 2. Метод, основанный на n-граммах слов\n",
                  " 3. Метод, основанный на законе Бенфорда\n",
                  " 4. Вернуться в главное меню")
            choice = int(input())
        return choice

    """Анализ текста и предсказание автора всеми доступными методами"""
    def analyze_by_all_methods(self, text):
        print(" Наиболее вероятные авторы по характеристикам:")
        # Список вероятных авторов по методам с низкой точностью
        not_probable_authors = self.identify_author_using_basic_methods(text)
        print("  Средняя длина предложения в тексте (в словах) = {}\n".format(not_probable_authors[0]),
              " Удельный словарный запас автора текста = {}\n".format(not_probable_authors[1]),
              " Процент служебных слов в тексте = {}".format(not_probable_authors[2])
              )

        # Список вероятных авторов по методам с высокой точностью
        probable_authors = []
        probable_author_benford = self.identify_author_using_benford(text)
        print("  Отклонения от закона Бенфорда: {}".format(probable_author_benford))
        not_probable_authors.append(probable_author_benford)

        probable_author_symbols_bigrams = self.identify_author_using_symbols_ngrams(text, 2)
        probable_author_symbols_trigrams = self.identify_author_using_symbols_ngrams(text, 3)
        print("  Биграммы символов:",
              "{}".format(probable_author_symbols_bigrams))
        print("  Триграммы символов:",
              "{}".format(probable_author_symbols_trigrams))
        probable_authors.append(probable_author_symbols_trigrams)
        probable_authors.append(probable_author_symbols_bigrams)

        for n in range(2, 7):
            author = self.identify_author_using_words_ngrams(text, n)
            probable_authors.append(author)
            print("  {}-граммы слов:".format(n),
              "{}".format(author))

        # Принцип мажоритарного голосования
        wfreq = nltk.FreqDist(probable_authors)
        most_popular_words = wfreq.most_common(2)
        author = most_popular_words[0].__getitem__(0)
        # При одинаковых результатах у 2-ух авторов, смотрим менее точные методы
        if len(most_popular_words) > 1:
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

    """Добавление эталонного текста """
    def add_reference_text(self, text, author_name, text_name):
        bm.add_reference_text(text, author_name)
        benford.add_reference_text(text, author_name, text_name)
        sngrams.change_n(2)
        sngrams.add_reference_text(text, author_name)
        sngrams.change_n(3)
        sngrams.add_reference_text(text, author_name)
        wngrams.change_n(2)
        wngrams.add_reference_text(text, author_name, text_name)
        wngrams.change_n(3)
        wngrams.add_reference_text(text, author_name, text_name)
        wngrams.change_n(4)
        wngrams.add_reference_text(text, author_name, text_name)
        wngrams.change_n(5)
        wngrams.add_reference_text(text, author_name, text_name)
        wngrams.change_n(6)
        wngrams.add_reference_text(text, author_name, text_name)

    """Меню добавления эталонного текста"""
    def menu_add_reference_text(self):
        directory = "BasicMethods"
        choice = -1
        text, text_name = self.menu_read_text()  # Выбор текста

        authors_list = []
        # Проверяем существует ли папка с авторами и есть ли в папке авторы, выбираем автора или добавляем нового
        if not os.path.exists(directory) or len(os.listdir(directory)) == 0:
            choice = 0
            print("У вас нет доступных авторов, добавьте нового\n")
        else:
            print("Выберите автора:\n")
            authors_list = os.listdir(directory)  # Список доступных авторов
            i = 0
            print(" {}. Добавить нового автора".format(i))
            for author in authors_list:
                i += 1
                print(" {}. {}".format(i, author.replace(".txt", "")))
            while choice < 0 or choice > len(authors_list):
                choice = int(input())

        if choice == 0:
            # Добавляем нового автора
            print("Введите имя автора в формате: И.О. Фамилия")
            author_name = input()
        else:
            author_name = authors_list.__getitem__(choice - 1).replace(".txt", "")

        self.add_reference_text(text, author_name, text_name)

    """Удаление данных об авторе"""
    def delete_author(self, author_name):
        bm.delete_author(author_name)
        sngrams.delete_author(author_name)
        wngrams.delete_author(author_name)
        benford.delete_author(author_name)
        print("Данные об авторе {} удалены успешно\n".format(author_name))

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

    """Меню удаления данных об авторе"""
    def menu_delete_author(self):
        directory = "BasicMethods"
        choice = -1
        # Проверяем существует ли папка с авторами и есть ли в папке авторы, выбираем автора или добавляем нового
        if not os.path.exists(directory) or len(os.listdir(directory)) == 0:
            choice = -1
            print("У вас нет доступных авторов, добавьте нового\n")
            return
        else:
            print("Выберите автора:")
            authors_list = os.listdir(directory)  # Список доступных авторов
            i = 0
            print(" 0. Удалить всех авторов")
            for author in authors_list:
                i += 1
                print(" {}. {}".format(i, author.replace(".txt", "")))
            while choice < 0 or choice > len(authors_list):
                choice = int(input())
        if choice == 0:
            self.delete_all_authors()
        else:
            author_name = authors_list.__getitem__(choice - 1).replace(".txt", "")
            self.delete_author(author_name)


menu = AutorStyleDefinition()
item = 0

while (item != 6):
    try:
        item = menu.main_menu()
        if item == 1:
            text_from_dir, name_text = menu.menu_read_text()
            menu.print_authors_using_basic_methods(menu.identify_author_using_basic_methods(text_from_dir))
        if item == 2:
            text_from_dir, name_text = menu.menu_read_text()
            method = menu.hard_methods_menu()
            if method == 1:
                menu.menu_symbols_ngrams(text_from_dir)
            if method == 2:
                menu.menu_words_ngrams(text_from_dir)
            if method == 2:
                menu.menu_benford(text_from_dir)
        if item == 3:
            text_from_dir, name_text = menu.menu_read_text()
            menu.analyze_by_all_methods(text_from_dir)
        if item == 4:
            menu.menu_add_reference_text()
        if item == 5:
            menu.menu_delete_author()
    except:
        print(" Некорректный ввод")
del menu  # Очищаем память
