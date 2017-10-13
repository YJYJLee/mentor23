import itertools
import nltk
from nltk.corpus import stopwords
from konlpy.tag import Twitter
from collections import Counter
import networkx
import collections
import re
t = Twitter()
def xplit(*delimiters):
    return lambda value: re.split('|'.join([re.escape(delimiters) for delimiter in delimiters]),value)

class Sentence:
    @staticmethod
    def co_occurence(sentence1,sentence2):
        p = sum((sentence1.bow & sentence2.bow).values())
        q = sum((sentence1.bow | sentence2.bow).values())
        return p/q if q else 0

    def __init__(self,text,index=0):
        self.index = index
        self.text = text
        token = t.morphs(self.text)
        filtered = []
        for w in token:
            if w not in stop_words:
                filtered.append(w)
        self.nouns = filtered
        self.bow = Counter(self.nouns)

    def __eq__(self, another):
        return hasattr(another,'index') and self.index==another.index

    def __hash__(self):
        return self.index

class TextRank:
    def __init__(self,text):
        self.sentences = get_sentences(text)
        self.graph = build_graph(self.sentences)
        self.pagerank = networkx.pagerank(self.graph,weight='weight')
        self.reordered = sorted(self.pagerank,key=self.pagerank.get,reverse=True)
        self.nouns=[]
        for sentence in self.sentences:
            self.nouns += sentence.nouns
        self.bow = collections.Counter(self.nouns)

    def summarize(self,count):
        if not hasattr(self,'reordered'):
            return ""
        count = int(len(self.reordered)*count)
        candidates = self.reordered[:count]
        candidates = sorted(candidates,key=lambda sentence: sentence.index)
        return '\n'.join([candidate.text for candidate in candidates])

def get_sentences(text):
    candidates = xplit('.','?','!','\n','.\n')(text.strip())
    sentences = []
    index = 0
    for candidate in candidates:
        candidate = candidate.strip()
        if len(candidate):
            sentences.append(Sentence(candidate,index))
            index += 1
    return sentences

def build_graph(sentences):
    graph = networkx.Graph()
    graph.add_nodes_from(sentences)
    pairs = list(itertools.combinations(sentences,2))
    for eins,zwei in pairs:
        graph.add_edge(eins,zwei,weight=Sentence.co_occurence(eins,zwei))
    return graph

def summarize_text(text):
    nltk.download('stopwords')
    global stop_words
    stop_words= set(stopwords.words('english'))
    text_rank = TextRank(text)
    #tr = text_rank.summarize(0.5)
    return text_rank
