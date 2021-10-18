from nltk.corpus.reader.plaintext import PlaintextCorpusReader
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
import glob
import sys

def get_words(file):
    words = list(set(corpus.words(file)))

    # remove stop words
    stop_words_list = list(stopwords.words('english'))
    stop_words_list.append('and')
    stop_words_list.append('or')

    words = list(filter(
        lambda e: len(e) >= 3 and e.lower() not in stop_words_list,
        words
    ))

    # remove punctuation
    words = [ word.lower() for word in words if word.isalpha() ]

    # lemmatize words
    words = [ WordNetLemmatizer().lemmatize(word) for word in words ]

    return words

occurences = {}

def analyze_question(qId):
    w1 = get_words('question_%s.txt' % qId)
    # w1t = get_words('text_%s.txt' % qId)
    w2 = get_words('answer_%s.txt' % qId)

    w = list(set(w1) & set(w2))
    # w = list(set(w1 + w1t) & set(w2))

    # print(w1)
    # print(w1t)
    # print(w2)
    # print(w)

    # sys.exit(0)

    if len(w) == 0:
        # no intersection found
        return

    w.sort()
    wk = '-'.join(w)
    if wk not in occurences:
        occurences[wk] = 1
    else:
        occurences[wk] += 1
    
    return wk

corpus_dir = '/opt/corpus/'
files = list(glob.glob('%s/*.txt' % corpus_dir))

qc = int(len(files) / 4)
files = list(map(lambda e: e.replace(corpus_dir, ''), files))

ids = [
    f.replace('question_', '').replace('.txt', '')
    for f in files
    if 'question' in f
]

corpus = PlaintextCorpusReader(corpus_dir, files)

for i in range(len(ids)):
    # print('*' * 50)
    # print('*' * 50)
    # print('*' * 50)

    with open('/opt/corpus/question_%s.txt' % ids[i], 'r') as h:
        q = h.read()

    # with open('/opt/corpus/answer_%s.txt' % ids[i], 'r') as h:
    #     a = h.read()

    # print(q)
    # print('*' * 50)

    # print(a)
    # print('*' * 50)

    wk = analyze_question(ids[i])
    # if wk in ['jenkins-pipeline', 'container-docker', 'containers-docker']:
    #     print(q)

for k in occurences:
    if occurences[k] > 1 and '-' in k:
        print('---', k)
        print(occurences[k])
