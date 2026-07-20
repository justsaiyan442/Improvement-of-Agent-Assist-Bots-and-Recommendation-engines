from keybert import KeyBERT


class KeywordExtractor:
    def __init__(self):
        self.kw_model = KeyBERT()
        self.speech = ''

    def extract(self, transcript):
        self.speech = transcript
        keywords = self.kw_model.extract_keywords(self.speech)
        return keywords

