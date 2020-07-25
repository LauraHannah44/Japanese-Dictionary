import pandas
import random


class Vocab(object):
    def __init__(self, writings, readings, translations,
                 word_type=None, category=None,
                 t_rat=0, r_rat=0, w_sim=None, t_sim=None, r_sim=None,
                 on_mind_map=False, notes=None
    ):
        self.writings = writings
        self.main_writing = self.get_string_rep(writings[0])
        self.readings = readings
        self.translations = translations
        self.main_translation = translations[0]
        self.word_type = word_type
        self.category = category
        self.rating = (t_rat, r_rat)
        self.similarity = (w_sim, t_sim, r_sim)
        self.on_mind_map = on_mind_map
        self.notes = notes

    @classmethod
    def fill_storage_dict(cls):
        data = pandas.read_excel("Vocab Storage.xlsx", sheet_name=cls == Word)
        for row_number in range(len(data.index)):
            row = data.loc[row_number, :]

            writings = row.loc["writings"].split("/")
            writings = [writing.split(", ") for writing in writings]
            raw_readings = row.loc["readings"].split("/")

            translation = row.loc["translations"].split("/")

            word_type = str(row.loc["word_type"])
            category = str(row.loc["category"])
            t_rat = str(row.loc["t_rating"])
            r_rat = str(row.loc["r_rating"])
            w_sim = str(row.loc["w_similarity"])
            t_sim = str(row.loc["t_similarity"])
            r_sim = str(row.loc["r_similarity"])
            in_mind_map = str(row.loc["in_mind_map"])
            notes = str(row.loc["notes"])

            word_type = (word_type, "unknown type")[word_type == "nan"]
            category = (category, None)[category == "nan"]
            t_rat = int((t_rat, 0)[t_rat == "nan"])
            r_rat = int((r_rat, 0)[r_rat == "nan"])
            w_sim = (w_sim, None)[w_sim == "nan"]
            t_sim = (t_sim, None)[t_sim == "nan"]
            r_sim = (r_sim, None)[r_sim == "nan"]
            in_mind_map = bool((in_mind_map, False)[in_mind_map == "nan"])
            notes = (notes, None)[notes == "nan"]

            storage_attribute = ("kanji", "word")[cls == Word]
            instance = cls(writings, raw_readings, translation,
                           word_type, category,
                           t_rat, r_rat, w_sim, t_sim, r_sim,
                           in_mind_map, notes)
            for writing in writings:
                cls.__dict__[storage_attribute][cls.get_string_rep(writing)] = instance
                word_type = instance.word_type.split(" ")[0]
                if cls == Word and word_type in ("adjective", "adverb", "noun", "numeric", "prefix", "pronoun", "suffix", "verb"):
                    cls.__dict__[word_type][cls.get_string_rep(writing)] = instance

    @staticmethod
    def get_string_rep(writing):
        representation = str()
        for character in writing:
            if isinstance(character, str):
                representation += character
            else:
                representation += character.main_writing
        return representation


class Kanji(Vocab):
    kanji = dict()

    def __init__(self, writings, raw_readings, translations,
                 word_type=None, category=None,
                 t_rat=0, r_rat=0, w_sim=None, t_sim=None, r_sim=None,
                 on_mind_map=False, notes=None
    ):
        readings = dict()
        for yomi in raw_readings:
            readings[yomi] = list()

        super().__init__(writings, readings, translations,
                         word_type, category,
                         t_rat, r_rat, w_sim, t_sim, r_sim,
                         on_mind_map, notes)

    def add_reading(self, yomi, *readings):
        if yomi not in self.readings.keys():
            self.readings[yomi] = list(readings)
            print("Added reading {} to kanji {}".format(yomi, self.main_writing))
        else:
            for reading in readings:
                if reading not in self.readings[yomi]:
                    self.readings[yomi].append(reading)

    def __repr__(self):
        return "Kanji(" + self.main_writing + ")"

    def __str__(self):
        summary = "kanji " + self.main_writing + " meaning “" + self.main_translation + "”"

        underscore = str()
        for character in summary:
            if character in HIRAGANA | KATAKANA | KANJI:
                underscore += "～"
            else:
                underscore += "~"
        summary += "\n" + underscore

        for yomi in self.readings:
            summary += "\nread as " + yomi
            if len(self.readings[yomi]) > 0:
                summary += " in "
                for i, reading in enumerate(self.readings[yomi]):
                    summary += reading.main_writing + " (" + "".join(reading.readings[0]) + ") "
                    summary += "meaning “" + reading.main_translation + "”"
                    if i < len(self.readings[yomi]) - 2:
                        summary += ", "
                    elif i == len(self.readings[yomi]) - 2:
                        summary += " and "

        if self.word_type is not None:
            summary += "\ngeneral word type: " + self.word_type
        if self.category is not None:
            summary += "\ncategory: " + self.category

        summary += "\ntranslation rating: " + str(self.rating[0])
        summary += "\nreading rating: " + str(self.rating[1])

        if self.similarity[0] is not None:
            summary += "\nwritten similarly as: " + self.similarity[0]
        if self.similarity[1] is not None:
            summary += "\ntranslated similarly as " + self.similarity[1]
        if self.similarity[2] is not None:
            summary += "\nread similarly as " + self.similarity[2]

        if self.notes is not None:
            summary += "\nnotes: " + self.notes

        return summary + "\n"


class Word(Vocab):
    word       = dict()
    adjective  = dict()
    adverb     = dict()
    noun       = dict()
    numeric    = dict()
    pronoun    = dict()
    suffix     = dict()
    verb       = dict()

    def __init__(self, writings, readings, translations,
                 word_type=None, category=None,
                 t_rat=0, r_rat=0, w_sim=None, t_sim=None, r_sim=None,
                 on_mind_map=False, notes=None
    ):
        for i, reading in enumerate(readings):
            readings[i] = reading.split(", ")

        for i, writing in enumerate(writings):
            for j, character in enumerate(writing):
                if character in Kanji.kanji.keys():
                    character = writings[i][j] = Kanji.kanji[character]
                    for reading in readings:
                        if len(reading) == len(writing):
                            character.add_reading(reading[j], self)

        super().__init__(writings, readings, translations,
                         word_type, category,
                         t_rat, r_rat, w_sim, t_sim, r_sim,
                         on_mind_map, notes)

    def __repr__(self):
        return "Word(" + self.main_writing + ")"

    def __str__(self):
        summary = "“" + self.word_type + "” " + self.main_writing
        summary += " meaning “" + self.main_translation + "”"

        underscore = str()
        for character in summary:
            if character in HIRAGANA | KATAKANA | KANJI:
                underscore += "～"
            else:
                underscore += "~"
        summary += "\n" + underscore

        summary += "\nread as "
        for i, reading in enumerate(self.readings):
            summary += "".join(reading)
            if i < len(self.readings) - 2:
                summary += ", "
            elif i == len(self.readings) - 2:
                summary += " or "

        summary += "\nfrom "
        print(self.main_translation)
        for writing in self.writings:
            for i, kanji in enumerate(writing):
                if kanji == self.readings[0][i]:
                    summary += kanji
                elif isinstance(kanji, str):
                    summary += kanji + " (" + self.readings[0][i] + ")"
                else:
                    summary += kanji.main_writing + " (" + self.readings[0][i] + ") meaning “" + kanji.main_translation + "”"
                if i < len(writing) - 2:
                    summary += ", "
                elif i == len(writing) - 2:
                    summary += " and "

        if self.category is not None:
            summary += "\ncategory: " + self.category

        summary += "\ntranslation rating: " + str(self.rating[0]) + "\nreading rating: " + str(self.rating[1])

        if self.similarity[0] is not None:
            summary += "\nwritten similarly as: " + self.similarity[0]
        if self.similarity[1] is not None:
            summary += "\ntranslated similarly as " + self.similarity[1]
        if self.similarity[2] is not None:
            summary += "\nread similarly as " + self.similarity[2]

        if self.notes is not None:
            summary += "\nnotes: " + self.notes

        return summary + "\n"


HIRAGANA  = set(list("あいうえおかきくけこさしすせそたちつてとなにぬねのはひふへほまみむめもやゆよらりるれろわをんがぎぐげござじずぜぞだぢづでどばびぶべぼぱぴぷぺぽ"))
KATAKANA  = set(list("アイウエオカキクケコサシスセソタチツテトナニヌネノハヒフヘホマミムメモヤユヨラリルレロワヲンガギグゲゴザジズゼゾダヂヅデドバビブベボパピプペポ"))
LOWERCASE = set(list("abcdefghijklmnopqrstuvwxyz"))
UPPERCASE = set(list("ABCDEFGHIJKLMNOPQRSTUVWXYZ"))
KANJI     = set()

Kanji.fill_storage_dict()
Word.fill_storage_dict()
kanji = Kanji.kanji
words = Word.word
vocab = {**kanji, **words}

KANJI = set(Kanji.kanji.keys())

MODE = "randomvocab"

if MODE == "all":
    print(kanji.values())
    print(words.values())
elif MODE == "hardcoded":
    print(kanji["気"])
    print(words["図書館"])
elif MODE == "randomkanji":
    while True:
        print(random.choice(list(kanji.values())))
        input()
elif MODE == "randomword":
    while True:
        print(random.choice(list(word.values())))
        input()
elif MODE == "randomvocab":
    while True:
        print(random.choice(list(vocab.values())))
        input()
elif MODE == "wordtypes":
    print("\n{} adjectives:\n{}".format(len(Word.adjective), Word.adjective.keys()))
    print("\n{} adverbs:\n{}".format(len(Word.adverb), Word.adverb.keys()))
    print("\n{} nouns:\n{}".format(len(Word.noun), Word.noun.keys()))
    print("\n{} numerics:\n{}".format(len(Word.numeric), Word.numeric.keys()))
    print("\n{} pronouns:\n{}".format(len(Word.pronoun), Word.pronoun.keys()))
    print("\n{} suffixes:\n{}".format(len(Word.suffix), Word.suffix.keys()))
    print("\n{} verbs:\n{}".format(len(Word.verb), Word.verb.keys()))
elif MODE == "checkunusedreadings":
    for test_kanji in kanji.values():
        for yomi in test_kanji.readings:
            if test_kanji.readings[yomi] == list():
                print("Reading {} for kanji {} unused".format(yomi, test_kanji.main_writing))