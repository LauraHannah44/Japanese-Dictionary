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

        self.t_rating = int((t_rating, 0)[math.isnan(t_rating)])  # translation
        self.r_rating = int((r_rating, 0)[math.isnan(r_rating)])  # reading

        self.w_similarity = (w_similarity, None)[w_similarity == "nan"]  # writing
        self.t_similarity = (t_similarity, None)[t_similarity == "nan"]  # translation
        self.r_similarity = (r_similarity, None)[r_similarity == "nan"]  # reading

        self.in_mind_map = bool((in_mind_map, False)[in_mind_map == "nan"])
        self.notes = (notes, None)[notes == "nan"]

    @classmethod
    def define_kanji_list(cls):
        data = pandas.read_excel("Kanji Storage.xlsx")
        for kanji_index in range(len(data.index)):
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

            t_rating = row.loc["t_rating"]
            r_rating = row.loc["r_rating"]

            w_similarity = str(row.loc["w_similarity"])
            t_similarity = str(row.loc["t_similarity"])
            r_similarity = str(row.loc["r_similarity"])

            in_mind_map = str(row.loc["in_mind_map"])
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
        return "Kanji(" + self.writing + ")"

    def __str__(self):
        summary = "kanji " + self.writing + " meaning “" + self.translation + "”"
        for yomi in self.readings:
            summary += "\nread as " + yomi
            if len(self.readings[yomi]) > 0:
                summary += " in "
                for reading in self.readings[yomi]:
                    summary += reading.writing + " (" + reading.reading + ") " + reading.translation + ", "
        if self.usage is not None:
            summary += "\nusage: " + self.usage
        if self.category is not None:
            summary += "\ncategory: " + self.category
        if self.w_similarity is not None:
            summary += "\nwritten similarly as: " + self.w_similarity
        if self.t_similarity is not None:
            summary += "\ntranslated similarly as " + self.t_similarity
        if self.r_similarity is not None:
            summary += "\nread similarly as " + self.r_similarity
        summary += "\ntranslation rating: " + str(self.t_rating) + "\nreading rating: " + str(self.r_rating)
        if self.notes is not None:
            summary += "\nnotes: " + self.notes
        return summary


class Word:
    words      = dict()
    nouns      = dict()
    pronouns   = dict()
    verbs      = dict()
    adjectives = dict()
    adverbs    = dict()

    def __init__(self, translation, kanji, word_type,
        category=None,
        t_rating=0, r_rating=0,
        t_similarity=None, r_similarity=None,
        in_mind_map=False, notes=None
    ):

        self.translation = translation
        self.kanji = kanji

        self.word_type = (word_type, None)[word_type == "nan"]
        self.category = (category, None)[category == "nan"]

        self.t_rating = int((t_rating, 0)[math.isnan(t_rating)])  # translation
        self.r_rating = int((r_rating, 0)[math.isnan(r_rating)])  # reading

        self.t_similarity = (t_similarity, None)[t_similarity == "nan"]  # translation
        self.r_similarity = (r_similarity, None)[r_similarity == "nan"]  # reading

        self.in_mind_map = bool((in_mind_map, False)[in_mind_map == "nan"])
        self.notes = (notes, None)[notes == "nan"]

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

    @classmethod
    def define_word_list(cls):
        data = pandas.read_excel("Word Storage.xlsx")
        for kanji_index in range(len(data.index)):
            row = data.loc[kanji_index, :]

            translation = row.loc["translation"]

            kanji = list()
            for reading, writing in zip(row.loc["reading"].split(", "), list(row.loc["writing"])):
                if reading == writing:
                    kanji.append(reading)
                else:
                    kanji.append((reading, Kanji.kanji[writing]))
            kanji = tuple(kanji)

            word_type = str(row.loc["word_type"])

            category = str(row.loc["category"])

            t_rating = row.loc["t_rating"]
            r_rating = row.loc["r_rating"]

            t_similarity = str(row.loc["t_similarity"])
            r_similarity = str(row.loc["r_similarity"])

            in_mind_map = str(row.loc["in_mind_map"])
            notes = str(row.loc["notes"])

            cls.words[row.loc["writing"]] = cls(translation, kanji, word_type, category,
                                     t_rating, r_rating, t_similarity, r_similarity,
                                     in_mind_map, notes)

    def __repr__(self):
        return "Word(" + self.writing + ")"

    def __str__(self):
        summary = self.word_type + " " + self.writing + " read as " + self.reading + ""
        summary += "\nmeaning “" + self.translation + "”"
        summary += "\nfrom "
        for kanji in self.kanji:
            if isinstance(kanji, str):
                summary += kanji + ", "
            else:
                summary += kanji[1].writing + " (" + kanji[0] + ") " + kanji[1].translation + ", "
        if self.category is not None:
            summary += "\ncategory: " + self.category
        summary += "\ntranslation rating: " + str(self.t_rating) + "\nreading rating: " + str(self.r_rating)
        if self.notes is not None:
            summary += "\nnotes: " + self.notes
        return summary


# generally want to learn to translate writing -> translation -> reading

Kanji.define_kanji_list()
print(Kanji.kanji)
kanji = Kanji.kanji

Word.define_word_list()
print(Word.words)
word = Word.words

print(word["学ぶ"])
print()
print(word["学生"])