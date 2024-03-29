import re, string
import nltk
from nltk.util import ngrams
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

def convert_to_lower(text):
    return text.lower()

def remove_emojis(text):
    text = re.sub(r"(?:\@|https?\://)\S+", "", text) #remove links and mentions
    text = re.sub(r"<.*?>","",text)

    wierd_pattern = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
        u"\U00002702-\U000027B0"
        u"\U000024C2-\U0001F251"
        u"\U0001f926-\U0001f937"
        u'\U00010000-\U0010ffff'
        u"\u200d"
        u"\u2640-\u2642"
        u"\u2600-\u2B55"
        u"\u23cf"
        u"\u23e9"
        u"\u231a"
        u"\u3030"
        u"\ufe0f"
        u"\u2069"
        u"\u2066"
        # u"\u200c"
        u"\u2068"
        u"\u2067"
        "]+", flags=re.UNICODE)
    
    return wierd_pattern.sub(r' ', text)

def remove_numbers(text):
    number_pattern = r'\d+'
    without_number = re.sub(pattern=number_pattern, repl=" ", string=text)
    return without_number


def remove_punctuation(text):
     #return text.translate(str.maketrans('', '', string.punctuation))
    return text.translate(str.maketrans(string.punctuation, ' ' * len(string.punctuation))).replace(' '*4, ' ').replace(' '*3, ' ').replace(' '*2, ' ').strip()

def remove_stopwords(text):
    removed = []
    list_stopw=['i', 'me', 'my', 'myself', 'we', 'our', 'ours',
    'ourselves', 'you', "you're", "you've",  "you'll",
    "you'd",  'your', 'yours',  'yourself',  'yourselves',
    'he',  'him',  'his',  'himself', 'she',
    "she's", 'her',  'hers', 'herself',
    'it', "it's",  'its',  'itself',
    'they',  'them',  'their',  'theirs',
    'themselves',  'what',  'which',  'who',
    'whom',  'this',  'that',  "that'll",
    'these',  'those',  'am',  'is',
    'are',  'was',  'were',  'be',
    'been',  'being',  'have',  'has',
    'had',  'having',  'do',  'does',
    'did',  'doing',  'a',  'an',
    'the',  'and',  'but',  'if',
    'or',  'because',  'as',  'until',
    'while',  'of',  'at',  'by',
    'for',  'with',  'about',  'against',
    'between',  'into',  'through',  'during',
    'before',  'after',  'above',  'below',
    'to',  'from',  'up',  'down',
    'in',  'out',  'on',  'off',
    'over',  'under',  'again',  'further',
    'then',  'once',  'here',  'there',
    'when',  'where',  'why',  'how',
    'all',  'any',  'both',  'each',
    'few',  'more',  'most',  'other',
    'some',  'such',  'no',  'nor',
    'not',  'only',  'own',  'same',
    'so',  'than',  'too',  'very',
    's',  't',  'can',  'will',
    'just',  'don',  "don't",  'should',
    "should've",  'now',  'd',  'll',  'm',  'o',
    're',  've',  'y',  'ain',
    'aren',  "aren't",  'couldn',  "couldn't",
    'didn',  "didn't",  'doesn',  "doesn't",
    'hadn',  "hadn't",  'hasn',  "hasn't",
    'haven',  "haven't",  'isn',  "isn't",
    'ma',  'mightn',  "mightn't",  'mustn',
    "mustn't",  'needn',  "needn't",  'shan',
    "shan't",  'shouldn',  "shouldn't",  'wasn',
    "wasn't",  'weren',  "weren't",  'won',
    "won't",  'wouldn',  "wouldn't"]
    stop_words = list(list_stopw +['’','“','“','amp','new','”','covid','via','us'])
    tokens = text.split()
    for i in range(len(tokens)):
        if tokens[i] not in stop_words:
            removed.append(tokens[i])
    return " ".join(removed)

def remove_extra_white_spaces(text):
    single_char_pattern = r'\s+[a-zA-Z]\s+'
    without_sc = re.sub(pattern=single_char_pattern, repl=" ", string=text)
    return without_sc

def preprocessText(text):
      return remove_extra_white_spaces(remove_stopwords(remove_punctuation(remove_numbers(remove_emojis(convert_to_lower(text))))))

