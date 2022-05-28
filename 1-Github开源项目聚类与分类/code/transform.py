from sklearn.feature_extraction.text import  TfidfVectorizer
import re
import nltk
from nltk.stem import WordNetLemmatizer 
from nltk.tokenize import word_tokenize as wt
from nltk.tag import pos_tag
from nltk.corpus import stopwords
import numpy as np

wnl = WordNetLemmatizer()

def lemmatize(words):
    out = []
    words = wt(words)
    for w in words:
        out.append(wnl.lemmatize(w))
    return " ".join(out)

def word_filter(sent, max_len = 50):
    sent = re.sub(r'[^a-zA-Z]', ' ', sent)
    words = wt(sent)
    sent_out = []
    num_words = 0
    for word in words:
        pattern = re.compile(r'[A-Z]{2,}')
        
        b1 = (word != '')
        b2 = (pattern.match(word) == None)    
        b3 = (len(word) > 1 and len(word) < 16)
        b4 = (num_words <= max_len)
        # b5 = (word not in stopwords.words('english'))
        b5 = True
        
        
        if all([b1, b2, b3, b4, b5]):
            word = word.lower()
            word = wnl.lemmatize(word)
            sent_out += [word]
            num_words += 1
    if len(sent_out) < max_len:
        sent_out += (max_len - len(sent_out)) * ['UNK']
    return sent_out[:max_len]
            

def transform(input_data, max_len = 50):
    
    transformed_data = []
    sents = []
    size = len(input_data)
    for t, d in enumerate(input_data):
        d = word_filter(d, max_len)
        transformed_data.append(' '.join(d))
        sents += [d]
        if t % 1000 == 0:
            print('\rComplete {num} sentences.'.format(num = t))
    try:
        tfidf_vec = np.load('./word/tfidf_vec.npy')
    except:
        vec = TfidfVectorizer(binary = False, decode_error = 'ignore', max_features = 5000, stop_words = 'english')
        tfidf_vec = np.array(vec.fit_transform(transformed_data).toarray())
    
    return tfidf_vec, sents
    