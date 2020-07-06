import os
import nltk

service_words = ["в",  "на",  "с",  "за",  "к",
                 "по",  "из",  "у",  "от",  "для",
                 "во",  "без",  "до",  "о",  "через",
                 "со",  "при", "про", "об", "ко", "над",
                 "из-за", "из-под", "под", "и", "что",
                 "но", "а", "да", "хотя", "когда",
                 "чтобы", "если", "тоже", "или",
                 "то есть", "зато", "будто", "не",
                 "как", "же", "даже", "бы", "ли",
                 "только", "вот", "то", "ни", "лишь",
                 "ведь", "вон", "нибудь", "уже",  "либо"]


class BasicMethods(object):

    """Вычисление количества служебных слов в тексте, список слов текста words_list"""
    def counting_service_words(self, words_list):
        service_words_count = 0
        for elem in words_list:
            if elem.__getitem__(0) in service_words:
                service_words_count += elem.__getitem__(1)
        return service_words_count

    """Вычисление базовых характеристик текста text"""
    def calculating_basic_characteristics(self, text):
        basic_characteristics_list = []

        wtokens = nltk.word_tokenize(text)  # Токенизируем текст
        token_count = len(wtokens)  # Число токенов в тексте
        tfreq = nltk.FreqDist(wtokens)  # Создаем словарь для токенов
        sentence_count = tfreq['.'] + tfreq['!'] + tfreq['?'] + tfreq['...'] + tfreq['..']  # Число предложений в тексте

        wtokens_nosym = [t for t in wtokens if t.isalnum()]  # Выделяем только слова и цифры из текста
        word_count = len(wtokens_nosym)  # Число слов в тексте

        average_len_sentence = float("{0:.3f}".format(word_count / sentence_count))  # Средняя длина предложения
        basic_characteristics_list.append(average_len_sentence)

        wfreq = nltk.FreqDist(wtokens_nosym)  # Создаем словарь для слов
        unique_word_count = len(wfreq)  # Число уникальных слов в тексте
        specific_vocabulary = float("{0:.3f}".format(unique_word_count / word_count))  # Удельный словарный запас
        basic_characteristics_list.append(specific_vocabulary)

        most_popular_words = wfreq.most_common(unique_word_count)  # Количество каждого уникального слова в тексте
        percent_of_service_words = float(
            "{0:.3f}".format(self.counting_service_words(most_popular_words) / word_count * 100))
        basic_characteristics_list.append(percent_of_service_words)

        return basic_characteristics_list

    """Предсказание автора текста text"""
    def identify_author(self, text):
        basic_characteristics_list = self.calculating_basic_characteristics(text)
        deviations_list = [1000.0, 1000.0, 1000.0]  # Минимальные отклонения по каждой характеристике
        probable_authors_list = ["", "", ""]  # Наиболее веорятные авторы по каждой из характеристик

        directory = "BasicMethods"
        authors_list = os.listdir(directory)  # Получаем список доступных авторов
        # Проходим по каждому автору и вычисляем наиболее вероятного по каждой из характеристик
        for author in authors_list:
            file_path = directory + "/" + author
            fp = open(file_path)
            i = 0
            for line in fp.readlines():
                dev = abs(float(line) - basic_characteristics_list[i])  # Отклонение
                if dev < deviations_list[i]:
                    deviations_list[i] = dev
                    probable_authors_list[i] = author.replace(".txt", "")
                i += 1
            fp.close()
        return probable_authors_list

    """Удаление автора из модели"""
    def delete_author(self, author_name):
        directory = "BasicMethods"
        if not os.path.exists(directory):
            return

        directory = directory + "/" + author_name + ".txt"
        if not os.path.exists(directory):
            try:
                fp = open(directory)
                fp.close()
            except IOError:
                print("  Автора {} не существует для базовых методов".format(author_name))
                return
        # Удаляем все данные для автора
        os.remove(directory)

        print("  Автор {} успешно удален для базовых методов".format(author_name))

    """Добавление эталонного текста text к author_name"""
    def add_reference_text(self, text, author_name):
        basic_characteristics_list = self.calculating_basic_characteristics(text)
        directory = "BasicMethods"

        # Проверяем существует ли папка с авторами, если нет, то создаем
        if not os.path.exists(directory):
            os.makedirs(directory)

        file_path = directory + "/" + author_name + ".txt"
        try:
            # Считываем средние значения для автора и пересчитываем их
            fp = open(file_path)
            average_basic_characteristics_list = []
            i = 0
            for line in fp.readlines():
                average_basic_characteristics_list.append(
                    float("{0:.3f}".format((float(line) + basic_characteristics_list[i]) / 2)))
                i += 1
            fp.close()
            fp = open(file_path, 'w', encoding='utf-8')
            for characteristic in average_basic_characteristics_list:
                fp.write(str(characteristic) + "\n")
        except IOError:
            # Если нет автора, создаем файл для него
            fp = open(file_path, 'w+', encoding='utf-8')
            for characteristic in basic_characteristics_list:
                fp.write(str(characteristic) + "\n")
        fp.close()
        print("  Базовые методы успешно выполнены")
