import emoji
import string
import nltk 
#nltk.download('punkt')
#nltk.download('stopwords')
from nltk import re,word_tokenize
from nltk.corpus import stopwords


MIN_YEAR = 1900
MAX_YEAR = 2100
def get_url_patern():
    return re.compile(
        r'(https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|https?:\/\/(?:www\.|(?!www))'
        r'[a-zA-Z0-9]\.[^\s]{2,}|www\.[a-zA-Z0-9]\.[^\s]{2,})')


def get_emojis_pattern():
    try:
       
        # UCS-4
        emojis_pattern =re.compile(u'([\U0001F600-\U0001F64F])|([\U0001F300-\U0001F5FF])|([\U0001F680-\U0001F6FF])|([\U0001F1E0-\U0001F1FF])|([\U00002702-\U000027B0])|([\U000024C2-\U0001F251])')
    except re.error:
        # UCS-2
        emojis_pattern = re.compile(
            u'([\u2600-\u27BF])|([\uD83C][\uDF00-\uDFFF])|([\uD83D][\uDC00-\uDE4F])|([\uD83D][\uDE80-\uDEFF])')
    return emojis_pattern
    # duplicated
    # return emoji.get_emoji_regexp()

def get_hashtags_pattern():
    return re.compile(r'#*')

def get_single_letter_words_pattern():
    return re.compile(r'(?<![\w\-])\w(?![\w\-])')

def get_two_letter_words_pattern():
    return re.compile(r'\W*\b\w{1,3}\b')

def get_blank_spaces_pattern():
    return re.compile(r'\s{2,}|\t')


def get_twitter_reserved_words_pattern():
    return re.compile(r'(RT|FAV|fav|VIA|via)')


def get_mentions_pattern():
    return re.compile(r'@\w*')

def get_stock_market_pattern():
    return re.compile(r'\$\w*')

def get_pourcentage_pattern():
    return re.compile(r'%')

def is_year(text):
    if (len(text) == 3 or len(text) == 4) and (MIN_YEAR < len(text) < MAX_YEAR):
        return True
    else:
        return False



class TwitterPreprocessor:

    def __init__(self, text: str):
        self.text = text

    def fully_preprocess(self):
        return self \
            .remove_urls() \
            .remove_mentions() \
            .remove_hashtags() \
            .remove_twitter_reserved_words() \
            .replace_emojis() \
            .remove_punctuation() \
            .remove_single_letter_words() \
            .remove_three_letter_words()\
            .remove_stopwords() \
            .lowercase() \
            .remove_non_ascii()\
            .remove_numbers() \
            .remove_blank_spaces()\
            .remove_stock_market()\
            .remove_pourcentage()
    
    def desc_preprocess(self):
        return self \
            .remove_urls() \
            .remove_mentions() \
            .remove_hashtags() \
            .remove_twitter_reserved_words() \
            .replace_emojis() \
            .remove_punctuation() \
            .remove_single_letter_words() \
            .lowercase() \
            .remove_numbers() \
            .remove_blank_spaces()
    
    def partially_preprocess(self):
        return self \
            .remove_urls() \
            .remove_mentions() \
            .remove_hashtags() \
            .remove_twitter_reserved_words() \
            .replace_emojis() \
            .remove_punctuation() \
            .remove_non_ascii()\
            .remove_blank_spaces()

    def pos_tag_preprocess(self):
        return self \
            .remove_urls() \
            .remove_mentions() \
            .remove_hashtags() \
            .remove_twitter_reserved_words() \
            .replace_emojis() \
            .remove_non_ascii() \
            .remove_blank_spaces()

    def remove_urls(self):
        self.text = re.sub(pattern=get_url_patern(), repl='', string=self.text)
        return self

    def replace_emojis(self): 
        self.text=emoji.demojize(self.text)
        #self.text = re.sub(pattern=get_emojis_pattern(),repl='',string=self.text)
        return self

    def remove_punctuation(self):
        self.text = self.text.translate(str.maketrans('', '', string.punctuation))
        return self

    def remove_mentions(self):
        self.text = re.sub(pattern=get_mentions_pattern(), repl='', string=self.text)
        return self
    
    def remove_pourcentage(self):
        self.text = re.sub(pattern=get_pourcentage_pattern(), repl='', string=self.text)
        return self
    
    def remove_stock_market(self):
        self.text = re.sub(pattern=get_stock_market_pattern(), repl='', string=self.text)
        return self
    
    def remove_hashtags(self):
        self.text = re.sub(pattern=get_hashtags_pattern(), repl='', string=self.text)
        return self

    def remove_twitter_reserved_words(self):
        self.text = re.sub(pattern=get_twitter_reserved_words_pattern(), repl='', string=self.text)
        return self

    def remove_single_letter_words(self):
        self.text = re.sub(pattern=get_single_letter_words_pattern(), repl='', string=self.text)
        return self

    def remove_three_letter_words(self):
        self.text = re.sub(pattern=get_two_letter_words_pattern(), repl='', string=self.text)
        return self

    def remove_blank_spaces(self):
        self.text = re.sub(pattern=get_blank_spaces_pattern(), repl=' ', string=self.text)
        return self

    def remove_stopwords(self, extra_stopwords=None):
        if extra_stopwords is None:
            extra_stopwords = []
        text = word_tokenize(self.text)
        stop_words = set(stopwords.words('english'))

        new_sentence = []
        for w in text:
            if w not in stop_words and w not in extra_stopwords:
                new_sentence.append(w)
        self.text = ' '.join(new_sentence)
        return self

    def remove_numbers(self, preserve_years=False):
        # text_list = self.text.split(' ')
        # for text in text_list:
        #     if text.isnumeric():
        #         if preserve_years:
        #             if not is_year(text):
        #                 text_list.remove(text)
        #         else:
        #             text_list.remove(text)

        self.text =re.sub(r'[0-9]+', '',self.text)
        return self

    def lowercase(self):
        self.text = self.text.lower()
        return self

    def remove_non_ascii(self):
        self.text = self.text.encode('ascii',errors='ignore').decode()
        return self
