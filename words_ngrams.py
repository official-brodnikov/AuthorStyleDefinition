import os
import shutil
import nltk
from nltk import ngrams

punctuation_signs = [",", ";", ":", "-", "'", '"', '``', '`', '[', ']', '(', ')']
end_signs = ["!", ".", "..", "...", "?"]

class WordsNgrams(object):
    """Конструктор, n - размер n-граммы"""
    def __init__(self, n):
        self.n = n

    """Изменить размер n-граммы слов на n"""
    def change_n(self, n):
        self.n = n

    """Формирование списка n-грамм слов для text"""
    def list_building_ngrams(self, text):
        n = self.n
        ngrams_list = []

        text_for_ngrams = text
        # Удаляем знаки препинания из текста
        for punctuation_sign in punctuation_signs:
            text_for_ngrams = text_for_ngrams.replace(punctuation_sign, '')

        tokens = nltk.word_tokenize(text_for_ngrams.lower())  # Токенизируем текст

        grams = ngrams(tokens, n)  # Формируем n-граммы слов
        # Добавляем в список неповторяющиеся n-граммы слов, слова которой находятся внутри одного предложения
        for gram in grams:
            b = True
            if gram not in ngrams_list:
                for end_sign in end_signs:
                    if end_sign in gram:
                        b = False
                if b:
                    ngrams_list.append(gram)

        return ngrams_list

    """Удаление автора из модели"""
    def delete_author(self, author_name):
        for n in range(2, 7):
            directory = str(n) + "-grams" # Каталог с эталонными текстами
            if os.path.exists(directory):
                directory = str(n) + "-grams/" + author_name  # Каталог с эталонными текстами для author_name
                # Рекурсивно удаляем все эталонные тексты для автора
                shutil.rmtree(directory)
        print("  Автор {} успешно удален для метода, основанном на n-граммах слов".format(author_name))

    """Добавление эталонного text с названием text_name к автору author_name"""
    def add_reference_text(self, text, author_name, text_name):
        n = self.n
        ngrams_list = self.list_building_ngrams(text)  # Формируем n-граммы слов для text
        directory = str(n) + "-grams/" + author_name  # Каталог с эталонными текстами для author_name
        # Если нет папки с автором, то создаем
        if not os.path.exists(directory):
            os.makedirs(directory)
        # Записываем n-граммы в файл
        file_path = directory + "/" + text_name + ".txt"
        fp = open(file_path, 'w+', encoding='utf-8')
        for characteristic in ngrams_list:
            fp.write(str(characteristic) + "\n")

        fp.close()
        print("  Метод, основанный на {}-граммах слов успешно выполнен".format(str(n)))

    """Коэффициент Жаккара"""
    def jaccard_similarity(self, a, b):
        c = a.intersection(b)
        return float(len(c)) / (len(a) + len(b) - len(c))

    """Вычисление коэффицента Жаккара для ngrams_list неизвестного текста и reference_ngrams_list эталонного текста"""
    def calculating_jaccard(self, ngrams_list, reference_ngrams_list):
        jac = self.jaccard_similarity(set(ngrams_list), set(reference_ngrams_list))
        return jac

    """Предсказание автора для text"""
    def identify_author(self, text):
        n = self.n
        max_jaccard = 0  # Наилучший средний коэффициент Жаккара
        probable_author = ""  # Наиболее вероятный автор
        values_ngrams_list = self.list_building_ngrams(text)  # Формируем n-граммы слов для text
        ngrams_list = []
        for ngram in values_ngrams_list:
            ngrams_list.append(str(ngram) + '\n')
        directory = str(n) + "-grams"  # Каталог с эталонными текстами
        # Проверяем есть ли эталонные тексты
        if not os.path.exists(directory):
            print("Модель не обучена, предсказание невозможно")
            return ""
        else:
            for author in os.listdir(directory):
                jaccard = 0.0  # Средний коэффициент Жаккара для автора
                i = 0  # Счетчик текстов для автора
                for reference_text in os.listdir(directory + "/" + author):
                    reference_ngrams_list = []  # Список n-грамм эталонного текста
                    file_path = directory + "/" + author + "/" + reference_text
                    fp = open(file_path, encoding='utf-8')
                    for ngram in fp.readlines():
                        reference_ngrams_list.append(str(ngram))
                    jaccard += self.calculating_jaccard(ngrams_list, reference_ngrams_list)
                    i += 1
                jaccard = jaccard / i
                # Обновляем наиболее вероятного автора, если необоходимо
                if max_jaccard < jaccard:
                    max_jaccard = jaccard
                    probable_author = author
            return probable_author

    def identify_author_by_ngrams_from_file(self, text, text_name, author_name, reference_texts_list, authors_list):
        n = self.n
        max_jaccard = 0  # Наилучший средний коэффициент Жаккара
        probable_author = ""  # Наиболее вероятный автор
        directory = "BankNgrams/" + str(n) + "-grams"  # Каталог с эталонными текстами
        ngrams_list = []
        file_path = directory + "/" + author_name + "/" + text_name
        fp = open(file_path, encoding='utf-8')
        for ngram in fp.readlines():
            ngrams_list.append(str(ngram))
        fp.close()
        for author in os.listdir(directory):
            if author in authors_list:
                jaccard = 0.0  # Средний коэффициент Жаккара для автора
                i = 0  # Счетчик текстов для автора
                for reference_text in os.listdir(directory + "/" + author):
                    if reference_text in reference_texts_list:
                        reference_ngrams_list = []  # Список n-грамм эталонного текста
                        file_path = directory + "/" + author + "/" + reference_text
                        fp = open(file_path, encoding='utf-8')
                        for ngram in fp.readlines():
                            reference_ngrams_list.append(str(ngram))
                        jaccard += self.calculating_jaccard(ngrams_list, reference_ngrams_list)
                        i += 1
                jaccard = jaccard / i
                # Обновляем наиболее вероятного автора, если необоходимо
                if max_jaccard < jaccard:
                    max_jaccard = jaccard
                    probable_author = author
        return probable_author
