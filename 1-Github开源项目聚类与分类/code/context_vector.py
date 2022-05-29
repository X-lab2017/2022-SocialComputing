from nltk.util import bigrams, pad_sequence
from collections import Counter
import numpy as np

def context_vec(sents, VOCAB_SIZE):
    s = [list(pad_sequence(sent, pad_left=True, left_pad_symbol = "<start>",
                         pad_right=True, right_pad_symbol = "<end>", n = 2)) for sent in sents]
    packet = []
    for sent in s:
        for w in sent:
            packet += [w]
            
    counter = Counter(packet)
    vocab = counter.most_common(VOCAB_SIZE - 1)
    word2idx = {w[0]: n + 1 for n, w in enumerate(vocab)}
    idx2word = {n + 1: w[0] for n, w in enumerate(vocab)}
    word2idx['UNK'] = 0
    idx2word[0] = 'UNK'
    
    bigram = [list(bigrams(sent)) for sent in s]
    
    mat = np.zeros((VOCAB_SIZE - 1, VOCAB_SIZE))
    for p in bigram:
        for (word, context) in p:
            c, w = 0, 0
            if word not in word2idx:
                continue
            c = word2idx[word] - 1
            if context in word2idx:
                w = word2idx[context] - 1
            mat[c, w] += 1.
    
    mat = (mat + 1.) / (mat.sum(axis = 1, keepdims = True) + VOCAB_SIZE)
    
    word_vec = []
    for sent in s:
        sent_vec = []
        for w in sent:
            if w == 'not' or w not in word2idx:
                sent_vec += [np.zeros((VOCAB_SIZE))]
            else:    
                idx = word2idx[w]
                sent_vec += [mat[idx - 1]]
        word_vec += [sent_vec]
        
    return np.array(word_vec)

def embedding_vec(sents, VOCAB_SIZE):
    s = [list(pad_sequence(sent, pad_left=True, left_pad_symbol = "<start>",
                         pad_right=True, right_pad_symbol = "<end>", n = 2)) for sent in sents]
    packet = []
    for sent in s:
        for w in sent:
            packet += [w]
            
    counter = Counter(packet)
    vocab = counter.most_common(VOCAB_SIZE - 1)
    word2idx = {w[0]: n + 1 for n, w in enumerate(vocab)}
    idx2word = {n + 1: w[0] for n, w in enumerate(vocab)}
    word2idx['UNK'] = 0
    idx2word[0] = 'UNK'
    
    result = [[word2idx[w] if w in word2idx else 0 for w in sent] for sent in s]
    return np.array(result)