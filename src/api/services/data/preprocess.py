import re
class TextPreprocessor:
    
    def __init__(self, pattern):
        self.pattern = re.compile(pattern)
    
    def preprocess(self, text):
        text = text.lower()
        text = re.sub(self.pattern, ' ', text)
        tokens = text.split()
        return tokens
    