import copy
import math
import pandas


class Kanji:
    kanji = dict()

    def __init__(self, writing, translation,
        readings=dict(),
        usage=None, category=None,
        t_rating=0, r_rating=0,
        w_similarity=None, t_similarity=None, r_similarity=None,
        in_mind_map=False, notes=None
    ):

        self.writing = writing
        self.translation = translation

        self.readings = copy.copy(readings)

        self.usage = (usage, None)[usage == "nan"]
        self.category = (category, None)[category == "nan"]

        self.t_rating = t_rating  # translation
        self.r_rating = r_rating  # reading

        self.w_similarity = w_similarity  # writing
        self.t_similarity = t_similarity  # translation
        self.r_similarity = r_similarity  # reading

        self.in_mind_map = in_mind_map
        self.notes = (notes, None)[notes == "nan"]  # use walrus operator?

    @classmethod
    def define_kanji_list(cls):
        data = pandas.read_excel("Kanji Storage.xlsx")
        for kanji_index in range(228):
            row = data.loc[kanji_index, :]
            writing = row.loc["writing"]
            translation = row.loc["translation"]
            yomi_list = row.loc["on-yomi"].split(", ") + row.loc["kun-yomi"].split(", ")
            readings = dict()
            for yomi in yomi_list:
                if yomi != "-":
                    readings[yomi] = list()
            usage = str(row.loc["usage"])
            category = str(row.loc["category"])
            t_rating = float(row.loc["t_rating"])
            r_rating = float(row.loc["r_rating"])
            w_similarity = float(row.loc["w_similarity"])
            t_similarity = float(row.loc["t_similarity"])
            r_similarity = float(row.loc["r_similarity"])
            in_mind_map = bool(row.loc["in_mind_map"])
            notes = str(row.loc["notes"])
            cls.kanji[writing] = cls(writing, translation, readings, usage, category,
                                     t_rating, r_rating, w_similarity, t_similarity, r_similarity,
                                     in_mind_map, notes)

    def add_reading(self, yomi, *readings):
        if yomi not in self.readings.keys():
            self.readings[yomi] = list(readings)
        else:
            for reading in readings:
                if reading not in self.readings[yomi]:
                    self.readings[yomi].append(reading)

    def __repr__(self):
        return "K(" + self.writing + ")"


class Word:
    def __init__(self, translation, kanji, word_type,
        category=None,
        t_rating=0, r_rating=0,
        in_mind_map=False, notes=None
    ):

        self.translation = translation
        self.kanji = kanji

        self.word_type = word_type
        self.category = category

        self.t_rating = t_rating  # translation
        self.r_rating = r_rating  # reading

        self.in_mind_map = in_mind_map
        self.notes = notes

        self.writing = str()
        self.reading = str()
        for reading_kanji in self.kanji:
            if isinstance(reading_kanji, tuple):
                reading_kanji[1].add_reading(reading_kanji[0], self)
                self.writing += reading_kanji[1].writing
                self.reading += reading_kanji[0]
            else:
                self.writing += reading_kanji
                self.reading += reading_kanji

    def __repr__(self):
        return "W(" + self.writing + ")"


# generally want to learn to translate writing -> translation -> reading

Kanji.define_kanji_list()
#print(Kanji.kanji)

words = list()
#words.append(Word("", (), ""))
words.append(Word("university", (("ダイ", Kanji.kanji["大"]), ("ガク", Kanji.kanji["学"])), "noun", category="learning", t_rating=5, r_rating=5, in_mind_map=True))
words.append(Word("university student", (("ダイ", Kanji.kanji["大"]), ("ガク", Kanji.kanji["学"]), ("セイ", Kanji.kanji["生"])), "noun", category="learning", t_rating=5, r_rating=5, in_mind_map=True))
words.append(Word("student", (("ガク", Kanji.kanji["学"]), ("セイ", Kanji.kanji["生"])), "noun", category="learning", t_rating=5, r_rating=5, in_mind_map=True))
words.append(Word("to study", (("まな", Kanji.kanji["学"]), "ぶ"), "verb", category="learning", t_rating=4, r_rating=3, in_mind_map=True))
words.append(Word("much", (("おお", Kanji.kanji["大"]), "いに"), "adverb", t_rating=4, r_rating=5, in_mind_map=True))
words.append(Word("big", (("おお", Kanji.kanji["大"]), "きい"), "adjective", t_rating=5, r_rating=5, in_mind_map=True))

print(Kanji.kanji["大"].__dict__)
