class Kanji:
    def __init__(self, translation, writing,
        usage=None, category=None,
        w_similarity=None, t_similarity=None, r_similarity=None,
        t_rating=0, r_rating=0,
        in_mind_map=False, notes=None
    ):

        self.translation = translation
        self.writing = writing

        self.readings = {}

        self.usage = usage
        self.category = category

        self.w_similarity = w_similarity  # writing
        self.t_similarity = t_similarity  # translation
        self.r_similarity = r_similarity  # reading

        self.t_rating = t_rating  # translation
        self.r_rating = r_rating  # reading

        self.in_mind_map = in_mind_map
        self.notes = notes

    def add_reading(self, yomi, *readings):
        if yomi not in self.readings.keys():
            self.readings[yomi] = list(readings)
        else:
            for reading in readings:
                if reading not in self.readings[yomi]:
                    self.readings[yomi].append(reading)

    def __repr__(self):
        return "Kanji(" + self.writing + ")"


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
        return "Word(" + self.writing + ")"


# generally want to learn to translate writing -> translation -> reading

large = Kanji("large", "大", usage="descriptor", w_similarity=5, t_rating=5, r_rating=5, in_mind_map=True)
learning = Kanji("learning", "学", category="learning", t_rating=5, r_rating=4, in_mind_map=True)
life = Kanji("life", "生", category="being", t_rating=5, r_rating=4, in_mind_map=True)

university = Word("university", (("ダイ", large), ("ガク", learning)), "noun", category="learning", t_rating=5, r_rating=5, in_mind_map=True)
university_student = Word("university student", (("ダイ", large), ("ガク", learning), ("セイ", life)), "noun", category="learning", t_rating=5, r_rating=5, in_mind_map=True)
student = Word("student", (("ガク", learning), ("セイ", life)), "noun", category="learning", t_rating=5, r_rating=5, in_mind_map=True)
to_study = Word("to study", (("まな", learning), "ぶ"), "verb", category="learning", t_rating=4, r_rating=3, in_mind_map=True)
